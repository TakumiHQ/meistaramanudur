BUCKET = meistaramanudur

upload:
	honcho run ssstatic -c public/ $(BUCKET)/web/ > .static-md5

deploy: upload
	git push -f heroku master
	heroku config:add STATIC_URL=`cat .static-md5`
	rm .static-md5
