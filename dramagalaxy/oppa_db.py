
import sys
from slugify import slugify
from random import randint
import time
import MySQLdb
import sys
import random
import string
import configparser

class save_to_db:

    def save_to_db(self,list):
        print ("Preparing for insertion!")
        created_at = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Check database config
    		path = sys.path[0]+"\\kdrama.conf"
    		config = configparser.ConfigParser()
    		config.readfp(open(r''+path))
    		db_user = config.get('Mysql Database Configuration', 'db_user')
    		db_password = config.get('Mysql Database Configuration', 'db_password')
    		db_name = config.get('Mysql Database Configuration', 'db_name')
    		db_host = config.get('Mysql Database Configuration', 'db_host')
    		db = MySQLdb.connect(db_host,db_user,db_password,db_name)
                movie = list[0]
                movie = movie[0]
                movie = movie[0]
                movie_casts = list[0]
                movie_casts = movie_casts[1]
                #print 'movie_casts: '+str(movie_casts)
                episode_title = movie[0]

                episode_link = movie[1]
                movie_title = movie[2]
                movie_link = movie[3]
                movie_photo_thumb = movie[4]
                movie_description = movie[5]
                movie_category = movie[6]
                movie_status = 1
                if(movie[7] == 'Ongoing'):
                    movie_status = 0
                movie_tags = movie[8]
                movie_released = movie[9]
                mp4s = movie[10]

                print '-----------------------------------'
                print 'Episode Title: '+str(episode_title)
                print 'Episode Link: '+str(episode_link)
                print 'Movie Title: '+str(movie_title)
                #print 'Movie Link: '+str(movie_link)
                #print 'Thumbnail: '+str(movie_photo_thumb)
                #print 'Description: '+str(movie_description)
                #print 'Category: '+str(movie_category)
                #print 'Status: '+str(movie_status)
                #print 'Tags: '+str(movie_tags)
                #print 'Released: '+str(movie_released)
                print 'Mp4: '+str(mp4s)
                slug = slugify(str(movie_title))+ "-"+str(randint(10, 5000))
                episode_slug =  slugify(str(episode_title))+ "-"+str(randint(10, 5000))
                cursor = db.cursor()
                query_movie = "SELECT id,movie_link,title from movies where title = '%s' and movie_link = '%s' "%(str(movie_title),str(movie_link))
                cursor.execute(query_movie)
                cursor.fetchall()
                if(cursor.rowcount == 0):
                    cursor_insert_movie = db.cursor()
                    cursor_insert_movie.execute('''insert into movies (created_at,updated_at,title,description,movie_link,movie_slug,category,status,date_released,cover_photo,is_visible)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                        ,(created_at,created_at,str(movie_title),str(movie_description),str(movie_link),slug,str(movie_category),movie_status,str(movie_released),str(movie_photo_thumb),1))
                    movie_id = cursor_insert_movie.lastrowid

                    for cast in movie_casts:
                        cast_name = str(cast[0])
                        cast_link = str(cast[1])
                        cast_alias = str(cast[2])
                        cast_country = str(cast[3])
                        cast_bdate = str(cast[4])
                        cast_height = str(cast[5])
                        cast_thumbnail = str(cast[6])

                        cursor_exist_cast = db.cursor()
                        query_exists_cast = "SELECT id,name,cast_link from casts where name = '%s'  "%(cast_name)
                        cursor_exist_cast.execute(query_exists_cast)
                        cursor_exist_cast.fetchall()
                        if(cursor_exist_cast.rowcount == 0):
                            cast_slug = slugify(cast_name)+ "-"+str(randint(10, 5000))
                            cursor_insert_cast = db.cursor()
                            cursor_insert_movie_cast = db.cursor()
                            cursor_insert_cast.execute('''INSERT into casts (created_at,updated_at,name,star_alias,cast_slug,cast_link,birth_place,height,cover_photo)
                            values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                            ,(created_at,created_at,cast_name,cast_alias,cast_slug,cast_link,cast_bdate,cast_height,cast_thumbnail))
                            cast_id = cursor_insert_cast.lastrowid
                            cursor_insert_movie_cast.execute('''INSERT into movie_casts (created_at,updated_at,cast_id,movie_id,status,is_visible)
                            values (%s,%s,%s,%s,%s,%s)'''
                            ,(created_at,created_at,cast_id,movie_id,1,1))

                    for tag in movie_tags:
                        cursor_exist_tag = db.cursor()
                        tag_slug = slugify(str(tag))+ "-"+str(randint(10, 5000))
                        query_exists_tag = "SELECT id,tag,tag_slug from tags where tag = '%s'  "%(str(tag))
                        cursor_exist_tag.execute(query_exists_tag)
                        cursor_exist_tag.fetchall()
                        if(cursor_exist_tag.rowcount == 0):
                            cursor_insert_tag = db.cursor()
                            cursor_insert_movie_tag = db.cursor()
                            cursor_insert_tag.execute('''INSERT into tags (created_at,updated_at,tag,tag_slug,status,is_visible)values (%s,%s,%s,%s,%s,%s)''',(created_at,created_at,str(tag),tag_slug,1,1))
                            tag_id = cursor_insert_tag.lastrowid
                            cursor_insert_movie_tag.execute('''INSERT into movie_tags (created_at,updated_at,movie_id,tag_id)values (%s,%s,%s,%s)''',(created_at,created_at,movie_id,tag_id))

                    cursor_exist_movie_episode = db.cursor()
                    query_exists_movie_episode = "SELECT id,episode_title,episode_link from movie_episodes where episode_title = '%s' and episode_title = '%s' "%(str(episode_title),str(episode_link))
                    cursor_exist_movie_episode.execute(query_exists_movie_episode)
                    cursor_exist_movie_episode.fetchall()
                    if(cursor_exist_movie_episode.rowcount == 0):
                        cursor_insert_movie_episodes = db.cursor()
                        cursor_insert_movie_episodes.execute('''INSERT into movie_episodes (created_at,updated_at,movie_id,episode_title,episode_slug,status,cover_photo,is_visible,views,episode_link)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                        ,(created_at,created_at,movie_id,str(episode_title),str(episode_slug),1,str(movie_photo_thumb),1,0,str(episode_link)))

                        episode_id = cursor_insert_movie_episodes.lastrowid
                        cursor_insert_episode_links = db.cursor()
                        for mp4 in mp4s:
                            cursor_insert_episode_links.execute('''INSERT into episode_links(created_at,updated_at,movie_id,episode_id,mp4_link,status,is_visible)
                            values (%s,%s,%s,%s,%s,%s,%s)''',(created_at,created_at,movie_id,episode_id,mp4,1,1))
                    else:
                        print 'Episode already Added!'
                    print 'New Movie Added!' +str(cursor_insert_movie)
                else:
                    print 'Movie record exists!'
                    movie_id = 0
                    for row in cursor:
                        movie_id = row[0]

                    cursor_exist_movie_episode = db.cursor()
                    query_exists_movie_episode = "SELECT id,episode_title,episode_link from movie_episodes where episode_title = '%s' and episode_link = '%s' "%(str(episode_title),str(episode_link))
                    cursor_exist_movie_episode.execute(query_exists_movie_episode)
                    cursor_exist_movie_episode.fetchall()
                    if(cursor_exist_movie_episode.rowcount == 0):
                        cursor_insert_movie_episodes = db.cursor()
                        cursor_insert_movie_episodes.execute('''INSERT into movie_episodes (created_at,updated_at,movie_id,episode_title,episode_slug,status,cover_photo,is_visible,views,episode_link)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                        ,(created_at,created_at,movie_id,str(episode_title),str(episode_slug),1,str(movie_photo_thumb),1,0,str(episode_link)))

                        episode_id = cursor_insert_movie_episodes.lastrowid
                        cursor_insert_episode_links = db.cursor()
                        for mp4 in mp4s:
                            cursor_insert_episode_links.execute('''INSERT into episode_links(created_at,updated_at,movie_id,episode_id,mp4_link,status,is_visible)
                            values (%s,%s,%s,%s,%s,%s,%s)''',(created_at,created_at,movie_id,episode_id,mp4,1,1))

                    else:
                        print 'Episode already Added!'
                print '|-----------------------------------|'


                db.commit()
                cursor.close()
                db.close()
        except MySQLdb.Error as e:
            print("Something went wrong: {}".format(e))