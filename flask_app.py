from flask import Flask, request, jsonify
import numpy as np
import genesis as gs
import threading

app = Flask(__name__)

# 글로벌 변수
scene = None
franka = None
dofs_idx = None


@app.route('/control', methods=['POST'])
def control_robot():
    global franka, dofs_idx

    # JSON 데이터를 입력받음
    data = request.json
    if not data or 'positions' not in data:
        return jsonify({"error": "Invalid input, 'positions' field is required"}), 400

    # 입력 받은 DOF의 목표 위치 설정
    positions = data['positions']
    if len(positions) != len(dofs_idx):
        return jsonify({"error": f"Expected {len(dofs_idx)} DOF values"}), 400

    # 로봇의 DOF 위치를 업데이트
    franka.control_dofs_position(
        np.array(positions),
        dofs_idx
    )
    return jsonify({"status": "success", "message": "Robot position updated"})


def init_simulation():
    """Genesis 시뮬레이션 초기화"""
    global scene, franka, dofs_idx

    gs.init(backend=gs.gpu)

    # Scene 생성
    scene = gs.Scene(
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(0, -3.5, 2.5),
            camera_lookat=(0.0, 0.0, 0.5),
            camera_fov=30,
            max_FPS=60,
        ),
        sim_options=gs.options.SimOptions(
            dt=0.01,
        ),
        show_viewer=True,
    )

    # 엔티티 추가
    plane = scene.add_entity(gs.morphs.Plane())
    franka = scene.add_entity(
        gs.morphs.MJCF(
            file='xml/franka_emika_panda/panda.xml',
            pos=(0.0, 1.0, 0.0),
            euler=(0, 0, 0),
        )
    )

    # Scene 빌드
    scene.build()

    # DOF 인덱스 가져오기
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

    # 로봇의 기본 제어 게인 설정
    franka.set_dofs_kp(
        kp=np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
        dofs_idx_local=dofs_idx,
    )
    franka.set_dofs_kv(
        kv=np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
        dofs_idx_local=dofs_idx,
    )


def simulation_loop():
    """Genesis 시뮬레이션 루프"""
    while True:
        scene.step()


if __name__ == '__main__':
    # 시뮬레이션 초기화
    init_simulation()

    # 시뮬레이션 루프를 별도 스레드에서 실행
    sim_thread = threading.Thread(target=simulation_loop, daemon=True)
    sim_thread.start()

    # Flask 서버를 별도 스레드에서 실행
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=15000), daemon=True)
    flask_thread.start()

    # Viewer는 메인 스레드에서 실행
    scene.viewer.start()
