import numpy as np
import genesis as gs

########################## init ##########################
gs.init(backend=gs.gpu)

########################## create a scene ##########################
scene = gs.Scene(
    viewer_options = gs.options.ViewerOptions(
        camera_pos    = (3, -1, 1.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        max_FPS       = 60,
    ),
    sim_options = gs.options.SimOptions(
        # dt = 0.01,
        # substeps = 4, # for more stable grasping contact
    ),
    show_viewer = True,
)

########################## entities ##########################
plane = scene.add_entity(
    gs.morphs.Plane(),
)
cube = scene.add_entity(
    gs.morphs.Box(
        size = (0.04, 0.04, 0.04),
        pos  = (0.65, 0.0, 0.02),
    )
)
franka = scene.add_entity(
    gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'),
)
########################## build ##########################
scene.build()

motors_dof = np.arange(7)
fingers_dof = np.arange(7, 9)

# set control gains
# Note: the following values are tuned for achieving best behavior with Franka
# Typically, each new robot would have a different set of parameters.
# Sometimes high-quality URDF or XML file would also provide this and will be parsed.
franka.set_dofs_kp(
    np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
)
franka.set_dofs_kv(
    np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
)
franka.set_dofs_force_range(
    np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
    np.array([ 87,  87,  87,  87,  12,  12,  12,  100,  100]),
)

# Get the end-effector link
end_effector = franka.get_link('hand')


# 로봇 관절 정보 출력 함수
def print_joint_info(robot):
    joints = robot.get_joints()  # 로봇의 모든 관절 정보 가져오기
    print("Joint Information:")
    for joint in joints:
        print(f"Name: {joint.name}")
        print(f"Type: {joint.type}")
        print(f"Range: {joint.range}")  # 관절 범위 출력
        print(f"Position: {joint.position}")  # 현재 위치
        print(f"Velocity: {joint.velocity}")  # 현재 속도
        print(f"Force: {joint.force}")  # 현재 힘
        print("-" * 20)

########################## motion planning and grasping ##########################
def run_sim(scene, enable_vis):
    # Step 1: Move to pre-grasp pose
    qpos = franka.inverse_kinematics(
        link=end_effector,
        pos=np.array([0.65, 0.0, 0.25]),
        quat=np.array([0, 1, 0, 0]),
    )
    qpos[-2:] = 0.04  # Open the gripper
    path = franka.plan_path(qpos_goal=qpos, num_waypoints=200)
    for waypoint in path:
        franka.control_dofs_position(waypoint)
        scene.step()

    for _ in range(100):  # Allow PD controller to stabilize
        scene.step()

    # Step 2: Reach down to grasp the cube
    qpos = franka.inverse_kinematics(
        link=end_effector,
        pos=np.array([0.65, 0.0, 0.135]),  # 큐브 위치로 이동
        quat=np.array([0, 1, 0, 0]),
    )
    franka.control_dofs_position(qpos[:-2], motors_dof)
    for _ in range(100):  # Allow the robot to reach
        scene.step()

    # Step 3: Grasp the cube
    franka.control_dofs_position(qpos[:-2], motors_dof)
    franka.control_dofs_force(np.array([-0.5, -0.5]), fingers_dof)  # Apply grasping force
    for _ in range(100):  # Allow the gripper to grasp
        scene.step()

    # Step 4: Lift the cube
    qpos = franka.inverse_kinematics(
        link=end_effector,
        pos=np.array([0.65, 0.0, 0.3]),  # 위로 들어 올림
        quat=np.array([0, 1, 0, 0]),
    )
    franka.control_dofs_position(qpos[:-2], motors_dof)
    for _ in range(200):  # Allow the robot to lift the cube
        scene.step()

    if enable_vis:
        scene.viewer.stop()
        print_joint_info(franka)  # 관절 정보 출력


# 시뮬레이션 실행을 별도 스레드에서 처리
gs.tools.run_in_another_thread(
    fn=run_sim,
    args=(scene, True),
)

# 뷰어 실행 (여기서 시각화가 시작됨)
scene.viewer.start()


