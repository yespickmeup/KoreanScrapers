/*
http://dramagalaxy.tv/
*/


drop schema if exists db_kdrama;
create schema db_kdrama;
use db_kdrama;

drop table if exists movies;
create table movies(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,title varchar(255)
,description text
,movie_slug varchar(255)
,category varchar(255)
,status int
,date_release date
,cover_photo varchar(500)
,movie_country_id varchar(255)
,is_visible int
);

drop table if exists movie_ratings;
create table movie_ratings(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,movie_id int
,rating int
,is_visible int
);

drop table if exists movie_countries;
create table movie_countries(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,country varchar(255)
,is_visible int
);

drop table if exists movie_tags;
create table movie_tags(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,movie_id int
,tag_id int
);
drop table if exists tags;
create table tags(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,tag varchar(255)
,tag_slug varchar(255)
,status int
,is_visible int
);



drop table if exists movie_episodes;
create table movie_episodes(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,movie_id int
,episode_title varchar(255)
,episode_slug varchar(255)
,status int
,cover_photo varchar(255)
,is_visible int
,views int
);

drop table if exists episode_links;
create table episode_links(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,movie_id int
,episode_id int
,mp4_link varchar(500)
,sequence int
,status int
,is_visible int
);

drop table if exists casts;
create table casts(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,name varchar(255)
,star_alias varchar(255)
,cast_slug varchar(255)
,birth_place varchar(255)
,height varchar(255)
,cover_photo varchar(255)
);


drop table if exists movie_casts;
create table movie_casts(
id int auto_increment primary key
,created_at datetime
,updated_at datetime
,cast_id int
,status int
,is_visible int
);










