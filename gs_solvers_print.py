import genesis as gs

# Genesis 초기화
gs.init(backend=gs.gpu)  # 또는 gs.cpu

# Scene 생성
scene = gs.Scene()

# Plane과 Cube 추가 (솔버 추가될 가능성)
plane = scene.add_entity(gs.morphs.Plane())
cube = scene.add_entity(
    gs.morphs.Box(
        pos=(0, 0, 1.0),
        size=(0.2, 0.2, 0.2),
    ),
)

# Scene 빌드
scene.build()

# Scene에 포함된 솔버 탐색
print("Exploring solvers in the scene:")
for solver in scene.sim.solvers:
    print(f"Solver: {type(solver).__name__}")
    print(dir(solver))  # Solver의 메서드와 속성 출력
    print("=" * 50)  # 구분선