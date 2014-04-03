% include('header.tpl', params = params)

<ul>
	<li><a href='/home_timeline{{'?accesstoken=' + params['accesstoken'] + '&userid=' + (params['userid'])}}'>Home TL</a></li>
	<li><a href='/user_timeline{{'?accesstoken=' + params['accesstoken'] + '&userid=' + (params['userid'])}}'>Yourselves' TL</a></li>
	<li><a href='/weibocr{{'?accesstoken=' + params['accesstoken'] + '&userid=' + (params['userid'])}}'>Count of cmmnts and rpst</a></li>
	<li><a href='/weibogo{{'?accesstoken=' + params['accesstoken'] + '&userid=' + (params['userid'])}}'>Go to webpage by weiboid</a></li>
</ul>
