
import urllib2

def internet_on():
    try:
        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def phone_home():
	if internet_on():
		print 'secret key'
		print 'send stats'
		print 'start syncing files!!'

def write_out_data(data):
	f=file

	file = open("data.file.txt",'+a')
	file.write(data)
	file.close()
	#write outs file list in form to be sucked in by javascript on webserver

