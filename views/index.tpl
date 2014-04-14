% import os

% include('header.tpl', params = params)
<ul>
	<li>Timeline
		<ul>
			<li><a href='/home_timeline{{'?accesstoken=' + params['accesstoken'] + '&userid=' + (params['userid'])}}'>Home TL</a></li>
			<li><a href='/user_timeline{{'?accesstoken=' + params['accesstoken'] + '&userid=' + (params['userid'])}}'>Yourselves' TL</a></li>
		</ul>
	</li>
	<li>Tools
		<ul>
			<li><a href='/weibocr{{'?accesstoken=' + params['accesstoken'] + '&userid=' + (params['userid'])}}'>Count of cmmnts and rpst</a></li>
			<li><a href='/weibogo{{'?accesstoken=' + params['accesstoken'] + '&userid=' + (params['userid'])}}'>Go to webpage by weiboid</a></li>
		</ul>
	</li>
% if params['csv']:
	<li>Downloads
    <ul>
% for f in params['csv']:
      <li><a href='/download?fn={{os.path.split(f)[1]}}'>{{os.path.split(f)[1]}}</a></li>
% end
    </ul>
	</li>
% end
</ul>
