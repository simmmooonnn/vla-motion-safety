"""Glue between an Isaac Lab environment and a GR00T policy.

GR00T's observation is a nested dict of three modalities and its action is a chunk of
future steps; this module builds that observation and sequences the returned chunk one
step at a time. It is pure Python (no Isaac / no GPU), so it can be unit-tested on any
machine and dropped onto the server unchanged. The GR00T API it targets (verified from
the NVIDIA/Isaac-GR00T `getting_started/policy.md`):

    observation = {
        "video":    {"<camera>": uint8 array (B, T, H, W, 3), RGB 0-255},
        "state":    {"<name>":   float32 array (B, T, D)},
        "language": {"task": [["<instruction>"]]},          # (B, 1) list-of-lists
    }
    action = {"<name>": float32 array (B, T, D)}            # a T-step chunk, physical units

Any object with a `get_action(observation) -> (action_dict, info)` method works as the
policy (the local `Gr00tPolicy` or the ZMQ `PolicyClient` both satisfy this), so the
server/laptop split is transparent here.
"""
from __future__ import annotations

from typing import Any, Callable

import numpy as np


def build_observation(
    images: dict[str, np.ndarray],
    state: dict[str, np.ndarray],
    instruction: str,
) -> dict[str, Any]:
    """Assemble a single-step, batch-size-1 GR00T observation.

    images:  {camera_name: HxWx3 uint8 RGB}
    state:   {state_name:  D-vector float}
    """
    video = {k: np.asarray(v, dtype=np.uint8)[None, None, ...] for k, v in images.items()}
    st = {k: np.asarray(v, dtype=np.float32).reshape(1, 1, -1) for k, v in state.items()}
    return {"video": video, "state": st, "language": {"task": [[instruction]]}}


class ActionChunker:
    """Query the policy once per chunk, then feed the chunk out one step at a time.

    GR00T returns `action_horizon` future steps; re-querying every step wastes compute and
    fights the policy's temporal consistency, so we execute `execute_steps` of each chunk
    before asking again (the GR00T evals call this `num_feedback_actions`).
    """

    def __init__(self, policy: Any, execute_steps: int = 16):
        if execute_steps < 1:
            raise ValueError("execute_steps must be >= 1")
        self.policy = policy
        self.execute_steps = execute_steps
        self._chunk: dict[str, np.ndarray] | None = None
        self._i = 0

    def reset(self) -> None:
        self._chunk, self._i = None, 0
        if hasattr(self.policy, "reset"):
            self.policy.reset()

    def act(self, observation: dict[str, Any]) -> dict[str, np.ndarray]:
        """Return the next single-step action dict {name: D-vector}."""
        if self._chunk is None or self._i >= self.execute_steps:
            action, _ = self.policy.get_action(observation)
            self._chunk, self._i = action, 0
        step = {k: np.asarray(v)[0, self._i, :] for k, v in self._chunk.items()}
        self._i += 1
        return step


def _selftest() -> None:
    # build_observation shapes
    obs = build_observation(
        images={"front": np.zeros((256, 256, 3), np.uint8)},
        state={"arm": np.zeros(7), "gripper": np.zeros(1)},
        instruction="pick up the cup",
    )
    assert obs["video"]["front"].shape == (1, 1, 256, 256, 3)
    assert obs["state"]["arm"].shape == (1, 1, 7)
    assert obs["language"]["task"] == [["pick up the cup"]]

    # ActionChunker: a fake policy returns a 4-step chunk and counts its calls
    class FakePolicy:
        def __init__(self):
            self.calls = 0

        def get_action(self, _obs):
            self.calls += 1
            chunk = np.tile(np.arange(4).reshape(1, 4, 1), (1, 1, 7)).astype(np.float32)
            return {"arm": chunk}, {}

    pol = FakePolicy()
    ch = ActionChunker(pol, execute_steps=4)
    steps = [ch.act(obs) for _ in range(4)]
    assert pol.calls == 1, "should query once for a 4-step chunk"
    assert [int(s["arm"][0]) for s in steps] == [0, 1, 2, 3], "chunk fed out in order"
    ch.act(obs)
    assert pol.calls == 2, "re-queries after the chunk is exhausted"
    print("groot_adapter self-test PASS")


if __name__ == "__main__":
    _selftest()
