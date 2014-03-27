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
		# redirect('/token')
		return template('index.tpl')
	r = client.request_access_token(code)
	access_token = r.access_token 
	expires_in = r.expires_in
	client.set_access_token(access_token, expires_in)
	return access_token

@route('/token')
def token():
	url = client.get_authorize_url()
	redirect(url, 302)

@route('/home_timeline')
def hometimeline():
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
	return 'weibocr'

# Run Server
run(host = 'localhost', port = 7777, reloader = True, debug = True)
