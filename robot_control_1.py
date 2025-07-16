import numpy as np
import genesis as gs

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
        dt = 0.01,
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
        pos   = (1.0, 1.0, 0.0),
        euler = (0, 0, 0),
    ),
)

########################## build ##########################
scene.build()

########################## run simulation ##########################
def run_sim(scene, enable_vis):
    for i in range(1000):  # 시뮬레이션 스텝 반복
        scene.step()
    if enable_vis:
        scene.viewer.stop()

# 시뮬레이션 실행을 별도 스레드에서 처리
gs.tools.run_in_another_thread(
    fn=run_sim,
    args=(scene, True),
)

# 뷰어 실행 (여기서 시각화가 시작됨)
scene.viewer.start()


