# Setup Guide

## 사전 요구사항

| 도구 | 최소 버전 | 설치 방법 |
|------|----------|----------|
| **Python** | 3.8+ | [python.org](https://www.python.org/) |
| **pip** | 최신 | Python에 포함 |
| **PostgreSQL** | 12+ | [postgresql.org](https://www.postgresql.org/) |
| **Playwright** | 최신 | `pip install playwright && playwright install` |

## 1단계: 클론 및 의존성 설치

```bash
git clone https://github.com/minjungsung/KakaoBot-API.git
cd KakaoBot-API

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 의존성 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install chromium
```

## 2단계: 데이터베이스 설정

### PostgreSQL 데이터베이스 생성

```bash
# PostgreSQL에 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE chatbot;
\q
```

### 스키마 초기화

```bash
# DDL 파일로 테이블 생성
psql -U postgres -d chatbot -f api/ddl/chatbot.sql
```

또는 Flask-Migrate를 통한 자동 생성:

```bash
flask db upgrade
```

### 환경변수 설정

`.env` 파일을 프로젝트 루트에 생성합니다.

```env
DB_URL=postgresql://postgres:password@localhost:5432/chatbot
```

## 3단계: 로컬 서버 실행

```bash
python run.py
```

서버가 `http://0.0.0.0:6000`에서 시작됩니다. (debug 모드)

### 동작 확인

```bash
# 명령어 테스트
curl "http://localhost:6000/api/command?msg=.한강온도&sender=test&room=testroom"

# 채팅 로그 테스트
curl "http://localhost:6000/api/chat?msg=hello&sender=test&room=testroom"
```

## 4단계: Vercel 배포

### Vercel CLI 사용

```bash
# Vercel CLI 설치
npm install -g vercel

# 배포
vercel

# 프로덕션 배포
vercel --prod
```

### 환경변수 설정 (Vercel)

Vercel 대시보드 → 프로젝트 설정 → Environment Variables:

| 변수명 | 값 | 설명 |
|--------|-----|------|
| `DB_URL` | `postgresql://...` | PostgreSQL 연결 URL |

### vercel.json 구조

```json
{
  "version": 2,
  "builds": [
    { "src": "api/main.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "api/main.py" }
  ]
}
```

## 5단계: 카카오톡 봇 설정

### 카카오톡 자동응답 봇 연동

1. 카카오톡 자동응답 봇 앱 설치 (안드로이드)
2. 봇 설정에서 API URL 입력:
   - 채팅 로그: `{VERCEL_URL}/api/chat`
   - 명령어 처리: `{VERCEL_URL}/api/command`
3. 파라미터 매핑 설정:
   - `msg` → 메시지 내용
   - `sender` → 발신자
   - `room` → 채팅방
   - `isGroupChat` → 그룹 여부

### 연동 흐름

```
카카오톡 메시지 수신
       │
       ▼
자동응답 봇 앱 (Android)
       │
       ├─ 일반 메시지 → GET /api/chat
       └─ 명령어 (.xxx) → GET /api/command
              │
              ▼
       Flask API 서버 (Vercel)
              │
              ▼
       응답 텍스트 → 카카오톡 전송
```

## 트러블슈팅

### Playwright 설치 오류

```bash
# 브라우저 바이너리 재설치
playwright install --with-deps chromium
```

### DB 연결 오류

```
sqlalchemy.exc.OperationalError: connection refused
```

→ PostgreSQL 서비스 실행 확인: `pg_isready`
→ `.env`의 `DB_URL` 형식 확인

### Vercel 빌드 실패

→ `requirements.txt`에 모든 의존성이 포함되어 있는지 확인
→ Playwright는 Vercel 서버리스 환경에서 제한적 — `requests + BS4` 대안 고려

### Selenium WebDriver 오류

```bash
# webdriver-manager가 자동으로 ChromeDriver 관리
pip install webdriver-manager
```
