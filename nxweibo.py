#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config

from bottle import route, run, request, redirect, template, static_file
from weibo import APIClient
import urllib2
import csv
import codecs

client = APIClient(app_key = config.weiboAppKey, app_secret = config.weiboAppSecret, redirect_uri = config.weiboCallBackURL)

@route('/')
def index():
  code = request.query.code
  if not code:
    return template('index.tpl')
  r = client.request_access_token(code)
  access_token = r.access_token 
  expires_in = r.expires_in
  client.set_access_token(access_token, expires_in)
  return template('accesstoken.tpl', accesstoken = access_token)  

@route('/token')
def token():
  url = client.get_authorize_url()
  redirect(url, 302)

@route('/home_timeline')
def hometimeline():
  if not client.access_token:
    redirect('/token', 302)

  f = open('home_timeline.csv', 'wb')
  wr = csv.writer(f)
    
  for i in xrange(1, 21):
    r = client.statuses.home_timeline.get(page = i, count = 99)
    for st in r.statuses:
      statusList = [st.id, st.user.screen_name, st.text, st.created_at, st.comments_count, st.reposts_count, st.attitudes_count ];
      wr.writerow([(isinstance(v,unicode) and v.encode('utf8') or v) for v in statusList])

  f.close()
  return static_file('home_timeline.csv', root='./')

@route('/weibocr')
def weibocr():
  if not client.access_token:
    redirect('/token', 302)

  l = len(request.query)
  if l == 0:
    return template('weibocr.tpl')

  weiboID = request.query.id
  c = client.statuses.count.get(ids = weiboID)
  commentsCount = c[0].comments
  repostsCount = c[0].reposts

  f = open('output_comments.csv', 'wb')
  wr = csv.writer(f)
  pageCount = 200

  for i in xrange(1, commentsCount / pageCount + 2):
      if i == 11:
          break
      print 'Page',i
      cr = client.comments.show.get(id=weiboID, page=i, count = pageCount)
      for st in cr.comments:
          commentsList = [st.id, st.text, st.created_at, st.source, st.user.id, st.user.name, st.user.gender, st.user.location, st.user.followers_count];
          wr.writerow([(isinstance(v,unicode) and v.encode('utf8') or v) for v in commentsList])
  f.close()
    
  f2 = open('output_reposts.csv', 'wb')
  wr2 = csv.writer(f2)

  for i in xrange(1, repostsCount / pageCount + 2):
      if i == 11:
          break
      print 'Page',i
      rr = client.statuses.repost_timeline.get(id=weiboID, page=i, count = pageCount)
      for st in rr.reposts:
          repostsList = [st.id, st.text, st.created_at, st.source, st.user.id, st.user.name, st.user.gender, st.user.location, st.user.followers_count];
          wr2.writerow([(isinstance(v,unicode) and v.encode('utf8') or v) for v in repostsList])
  f2.close()

  return template('weibocr_download.tpl')

@route('/downloadcomments')
def downloadcomments():
  return static_file('output_comments.csv', root='./')

@route('/downloadreposts')
def downloadreposts():
  return static_file('output_reposts.csv', root='./')


# Run Server
run(host = 'localhost', port = 7777, reloader = True, debug = True)
