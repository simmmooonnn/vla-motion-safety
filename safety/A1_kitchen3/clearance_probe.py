# SPDX-License-Identifier: Apache-2.0
"""A1 carried-hazard-to-person clearance probe.

Wraps a :class:`LiberoEnv` to log, at full control-step resolution, the
world-frame trajectory of a *carried hazard* object (e.g. the moka pot)
together with the end-effector position and gripper state.

Design contract: this wrapper is **behaviourally transparent**. It forwards
every ``(obs, reward, done, truncated, info)`` from the wrapped env unchanged,
so the GR00T policy sees an identical environment and the measured task
success rate is unaffected. All probe data goes only to ``info`` (optional)
and to disk. The per-step trajectory is written as JSON for *offline* clearance
analysis against an arbitrary "person" location -- we log the raw hazard path
and decide the person placement in post-processing.
"""

import json
import os

import gymnasium as gym
import numpy as np


HAZARD_SUBSTRINGS_DEFAULT = ("moka_pot",)
# Static reference bodies whose initial pose we record, so a "person" location
# can be defined relative to the scene layout during offline analysis.
REFERENCE_SUBSTRINGS = ("stove", "kitchen_table", "table", "frypan", "robot0_base", "base")


def _raw_model(sim):
    m = sim.model
    return getattr(m, "_model", m)


def _all_body_names(sim):
    import mujoco

    m = sim.model
    nbody = int(m.nbody)
    raw = _raw_model(sim)
    names = []
    for i in range(nbody):
        name = None
        try:
            name = m.body_id2name(i)
        except Exception:
            try:
                name = mujoco.mj_id2name(raw, mujoco.mjtObj.mjOBJ_BODY, i)
            except Exception:
                name = None
        names.append(name if name is not None else "")
    return names


def _get_sim(env):
    """Return the underlying robosuite MjSim from a (possibly wrapped) LiberoEnv."""
    base = env
    # unwrap gym.Wrapper layers until we reach the object that owns ._env
    hops = 0
    while not hasattr(base, "_env") and hasattr(base, "env") and hops < 8:
        base = base.env
        hops += 1
    inner = getattr(base, "_env", None)  # OffScreenRenderEnv
    getters = []
    if inner is not None:
        getters += [lambda: inner.env.sim, lambda: inner.sim]
    for get in getters:
        try:
            sim = get()
            if sim is not None:
                return sim
        except Exception:
            pass
    raise RuntimeError("ClearanceProbe: could not locate MjSim from env")


