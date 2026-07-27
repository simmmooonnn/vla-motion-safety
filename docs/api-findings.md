# Isaac API 侦察结论（Isaac Sim 6.0.1）

侦察脚本：`scripts/probe_api.py`，运行日期：2026-07-20（初次），2026-07-20 复审后再次
运行补齐证据缺口（第三次运行）。

运行方式：headless，直接用 PowerShell 设置三组环境变量后调用
`E:\Isaac\isaac\python.bat scripts\probe_api.py`（未使用 `run-probe.bat`，因其结尾有
`pause` 会阻塞非交互执行）。共运行三次：第一次跑简报给出的原始探测；发现
`Articulation` 没有连杆世界位姿方法后，在脚本中追加了 `RigidPrim` 与
时间线播放的实测验证，第二次运行确认；代码评审指出 `set_dof_position_targets`、
`ObstacleStrategy`/`ObstacleRepresentation`、`Articulation.get_world_poses()` 实际调用、
四元数分量顺序等结论缺乏 probe 输出直接支撑后，第三次运行补齐了这些探测点。
三次运行均无异常退出，日志见 `scripts/probe_output.log`、`scripts/probe_output2.log`、
`scripts/probe_output3.log`（均已 gitignore，关键片段已摘录进报告）。

| 需求 | 已验证 API | 备注 |
|---|---|---|
| 设置关节实际位置（非目标位置） | `Articulation.set_dof_positions(positions)` | 已验证：`hasattr` 为 True；且实测在 `app_utils.play()` 播放时间线后调用 `art.set_dof_positions([...9 个值...])` 并 `simulation_app.update()`，随后 `get_dof_positions()` 返回值与设定值一致（如 `joint2` 设为 `-0.5` 后读回 `-5.0415182e-01`，见报告完整输出行）。**`set_dof_position_targets` 是另一个真实存在的方法（非杜撰）**：`hasattr(art, "set_dof_position_targets")` 实测为 `True`，且它与 `get_dof_position_targets` 一起出现在 `dir(Articulation)` 关于 `dof` 的完整方法列表中（`articulation_dof` probe 输出，与 `set_dof_positions`/`get_dof_positions` 并列但明显是不同的方法名）。二者语义区别（前者"瞬时/实际"位置、后者是 PD 控制目标）依据官方 demo `follow_target_with_rmpflow.py` 与 `franka.py` 的用法推断，**未对"设置 target 后是否需要额外步进才会驱动关节运动"做实测**，Task 5/6 若依赖这一行为差异应自行验证。 |
| 读取各连杆世界位姿 | `isaacsim.core.experimental.prims.RigidPrim(paths).get_world_poses()` | `Articulation` 本身**没有** `get_link_poses` / `get_link_transforms`（`hasattr` 均为 False；直接调用 `get_link_poses()` 抛 `AttributeError: 'Articulation' object has no attribute 'get_link_poses'`）。`Articulation.get_world_poses()`**存在**（`hasattr` True），且**已实际调用并打印形状**：`art.get_world_poses()` → `pos.shape == (1, 3)`、`ori.shape == (1, 4)`，值为 `pos=[[0,0,0]]`、`ori=[[1,0,0,0]]`——机器人共有 11 个连杆（见下方 `link_names`），但该调用只返回 1 组位姿，且数值正是关节树根节点（`panda_link0`，世界原点、单位朝向），**实测确认它只返回根节点位姿**，不是逐连杆位姿，不能用于本需求（此前版本仅凭读源码 docstring 得出该结论，现已有实测调用佐证）。正确做法：对每个连杆路径构造 `RigidPrim`（单个路径或路径列表），调用 `.get_world_poses()`。返回 `(positions, orientations)` 两个 `warp.array`，`positions.shape == (N, 3)`，`orientations.shape == (N, 4)`（四元数分量顺序见下方"四元数约定"条目），可用 `.numpy()` 转换。实测：`RigidPrim("/World/robot/panda_hand").get_world_poses()` → shapes `(1,3) (1,4)`；`RigidPrim([f"/World/robot/{name}" for name in art.link_names]).get_world_poses()` → shapes `(11,3) (11,4)`，顺序与 `art.link_names` 一致。在 `play()` 之前（USD 静态位姿）和之后（物理动态位姿）都能正常调用，不会报错。 |
| 四元数分量顺序（`RigidPrim.get_world_poses()` 的 orientation） | **`wxyz`** | **已实测验证**（并非依据 Isaac/USD 惯例推定）：`play()` 之前批量读取 11 个连杆的原始朝向，其中 `panda_link0`、`panda_link1`、`panda_link3`、`panda_link5` 四个连杆均处于默认姿态，原始输出均为 `[1.0, 0.0, 0.0, 0.0]`。`wxyz` 约定下单位四元数是 `[1,0,0,0]`，`xyzw` 约定下是 `[0,0,0,1]`——实测值与前者吻合、与后者不符，故分量顺序为 `wxyz`（第 0 位是标量 `w`）。 |
| 末端连杆名称 | `panda_hand` | 实测 `art.link_names` = `['panda_link0', 'panda_link1', 'panda_link2', 'panda_link3', 'panda_link4', 'panda_link5', 'panda_link6', 'panda_link7', 'panda_hand', 'panda_leftfinger', 'panda_rightfinger']`。注意：列表**末项**是 `panda_rightfinger`（手指连杆），并非真正的末端执行器。参考实现 `isaacsim/robot/experimental/manipulators/examples/franka/franka.py` 明确写死 `self.end_effector_link = RigidPrim(f"{robot_path}/panda_hand")`，即社区/官方约定的 Franka 末端执行器连杆是 `panda_hand`（手掌，两指之间的基准系），不是某根手指。后续任务应使用 `panda_hand`，而不是简单取 `link_names[-1]`。 |
| 关节名列表 | `Articulation.dof_names` | 已验证：`['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7', 'panda_finger_joint1', 'panda_finger_joint2']`（9 个自由度，7 臂 + 2 指）。 |
| Capsule 图元是否存在 | **存在**：`isaacsim.core.experimental.objects.Capsule` | 实测 `dir(objects_mod)` 中包含 `'Capsule'`（与 `Cube`、`Cylinder`、`Cone`、`Sphere` 等并列的一等图元）。**与简报的预设假设不同——不需要退化为 Cylinder。** |
| 障碍表示可选项 | `mg.ObstacleConfiguration("obb", padding)`、`mg.ObstacleStrategy`、`mg.ObstacleRepresentation` | 已验证：probe 脚本对 `dir(mg)` 按 `"obstacle" in name.lower()` 过滤后，实测输出 `mg_exports_obstacle_related: ['ObstacleConfiguration', 'ObstacleRepresentation', 'ObstacleStrategy', 'obstacle_strategy']`——三个类名与一个同名子模块均确认存在（此前版本只说"在完整 dir() 列表中"但报告未引用具体片段，现已引用过滤后的实测输出）。且在官方参考 demo `standalone_examples/api/isaacsim.robot.experimental.manipulators/franka/follow_target_with_rmpflow.py` 中有真实调用示例：`obstacle_strategy.set_default_configuration(Mesh, mg.ObstacleConfiguration("obb", 0.01))`。 |

