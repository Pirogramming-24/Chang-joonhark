from transformers import pipeline

# 1. 사용할 모델 이름 정의
MODEL_NAMES = {
    'sentiment': "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    'summary': "sshleifer/distilbart-cnn-12-6",
    'translate': "Helsinki-NLP/opus-mt-ko-en"
}

# 2. 로딩된 파이프라인을 저장할 전역 변수 (캐시 역할)
# 처음엔 비어있다가, 사용자가 기능을 쓰면 여기에 저장됩니다.
LOADED_PIPELINES = {}

def load_pipeline_model(task):
    """
    모델이 로딩되어 있으면 반환하고, 없으면 새로 로딩해서 저장함.
    """
    if task in LOADED_PIPELINES:
        return LOADED_PIPELINES[task]

    print(f"🔄 모델 로딩 시작: {task} (처음 한 번만 실행됨)...")
    
    model_name = MODEL_NAMES[task]
    
    # task 이름 매핑 (Django 앱 task 이름 -> Transformers task 이름)
    tf_task = ""
    if task == 'sentiment':
        tf_task = "text-classification"
    elif task == 'summary':
        tf_task = "summarization"
    elif task == 'translate':
        tf_task = "translation_ko_to_en" # 번역은 방향 지정 필요

    # 파이프라인 생성 (여기서 모델 다운로드/로딩 발생)
    pipe = pipeline(tf_task, model=model_name)
    
    # 캐시에 저장
    LOADED_PIPELINES[task] = pipe
    print(f"✅ 모델 로딩 완료: {task}")
    
    return pipe

def get_ai_response(task, input_text):
    """
    뷰(View)에서 호출하는 함수
    """
    try:
        # 1. 해당 기능의 파이프라인 가져오기
        pipe = load_pipeline_model(task)
        
        # 2. 모델 실행
        # (결과는 리스트 형태 [ {...} ] 로 나옴)
        result = pipe(input_text)
        
        # 3. 결과 파싱 (모델마다 결과 형식이 조금씩 다름)
        if task == 'sentiment':
            # 예: [{'label': 'POSITIVE', 'score': 0.99}]
            label = result[0]['label']
            score = round(result[0]['score'] * 100, 2)
            return f"{label} ({score}%)"
            
        elif task == 'summary':
            # 예: [{'summary_text': '요약된 문장...'}]
            return result[0]['summary_text']
            
        elif task == 'translate':
            # 예: [{'translation_text': 'Translated text...'}]
            return result[0]['translation_text']
            
        return str(result)

    except Exception as e:
        print(f"Error processing {task}: {e}")
        return f"에러 발생: {str(e)}"