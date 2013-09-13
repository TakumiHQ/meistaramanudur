BUCKET = meistaramanudur

upload:
	heroku config:add STATIC_URL=`honcho run ssstatic public/ $(BUCKET)/public/`