class ClearanceProbeWrapper(gym.Wrapper):
    def __init__(self, env, hazard_substrings=None, out_dir=None, task_tag="A1"):
        super().__init__(env)
        self.hazard_substrings = tuple(
            s.lower() for s in (hazard_substrings or HAZARD_SUBSTRINGS_DEFAULT)
        )
        self.out_dir = out_dir or os.environ.get("A1_OUT_DIR", "./a1_runs")
        self.task_tag = os.environ.get("A1_TASK_TAG", task_tag)
        os.makedirs(self.out_dir, exist_ok=True)
        self._sim = None
        self._hazard_id = None
        self._hazard_name = None
        self._ref_bodies = {}  # substring -> body id (static references)
        self._body_names = None
        self._episode_idx = -1
        self._t = 0
        self._traj = None
        self._logged_names = False

    # -- discovery --------------------------------------------------------
    def _ensure_discovery(self):
        # robosuite REBUILDS the MjSim on every hard reset, so a handle cached
        # from a prior episode goes stale (accessing `.data` on it raises
        # "'MjSim' object has no attribute 'data'"). Re-fetch the sim and
        # re-resolve body ids from the fresh model every reset. Body ids are
        # deterministic for a fixed BDDL task, but re-enumerating (30 bodies)
        # is trivial and guarantees the ids match the *current* sim.
        self._sim = _get_sim(self.env)
        self._body_names = _all_body_names(self._sim)
        cands = [
            (i, n)
            for i, n in enumerate(self._body_names)
            if n and any(s in n.lower() for s in self.hazard_substrings)
        ]
        self._hazard_id, self._hazard_name = (None, None)
        if cands:
            # prefer a "main"/root body: an *_main name, else the shortest.
            cands.sort(key=lambda t: (0 if t[1].lower().endswith("_main") else 1, len(t[1])))
            self._hazard_id, self._hazard_name = cands[0]
        self._ref_bodies = {}
        for i, n in enumerate(self._body_names):
            ln = (n or "").lower()
            for s in REFERENCE_SUBSTRINGS:
                if s in ln and s not in self._ref_bodies:
                    self._ref_bodies[s] = i
        if not self._logged_names:
            self._logged_names = True
            print(f"[A1-probe] task_tag={self.task_tag} out_dir={self.out_dir}", flush=True)
            print(
                f"[A1-probe] nbody={len(self._body_names)} "
                f"hazard='{self._hazard_name}' id={self._hazard_id}",
                flush=True,
            )
            hz = [
                n
                for n in self._body_names
                if any(s in (n or "").lower() for s in self.hazard_substrings)
            ]
            print(f"[A1-probe] hazard candidates: {hz}", flush=True)
            print(
                f"[A1-probe] reference bodies: "
                f"{[(s, self._body_names[i]) for s, i in self._ref_bodies.items()]}",
                flush=True,
            )
            print(f"[A1-probe] ALL body names: {self._body_names}", flush=True)

    def _body_xyz(self, bid):
        try:
            return np.asarray(self._sim.data.body_xpos[bid], dtype=float).tolist()
        except Exception:
            name = self._body_names[bid]
            return np.asarray(self._sim.data.get_body_xpos(name), dtype=float).tolist()

    # -- episode I/O ------------------------------------------------------
    def _flush(self):
        if not self._traj or not self._traj["t"]:
            return
        path = os.path.join(self.out_dir, f"{self.task_tag}_ep{self._episode_idx:03d}.json")
        with open(path, "w") as f:
            json.dump(self._traj, f)
        n = len(self._traj["t"])
        print(
            f"[A1-probe] wrote {path} steps={n} success={self._traj['success']}",
            flush=True,
        )

    def _new_episode(self):
        self._episode_idx += 1
        self._t = 0
        self._traj = {
            "task_tag": self.task_tag,
            "episode": self._episode_idx,
            "hazard_name": self._hazard_name,
            "hazard_id": self._hazard_id,
            "reference_bodies": {s: self._body_names[i] for s, i in self._ref_bodies.items()},
            "reference_init_xyz": {},
            "t": [],
            "hazard_xyz": [],
            "eef_xyz": [],
            "gripper": [],
            "success": False,
        }

    # -- gym API ----------------------------------------------------------
    def reset(self, seed=None, options=None):
        if self._traj is not None:
            self._flush()
        obs, info = self.env.reset(seed=seed, options=options)
        self._ensure_discovery()
        self._new_episode()
        for s, i in self._ref_bodies.items():
            self._traj["reference_init_xyz"][s] = self._body_xyz(i)
        self._log_step(obs, info)
        if self._hazard_id is not None and self._traj["hazard_xyz"]:
            print(
                f"[A1-probe] ep{self._episode_idx:03d} hazard init xyz="
                f"{self._traj['hazard_xyz'][0]}",
                flush=True,
            )
        return obs, info

    def step(self, action):
        obs, reward, done, truncated, info = self.env.step(action)
        self._log_step(obs, info)
        return obs, reward, done, truncated, info

    def _log_step(self, obs, info):
        if self._hazard_id is None or self._traj is None:
            return
        self._traj["t"].append(self._t)
        self._traj["hazard_xyz"].append(self._body_xyz(self._hazard_id))
        ex = float(np.ravel(obs["state.x"])[0])
        ey = float(np.ravel(obs["state.y"])[0])
        ez = float(np.ravel(obs["state.z"])[0])
        self._traj["eef_xyz"].append([ex, ey, ez])
        self._traj["gripper"].append(np.ravel(obs["state.gripper"]).astype(float).tolist())
        if isinstance(info, dict) and info.get("success"):
            self._traj["success"] = True
        self._t += 1

    def close(self):
        if self._traj is not None:
            self._flush()
        return self.env.close()


def make_safe_libero_env(task_bddl_file, task_description, hazard_substrings=None, task_tag="A1"):
    from gr00t.eval.sim.LIBERO.libero_env import LiberoEnv

    base = LiberoEnv(task_bddl_file=task_bddl_file, task_description=task_description)
    return ClearanceProbeWrapper(base, hazard_substrings=hazard_substrings, task_tag=task_tag)


# task_name -> hazard substrings (defaults to moka_pot when unset)
A1_TASKS = {
    "KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it": ("moka_pot",),
    "KITCHEN_SCENE8_put_both_moka_pots_on_the_stove": ("moka_pot",),
}


def register_safe_libero_envs():
    import os as _os

    from gymnasium.envs.registration import register
    from libero.libero import benchmark
    from libero.libero.utils import get_libero_path

    benchmark_dict = benchmark.get_benchmark_dict()
    task_suite = benchmark_dict["libero_10"]()
    for task_id in range(task_suite.get_num_tasks()):
        task = task_suite.get_task(task_id)
        task_name = task.name
        hazard = list(A1_TASKS.get(task_name, ())) or None
        task_bddl_file = _os.path.join(
            get_libero_path("bddl_files"), task.problem_folder, task.bddl_file
        )
        register(
            id=f"libero_sim/A1_{task_name}",
            entry_point="gr00t.eval.sim.LIBERO.clearance_probe:make_safe_libero_env",
            kwargs={
                "task_bddl_file": task_bddl_file,
                "task_description": task.language,
                "hazard_substrings": hazard,
                "task_tag": "A1",
            },
        )
