import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

url1  = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?"
#taskClCds = [None, 1, 2, 3, 4, 5, 6, 11, 20]
#업무구분 옵션 - None 전체, 1 물품, 2 외자, 3 공사, 4 기타, 5 용역, 6 리스, 11 비축, 20 민간
#bidNm = None
#공고명 utf-8로 변환해서 보내야함.
#searchDtType = [1, 2]
#공고/개찰일 선택 - 1 공고일, 2 개찰일
#formBidDt = None
#시작 날짜
#toBidDt = None
#끝나는 날짜
#radOrgan = [1, 2]
#기관명 옵션 - 1 공고기관, 2 수요기관
#instNm = None
#기관명 utf-8로 변환해서 보내야함.
#area = [00, 11, 26, 28, 27, 29, 30, 31, 36, 41, 42, 43, 44, 45, 46, 47, 48, 49]
#참가제한지역 - 00 전국, 11 서울, 26 부산, 28 인천, 27 대구, 29 광주, 30 대전, 31 울산, 41 경기, 42 강원, 43 충북, 44 충남, 45 전북, 46 전남, 47 경북, 48 경남, 49 제주

#url2 = "taskClCds=" + taskClCds[1] + "&" + "bidNm=" + bidNm + "&" + "searchDtType=" + searchDtType[1] + "&" + "formBidDt=" + formBidDt + "&" + "toBidDt=" + toBidDt + "&" + "radOrgan=" + radOrgan[1] + "&" + "instNm=" + instNm + "&" + "area=" + area[1] + "&"
formBidDt = "2020/" + input("시작 날짜를 입력 : ")
toBidDt = "2020/" + input("끝나는 날짜를 입력 : ") 

task_list = []
num_list = []
title_list =[]
url_list = []
type_list = []
start_list = []

def get_info(raw_row):
    cancel = raw_row.find_all('td')[2].text
    deadline = raw_row.find_all('td')[7].find_all('span')[0].text
    
    if cancel == '일반' :
        if deadline == '(-)' :
            print(deadline)
            task_list.append(raw_row.find_all('td')[0].text)
            num_list.append(raw_row.find_all('td')[1].text)
            title_list.append(raw_row.find_all('td')[3].text)
            url_list.append(raw_row.a['href'])
            type_list.append(raw_row.find_all('td')[6].text)
            start_list.append(raw_row.find_all('td')[7].text.replace('(-)',""))
        else :
            print("마감")
    else :
        print("취소")

for i in range(1, 21):
    url3 = "taskClCds=&bidNm=&searchDtType=1" + "&fromBidDt=" + formBidDt + "&toBidDt=" + toBidDt + "&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=%C7%D1%B1%B9%C0%CE%C5%CD%B3%DD%C1%F8%C8%EF%BF%F8&area=&regYn=Y&bidSearchType=1&searchType=1" + "&maxPageViewNoByWshan=" + str(i) + "&currentPageNo=" + str(i)
    url = url1 + url3
    req = requests.get(url)
    html = req.text
    status = req.status_code

    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('tr')

    if len(title) > 3:
        print("-------------" + str(i) + "-------------")
        print("상태 : " + str(status))
        print("정보의 수 : " + str(len(title)-1))

        for i in range(1, len(title)):
            get_info(title[i])
    else:
        pass

df = pd.DataFrame(list(zip(task_list,num_list,title_list,url_list,type_list,start_list)), columns=['업무','공고번호','공고명','링크','계약방법','입력일시'])
df.to_csv("nara.csv",index=False,encoding='utf-8-sig')