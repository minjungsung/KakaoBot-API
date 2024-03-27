import bs4, requests, random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random
import time
from api import db
from sqlalchemy.sql import func
from playwright.sync_api import sync_playwright
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

import re


def getTodayWeather(area):
    with sync_playwright() as p:
        # Launch the browser. Replace 'chromium' with 'firefox' or 'webkit' if needed.
        browser = p.chromium.launch(
            headless=True
        )  # Set headless=False if you want to see the browser
        page = browser.new_page()
        page.goto(
            f"https://search.daum.net/search?q={area}%20날씨", wait_until="networkidle"
        )

        # Now, use Playwright's API to interact with the page similar to how you did with BeautifulSoup
        # Example: Extracting temperature
        now_temp = page.query_selector(
            "div.info_temp div span span > strong"
        ).inner_text()
        desc_temp = page.query_selector(
            "div.info_temp div span span > span"
        ).inner_text()
        txt_desc = page.query_selector("div.info_temp > p").inner_text()
        wind = (
            page.query_selector("dl.dl_weather > dt").inner_text()
            + " "
            + page.query_selector("dl.dl_weather > dd").inner_text()
        )
        humidity = (
            page.query_selector("dl.dl_weather > dt:nth-of-type(2)").inner_text()
            + " "
            + page.query_selector("dl.dl_weather > dd:nth-of-type(2)").inner_text()
        )
        fine_dust = (
            page.query_selector("dl.dl_weather > dt:nth-of-type(3)").inner_text()
            + " "
            + page.query_selector("dl.dl_weather > dd:nth-of-type(3)").inner_text()
        )

        # Construct the response string as before
        res = f"""[{area} 날씨 정보]
위치: (You'll need to adapt this part)
온도: {now_temp} 
날씨: {desc_temp} ({txt_desc})   
{wind} | {humidity} | {fine_dust}

(Additional data and 출처 : 다음날씨)
"""
        browser.close()
        return res


def getTomorrowWeather(area):

    source = requests.get(
        "https://search.daum.net/search?q=" + "내일%20" + area + "%20날씨",
        headers=headers,
    )
    soup = BeautifulSoup(source.content, "html.parser")

    cont_tomorrow = soup.find("div", {"class": "cont_tomorrow"})
    am_weather = (
        cont_tomorrow.select("div.info_tomorrow span.tit_ampm > span.txt_weather")
    )[0].text
    am_temp = (
        cont_tomorrow.select("div.info_tomorrow span.desc_temp > strong.txt_temp")
    )[0].text
    pm_weather = (
        cont_tomorrow.select("div.info_tomorrow span.tit_ampm > span.txt_weather")
    )[1].text
    pm_temp = (
        cont_tomorrow.select("div.info_tomorrow span.desc_temp > strong.txt_temp")
    )[1].text

    area_hourly = soup.find("div", {"class": "area_hourly"})
    time_list = [
        item.select_one(".txt_time").text
        for item in area_hourly.select("ul.list_hourly > li")
    ]
    weather_hourly = [
        item.select_one(".ico_nws").text
        for item in area_hourly.select("ul.list_hourly > li")
    ]
    area_rain = soup.find("div", {"class": "area_rain"})
    rain_hourly = [
        item.select_one(".txt_emph").text.strip()
        for item in area_rain.select("ul.list_hourly > li")
    ]
    area_wind = soup.find("div", {"class": "area_wind"})
    wind_hourly = [
        item.select_one(".txt_num").text
        for item in area_wind.select("ul.list_hourly > li")
    ]
    wind_direct_hourly = [
        item.select_one(".ico_wind").text
        for item in area_wind.select("ul.list_hourly > li")
    ]
    area_damp = soup.find("div", {"class": "area_damp"})
    damp_hourly = [
        item.select_one(".txt_num").text
        for item in area_damp.select("ul.list_hourly > li")
    ]

    data_hourly = ""
    for i in range(0, len(weather_hourly)):
        data_hourly = (
            data_hourly
            + f"{time_list[i]}:{weather_hourly[i]} / 강수확률({rain_hourly[i]}) / 습도({damp_hourly[i]}) / {wind_direct_hourly[i]}({wind_hourly[i]})\n"
        )

    area_tab = soup.find("div", {"class": "tab_region"})
    local_area = [item.text for item in area_tab.select("ul.list_tab > li")]
    local_area = " ".join(
        [
            item.strip()
            for item in local_area
            if item.strip() not in ["전국", "시·군·구", "읍·면·동"]
            and not item.strip().startswith("다른")
        ]
    )

    res = f"""[내일 {area} 날씨 정보]
위치: {local_area}
오전: {am_weather}({am_temp})
오후: {pm_weather}({pm_temp})

{data_hourly}
*(출처 : 다음날씨)
"""
    return res


