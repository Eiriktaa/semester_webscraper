#!/usr/bin/python3
import bs4,csv
import requests
import os
#Ping service
from discord import Webhook,RequestsWebhookAdapter

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Accept-Language': 'en-US',
}

workdir = os.path.dirname(__file__)

def get_web_data_from_url(url):
    res = requests.get(url,headers=headers) 
    res.raise_for_status()#Checks for valid statuses

    soup = bs4.BeautifulSoup(res.text,"lxml")
    message = soup.select("div.vrtx-frontpage-box:nth-child(2)")
    return message

def parse_message(message):
    parsed_text =""
    for m in message:
        parsed_text += m.text
    return parsed_text

def write_file(parsed_text,filename):
    with open(filename,'w+') as file:
        file.write(parsed_text)

def compare_new_data_to_file(new_data,filename):
  try:  
      with open(os.path.join(workdir,filename),"r") as file:
        filedata =  file.read()
        return filedata == new_data
  except:
            #file does not exist
        return False

def notify_users(message):
    hook = Webhook.from_url(os.getenv("PING_WEBHOOK"),adapter=RequestsWebhookAdapter())
    hook.send(message)       
       

with open(os.path.join(workdir,"fag.csv"),newline="") as fagliste :
    fagkoder = csv.reader(fagliste)
    for fag in fagkoder:
        print(fag[0])
        new_data = parse_message(get_web_data_from_url(fag[1]))
        data_unchanged = compare_new_data_to_file(new_data,fag[0])

        if data_unchanged:
            continue
        else:
            notify_users(f"New message posted  in {fag[0]}\n{fag[1]} ")
            write_file(new_data,os.path.join(workdir,fag[0]))
    

