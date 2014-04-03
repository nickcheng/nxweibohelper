% include('header.tpl', params = params)

<hr />
<a href='/download{{'?fn='+params['commentsfilename']}}'>Download Comments: {{params['commentsfilename']}}</a><br />
<a href='/download{{'?fn='+params['repostsfilename']}}'>Download Reposts: {{params['repostsfilename']}}</a><br />