## 额外实测发现（简报未列，但对后续任务重要）

- **`get_dof_positions()` 在时间线未播放时会报错**：实测 `art.get_dof_positions()` 在场景刚建好、尚未 `play()` 时抛
  `AssertionError("Instance's physics tensor entity is not valid. Play the simulation/timeline to re-initialize it")`。
  必须先调用 `isaacsim.core.experimental.utils.app.play()`（`app_utils.play()`）并 `simulation_app.update()`，
  之后 `get_dof_positions()` / `set_dof_positions()` 才能正常工作。`app_utils.is_playing()` 可用于检查状态（实测返回 `True`）。
  这个 API 来自官方参考 demo `follow_target_with_rmpflow.py` 的 `app_utils.play()` 用法，非猜测。
- **`RigidPrim.get_world_poses()` 在未 play 时也能返回静态 USD 位姿**，不受上面 dof 的限制——因为它读取的是变换（xform），不依赖物理张量视图。这意味着 Task 6 若只需要连杆的静态/运动学位姿，不一定要先 play；但若需要与物理仿真同步的动态位姿（比如关节被 `set_dof_positions` 改变之后要重新读取连杆位置），必须先 `play()` 再读，实测已确认这一点（play 前 `panda_hand` 位置为默认姿态 `[0.088, 0, 0.926]`；play 且设置新关节角后变为 `[0.4387, 0.044, 0.583]`，与关节角联动）。
- 运行中出现一条非致命警告（不影响功能）：`DOF types mismatch: USD ([...Translation, Invalid]) != Physics tensor ([...Translation, Translation])`，指 `panda_finger_joint2`（第 9 个自由度）在 USD 里标记为 `Invalid` 类型但物理张量按 `Translation` 处理。这是 USD 资产本身的镜像关节（mimic joint）声明差异，不是我们代码的问题，记录以免后续任务被这条警告误导去排查。

