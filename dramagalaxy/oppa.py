#http://www.dramagalaxy.tv/drama-shows


from bs4 import BeautifulSoup
from slugify import slugify
from random import randint
import requests
import time
import MySQLdb
import configparser
import sys
import httplib
import random
import string
import re
import oppa_db


print ("*****************************************")
print ("Hello OPPA, Mashisoyo!")
print ("*****************************************")



page=1
loop=0
default_url = 'http://www.dramagalaxy.tv/drama-updates/'
db = oppa_db.save_to_db()

print "Enter Page No.:"
page = raw_input("")
page = page or '1'

while loop == 0:

    url = default_url+str(page)
    page = int(page)
    print 'Url: '+str(url)
    print '------------------------------------------------------------------------------------------------------------------------------------------'
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data,"lxml")

    movie_lists = []
    movies = soup.find("table",{"id" : "updates"})
    trs = movies.findAll("tr")
    print 'No of rows: ' +str(len(trs))
    for tr in trs:

        movie_info = []

        tds = tr.findAll("td")
        td1 = tds[0]
        td2 = tds[2]
        lis = td1.findAll("li")
        for li in lis:
            episode_title = li.find("a").text
            episode_title = str(episode_title)
            episode_link = li.find("a")["href"]
            episode_link = str(episode_link)

            #To Episode Link
            r2 = requests.get(episode_link)
            data2 = r2.text
            soup2 = BeautifulSoup(data2,"lxml")
            span = soup2.find("span",{"class":"bold"})
            movie_title = span.find("a").text
            movie_title = str(movie_title)
            movie_link =  span.find("a")["href"]
            movie_link = str(movie_link)
            episode_mp4s = soup2.findAll("div",{"class":"vmargin"})
            episode_mp41 = soup2.find_all("div",class_=re.compile('vmargin'))
            mp4s = []
            for mp4 in episode_mp4s:

                try:
                    mp4_iframe = mp4.find("iframe")['src']
                    mp4s.append(str(mp4_iframe))
                except Exception as e:
                    mp4s = []

            r3 = requests.get(movie_link)
            data3 = r3.text
            soup3 = BeautifulSoup(data3,"lxml")
            movie_details = soup3.findAll("div",{"id":"series_details"})
            movie_details = movie_details[0]
            movie_divs = movie_details.findAll("div")
            movie_thumb = soup3.find('div',{"class":"left_col"})
            movie_thumb = movie_thumb.find('img')['src']
            movie_thumb = str(movie_thumb)
            movie_description = ""
            movie_category = ""
            movie_status = ""
            movie_released = ""
            movie_genres = ""
            if(len(movie_divs)==9):
                movie_description = movie_divs[2]
                movie_category = movie_divs[4]
                movie_status = str(movie_divs[5])
                movie_released = str(movie_divs[6])
                movie_genres = movie_divs[8]
            else:
                movie_description = movie_divs[0]
                movie_category = movie_divs[2]
                movie_status = str(movie_divs[3])
                movie_released = str(movie_divs[4])
                movie_genres = movie_divs[6]

            movie_description = movie_description.findAll("div")
            movie_description = movie_description[0]
            movie_description = str(movie_description)
            movie_description = movie_description.replace("<div>","")
            movie_description = movie_description.replace("        </div>","")
            movie_description = movie_description.replace("     ","")
            movie_description = movie_description.replace("\r","")
            movie_description = movie_description.replace("\n","")
            clean = re.compile('<.*?>')
            movie_description = re.sub(clean, '', movie_description)
            movie_description = str(movie_description)
            movie_category = movie_category.find("a").text
            movie_category = str(movie_category)
            movie_status = movie_status.replace("<span>Status:</span>","")
            movie_status = movie_status.replace("\r","")
            movie_status = movie_status.replace("\n","")
            movie_status = movie_status.replace("<div>        ","")
            movie_status = movie_status.replace("      </div>","")
            movie_status = str(movie_status)
            movie_released = movie_released.replace('<span>Released:</span>','')
            movie_released = movie_released.replace('</div>','')
            movie_released = movie_released.replace('<div>','')
            movie_released = movie_released.replace("\r","")
            movie_released = movie_released.replace("\n","")
            movie_released = movie_released.replace('        ','')
            movie_released = movie_released.replace('      ','')
            movie_genres = movie_genres.findAll("a")
            video_tags = []
            for video_tag in movie_genres:
                video_tags.append(video_tag.text)
            video_tags = [str(r) for r in video_tags]
            cast_overviews = soup3.find("div",{"id":"starring"})
            cast_overviews = cast_overviews.findAll("li")


            movie_casts = []
            for cast_overview in cast_overviews:
                cast_overview = cast_overview.findAll("a")
                cast_overview = cast_overview[1]
                cast_profile_link = cast_overview['href']
                cast_profile_link = str(cast_profile_link)
                cast_name = cast_overview.text
                cast_name = str(cast_name)
                r4 = requests.get(cast_profile_link)
                data4 = r4.text
                soup4 = BeautifulSoup(data4,"lxml")
                cast_photo_thumb = soup4.find('div',{"class":"left_col"})
                cast_photo_thumb = cast_photo_thumb.find('img')['src']
                cast_photo_thumb = str(cast_photo_thumb)
                cast_details = soup4.find("div",{"id":"actor_details"})
                cast_details = cast_details.findAll("div")
                cast_alias_name = cast_details[0]
                cast_alias_name = str(cast_alias_name).replace("<span>Star Alias:</span><br/>","")
                cast_alias_name = cast_alias_name.replace("\r","")
                cast_alias_name = cast_alias_name.replace("\n","")
                cast_alias_name = cast_alias_name.replace('<div class="row">        ','')
                cast_alias_name = cast_alias_name.replace('      </div>','')
                cast_alias_name = str(cast_alias_name)
                cast_bplace = str(cast_details[1])
                cast_bplace = cast_bplace.replace('<span>Birth Place:</span> ','')
                cast_bplace = cast_bplace.replace('      </div>','')
                cast_bplace = cast_bplace.replace("\r","")
                cast_bplace = cast_bplace.replace("\n","")
                cast_bplace = cast_bplace.replace('<div class="row">','')
                cast_bdate = str(cast_details[2])
                cast_bdate = cast_bdate.replace('<span>Birth Date:</span> ','')
                cast_bdate = cast_bdate.replace('      </div>','')
                cast_bdate = cast_bdate.replace("\r","")
                cast_bdate = cast_bdate.replace("\n","")
                cast_bdate = cast_bdate.replace('<div class="row">','')
                cast_height = str(cast_details[3])
                cast_height = cast_height.replace('<span>Height:</span> ','')
                cast_height = cast_height.replace('      </div>','')
                cast_height = cast_height.replace("\r","")
                cast_height = cast_height.replace("\n","")
                cast_height = cast_height.replace('<div class="row" id="height">','')
                movie_casts.append([cast_name,cast_profile_link,cast_alias_name,cast_bplace,cast_bdate,cast_height,cast_photo_thumb])

            movie_info.append([episode_title,episode_link,movie_title,movie_link,movie_thumb,movie_description,movie_category,movie_status,video_tags,movie_released,mp4s])
            movie_lists.append([movie_info,movie_casts])
            db.save_to_db(movie_lists)
            movie_info = []
            movie_casts = []
            movie_lists = []

    page-=1
    loop=0

print 'Oppa Mashisoyo!!!'

