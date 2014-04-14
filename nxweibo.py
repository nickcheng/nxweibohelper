#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
import bottle
from bottle import Bottle, route, run, request, redirect, template, static_file
from vendor.weibo import APIClient
import urllib2
import csv
import codecs
import time
import datetime
import os

client = APIClient(app_key = weiboAppKey, app_secret = weiboAppSecret, redirect_uri = weiboCallBackURL)

def preprocess(request):
  params = {
    'accesstoken': request.query.accesstoken or '',
    'userid': request.query.userid or ''
  }
  return params

def timestamp():
  ts = repr(time.time())
  dt = datetime.datetime.fromtimestamp(time.mktime(time.gmtime())).strftime('%Y%m%d%H%M%S')
  result = dt + '_' + ts
  return result

def getCSVFiles():
  curPath = os.getcwd()
  fileList = os.listdir(curPath)
  csvFiles = []
  for f in fileList:
    if f.endswith('.csv'):
      csvFiles.append(os.path.join(curPath, f))

  return sorted(csvFiles)

@route('/')
def index():
  params = preprocess(request)

  # Code -> Token
  code = request.query.code
  if code:
    r = client.request_access_token(code)
    params['accesstoken'] = r.access_token
    params['userid'] = str(r.uid)

  # Get files in folder
  params['csv'] = getCSVFiles()
  
  return template('index.tpl', params = params)

@route('/token')
def token():
  url = client.get_authorize_url()
  redirect(url, 302)

@route('/home_timeline')
def hometimeline():
  params = preprocess(request)
  #
  if not params['accesstoken']:
    redirect('/token', 302)

  fn = 'home_timeline' + '_' + params['userid'] + '_' + timestamp() + '.csv'
  f = open(fn, 'wb')
  wr = csv.writer(f)
    
  for i in xrange(1, 41):
    r = client.statuses.home_timeline.get(source = weiboAppKey, access_token = params['accesstoken'], page = i, count = 50)
    for st in r.statuses:
      statusList = [st.id, st.user.screen_name, st.text, st.created_at, st.comments_count, st.reposts_count, st.attitudes_count];
      wr.writerow([(isinstance(v,unicode) and v.encode('utf8') or v) for v in statusList])

  f.close()
  return static_file(fn, root = './', download = fn)

@route('/user_timeline')
def usertimeline():
  params = preprocess(request)
  #
  if not params['accesstoken']:
    redirect('/token', 302)

  fn = 'user_timeline' + '_' + params['userid'] + '_' + timestamp() + '.csv'
  f = open(fn, 'wb')
  wr = csv.writer(f)
    
  for i in xrange(1, 41):
    print 'Page',i
    r = client.statuses.user_timeline.get(source = weiboAppKey, access_token = params['accesstoken'], uid = params['userid'], page = i, count = 50)
    for st in r.statuses:
      statusList = [st.id, st.user.screen_name, st.text, st.created_at, st.comments_count, st.reposts_count, st.attitudes_count];
      wr.writerow([(isinstance(v,unicode) and v.encode('utf8') or v) for v in statusList])

  f.close()
  return static_file(fn, root = './', download = fn)

@route('/weibocr')
def weibocr():
  params = preprocess(request)
  #
  if not params['accesstoken']:
    redirect('/token', 302)

  weiboID = 0
  if request.query.id:
    weiboID = request.query.id
  elif request.query.link:
    weiboID = weiboLink2ID(request.query.link, params)
  else:
    return template('weibocr.tpl', params = params)

  print weiboID
  c = client.statuses.count.get(source = weiboAppKey, access_token = params['accesstoken'], ids = weiboID)
  commentsCount = c[0].comments
  repostsCount = c[0].reposts

  fn1 = 'output_comments' + '_' + weiboID + '_' + timestamp() + '.csv'
  f = open(fn1, 'wb')
  wr = csv.writer(f)
  pageCount = 200

  for i in xrange(1, commentsCount / pageCount + 2):
      if i == 11:
          break
      print 'Page',i
      cr = client.comments.show.get(source = weiboAppKey, access_token = params['accesstoken'], id=weiboID, page=i, count = pageCount)
      for st in cr.comments:
          commentsList = [st.id, st.text, st.created_at, st.source, st.user.id, st.user.name, st.user.gender, st.user.location, st.user.followers_count];
          wr.writerow([(isinstance(v,unicode) and v.encode('utf8') or v) for v in commentsList])
  f.close()
    
  fn2 = 'output_reposts' + '_' + weiboID + '_' + timestamp() + '.csv'
  f2 = open(fn2, 'wb')
  wr2 = csv.writer(f2)

  for i in xrange(1, repostsCount / pageCount + 2):
      if i == 11:
          break
      print 'Page',i
      rr = client.statuses.repost_timeline.get(source = weiboAppKey, access_token = params['accesstoken'], id=weiboID, page=i, count = pageCount)
      for st in rr.reposts:
          repostsList = [st.id, st.text, st.created_at, st.source, st.user.id, st.user.name, st.user.gender, st.user.location, st.user.followers_count];
          wr2.writerow([(isinstance(v,unicode) and v.encode('utf8') or v) for v in repostsList])
  f2.close()

  params['commentsfilename'] = fn1
  params['repostsfilename'] = fn2
  return template('weibocr_download.tpl', params = params)

@route('/download')
def download():
  fn = request.query.fn
  return static_file(fn, root = './', download = fn)

@route('/weibogo')
def weibogo():
  params = preprocess(request)
  #
  if not params['accesstoken']:
    redirect('/token', 302)

  weiboID = request.query.id
  if not weiboID:
    return template('weibogo.tpl', params = params)

  url = weiboID2URL(weiboID, params)

  redirect(url)

def weiboID2URL(weiboID, params):
  cr = client.statuses.show.get(source = weiboAppKey, access_token = params['accesstoken'], id = weiboID)
  userID = cr.user.id
  cr2 = client.statuses.querymid.get(source = weiboAppKey, access_token = params['accesstoken'], id = weiboID, type = 1)
  url = 'http://weibo.com/%s/%s' % (userID, cr2.mid)
  return url

def weiboLink2ID(weiboLink, params):
  #http://weibo.com/1655001967/AD2k2fhs3?mod=weibotime
  ss = weiboLink
  a = ss.find('weibo.com/')
  begin = ss.find('/', a + 10) + 1
  end = ss.find('?')
  mid = ss[begin:] if end < 0 else ss[begin:end]

  #
  cr = client.statuses.queryid.get(source = weiboAppKey, access_token = params['accesstoken'], mid = mid, type = 1, isBase62 = 1)
  result = cr.id

  return result

# Run Server
if __name__ == '__main__':
  run(host = 'localhost', port = 7777, reloader = True, debug = True)

app = bottle.default_app()