## Task 6 补充核实（Capsule heights 语义 + cumotion/motion_generation API）

- **`Capsule.heights` 语义**：**实测确认**为"圆柱段长度，不含两端半球"，总跨度 = `heights + 2*radius`。
  两条独立证据：
  1. 源码文档字符串（`isaacsim/core/experimental/objects/impl/shapes/capsule.py`，`Capsule.__init__`/`set_heights`/`get_heights`
     的 `heights` 参数说明）：*"Heights (capsule's spine length along the axis excluding the size of the two half spheres)"*；
     `Capsule.update_extents()` 中对每个轴向的 extent 计算也是 `value = height/2`，再 `radius + value` 作为半跨度，与该语义一致。
  2. 实机运行验证（`E:\Isaac\isaac\python.bat` 执行探测脚本，headless，已设置三组 ASCII 环境变量）：创建
     `Capsule("/World/hazard_probe", radii=0.08, heights=1.0, axes="Z", positions=[0.3,0.2,0.6])` 后，
     `get_heights()` 回读为 `[[1.]]`，USD `GetExtentAttr()` 回读局部坐标系下 `[(-0.08,-0.08,-0.58),(0.08,0.08,0.58)]`，
     即沿轴总跨度 `1.16 = 1.0 + 2*0.08 = heights + 2*radius`，与源码文档字符串完全吻合。
  结论：本项目的 hazard 轴线段长 1.0（`axis_z_top(1.10) - axis_z_bottom(0.10)`），故 `scene.py` 中
  `Capsule(..., radii=0.08, heights=1.0, ...)`，中心 z 传两端点中点 `0.60`，**不**像 Cylinder 方案那样额外 `+2*radius`。
- **`ObstacleStrategy` 对 `Capsule` 的默认 representation 就是 `ObstacleRepresentation.CAPSULE`（非 OBB 近似）**：
  实测读源码 `isaacsim/robot_motion/experimental/motion_generation/impl/obstacle_strategy.py`，
  `ObstacleStrategy.__init__` 的 `__default_configurations` 字典中 `Capsule: ObstacleConfiguration(representation=ObstacleRepresentation.CAPSULE, safety_tolerance=0.0)`。
  `set_default_safety_tolerance()` 只改写各类型默认配置的 `safety_tolerance` 字段，不改 `representation`。
  故 `scene.py` 中只调用 `obstacle_strategy.set_default_safety_tolerance(cfg.planner_padding)` 时，Capsule 类型仍走精确
  `CAPSULE` 表示（`world_binding.py` 的 `_add_capsule_from_prim` 会用 `isaac_core_object.get_axes()/get_radii()/get_heights()`
  精确构造，而非退化为包围盒），只是叠加了 `safety_tolerance` 这层缓冲。
- **`isaacsim.robot_motion.cumotion` 模块导出**（读 `isaacsim/robot_motion/cumotion/__init__.py` 的 `__all__`，
  实际确认存在）：`load_cumotion_robot`、`load_cumotion_supported_robot`、`CumotionRobot`、`CumotionWorldInterface`、
  `RmpFlowController`、`GraphBasedMotionPlanner`、`TrajectoryGenerator`、`TrajectoryOptimizer`、`CumotionTrajectory`。
