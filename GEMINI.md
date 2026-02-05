# GEMINI.md - BizTone Converter (업무 말투 변환기)

이 파일은 BizTone Converter 프로젝트의 구조, 기술 스택, 실행 방법 및 개발 가이드를 담고 있습니다.

## 1. 프로젝트 개요 (Project Overview)
**BizTone Converter**는 일상적인 표현을 비즈니스 상황에 적합한 전문적인 말투로 변환해주는 AI 기반 웹 솔루션입니다. 사용자는 대상을 '상사', '동료', '고객'으로 선택하여 각 상황에 최적화된 결과물을 얻을 수 있습니다.

- **주요 목적**: 업무 생산성 향상, 커뮤니케이션 품질 표준화, 비즈니스 작문 보조.
- **주요 대상**: 신입사원, 주니어 직원, 고객 응대 전문가 등.

## 2. 기술 스택 (Tech Stack)

### 프론트엔드 (Frontend)
- **HTML5 / CSS3**: Tailwind CSS를 활용한 현대적이고 반응형인 UI 구성.
- **JavaScript (ES6+)**: Fetch API를 사용한 비동기 통신 및 DOM 조작.
- **폰트**: Pretendard (가독성 높은 웹폰트).

### 백엔드 (Backend)
- **Python 3.11**: 메인 개발 언어.
- **Flask**: 경량 웹 프레임워크를 사용한 RESTful API 제공.
- **Groq AI API**: `moonshotai/kimi-k2-instruct-0905` 모델을 활용한 자연어 변환.
- **dotenv**: 환경 변수 관리 (`GROQ_API_KEY`).

## 3. 프로젝트 구조 (Project Structure)
```
C:\vibe_coding\biztalk_llm\
├── backend/
│   ├── app.py             # Flask 애플리케이션 및 AI 연동 로직
│   ├── requirements.txt   # 백엔드 의존성 패키지
│   └── .env               # 환경 변수 (API 키 등)
├── frontend/
│   ├── index.html         # 메인 페이지 구조
│   ├── css/               # 스타일 시트 (style.css - 현재 Tailwind 사용 중)
│   └── js/
│       └── script.js      # 클라이언트 측 로직 (API 호출, 복사 기능 등)
├── PRD.md                 # 제품 요구사항 문서 (Product Requirements Document)
├── 프로그램개요서.md      # 프로젝트 기획 및 설계 요약
├── my-rules.md            # Gemini CLI 지침 (한국어)
└── GEMINI.md              # 프로젝트 안내서 (본 파일)
```

## 4. 실행 및 테스트 (Running and Testing)

### 백엔드 실행
1. 가상 환경 활성화:
   ```powershell
   # Windows
   .venv\Scripts\activate
   ```
2. 의존성 설치:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. 환경 변수 설정: `backend/.env` 파일에 `GROQ_API_KEY`를 설정합니다.
4. 서버 실행:
   ```bash
   python backend/app.py
   ```
### Vercel 배포 시 주의사항
- Vercel 대시보드에서 `GROQ_API_KEY` 환경 변수를 반드시 설정해야 합니다.
- `vercel.json` 설정에 따라 `/api/*` 요청은 Flask 백엔드로, 그 외 요청은 프론트엔드 정적 파일로 라우팅됩니다.

## 5. 개발 규칙 및 컨벤션 (Development Conventions)

- **언어**: 사용자 피드백 및 응답은 한국어를 기본으로 합니다. (참조: `my-rules.md`)
- **API 디자인**: `/api/convert` 엔드포인트를 통해 JSON 형식으로 통신합니다.
- **AI 프롬프트**: `backend/app.py` 내의 `PROMPTS` 딕셔너리에 대상별(Upward, Lateral, External) 지침이 정의되어 있습니다.
- **코드 스타일**:
    - 백엔드: PEP 8 표준 준수 및 명확한 로깅 사용.
    - 프론트엔드: Tailwind CSS 클래스를 활용한 유틸리티 우선 방식 지향.

## 6. 향후 계획 (Roadmap)
- [x] Vercel을 통한 배포 파이프라인 구축 (`vercel.json` 설정 완료).
- [ ] 변환 결과의 주요 변경점 하이라이트 기능 추가.
- [ ] 사용자 피드백(도움됨/안됨) 수집 기능 구현.
