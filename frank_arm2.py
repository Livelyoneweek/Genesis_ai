import genesis as gs

# 시뮬레이션을 실행하며, 시뮬레이션이 끝난 후 Viewer를 중지합니다.
def run_sim(scene, enable_vis):
    for i in range(1000):
        scene.step()
    if enable_vis:
        scene.viewer.stop()

# Genesis 환경을 초기화
gs.init(backend=gs.metal)

# scene 객체 생성
scene = gs.Scene(
    sim_options=gs.options.SimOptions(),
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(3.5, 0.0, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
    ),
    show_viewer=True,
    rigid_options=gs.options.RigidOptions(
        dt=0.01,
        gravity=(0.0, 0.0, -10.0),
    ),
)

# 씬에 엔티티 추가
plane = scene.add_entity(gs.morphs.Plane())
franka = scene.add_entity(
    gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'),
)

#씬 빌드
scene.build()

# 시뮬레이션 인자 주면서 실행
gs.tools.run_in_another_thread(
    fn=run_sim, 
    args=(scene, True))

# 씬 뷰어 실행
scene.viewer.start()