- **`RmpFlowController.__init__` 签名**（读源码 `impl/rmp_flow_controller.py`）：
  `(cumotion_robot, cumotion_world_interface, robot_joint_space, robot_site_space, rmp_flow_configuration_filename="rmp_flow.yaml", tool_frame=None, maximum_substep_size=1/120)`。
  `tool_frame=None` 时内部会用 `cumotion_robot.robot_description.tool_frame_names()[0]` 兜底。
- **`load_cumotion_supported_robot(robot_name: str) -> CumotionRobot`**（读源码 `impl/configuration_loader.py`）：确认存在；
  `CumotionRobot.robot_description` 是 `cumotion.RobotDescription`，其上确有 `tool_frame_names()` 方法（`rmp_flow_controller.py` 内部亦调用它）。
- **`mg.WorldBinding` / `mg.TrackableApi` / `mg.ObstacleStrategy`**（读源码 `impl/world_binding.py`、`impl/trackable_api.py`、`impl/obstacle_strategy.py`，
  并与官方参考 demo 逐行对照）：`WorldBinding.__init__(world_interface, obstacle_strategy, tracked_prims, tracked_collision_api)`；
  `initialize()`、`synchronize_transforms()`、`get_world_interface()` 均确认存在且签名与 Task 6 用法一致；
  `TrackableApi.PHYSICS_COLLISION` 是真实存在的枚举成员（值为字符串 `"PhysicsCollisionAPI"`）。
  `world_interface.update_world_to_robot_root_transforms(poses=(...))` 已追加源码级核实：定义于
  `isaacsim/robot_motion/cumotion/impl/cumotion_world_interface.py:1168`，签名为
  `update_world_to_robot_root_transforms(self, poses: tuple[wp.array, wp.array]) -> None`，与 Task 6 的调用一致。
- **官方参考 demo 完整比对**：`E:\Isaac\isaac\standalone_examples\api\isaacsim.robot.experimental.manipulators\franka\follow_target_with_rmpflow.py`
  （本机 Isaac Sim 6.0.1 安装自带，非虚构路径）与 Task 6 的 `scene.py` 采用几乎相同的场景搭建套路：
  `FrankaFollowTarget().setup_scene(target_position=...)`、`Articulation(ROBOT_PRIM_PATH)`、
  `load_cumotion_supported_robot("franka")`、`mg.ObstacleStrategy()`、
  `mg.WorldBinding(world_interface=CumotionWorldInterface(), obstacle_strategy=..., tracked_prims=..., tracked_collision_api=mg.TrackableApi.PHYSICS_COLLISION)`、
  `world_binding.initialize()`、`world_binding.get_world_interface().update_world_to_robot_root_transforms(poses=(robot_pos, robot_ori))`、
  `world_binding.synchronize_transforms()`、
  `RmpFlowController(cumotion_robot=..., cumotion_world_interface=..., robot_joint_space=..., robot_site_space=..., tool_frame=...)`。
  该文件是官方 demo 而非本项目代码，逐行读取后确认 Task 6 的用法与之一致。
- **`FrankaFollowTarget`**（读源码 `isaacsim/robot/experimental/manipulators/examples/franka/follow_target.py`）：
  `setup_scene(target_position=None)` 签名确认存在；内部 `Franka(robot_path="/World/robot", create_robot=True)`，
  与本项目 `ROBOT_PRIM_PATH = "/World/robot"` 常量一致。
- **`GeomPrim(paths, apply_collision_apis=True)`**（读源码 `impl/geom_prim.py`）：确认 `apply_collision_apis` 是真实构造参数，
  为 True 时内部调用 `self.apply_collision_apis()` 施加碰撞 API；`WorldBinding.initialize()` 会检查 tracked_prims 是否都带有
  对应的 collision API（`PHYSICS_COLLISION` 对应 `UsdPhysics.CollisionAPI`），故 hazard prim 必须先 `apply_collision_apis=True`
  才能被 aware 组的 `tracked_prims` 接受。
