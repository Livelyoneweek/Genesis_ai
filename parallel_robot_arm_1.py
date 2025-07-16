import numpy as np
import genesis as gs
import torch

########################## init ##########################
gs.init(backend=gs.gpu)

########################## create a scene ##########################
scene = gs.Scene(
    viewer_options = gs.options.ViewerOptions(
        camera_pos    = (0, -3.5, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        max_FPS       = 60,
    ),
    sim_options = gs.options.SimOptions(
        # dt = 0.01,
    ),
    show_viewer = True,
)

########################## entities ##########################
plane = scene.add_entity(
    gs.morphs.Plane(),
)

# when loading an entity, you can specify its pose in the morph.
franka = scene.add_entity(
    gs.morphs.MJCF(
        file  = 'xml/franka_emika_panda/panda.xml',
        pos   = (0.0, 1.0, 0.0),
        euler = (0, 0, 0),
    ),
)

########################## build ##########################
B = 10  # 병렬 환경 개수
scene.build(n_envs=B, env_spacing=(1.0, 1.0))  # 20개의 환경 생성


jnt_names = [
    'joint1',
    'joint2',
    'joint3',
    'joint4',
    'joint5',
    'joint6',
    'joint7',
    'finger_joint1',
    'finger_joint2',
]
dofs_idx = [franka.get_joint(name).dof_idx_local for name in jnt_names]

############ Optional: set control gains ############
# set positional gains
franka.set_dofs_kp(
    kp             = np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
    dofs_idx_local = dofs_idx,
)
# set velocity gains
franka.set_dofs_kv(
    kv             = np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
    dofs_idx_local = dofs_idx,
)
# set force range for safety
franka.set_dofs_force_range(
    lower          = np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
    upper          = np.array([ 87,  87,  87,  87,  12,  12,  12,  100,  100]),
    dofs_idx_local = dofs_idx,
)

########################## run simulation ##########################
def run_sim(scene, enable_vis):
    for i in range(1250):
        if i == 0:
            franka.control_dofs_position(
                torch.tile(
                    torch.tensor([1, 1, 0, 0, 0, 0, 0, 0.04, 0.04], device=gs.device),
                    (B, 1),
                ),
                dofs_idx,
            )
        elif i == 250:
            franka.control_dofs_position(
                torch.tile(
                    torch.tensor([-1, 0.8, 1, -2, 1, 0.5, -0.5, 0.04, 0.04], device=gs.device),
                    (B, 1),
                ),
                dofs_idx,
            )
        elif i == 500:
            franka.control_dofs_position(
                torch.tile(
                    torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0], device=gs.device),
                    (B, 1),
                ),
                dofs_idx,
            )
        elif i == 750:
            # Control first DOF with velocity, others with position
            franka.control_dofs_position(
                torch.tile(
                    torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0], device=gs.device),
                    (B, 1),
                )[:, 1:],
                dofs_idx[1:],
            )
            franka.control_dofs_velocity(
                torch.tile(
                    torch.tensor([1.0, 0, 0, 0, 0, 0, 0, 0, 0], device=gs.device),
                    (B, 1),
                )[:, :1],
                dofs_idx[:1],
            )
        elif i == 1000:
            franka.control_dofs_force(
                torch.tile(
                    torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0], device=gs.device),
                    (B, 1),
                ),
                dofs_idx,
            )

        # Log control and internal forces for debugging (1st robot in batch)
        print(f"Step {i}")
        print('control force:', franka.get_dofs_control_force(dofs_idx)[:1])
        print('internal force:', franka.get_dofs_force(dofs_idx)[:1])

        scene.step()  # 시뮬레이션 스텝 진행

    if enable_vis:
        scene.viewer.stop()


# 시뮬레이션 실행을 별도 스레드에서 처리
gs.tools.run_in_another_thread(
    fn=run_sim,
    args=(scene, True),
)

# 뷰어 실행 (여기서 시각화가 시작됨)
scene.viewer.start()