import genesis as gs
import numpy as np

# Genesis 환경 초기화
gs.init(backend=gs.metal)

def run_sim(scene, cam):
    """시뮬레이션 실행 함수"""
    cam.start_recording()

    for i in range(120):
        scene.step()
        cam.set_pose(
            pos=(3.0 * np.sin(i / 60), 3.0 * np.cos(i / 60), 2.5),
            lookat=(0, 0, 0.5),
        )
        cam.render()

    cam.stop_recording(save_to_filename='video.mp4', fps=60)
    scene.viewer.stop()

# Scene 객체 생성
scene = gs.Scene(
    sim_options=gs.options.SimOptions(),
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(3.5, 0.0, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
    ),
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        world_frame_size=1.0,
        show_link_frame=False,
        show_cameras=False,
        plane_reflection=True,
        ambient_light=(0.1, 0.1, 0.1),
    ),
    rigid_options=gs.options.RigidOptions(
        dt=0.01,
        gravity=(0.0, 0.0, -10.0),
    ),
    show_viewer=True,
    renderer=gs.renderers.Rasterizer(),
)

# 씬에 카메라 추가
camera = scene.add_camera(
    model="pinhole",
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0, 0, 0.5),
    fov=30,
    GUI=False,
)

# 씬에 엔티티 추가
plane = scene.add_entity(gs.morphs.Plane())
franka = scene.add_entity(
    gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'),
)

# 씬 빌드
scene.build()

# 시뮬레이션 쓰레드에서 실행
gs.tools.run_in_another_thread(
    fn=run_sim,
    args=(scene, camera)  # 카메라를 인자로 전달
)

# 씬 뷰어 실행
scene.viewer.start()
