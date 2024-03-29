from flask import request
from api.service import service
import logging
from logging.handlers import RotatingFileHandler
from api import app, db
import traceback
from api.model.chats import chats

zodiac_commands = [
    "쥐띠",
    "소띠",
    "호랑이띠",
    "토끼띠",
    "용띠",
    "뱀띠",
    "말띠",
    "양띠",
    "원숭이띠",
    "닭띠",
    "개띠",
    "돼지띠",
]
horoscope_commands = [
    "양자리",
    "황소자리",
    "쌍둥이자리",
    "게자리",
    "사자자리",
    "처녀자리",
    "천칭자리",
    "전갈자리",
    "사수자리",
    "염소자리",
    "물병자리",
    "물고기자리",
]


@app.route("/api/chat", methods=["GET"])
def chat():
    msg = request.args.get("msg")
    sender = request.args.get("sender")
    room = request.args.get("room")
    isGroupChat = request.args.get("isGroupChat")

    # db 로깅
    try:
        new_chat = chats(
            room=room, sender=sender, msg=msg, isGroupChat=bool(isGroupChat)
        )
        db.session.add(new_chat)
        db.session.commit()
    except Exception as e:
        print(e)
        traceback.print_exc()
    return ""


@app.route("/api/command", methods=["GET"])
def command():

    msg = request.args.get("msg")
    sender = request.args.get("sender")
    room = request.args.get("room")
    isGroupChat = request.args.get("isGroupChat")

    # db 로깅
    new_chat = chats(room=room, sender=sender, msg=msg, isGroupChat=bool(isGroupChat))
    db.session.add(new_chat)
    db.session.commit()

    msgSplit = msg.split()
    res = ""
    try:
        if "vs" in msg:
            msgSplit = msg.split("vs")
            res = service.getVs(msgSplit, sender)

        if msgSplit[0][0] == ".":

            if msgSplit[0] in [".안녕", ".명령어", ".도움말", ".help"]:
                res = f"""안녕하세요, {sender}님!\U0001F60D
<민정봇 커맨드 매뉴얼>

NAME
    민정봇

[기본 명령어]
    .명령어, .도움말, .help : 커맨드 목록

*대괄호 [ ] 빼고 입력해주세요.    
[정보 검색]

>>  .구글 [검색어]
>>  .맛집 [검색어/지역명]
>>  .로또 [숫자]
>>  .채팅순위 [오늘/일주일/한달]
>>  .넌뭐야
>>  .한강온도
>>  .실검

"""
            elif msgSplit[0] == ".넌뭐야":
                res = "저는 민정봇이에오"

            elif msgSplit[0] == ".구글":
                if len(msgSplit) != 1:
                    keyword = msg.replace(msgSplit[0], "").strip()
                    keyword = keyword.replace(" ", "+")
                    res = service.googleSearch(keyword)
                else:
                    res = "검색어를 입력해주세요. \n사용법 : .구글 [검색어]"

            elif msgSplit[0] == ".맛집":
                area = ""
                if len(msgSplit) != 1:
                    area = msg.replace(msgSplit[0], "").strip()
                    area = area.replace(" ", "+")
                    res = service.getRestaurantByArea(area.strip())
                else:
                    res = "지역을 입력해주세요. \n사용법 : .맛집 [지역명]"

            elif msgSplit[0] == ".로또":
                print(len(msgSplit))
                if len(msgSplit) != 1:
                    num = msg.replace(msgSplit[0], "").strip()
                    if num.isdigit():
                        res = service.getLottery(sender, int(num))
                    else:
                        res = "숫자를 입력해주세요.\n사용법: .로또 [세트 개수]"
                else:
                    res = service.getLottery(sender, 1)

            elif msgSplit[0] == ".채팅순위":
                res = service.getChatRank(room, msgSplit[1])

            #             elif msgSplit[0] == ".예보":
            #                 area = ""
            #                 if len(msgSplit) != 1:
            #                     if len(msgSplit) >= 3:
            #                         for i in range(1, len(msgSplit)):
            #                             print(i)
            #                             area = area + msgSplit[i] + " "
            #                     else:
            #                         area = msgSplit[1]
            #                     res = service.getTomorrowWeather(area.strip())
            #                 else:
            #                     res = "지역을 입력해주세요. \n사용법 : .예보 [지역명]"

            #             elif msgSplit[0] == ".나무":
            #                 if len(msgSplit) != 1:
            #                     keyword = msg.replace(msgSplit[0], "").strip()
            #                     keyword = keyword.replace(" ", "+")
            #                     res = service.namuSearch(keyword)
            #                 else:
            #                     res = "검색어를 입력해주세요. \n사용법 : .나무 [검색어]"
            #             elif msgSplit[0] == ".유튜브":
            #                 if len(msgSplit) != 1:
            #                     keyword = msg.replace(msgSplit[0], "").strip()
            #                     keyword = keyword.replace(" ", "+")
            #                     print(keyword)
            #                     res = service.youtubeSearch(keyword)
            #                 else:
            #                     res = "검색어를 입력해주세요. \n사용법 : .유튜브 [검색어]"
            #             elif msgSplit[0] == ".뉴스":
            #                 if len(msgSplit) != 1:
            #                     keyword = msg.replace(msgSplit[0], "").strip()
            #                     if keyword.isdigit():
            #                         keyword = int(keyword)
            #                         if keyword < 5:
            #                             res = service.getNews(keyword)
            #                         else:
            #                             res = "분야를 다시 입력해 주세요."
            #                     else:
            #                         keyword = keyword.replace(" ", "+")
            #                         res = service.getNewsSearch(keyword)
            #                 else:
            #                     res = """분야를 입력해주세요.
            # 사용법 : !뉴스 [0|1|2|3|4|검색어]

            # 0 : 정치
            # 1 : 경제
            # 2 : 사회
            # 3 : 생활/문화
            # 4 : IT/과학
            # 검색어 : 관련 뉴스 검색
            # """
            elif msgSplit[0] == ".실검":
                res = service.realtime()
            #             elif msgSplit[0] == ".환율":
            #                 res = service.getExchangeRate()
            #             elif msgSplit[0] == ".비트":
            #                 res = service.getAllCoins()

            #             elif msgSplit[0] == ".지도":
            #                 area = ""
            #                 if len(msgSplit) != 1:
            #                     area = msg.replace(msgSplit[0], "").strip()
            #                     area = area.replace(" ", "+")
            #                     res = service.getMapSearch(area.strip())
            #                 else:
            #                     res = "지역을 입력해주세요. \n사용법 : .지도 [지역명]"
            #             elif msgSplit[0] in [".메뉴추천", ".점메추", ".저메추"]:
            #                 res = service.getMenu(sender)

            elif msgSplit[0] == ".한강온도":
                res = service.getHanRiverTemp()
            #             elif msgSplit[0] == ".자살":
            #                 res = service.getSuicide(sender)
            #             elif msgSplit[0] in [
            #                 "!고마워",
            #                 "!감사해",
            #                 "!넌최고야",
            #                 "!사랑해",
            #                 "!재밌어",
            #             ]:
            #                 res = service.getThanks()
            #             elif msgSplit[0] == ".강퇴":
            #                 if len(msgSplit) != 1:
            #                     name = msg.replace(msgSplit[0], "").strip()
            #                     name = name.replace(" ", "")
            #                     res = service.getOut(name)
            #                 else:
            #                     res = "강퇴할 사람을 입력해주세요. \n사용법 : .강퇴 [닉네임]"

            #             elif msgSplit[0] in [".멜론차트", ".멜론"]:
            #                 res = service.getMelonChart()
            elif msgSplit[0] in [".영화", ".현재상영작", ".영화추천"]:
                res = service.getMovieList()
            # else:
                # res = (
                #     "명령을 인식할 수 없습니다.\n.명령어로 명령어를 조회할 수 있습니다."
                # )

    except Exception as e:
        print(e)
        traceback.print_exc()
        res = ""

    return res
