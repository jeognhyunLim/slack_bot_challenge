from slacker import Slacker
import websocket
import json

import urllib.request
from bs4 import BeautifulSoup

slack = Slacker('xoxb-502213453520-507527209730-VzzPkJwu1GyClAlfKzuaDj3m')

jeonghyun_bot_id = 'UEXFH65MG'
jobkorea_url = "http://www.jobkorea.co.kr"
default_url = "http://www.jobkorea.co.kr/starter/"

'''
schLocal => 서울 = I000 , 경기 = b000 
schPart => it = 10016
schWork => 정규직 =1, 인턴 = 2
schOrderBy => 등록순 = 0 , 마감순 = 1
'''

# 잡코리아 크롤링
def jobkorea_crawler(url):

    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    list = soup.find("ul", class_="filterList")
    noSelect = list.find("li" , class_="scNoSelect")

    info_list = []

    #검색 결과가 없는경우 빈 리스트 반환
    if noSelect :
        return info_list

    # [ { 채용 정보 1 } ,  { 채용 정보2 } ... ]
    for row in list.find_all("li"):
        company = row.find("a", class_="coLink").get_text()
        contents = row.find("a", class_="link")
        contents_title = contents.find("span").get_text()
        contents_link = jobkorea_url + contents["href"]

        fields = [sub.get_text() for sub in row.find("div", class_="sTit").find_all("span")]
        target = row.find("div", class_="sDesc").find("strong").get_text()
        date = row.find("div", class_="side").find("span", class_="day").get_text()

        result = {'company': company, "fields": fields, "contents_title": contents_title,"contents_link": contents_link, "target": target, "date": date}
        info_list.append(result)

    return info_list

# 사용법 안내 메세지
def send_init_message(channel):

    attachments_dict = dict()
    attachments_dict["color"] = "#00FF00"
    attachments_dict["author_name"] = "jeonghyun_bot 사용법"
    attachments_dict['pretext'] = "안녕하세요 jeonhyun_bot 입니다. IT 채용 정보를 검색해드립니다"
    attachments_dict['fallback'] = "확인하세요"
    attachments_dict['footer'] = "contact @jeonghyun"
    attachments_dict['text'] = "\n*[지역]* :  서울 | 경기 | 인천 | 대전 | 세종 | 충남 | 충북 | 광주 | 전남 | 전북 | 대구 | 경북 | 부산 | 울산 | 경남 | 강원 | 제주" \
                               "\n *[고용]* : 정규직 | 인턴 | 전환형 | 계약직" \
                               "\n *[정렬]* : 마감순 | 등록순" \
                               "\n\n *예시 >> @jeonghyun_bot 서울 정규직 마감순*" \
                               "\n\t\t\t  *@jeonghyun_bot 서울 경기 인턴* "
    attachments_dict['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
    attachments = [attachments_dict]

    slack.chat.post_message(text=None, channel=channel, username='jeonghyun_bot', attachments=attachments)

# 잡코리아에서 정보 얻어오기
def send_jobkorea_info(text, channel):
    local = ""
    work = ''
    order = ''
    local_dic = {'전체':'', '서울': 'I000', '경기': 'B000', '인천': 'K000', '대전': 'G000', '세종': '1000', '충남': 'O000', '충북': 'P000',
                 '광주': 'E000', '전남': 'L000', '전북': 'M000', '대구': 'F000', '경북': 'D000', '부산': 'H000', '울산': 'J000',
                 '경남': 'C000', '강원': 'A000', '제주': 'N000'}

    work_dic = {'정규': '1', '인턴': '2', '전환형': '3', '계약': '4'}

    # 지역
    for local_text in local_dic.keys():
        if local_text in text:
            local += ',' + local_dic[local_text]

    # 고용형태
    for work_text in work_dic.keys():
        if work_text in text:
            work += ',' + work_dic[work_text]
    # 정렬
    if "마감" in text:
        order = '1'
    elif "등록" in text:
        order = '0'

    # 지역과 고용형태 모두  입력되지 않은경우
    if local == '' and work == '':
        send_init_message(channel)
        return

    # 검색 url을 만들어서 크롤링 함수로 전달
    search_url = "http://www.jobkorea.co.kr/starter/?schLocal=" + local + "&schPart=10016&schEduLevel=&schWork=" + work + "&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=" + order + "&schTxt="
    info_dic_list = jobkorea_crawler(search_url)

    # 검색 결과가 없는 경우
    if len(info_dic_list) == 0:
        attachments_dict = dict()
        attachments_dict["color"] ="#FF0000"
        attachments_dict["text"] = "*검색 결과가 없습니다 ㅠ.ㅠ*"
        attachments = [attachments_dict]
        slack.chat.post_message( channel=channel, username='jeonghyun_bot', attachments=attachments)
        return

    for dic in info_dic_list[0:5]:
        attachments_dict = dict()
        attachments_dict["color"] = "#FF0000"
        attachments_dict['pretext'] = dic["company"]
        attachments_dict['title'] = dic["contents_title"]
        attachments_dict['title_link'] = dic["contents_link"]
        attachments_dict['fallback'] = "확인하세요"
        attachments_dict['text'] = "기업명 : " + dic["company"] + "\n분야 : " + " ".join(dic["fields"]) + "\n모집: " + dic["target"] + "\n*기한 : " + dic["date"]+"*"
        attachments_dict['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
        attachments = [attachments_dict]

        slack.chat.post_message(text=None, channel=channel, username='jeonghyun_bot', attachments=attachments)
    # 잡코리아 사이트 연결 버튼
    if len(info_dic_list) > 5 :
        attachments_dict = { "text": "Do you want to more infomation?",
                             "actions": [{ "name": "choice",
                                           "text": "Go Job Korea",
                                           "type": "button",
                                           "value": "go Job Korea",
                                           "style": "danger",
                                           "url": search_url},
                                         ]}
        slack.chat.post_message(text=None, channel=channel, username='jeonghyun_bot', attachments=[attachments_dict])

def bot_run(text, channel):

    if text == '':
        send_init_message(channel)
    else:
        send_jobkorea_info(text, channel)

def run():

    res = slack.rtm.connect()
    endpoint = res.body['url']

    ws = websocket.create_connection(endpoint)
    ws.settimeout(5)

    # 해당 봇이 멘션된 경우만 bot_run()
    while True:
        try:
            msg = json.loads(ws.recv())
            if msg["type"] == "message" and 'text' in msg:
                text = msg["text"]
                try:
                    bot_id = text.split()[0].replace("<@", "").replace(">","")
                    if bot_id == jeonghyun_bot_id:
                        bot_run(text.replace(text.split()[0], "").strip(), msg["channel"])
                except:
                    pass
            print(msg)

        except websocket.WebSocketTimeoutException:
            ws.send(json.dumps({'type': 'ping'}))

        except websocket.WebSocketConnectionClosedException:
            print("Connection closed")
            break

        except Exception as e:
            print(e)
            break
    ws.close()

if __name__ == '__main__':
    run()

