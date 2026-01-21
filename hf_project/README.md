# 🤖 Django AI Playground (Hugging Face Integration)

Django 웹 프레임워크와 Hugging Face Inference API를 연동하여 제작한 AI 웹 서비스입니다.  
사용자는 감정 분석, 뉴스 요약, 한영 번역 기능을 탭 형태로 편리하게 이용할 수 있으며, AJAX 비동기 통신을 적용하여 빠른 사용자 경험을 제공합니다.

## ✨ 주요 기능 (Key Features)

* **3가지 AI 기능 제공:**
    1.  **😊 감정 분석 (Sentiment Analysis):** 영어 문장의 긍정/부정 여부 판단
    2.  **📝 뉴스 요약 (Summarization):** 긴 영어 텍스트를 핵심 내용 3줄로 요약
    3.  **🇰🇷🇬🇧 한영 번역 (Translation):** 한국어 문장을 자연스러운 영어로 번역
* **사용자 권한 관리 (Auth System):**
    * 회원가입/로그인 기능 구현
    * **Public:** 감정 분석은 누구나 사용 가능
    * **Private:** 요약 및 번역은 로그인한 사용자만 접근 가능 (접근 시도 시 로그인 유도)
* **비동기 처리 (AJAX):** 페이지 새로고침 없이 AI 응답을 받아오며, 로딩 인디케이터(Spinner) 제공
* **데이터베이스 연동:** 로그인한 사용자의 AI 대화 내역(History) 자동 저장 및 조회
* **UI/UX:** 반응형 디자인, 카드 UI, 현재 탭 강조 기능

---

## 🧠 사용된 AI 모델 (Models)

Hugging Face의 Inference API를 사용하여 서버 부하 없이 고성능 모델을 활용합니다.

| 기능 | 모델명 (Hugging Face ID) | 설명 |
| :--- | :--- | :--- |
| **감정 분석** | `distilbert-base-uncased-finetuned-sst-2-english` | 가볍고 빠른 DistilBERT 기반의 영어 감정 분류 모델 |
| **뉴스 요약** | `sshleifer/distilbart-cnn-12-6` | CNN 뉴스 데이터로 학습된 BART 기반 요약 모델 |
| **한영 번역** | `Helsinki-NLP/opus-mt-ko-en` | MarianMT 기반의 고성능 한국어 → 영어 번역 모델 |

---

## 🛠 실행 방법 (Installation & Run)

이 프로젝트는 **Python 3.9+** 환경에서 실행하는 것을 권장합니다.

### 1. 가상환경 설치 및 활성화
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (.env)

프로젝트 루트 경로에 .env 파일을 생성하고 Hugging Face API 키를 입력합니다.
```bash
# .env 파일 예시
HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
### 4. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 서버 실행
```bash
python manage.py runserver
```