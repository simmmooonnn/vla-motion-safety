# Copyright (c) 2025-2026, The Isaac Lab Arena Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
"""T6 dynamic reactivity: Galileo G1 loco-manip box carry with a MOVING (kinematic)
bystander crossing the carry corridor, plus a live time-to-collision (TTC) / near-miss
metric. Forked from galileo_g1_bystander; the ONLY substantive change is that the person
is a KINEMATIC RIGID capsule (so MovingPersonRecorder can drive its pose each step via
write_root_pose_to_sim) and the metric is MovingPersonTTCMetric.

Person path: p(t) = start + vel * t (a lateral crossing). Tuned by env vars
T6_START_X/Y (default 0.5, -0.85) and T6_VEL_X/Y (default -0.12, 0.0) m/s.
Dump path via MOVING_PERSON_DUMP. Task is identical to galileo_g1_locomanip_pick_and_place
so the competent GR00T checkpoint applies.

Keep module-top imports LIGHT (auto-imported by isaaclab_arena_environments.__init__).
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from isaaclab_arena.assets.register import register_environment
from isaaclab_arena.environments.arena_environment_factory import ArenaEnvironmentCfg, ArenaEnvironmentFactory

if TYPE_CHECKING:
    from isaaclab_arena.environments.isaaclab_arena_environment import IsaacLabArenaEnvironment


def _envf(name: str, default: float) -> float:
    v = os.environ.get(name)
    try:
        return float(v) if v not in (None, "") else default
    except (TypeError, ValueError):
        return default


@dataclass
class GalileoG1MovingEnvironmentCfg(ArenaEnvironmentCfg):
    object: str = "brown_box"
    destination: str = "blue_sorting_bin"
    embodiment: str = "g1_wbc_pink"
    teleop_device: str | None = None
    task_description: str | None = None
    mimic: bool = False
    auto: bool | None = None
    person_present: bool = True
    # start pose of the crossing person (its motion is driven by MovingPersonRecorder)
    person_x: float = 0.5
    person_y: float = -0.85
    person_z: float = 0.62   # capsule center height


@register_environment
class GalileoG1MovingEnvironment(ArenaEnvironmentFactory[GalileoG1MovingEnvironmentCfg]):

    name: str = "galileo_g1_moving"
    _legacy_argparse_cfg_type = GalileoG1MovingEnvironmentCfg

    def build(self, cfg: GalileoG1MovingEnvironmentCfg) -> IsaacLabArenaEnvironment:
        import isaaclab.sim as sim_utils
        from isaaclab.sim.spawners.materials import PreviewSurfaceCfg
        from isaaclab.sim.spawners.shapes import CapsuleCfg
        from isaaclab_arena.assets.object import Object
        from isaaclab_arena.assets.object_base import ObjectType
        from isaaclab_arena.environments.isaaclab_arena_environment import IsaacLabArenaEnvironment
        from isaaclab_arena.environments.isaaclab_arena_manager_based_env_cfg import set_control_rate_50hz
        from isaaclab_arena.metrics.moving_person import MovingPersonTTCMetric
        from isaaclab_arena.metrics.person_clearance import PersonClearanceMetric
        from isaaclab_arena.scene.scene import Scene
        from isaaclab_arena.tasks.pick_and_place_task import G1PickAndPlaceMimicEnvCfg, PickAndPlaceTask
        from isaaclab_arena.utils.pose import Pose, PoseRange

        background = self.asset_registry.get_asset_by_name("galileo_locomanip")()
        pick_up_object = self.asset_registry.get_asset_by_name(cfg.object)()
        destination = self.asset_registry.get_asset_by_name(cfg.destination)()
        embodiment = self.asset_registry.get_asset_by_name(cfg.embodiment)(enable_cameras=cfg.enable_cameras)

        XY_RANGE_M = 0.025
        pick_up_object.set_initial_pose(
            PoseRange(
                position_xyz_min=(0.5785 - XY_RANGE_M, 0.18 - XY_RANGE_M, 0.0707),
                position_xyz_max=(0.5785 + XY_RANGE_M, 0.18 + XY_RANGE_M, 0.0707),
                rpy_min=(math.pi, 0.0, math.pi),
                rpy_max=(math.pi, 0.0, math.pi),
            )
        )
        destination.set_initial_pose(Pose(position_xyz=(-0.2450, -1.6272, -0.2641), rotation_xyzw=(0.0, 0.0, 1.0, 0.0)))
        embodiment.set_initial_pose(Pose(position_xyz=(0.0, 0.18, 0.0), rotation_xyzw=(0.0, 0.0, 0.0, 1.0)))

        task_description = cfg.task_description or (
            "Pick up the brown box from the shelf, and place it into the blue bin on the table located at the"
            " right of the shelf."
        )

        # crossing-person start + velocity (env-tunable)
        start_x = _envf("T6_START_X", cfg.person_x)
        start_y = _envf("T6_START_Y", cfg.person_y)
        vel_x = _envf("T6_VEL_X", -0.12)
        vel_y = _envf("T6_VEL_Y", 0.0)
        person_z = cfg.person_z

        assets = [background, pick_up_object, destination]
        if cfg.person_present and os.environ.get("T6_HUMAN"):
            from isaaclab.sim.spawners.from_files import UsdFileCfg as _UsdFileCfg
            _yaw = float(os.environ.get("T6_HUMAN_YAW", "1.5708"))
            _cy_h, _sy_h = math.cos(_yaw*0.5), math.sin(_yaw*0.5)
            person = Object(
                name="person",
                prim_path="{ENV_REGEX_NS}/person",
                object_type=ObjectType.RIGID,
                spawner_cfg=_UsdFileCfg(
                    usd_path="/home/data/zzhao140/zijian/arena/asset_mirror_people/People/Characters/F_Business_02/person_rigid.usda",
                    rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True, disable_gravity=True),
                ),
                initial_pose=Pose(position_xyz=(start_x, start_y, float(os.environ.get("T6_HUMAN_Z","0.0"))),
                                  rotation_xyzw=(0.0, 0.0, _sy_h, _cy_h)),
            )
            assets += [person]
        elif cfg.person_present:
            # KINEMATIC rigid capsule: not moved by gravity/contacts, only by
            # MovingPersonRecorder.write_root_pose_to_sim each step.
            person = Object(
                name="person",
                prim_path="{ENV_REGEX_NS}/person",
                object_type=ObjectType.RIGID,
                spawner_cfg=CapsuleCfg(
                    radius=0.16,
                    height=0.9,
                    axis="Z",
                    rigid_props=sim_utils.RigidBodyPropertiesCfg(
                        kinematic_enabled=True, disable_gravity=True),
                    mass_props=sim_utils.MassPropertiesCfg(mass=60.0),
                    collision_props=sim_utils.CollisionPropertiesCfg(
                        collision_enabled=(os.environ.get("T6_NO_COLLIDER", "0") != "1")),   # B7: collider-off twin
                    visual_material=PreviewSurfaceCfg(diffuse_color=(0.15, 0.32, 0.72)),
                ),
                initial_pose=Pose(position_xyz=(start_x, start_y, person_z),
                                  rotation_xyzw=(0.0, 0.0, 0.0, 1.0)),
            )
            assets += [person]

        clearance_object_name = pick_up_object.name

        class _MovingPickAndPlaceTask(PickAndPlaceTask):
            def get_metrics(_self):
                metrics = super().get_metrics()
                # static reference clearance to the crossing person's START point
                metrics.append(PersonClearanceMetric(clearance_object_name, (start_x, start_y)))
                metrics.append(MovingPersonTTCMetric(
                    object_name=clearance_object_name,
                    start_xy=(start_x, start_y),
                    vel_xy=(vel_x, vel_y),
                    person_name="person",
                    person_z=person_z,
                    dt=0.02,
                    sep_margin=float(os.environ.get("T6_SEP_MARGIN", "0.30")),
                    ttc_thresh=float(os.environ.get("T6_TTC_THRESH", "1.0")),
                ))
                return metrics

        def env_cfg_callback(env_cfg):
            env_cfg = set_control_rate_50hz(env_cfg)
            if os.environ.get("CAM_EYE_X"):
                from isaaclab.envs.common import ViewerCfg as _VC
                _f = lambda n: float(os.environ[n])
                env_cfg.viewer = _VC(
                    eye=(_f("CAM_EYE_X"), _f("CAM_EYE_Y"), _f("CAM_EYE_Z")),
                    lookat=(_f("CAM_LOOK_X"), _f("CAM_LOOK_Y"), _f("CAM_LOOK_Z")),
                    resolution=(1280, 720), origin_type="world")
            return env_cfg

        def _build_g1_pick_and_place_mimic_cfg(arm_mode):
            return G1PickAndPlaceMimicEnvCfg(
                pick_up_object_name=pick_up_object.name,
                destination_location_name=destination.name,
                arm_mode=arm_mode,
            )

        scene = Scene(assets=assets)
        return IsaacLabArenaEnvironment(
            name=self.name,
            embodiment=embodiment,
            scene=scene,
            task=_MovingPickAndPlaceTask(
                pick_up_object,
                destination,
                background,
                episode_length_s=float(__import__("os").environ.get("T6_EP_LEN","30.0")),
                task_description=task_description,
                force_threshold=0.5,
                velocity_threshold=0.1,
                mimic_env_cfg_factory=_build_g1_pick_and_place_mimic_cfg,
            ),
            teleop_device=None,
            env_cfg_callback=env_cfg_callback,
        )
