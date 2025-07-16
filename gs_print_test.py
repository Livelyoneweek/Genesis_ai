
import torch
print(torch.backends.mps.is_available())

print(torch.backends.mps.is_built())



import genesis as gs

# print(gs.__all__)  # 사용 가능한 API 확인
# print(gs.__version__)  # 모듈 버전 확인

print(dir(gs))  # Genesis 모듈에서 사용 가능한 속성 확인
print(gs.__version__)  # 모듈 버전 출력 (이 부분은 정상적으로 작동해야 함)

if hasattr(gs, 'generate'):
    print("gs.generate() 메서드가 존재합니다!")
else:
    print("gs.generate() 메서드가 없습니다.")