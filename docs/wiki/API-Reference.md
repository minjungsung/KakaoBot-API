# API Reference

## 기본 정보

| 항목 | 값 |
|------|-----|
| **로컬 Base URL** | `http://localhost:6000` |
| **Vercel Base URL** | Vercel 배포 URL |
| **프로토콜** | HTTP/REST |
| **응답 형식** | Plain Text |

## 엔드포인트

### `GET /api/chat`

일반 채팅 메시지를 데이터베이스에 로그로 저장합니다.

**쿼리 파라미터:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `msg` | string | Yes | 메시지 내용 |
| `sender` | string | Yes | 발신자 닉네임 |
| `room` | string | Yes | 채팅방 이름 |
| `isGroupChat` | boolean | No | 그룹 채팅 여부 |

**요청 예시:**
```http
GET /api/chat?msg=안녕하세요&sender=민정&room=친구방&isGroupChat=true
```

**응답:**
```
(빈 문자열)
```

---

### `GET /api/command`

`.` 접두사 명령어를 처리하고 결과를 반환합니다.

**쿼리 파라미터:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `msg` | string | Yes | 명령어 메시지 |
| `sender` | string | Yes | 발신자 닉네임 |
| `room` | string | Yes | 채팅방 이름 |
| `isGroupChat` | boolean | No | 그룹 채팅 여부 |

**명령어 목록 및 응답 예시:**

#### `.명령어` / `.도움말` / `.help` / `.안녕`

```http
GET /api/command?msg=.명령어&sender=민정&room=친구방
```

```
안녕하세요, 민정님!😍
<민정봇 커맨드 매뉴얼>

[기본 명령어]
    .명령어, .도움말, .help : 커맨드 목록

[정보 검색]
>>  .구글 [검색어]
>>  .맛집 [검색어/지역명]
>>  .로또 [숫자]
>>  .채팅순위 [오늘/일주일/한달]
>>  .넌뭐야
>>  .한강온도
>>  .실검
```

#### `.구글 [검색어]`

```http
GET /api/command?msg=.구글 NestJS&sender=민정&room=친구방
```

```
https://www.google.com/search?q=NestJS
```

#### `.맛집 [지역명]`

```http
GET /api/command?msg=.맛집 강남&sender=민정&room=친구방
```

```
['강남 맛집' 카카오맵 검색 결과]

1. 레스토랑A(양식)
주소: 서울시 강남구 ...
링크: https://...

2. 레스토랑B(한식)
주소: 서울시 강남구 ...
링크: https://...
```

#### `.로또 [숫자]`

```http
GET /api/command?msg=.로또 3&sender=민정&room=친구방
```

```
민정님을 위한 로또 추천번호!

번호 1: [3, 12, 18, 25, 33, 42]
번호 2: [7, 14, 21, 28, 35, 44]
번호 3: [1, 9, 17, 26, 38, 45]
```

#### `.채팅순위 [기간]`

```http
GET /api/command?msg=.채팅순위 오늘&sender=민정&room=친구방
```

```
[친구방] 채팅방의 채팅순위입니다. (기간: 오늘)
총 채팅 갯수 : 150개

1위 민정 - 채팅 45개 (30.0% Lv.10)
2위 철수 - 채팅 30개 (20.0% Lv.7)
```

#### `.한강온도`

```http
GET /api/command?msg=.한강온도&sender=민정&room=친구방
```

```
[현재 한강물 온도]

온도 : 18.5°C
```

#### `A vs B` (선택)

```http
GET /api/command?msg=치킨 vs 피자&sender=민정&room=친구방
```

```
선택이 어려운 "민정"님을 위한 결과는~
[치킨] 입니다!
```

## 에러 처리

명령어 실행 중 에러 발생 시 빈 문자열(`""`)을 반환하며, 서버 로그에 traceback을 출력합니다.

```python
except Exception as e:
    print(e)
    traceback.print_exc()
    res = ""
```

## 데이터베이스 모델

### chats

모든 수신 메시지를 기록합니다.

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | SERIAL PK | 자동 증가 ID |
| room | VARCHAR(300) | 채팅방 이름 |
| sender | VARCHAR(300) | 발신자 |
| msg | TEXT | 메시지 내용 |
| isGroupChat | BOOLEAN | 그룹 채팅 여부 |
| create_date | TIMESTAMP | 생성 일시 |
| update_date | TIMESTAMP | 수정 일시 |
