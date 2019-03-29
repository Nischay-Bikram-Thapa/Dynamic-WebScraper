import requests as req 
from bs4 import BeautifulSoup
import re 
import time
import math
import threading

base_url = 'https://www.hamrodoctor.com'
hospital_url = base_url + '/hospitals'
paging = 10
#Get Pages count from the pagination block
def get_pages(url,paging):
    response = req.get(url)
    content = response.text.replace('\n','')
    pattern = r'<div class="tg-pagehead"(.*?)<small>(.*?)([0-9]+)'
    result = re.search(pattern,content)
    records = int(result.group(3))
    return math.ceil(records/paging)

total_pages = get_pages(hospital_url,paging)
#Decode Email protection
def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email
#Extract details for all the pages and tabs
def visit_detail_page(url):
    response = req.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    title = soup.select('#marketing_special_name')[0]
    print(title.text.strip())
    address = soup.select('div.hospital-profile-gradient div.hosp-text-color')[0]
    print(address.text.strip())
    email_data = soup.select('span.__cf_email__')[0]
    email =cfDecodeEmail(email_data['data-cfemail'])
    print(email)
    hospital_detail = soup.select('div.panel-body div.tg-directposthead')
    for detail in hospital_detail:
        doctor=detail.find('a')
        print(doctor.text)
        subject=detail.find('div')
        print(subject)
#Visit all the pages in the website
def visit_page(page_no):
        response = req.get(hospital_url+"/index/page:"+str(page_no))
        soup = BeautifulSoup(response.text,"html.parser")
        result = soup.select('div.tg-directinfo div.tg-directposthead h3 a')
        for link in result:
           url = base_url + link['href']
           visit_detail_page(url)
#Run thread for parallel processing
def run(start,end):
    if(start<=end):
       thread = threading.Thread(target=visit_page,args=(start,))
       thread.start()
       run(start+1,end)

run(1,total_pages)