def getOverseasWeather(area):

    source = requests.get(
        "https://search.daum.net/search?q=" + area + "%20날씨", headers=headers
    )
    soup = BeautifulSoup(source.content, "html.parser")

    area_today = soup.find("div", {"class": "area_today"})

    now_temp = (area_today.select("div.today_item > em.num_avg"))[0].text
    txt_info = (area_today.select("div.today_item div.wrap_txt > span.txt_info"))[
        0
    ].text.strip()
    txt_time = (area_today.select("div.today_item div.wrap_txt > span.txt_time"))[
        0
    ].text.strip()
    wind = (
        (area_today.select("div.today_item dl > dt"))[0].text
        + " "
        + (area_today.select("div.today_item dl > dd"))[0].text
    )
    humidity = (
        (area_today.select("div.today_item dl > dt"))[1].text
        + " "
        + (area_today.select("div.today_item dl > dd"))[1].text
    )
    fine_dust = (
        (area_today.select("div.today_item dl > dt"))[2].text
        + " "
        + (area_today.select("div.today_item dl > dd"))[2].text
    )

    area_hourly = soup.find("div", {"class": "area_hourly"})
    time_list = [
        item.select_one(".txt_time").text
        for item in area_hourly.select("ul.list_hourly > li")
    ]
    weather_hourly = [
        item.select_one(".ico_wtws").text
        for item in area_hourly.select("ul.list_hourly > li")
    ]
    area_rain = soup.find("div", {"class": "area_rain"})
    rain_hourly = [
        item.select_one(".txt_emph").text.strip()
        for item in area_rain.select("ul.list_hourly > li")
    ]
    area_wind = soup.find("div", {"class": "area_wind"})
    wind_hourly = [
        item.select("span")[-1].text for item in area_wind.select("ul.list_hourly > li")
    ]
    wind_direct_hourly = [
        item.select_one(".ico_wind").text
        for item in area_wind.select("ul.list_hourly > li")
    ]
    area_damp = soup.find("div", {"class": "area_damp"})
    damp_hourly = [
        item.select("span")[-1].text for item in area_damp.select("ul.list_hourly > li")
    ]

    data_hourly = ""
    for i in range(0, len(weather_hourly)):
        data_hourly = (
            data_hourly
            + f"{time_list[i]}:{weather_hourly[i]} / 강수확률({rain_hourly[i]}) / 습도({damp_hourly[i]}) / {wind_direct_hourly[i]}({wind_hourly[i]})\n"
        )

    area_tab = soup.find("div", {"class": "tab_comp tab_tree"})
    local_area = [item.text for item in area_tab.select("ul.list_tab.list_opt > li")]
    local_area = " ".join(
        [
            item.strip()
            for item in local_area
            if item.strip() not in ["전국", "시·군·구", "읍·면·동"]
            and not item.strip().startswith("다른")
        ]
    )

    res = f"""[{area} 날씨 정보]
위치: {local_area}
온도: {now_temp} 
날씨: {txt_info} ({txt_time})   
{wind} | {humidity} | {fine_dust}

{data_hourly}
*(출처 : 다음날씨)
"""
    return res


