#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020/9/11 15:03
# Project: crawl-and-download-music
# @Author: ningninga
# @Email :


import requests
import json
import os


def music_download():
    kw = input("please enter the name of the song which you want to know：")
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
        "Cookie":"_ga=GA1.2.1083049585.1590317697; _gid=GA1.2.2053211683.1598526974; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1597491567,1598094297,1598096480,1598526974; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1598526974; kw_token=HYZQI4KPK3P",
        "Referer": "http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6",
        "csrf": "HYZQI4KPK3P",
    }
    # parameter list
    params = {
        "key": kw,
        # pages
        "pn": "1",
        # the number of the songs
        "rn": "10",
        "httpsStatus": "1",
        "reqId": "cc337fa0-e856-11ea-8e2d-ab61b365fb50",
    }
    # create a list
    music_list = []
    url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
    res = requests.get(url=url, headers=headers, params=params)
    res.encoding = "utf-8"
    text = res.text
    # transfer the type into json
    json_list = json.loads(text)
    datapack = json_list["data"]["list"]
    # ergodic to get all of the data that we need,such as the name of the song, singer, id
    for i in datapack:
        # the name of the song
        music_name = i["name"]
        # the name of the singer
        music_singer = i["artist"]
        # id
        rid = i["rid"]
        # api
        api_music = "http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3" \
                    "&br=128kmp3&from=web&t=1598528574799&httpsStatus=1" \
                    "&reqId=72259df1-e85a-11ea-a367-b5a64c5660e5".format(rid)
        api_res = requests.get(url = api_music)
        music_url = json.loads(api_res.text)["url"]
        print(music_name)
        print(music_singer)
        print(music_url)
        # store the data into the dict in order to make it easy to search
        music_dict = {}
        music_dict["name"] = music_name
        music_dict["url"] = music_url
        music_dict["singer"] = music_singer
        music_list.append(music_dict)
    print(len(music_list))
    # download
    xiazai = input("please enter the name of the song which you want to download:")
    # positon
    root = 'F:\\music/'
    for i in range(len(music_list)):
        try:
            if xiazai == music_list[i]["name"]:
                # create the directory
                if not os.path.exists(root):
                    os.mkdir(root)
                # get the url of the song from dict
                music_content = requests.get(url = music_list[i]["url"]).content
                with open(root + "{}-{}.mp3".format(music_list[i]['name'],music_list[i]['singer']),"wb") as f:
                    f.write(music_content)
                    print("download  completed!")
            else:
                print("the name of the song does not in the list")
                continue
        except:
            print("download failed")
if __name__ == "__main__":
    print('Kuwo music - start')
    music_download()
    print('Kuwo music - end')