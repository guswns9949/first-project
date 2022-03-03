#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from tqdm import tqdm_notebook
from Screenshot import Screenshot_Clipping
import requests
from bs4 import BeautifulSoup
import time
from os.path import getsize
import os.path
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
from Screenshot import Screenshot_Clipping
from selenium.webdriver.chrome.options import Options
import datetime


# In[6]:


# 현재날짜시간초로 고유값 라벨링 해주는 도구
def time_label():
    date_time = datetime.datetime.now()
    now_time = str(date_time).replace(" ","").replace("-","").replace(":","").replace(".","")
    return now_time

# 11칸 짜리 nan값 리스트 만들기
def nan_list_make():
    baseList = np.empty(12)
    baseList[:] = np.nan
    baseList = list(baseList)
    baseList
    return baseList

# 추가할 행 계산기
def row_count(img_list):
    row_cal = divmod(len(img_list),10)
    row_cnt = row_cal[0]
    if row_cal[1] > 0 :
        row_cnt += 1
    return row_cnt

# 리스트 10개씩 분할
def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


# In[7]:


# 크롤링 코드
def image_download(BASE_URL, title):
    # 코드실행시각
    now_label = str(time_label())
    
    title_list = []
    title_url_list = []
    write_date_list = []
    img_path_list = []
    page_screenshot_list = []
    
    # 스샷찍을 도구----------------------
    options = wb.ChromeOptions() # 셀레니움 옵션
    options.add_argument("--incognito")#추가
    options.add_argument("--headless")#추가
    options.add_argument("--no-sandbox")#추가
    options.add_argument("--disable-setuid-sandbox")#추가
    options.add_argument("--disable-dev-shm-usage")#추가
    options.add_argument("--disable-setuid-sandbox")#추가
    options.add_argument("headless") # 브라우저 창 없이 실행
    options.add_argument("window-size=1920x1080")  # 브라우저 사이즈 조절
    options.add_argument("disable-gpu")
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36") #변경
    options.add_argument("lang=ko_KR") 
    options.add_argument("Content-Type=application/json; charset=utf-8") 
    options.add_experimental_option("excludeSwitches",['enable-logging'])#추가
    driver = wb.Chrome(options=options) #변경
    driver.implicitly_wait(3) # seconds

    # 헤더 설정 (필요한 대부분의 정보 제공 -> Bot Block 회피)
    headers = {
    "Connection" : "keep-alive",
    "Cache-Control" : "max-age=0",
    "sec-ch-ua-mobile" : "?0",
    "DNT" : "1",
    "Upgrade-Insecure-Requests" : "1",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site" : "none",
    "Sec-Fetch-Mode" : "navigate",
    "Sec-Fetch-User" : "?1",
    "Sec-Fetch-Dest" : "document",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "ko-KR,ko;q=0.9"
    }

    # 페이지 가공
    res = requests.get(BASE_URL, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    
    write_date = soup.select_one("span.date.m_no").text # 작성일 데이터 수집
    date_check = str(write_date).split(" ")[0].replace(".","")  # 날짜까지만
    
    # 페이지 스크린샷 -- 여기만 셀레니움으로 실행
    driver.get(BASE_URL)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    image_download_contents = soup.select("a.highslide.highslide-move")
    screenshot = driver.save_screenshot(f'./F_screenshot/sshot_{now_label}.jpg')
    time.sleep(0.3)

    driver.quit()
    
    # 데이터 수집,이미지 저장
    for img_tag in image_download_contents:
        title_list.append(title)
        title_url_list.append(BASE_URL)
        write_date_list.append(write_date) # write_date : 게시글 작성 시간
        page_screenshot_list.append(f'sshot_{now_label}.jpg')

        # 이미지 저장
        img_url = img_tag['href']
        save_time = time_label()
        savename = f"img_{save_time}.jpg"
        urlretrieve("https:"+img_url, f"./F_image/{savename}.jpg")
        time.sleep(0.3)
        img_path_list.append(savename)
        
    return title_list, title_url_list, write_date_list, img_path_list, page_screenshot_list

