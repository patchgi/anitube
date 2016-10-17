# coding:utf-8
from urllib.request import Request, urlopen
import urllib.request
from bs4 import BeautifulSoup
import time
from getProgressBar import getProgressBar
import sys
import os

class Anitube:

    base_urls = []
    page_count = 1
    word = ""

    def __init__(self, _word):
        _word = _word.replace(" ", "+")
        first_url = "http://www.anitube.se/search/?sort=&search_type=videos&search_id=" + _word
        self.word = _word
        self.base_urls.append(first_url)


    # 検索結果(20Links)のページのHTML取得
    def getBaseSoup(self):
        soups = []
        req = Request(self.base_urls[0], headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        flicks_soup = soup.find("ul", id = "pagination-flickr")
        str_flicks = str(flicks_soup)
        li_count = str_flicks.count("<li")

        #検索結果のページURL取得
        if li_count != 8:
            self.page_count = li_count
        else:
            self.page_count = int(flicks_soup.find_all("li")[6].string)
            print (self.page_count)

        for i in range(2, self.page_count + 1):
            self.base_urls.append("http://www.anitube.se/search/" + str(i) + "/?sort=&search_type=videos&search_id=" + self.word)


        #検索結果のURLをHTMLに変換
        for url in self.base_urls:
            #503対策
            time.sleep(1)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')
            soups.append(soup)
        return soups


    # 検索結果の動画のページのURLを取得
    def getChildURLs(self):
        result = []
        soups = self.getBaseSoup()
        for soup in soups:
            title_tags = soup.find_all(class_ = "videoTitle")
            for tag in title_tags:
                result.append(tag.find("a").get("href"))
        return result


    # 再生ページのURLから動画情報URL取得
    def getMovieinfoURL(self):
        movie_urls = self.getChildURLs()
        info_urls = []

        for idx, url in enumerate(movie_urls):
            #time.sleep(1)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')
            info_url = soup.find(id = "videoPlayer").find_all("script")[2].get("src")
            info_urls.append(info_url)

            progress = {
            "progress":idx,
            "parameter":len(movie_urls)
            }
            progressBar=getProgressBar(progress)
            sys.stdout.write("getMovieinfo" + progressBar)
            sys.stdout.flush()
        print("")
        return info_urls


    # 動画情報ページから動画URLを取得
    def getMovieURL(self):
        info_urls = self.getMovieinfoURL()
        movie_urls = []
        for url in info_urls:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = str(urlopen(req).read())
            url_mp4 = html[578:650]
            if url_mp4[0] != "h":
                url_mp4 = html[435:504]
            movie_urls.append(url_mp4)
        return movie_urls


    def download(self, _path = ""):
        movie_urls = self.getMovieURL()
        for idx, url in enumerate(movie_urls):
            progress = {
            "progress":idx,
            "parameter":len(movie_urls)
            }
            progressBar=getProgressBar(progress)
            sys.stdout.write("downloading" +progressBar)
            sys.stdout.flush()
            url_obj = urllib.request.urlopen(url)
            os.mkdir(_path)
            local = open(_path+"/"+ os.path.basename(url), 'wb')
            local.write(url_obj.read())

            url_obj.close()
            local.close()
