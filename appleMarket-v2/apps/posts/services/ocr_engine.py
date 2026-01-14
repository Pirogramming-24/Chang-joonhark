from paddleocr import PaddleOCR

class OCREngine:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("🚀 AI 모델(PaddleOCR) 로딩 중...")
            cls._instance = super(OCREngine, cls).__new__(cls)
            
            try:

                cls._instance.model = PaddleOCR(
                    lang='korean', 
                    ocr_version='PP-OCRv3', 
                    use_angle_cls=False,
                    show_log=False
                )
                print("✅ 모델 로딩 성공!")
            except Exception as e:
                print(f"❌ 모델 로딩 오류: {e}")
                cls._instance.model = None

        return cls._instance

    def extract_text(self, img):
        if not self.model:
            return []
            
        try:

            result = self.model.ocr(img, cls=False) 
            texts = []
            if result and result[0]:
                for line in result[0]:
                    # 신뢰도 60% 이상인 글자만 읽기 (이상한 노이즈 제거)
                    if line[1][1] > 0.6:
                        texts.append(line[1][0])
            return texts
        except Exception as e:
            print(f"📉 OCR 분석 중 오류: {e}")
            return []