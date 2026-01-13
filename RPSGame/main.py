import cv2
import mediapipe as mp
import math
import visualization  # visualization.py 모듈

# visualization.py의 draw_manual 함수 호환용 클래스
class DetectionResult:
    def __init__(self, multi_hand_landmarks):
        self.hand_landmarks = multi_hand_landmarks

def get_distance(p1, p2):
    """두 점 사이의 유클리드 거리 계산"""
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def determine_rps(hand_landmarks):
    """
    제안해주신 로직 적용:
    1. 손목(0)과 TIP(손끝) 거리 vs 손목(0)과 PIP(중간마디) 거리 비교
    2. 펴진 손가락 개수로 가위/바위/보 판별 (엄지 제외)
    """
    # 랜드마크 리스트 추출
    lm = hand_landmarks.landmark
    
    # 손가락 별 인덱스 정의 (엄지 제외)
    # [Tip 인덱스, PIP 인덱스]
    finger_indices = {
        "Index": [8, 6],   # 검지
        "Middle": [12, 10],# 중지
        "Ring": [16, 14],  # 약지
        "Pinky": [20, 18]  # 소지
    }
    
    # 펴진 손가락 개수 세기
    extended_count = 0
    
    wrist = lm[0] # 손목 좌표
    
    for name, indices in finger_indices.items():
        tip = lm[indices[0]]
        pip = lm[indices[1]]
        
        # (1) TIP과 손목 사이의 거리
        dist_tip_wrist = get_distance(tip, wrist)
        # (2) PIP와 손목 사이의 거리
        dist_pip_wrist = get_distance(pip, wrist)
        
        # 거리를 비교하여 펴졌는지 판단
        # 손가락을 펴면 손목에서 손끝까지의 거리가 중간마디까지의 거리보다 멉니다.
        if dist_tip_wrist > dist_pip_wrist:
            extended_count += 1
            
    # 개수에 따른 결과 판별
    if extended_count == 0:
        return 0 # Rock (바위) - 모두 접힘
    elif extended_count == 2:
        return 2 # Scissors (가위) - 검지, 중지 2개만 펴짐
    elif extended_count == 4:
        return 1 # Paper (보) - 4개 모두 펴짐 (엄지 제외)
    
    return None # 그 외(1개나 3개 펴진 경우 등)는 판별 불가

def main():
    # MediaPipe Hands 설정
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    print("카메라가 시작됩니다. 종료하려면 'q'를 누르세요.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # 1. 미러링 및 색상 변환
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 2. MediaPipe 처리
        results = hands.process(frame_rgb)

        # 3. 결과 처리
        rps_result = None

        if results.multi_hand_landmarks:
            # 시각화를 위한 래퍼 생성
            detection_result = DetectionResult(results.multi_hand_landmarks)
            
            # 랜드마크 그리기
            frame = visualization.draw_manual(frame, detection_result)

            # 첫 번째 감지된 손에 대해 로직 수행
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # 가위바위보 판별 (거리 기반 로직)
            rps_result = determine_rps(hand_landmarks)

        # 4. 결과 텍스트 출력
        frame = visualization.print_RSP_result(frame, rps_result)

        # 5. 화면 출력
        cv2.imshow('Rock Paper Scissors', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == "__main__":
    main()