def getLottery(sender, num):
    if num > 10:
        num = 10
    lotto_numbers = []
    for i in range(0, num):
        lotto_numbers.append(sorted(random.sample(range(1, 46), 6)))
    print(lotto_numbers)
    res = f"""{sender}님을 위한 로또 추천번호!\n\n"""

    for index, item in enumerate(lotto_numbers):
        res = res + f"번호 {str(index+1)}: {item}\n"

    return res


def googleSearch(keyword):
    link = "https://www.google.com/search?q=" + keyword
    return link


def namuSearch(keyword):
    with sync_playwright() as p:
        # Launch the browser. Replace 'chromium' with 'firefox' or 'webkit' if needed.
        browser = p.chromium.launch(
            headless=True
        )  # Set headless=False if you want to see the browser
        page = browser.new_page()
        page.goto(
            f"https://www.google.com/search?q={keyword}", wait_until="networkidle"
        )

        # Use Playwright's selectors to find the first search result's link
        # Note: Google's search result structure can change, so the selector might need adjustments
        first_result_selector = "div.yuRUbf > a"
        first_result = page.query_selector(first_result_selector)
        link = first_result.get_attribute("href")

        browser.close()
        return link


def youtubeSearch(keyword):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )  # Launch the browser in headless mode
        page = browser.new_page()
        page.goto(
            f"https://www.youtube.com/results?search_query={keyword}",
            wait_until="networkidle",
        )

        # Define the selectors for the video titles and links
        video_title_selector = "ytd-video-renderer #video-title"
        video_link_selector = "ytd-video-renderer #video-title"

        # Extract the titles and links of the first three videos
        video_titles = page.query_selector_all(video_title_selector)
        video_links = page.query_selector_all(video_link_selector)

        # Prepare the search results
        res = f"[\"{keyword.replace('+', ' ')}\" YouTube search results:]\n\n"
        for i in range(
            min(3, len(video_titles))
        ):  # Ensure we don't exceed the number of found videos
            title = video_titles[i].inner_text().replace("\n", "")
            link = video_links[i].get_attribute("href")
            res += f"{i + 1}. {title}\n{link}\n\n"

        browser.close()
        return res.strip()


def getNews(keyword):
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=" + str(
        100 + keyword
    )

    driver.get(url)
    html_source = driver.page_source
    soup_source = BeautifulSoup(html_source, "html.parser")

    snb = soup_source.find("td", {"class": "snb"})
    subject = snb.select("div.snb h2 > a")[0].text
    head = soup_source.find("ul", {"class": "sh_list"})
    headline = head.select("div.sh_text > a")

    now = datetime.now()
    # 원하는 형식으로 포맷팅
    formatted_now = now.strftime("%Y.%m.%d %H:%M")

    res = f"""[{subject} 분야 Top 10]
검색일시 : {formatted_now}
"""
    res = res + "\n\n"

    for index, news in enumerate(headline):
        res = res + str(index + 1) + ". " + news.text + "\n" + news.get("href")
        res = res + "\n\n"

    return res


def getNewsSearch(keyword):
    source = requests.get(
        "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + keyword,
        headers=headers,
    )
    soup = bs4.BeautifulSoup(source.content, "html.parser")
    news_list = soup.find(class_="list_news")
    news_company = news_list.select("div.info_group > a.info.press")
    news_title = news_list.select("div > a.news_tit")

    res = f"""[\"{keyword.replace("+"," ")}\" 관련 뉴스 검색 결과]
    
"""
    for i in range(0, len(news_company)):
        res = (
            res
            + str(i + 1)
            + ". "
            + news_title[i].text
            + " / "
            + news_company[i].text
            + "\n"
            + news_title[i].get("href")
        )
        res = res + "\n\n"
    res = res + "(출처 : 네이버뉴스)"
    return res.strip()


