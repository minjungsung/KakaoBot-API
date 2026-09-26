# KakaoBot-API

카카오톡 챗봇 연동 API 서버입니다. Flask 기반 웹 서버로 카카오톡 메시지를 수신하고, 다양한 명령어(날씨, 맛집, 로또, 뉴스, 한강온도 등)에 대한 응답을 반환합니다.

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프레임워크** | Flask 2.3 |
| **런타임** | Python 3.x |
| **데이터베이스** | PostgreSQL (SQLAlchemy ORM) |
| **마이그레이션** | Flask-Migrate (Alembic) |
| **웹 스크래핑** | BeautifulSoup4, Playwright, Selenium |
| **배포** | Vercel (Serverless Python) |
| **API 유형** | REST (카카오톡 자동응답 봇 연동) |

## 주요 기능

| 명령어 | 기능 | 데이터 소스 |
|--------|------|------------|
| `.명령어` / `.도움말` | 커맨드 매뉴얼 출력 | 내장 |
| `.구글 [검색어]` | Google 검색 링크 반환 | Google |
| `.맛집 [지역명]` | 카카오맵 맛집 검색 | 카카오맵 |
| `.로또 [숫자]` | 로또 번호 추천 | 랜덤 생성 |
| `.채팅순위 [기간]` | 채팅방 채팅 랭킹 | PostgreSQL |
| `.한강온도` | 현재 한강 수온 | hangang.ivlis.kr |
| `.실검` | 실시간 검색어 TOP 10 | signal.bz |
| `.영화` | 현재 상영작 목록 | 메가박스 |
| `.넌뭐야` | 봇 자기소개 | 내장 |
| `A vs B` | 랜덤 선택 | 랜덤 |

## 기술 스택 상세

```
Flask 2.3.3              → 웹 프레임워크
Flask-SQLAlchemy 3.0.5   → ORM
Flask-Migrate 4.0.5      → DB 마이그레이션
SQLAlchemy 2.0.20        → SQL 툴킷
psycopg2-binary          → PostgreSQL 드라이버
BeautifulSoup4 (bs4)     → HTML 파싱
Playwright               → 브라우저 자동화
Selenium                 → 브라우저 자동화 (레거시)
requests                 → HTTP 클라이언트
tiktoken                 → 토큰 카운팅
python-dotenv            → 환경변수
```

## 프로젝트 구조

```
KakaoBot-API/
├── run.py                  # 로컬 개발 서버 진입점 (port 6000)
├── vercel.json             # Vercel 배포 설정
├── requirements.txt        # Python 의존성
│
├── api/
│   ├── __init__.py         # Flask 앱 초기화, DB 설정
│   ├── main.py             # 라우트 핸들러 (chat, command)
│   ├── model/
│   │   ├── chats.py        # 채팅 로그 모델
│   │   ├── menues.py       # 메뉴 추천 모델
│   │   └── sentences.py    # 정형 문장 모델
│   ├── service/
│   │   └── service.py      # 비즈니스 로직 (스크래핑, 검색 등)
│   └── ddl/
│       └── chatbot.sql     # PostgreSQL 스키마 (DDL)
│
└── .github/workflows/      # CI/CD
```

## Wiki 페이지 목록

- [[Architecture]] — API 구조 및 카카오톡 연동 흐름
- [[API Reference]] — 엔드포인트 상세
- [[Setup Guide]] — 로컬 실행, Vercel 배포, 카카오톡 설정
