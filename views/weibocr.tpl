% include('header.tpl', params = params)

<form action='/weibocr'>
	weiboID:
	<input type='text' name = 'id' />
	<input type='hidden' name = 'accesstoken' value='{{params['accesstoken']}}' />
	<input type='hidden' name = 'userid' value='{{params['userid']}}' />
	<input type='submit' value='Submit' />
</form>
<form action='/weibocr'>
	weiboLink:
	<input type='text' name = 'link' />
	<input type='hidden' name = 'accesstoken' value='{{params['accesstoken']}}' />
	<input type='hidden' name = 'userid' value='{{params['userid']}}' />
	<input type='submit' value='Submit' />
</form>