def realtime():
    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Setup Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)


    # URL of the page to scrape
    url = "https://signal.bz/"
    driver.get(url)

    # Wait for the page to load dynamically loaded content
    driver.implicitly_wait(10)  # Adjust the wait time as necessary

    # Now you can use BeautifulSoup to parse the page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Your scraping logic here
    ranks = soup.select(".realtime-rank .rank-layer")

    now = datetime.now()
    formatted_now = now.strftime("%Y.%m.%d %H:%M")

    res = f"[실시간 검색어 TOP 10]\n검색일시 : {formatted_now}\n\n"

    for i, rank in enumerate(ranks[:10]):  # Limit to top 10
        rank_num = rank.select_one(".rank-num").text.strip()
        rank_text = rank.select_one(".rank-text").text.strip()
        res += f"{rank_num}. {rank_text}\n"

    res += "\n(출처 : 시그널 실시간검색어)"
    
    # Don't forget to close the browser
    driver.quit()

    return res.strip()


def getZodiac(keyword):
    zodiac_list = [
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
    url = "https://unse.daily.co.kr/?p=zodiac#unseback"
    driver.get(url)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser", from_encoding="cp949")

    total_luck = soup.find(id="code_" + str(zodiac_list.index(keyword) + 1))
    total = total_luck.select("li.start_li div.txt_box > p")[0].text
    li_tags = total_luck.find_all("li")[1:]

    tit = [item.find("span").text for item in li_tags]
    txt = [item.find("p").text for item in li_tags]
    print(tit)
    print(txt)

    now = datetime.now()
    # 원하는 형식으로 포맷팅
    formatted_now = now.strftime("%Y.%m.%d")

    res = f"""[{formatted_now} {keyword} 운세]
    
(총평)
{total}

(나이별)
"""
    for i in range(0, len(tit)):
        res = res + f"19{tit[i].strip()} : {txt[i].strip()}\n"

    res = res + "\n(출처 : 데일리운세)"
    return res


def getHoroscope(keyword):
    url = "https://www.fortunade.com/unse/free/star/daily.php?gtype=2"
    source = requests.get(url, headers=headers)
    soup = BeautifulSoup(source.content, "html.parser", from_encoding="cp949")
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
    scope = horoscope_commands.index(keyword) if keyword in horoscope_commands else None

    element = soup.find(id=f"result_{int(scope+1)}")
    contents = element.select("div.today_item > div.desc")[0]
    now = datetime.now()
    # 원하는 형식으로 포맷팅
    formatted_now = now.strftime("%Y.%m.%d")

    res = f"""[{formatted_now} {keyword} 운세]

{contents.text}
"""
    return res


def getExchangeRate():
    source = requests.get(
        "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=환율",
        headers=headers,
    )
    soup = bs4.BeautifulSoup(source.content, "html.parser")

    nation_name = list(
        map(lambda row: [th.text for th in row.find_all("th")], soup.find_all("tr"))
    )
    price = list(
        map(lambda row: [td.text for td in row.find_all("td")], soup.find_all("tr"))
    )
    price.pop(0)
    nation_name.pop(0)
    res = """\U0001F4B2[환율 정보]\U0001F4B2\n\n"""

    for i in range(0, len(nation_name)):

        res = res + nation_name[i][0] + " : \U000020A9" + price[i][0] + "\n"

    res = res + "\n출처(네이버 환율)"
    return res.strip()


def getAllCoins():
    import re

    url = "https://kr.investing.com/crypto/currencies?currency=krw"
    # url = "https://kr.investing.com/crypto/"
    driver.get(url)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")

    # title =soup.find_all("td","left bold elp name cryptoName first js-currency-name")
    # ticker = soup.find_all("td","left noWrap elp symb js-currency-symbol")
    # price = soup.find_all("td","price js-currency-price")
    title = soup.find_all("div", "crypto-coins-table_cellNameText__aaXmK")
    ticker = soup.find_all("span", "text-common-grey pt-0.5 text-xs")
    price = soup.find_all(
        "td",
        "datatable_cell__LJp3C datatable_cell--align-end__qgxDQ text-secondary !text-sm crypto-coins-table_thirdMobileCell__f8EsE",
    )
    now = datetime.now()
    # 원하는 형식으로 포맷팅
    formatted_now = now.strftime("%Y.%m.%d %H:%M:%S")
    res = f"""[{formatted_now} \U000020BF 시세]"""
    res = res + "\n\n"

    for i in range(0, 10):
        cleaned_number = re.sub(r"\.\d+", "", price[i].text)
        res = (
            res
            + str(i + 1)
            + "."
            + (title[i].text).strip()
            + f"({ticker[i].text})"
            + f": {cleaned_number}\n"
        )

    res = res + "\n(출처 : 인베스팅닷컴)"
    return res.strip()


def getRestaurantByArea(area):

    url = "https://map.kakao.com/?q=" + area + "맛집"

    driver.get(url)
    time.sleep(1)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")

    rest_names = soup.find_all("a", "link_name")
    rest_sub = soup.find_all("span", "subcategory clickable")
    # open_time = soup.find_all("p","periodWarp")
    rest_address = soup.find_all("div", "addr")
    rest_link = soup.find_all("a", "moreview")

    res = f"""['{area.replace("+"," ")} 맛집' 카카오맵 검색 결과]\n\n"""

    count = len(rest_names) if len(rest_names) < 10 else 10
    if count == 0:
        res = "검색 결과가 없습니다."
    else:
        for i in range(0, count):
            res = (
                res
                + f"{str(i+1)}. {rest_names[i].text}({rest_sub[i].text})\n주소: {rest_address[i].p.text} \n링크: {rest_link[i].get('href')}\n\n"
            )
    return res


def getVs(msgSplit, sender):
    print(msgSplit)
    random_choice = random.choice(msgSplit)
    res = f"""선택이 어려운 "{sender}"님을 위한 결과는~
[{random_choice.strip()}] 입니다!
"""
    return res


def getMapSearch(area):
    url = "https://map.naver.com/p/search/" + area
    driver.get(url)
    time.sleep(1)
    variable = driver.current_url
    return variable


def getChatRank(room, period):
    from sqlalchemy import desc
    from api.model.chats import chats
    from datetime import datetime, timedelta

    # Determine the start date based on the period
    today = datetime.now()
    if period == "한달":
        start_date = today - timedelta(days=30)
    elif period == "일주일":
        start_date = today - timedelta(days=7)
    elif period == "오늘":
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # Default to showing all time if period is not recognized
        start_date = datetime.min

    results = (
        db.session.query(chats.sender, func.count().label("cnt"))
        .filter(chats.room == room, chats.create_date >= start_date)
        .group_by(chats.sender)
        .order_by(desc("cnt"))
        .all()
    )

    total_count = sum(result.cnt for result in results)
    max_count = max(result.cnt for result in results) if results else 0
    min_count = min(result.cnt for result in results) if results else 0
    level_range = max_count - min_count

    res = f"[{room}] 채팅방의 채팅순위입니다. (기간: {period})\n총 채팅 갯수 : {total_count}개\n\n"
    for index, result in enumerate(results):
        if level_range == 0:
            level = 1  # Default level when there's no range
        else:
            level = round(((result.cnt - min_count) / level_range) * 9) + 1
        res += f"{index+1}위 {result.sender} - 채팅 {result.cnt}개 ({result.cnt/total_count*100:.1f}% Lv.{level})\n\n"

    return res.strip()


def getMenu(sender):
    from api.model.menues import menues

    random_menu = db.session.query(menues).order_by(func.rand()).first()
    res = f"""\U00002728{sender}님\U00002728을 위한 추천메뉴!
[{random_menu.menu}] 어떠신가요?\U0001F61D
"""
    return res


def getRandomTest():
    contens_url = ["https://www.simcong.com/", "https://www.banggooso.com/"]

    url = random.choice(contens_url)

    source = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(source.content, "html.parser")
    res = ""
    if url == contens_url[0]:
        links = [
            item.a["href"] for item in soup.find_all("li", {"class": "main_hot_item"})
        ]
        get_one_link = random.choice(links)
        res = url + get_one_link
    elif url == contens_url[1]:
        feed_list = soup.find("ul", {"class": "feed-list"})
        links = [item.a["href"] for item in feed_list.select("ul > li")]
        get_one_link = random.choice(links)
        if get_one_link.startswith("javascript"):
            res = extract_url(get_one_link)
        else:
            res = url + get_one_link
    return res


# 문자열에서 링크만 추출
def extract_url(input_string):
    pattern = r'(https?://[^\s"\';]+)'
    url = re.search(pattern, input_string)
    if url:
        return url.group(0)
    else:
        return None


def getHanRiverTemp():
    # URL of the page to scrape
    url = "https://hangang.ivlis.kr/"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Use BeautifulSoup's selectors to find the temperature
    # Assuming the temperature is within an <h2> tag with id="temp1"
    river_temp_tag = soup.find("h2", id="temp1")
    river_temp = (
        river_temp_tag.text.strip() if river_temp_tag else "Temperature not found"
    )

    res = f"""[현재 한강물 온도]

온도 : {river_temp}
"""
    return res


def getSorry():
    from api.model.sentences import sentences

    random_sen = (
        db.session.query(sentences.sentence)
        .filter(sentences.sep == "sorry")
        .order_by(func.rand())
        .first()
    )
    return random_sen.sentence


def getThanks():
    from api.model.sentences import sentences

    random_sen = (
        db.session.query(sentences.sentence)
        .filter(sentences.sep == "thank")
        .order_by(func.rand())
        .first()
    )
    return random_sen.sentence


def getOut(name):
    res = f"{name}님을 강퇴하려고 하였으나, 영험한 힘이 그를 보호하였습니다\U0001F607"
    return res


def getHentai():
    res = f"변태새끼."
    return res


def getMelonChart():
    url = "https://www.melon.com/chart/index.htm"
    driver.get(url)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    now = datetime.now()
    formatted_now = now.strftime("%Y.%m.%d")
    title = soup.find_all("div", {"class": "ellipsis rank01"})
    title_list = [item.select_one("span > a").text for item in title]
    artist = soup.find_all("div", {"class": "ellipsis rank02"})
    artist_list = [item.select_one("span > a").text for item in artist]

    res = f"[{formatted_now} 멜론 차트100\U0001F3B5]\n\n"
    for i in range(0, len(title_list)):
        res = res + f"{str(i+1)}. {title_list[i]} - {artist_list[i]}\n"
    res = res + "(출처 : Melon)"
    return res


def getMovieList():
    url = "https://www.megabox.co.kr/movie"
    driver.get(url)
    time.sleep(0.5)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    now = datetime.now()
    formatted_now = now.strftime("%Y.%m.%d")
    movie_list = soup.find("ol", {"class": "list"})
    print(movie_list)
    movie_title = movie_list.select("li > div.tit-area")
    title = [item.select_one("p.tit").text for item in movie_title]
    movie_rate = movie_list.select("li > div.rate-date")
    rate = [item.select_one("span.rate").text for item in movie_rate]
    date = [item.select_one("span.date").text for item in movie_rate]

    res = f"[{formatted_now} 현재상영작\U0001F3A5]\n\n"
    for i in range(0, len(title)):
        res = res + f"{str(i+1)}. {title[i]} | {rate[i]} | {date[i]}\n"
    res = res + "(출처 : 메가박스)"
    return res