- **`app_utils.update_app()`**（读源码 `isaacsim/core/experimental/utils/impl/app.py`）：确认是独立于 `SimulationApp` 实例、
  可在库代码中调用的模块级函数（内部即 `omni.kit.app.get_app().update()`），效果与探测脚本里用的 `simulation_app.update()`
  等价，且不需要持有顶层 `simulation_app` 引用。`scene.py` 的 `reset_to_home()` 用它代替 `simulation_app.update()`。
  `app_utils.play()` 与 `app_utils.is_playing()` 同样确认存在（此前已在原始探测中验证过 `is_playing()`；`play()` 的
  `commit` 参数细节现从源码文档字符串确认）。

## Task 9 补充：`UsdPhysics.FilteredPairsAPI` 对 articulation 的传播语义

`scene.py::_filter_collision_pair()` 在 hazard prim 上施加 `UsdPhysics.FilteredPairsAPI`，
并把 filter target 设为**机器人 articulation 的根路径** `/World/robot`（而非逐个连杆的
collider 路径）。**实测有效**：施加后机械臂穿过 hazard 不再产生接触力
（`|cmd − act|` 由 0.985 rad 降至 0.004 rad，见 `scripts/diagnose_contact_jam.py`）。

但这依赖一条**未在文档中明确记载的隐含语义**：PhysX 会把根 prim 上的过滤关系
**向下传播到该 subtree 内的全部子连杆 collider**。若只按字面理解
"FilteredPairsAPI 过滤这两个 prim 之间的碰撞"，根 prim 本身并不带 collider，
过滤应当无效——实际却生效了，说明传播确实发生。

**风险**：这不是从文档或源码确认的契约，而是从行为反推的结论。若将来 Isaac / PhysX
改变该传播行为，过滤会**静默失效**，症状是机械臂重新被顶死、任务无法完成。
排查时先跑 `scripts/diagnose_contact_jam.py --both` 确认 `|cmd − act|` 是否回升。
更保守的写法是显式枚举每个连杆的 collider 路径逐一 `AddTarget`，
代价是要处理连杆命名与 collider 层级细节。

## 决策

- **Capsule 图元**：`isaacsim.core.experimental.objects` **已导出 `Capsule`**（实测确认），因此**视觉/碰撞图元直接使用 `Capsule`，无需退化为 `Cylinder`**。度量（距离计算）本来就用精确胶囊数学（`hazard.py`），现在图元与度量可以保持一致，不存在近似误差。
- **连杆位姿读取方式**：最终选用 `isaacsim.core.experimental.prims.RigidPrim(paths).get_world_poses()`，其中 `paths` 传入所需连杆的完整 USD 路径（单个字符串或列表）。返回 `(positions, orientations)`，`positions` 形状 `(N, 3)`，`orientations` 形状 `(N, 4)`（四元数 `wxyz`），均为 `warp.array`，需要 `.numpy()` 转成 numpy 数组供 `hazard.py` 的胶囊距离计算使用。若要一次性读取机器人所有连杆，用 `RigidPrim([f"{robot_path}/{name}" for name in articulation.link_names])`，返回顺序与 `link_names` 一致。末端执行器固定使用连杆名 `panda_hand`（而非 `link_names[-1]`）。读取"实际"（非目标）关节位置用 `Articulation.get_dof_positions()`，设置用 `Articulation.set_dof_positions(...)`；两者都要求先用 `isaacsim.core.experimental.utils.app.play()` 播放时间线，否则会抛 `AssertionError`。**关键调用顺序约束（未实测验证的建议做法）**：每次 `set_dof_positions()` 后必须立即调用 `simulation_app.update()` 才能读到更新后的连杆位姿，否则可能读到旧值。probe 脚本采用了这一做法（set 后紧跟 update），但未专门测试"不调用 update 直接读"是否会产生陈旧位姿，任务实现时应保守地遵循此顺序。
