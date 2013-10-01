from os import path, makedirs, statvfs, remove
import contextlib, cv2 

class assets():
    def webConfig(self):
    	pass
    	#will eventually check for internet connection then load latest config file
    
    def folderCheck(self):
        for f in self.folders:
            if not path.exists(self.folders[f]): makedirs(self.folders[f])    
   
    def assetPaths(self):
    	self.volumes={"usb":"photobusb"}#possible output locations
        #check if folders exist
        sc = self.storageCheck("photoboothb")
        if sc[1]:
        	baseLoc=sc[2]
        else:
        	baseLoc=""

        dAsset="resources" #assets folder
        dEvent="event" #/event folder
        dAsset=path.join(baseLoc,dAsset)
        dEvent=path.join(baseLoc,dEvent)
      
    
        self.images={   "background":path.join(dAsset,"clean.jpg"),
                        "thanks":path.join(dAsset,"thankyou.jpg"),
                        "cheese":path.join(dAsset,"saycheese.png"),
                        "count":path.join(dAsset,"countdown.avi")}

        self.audio={    "click":path.join(dAsset,"Sounds","CAMERA.WAV"),
                        "complete":path.join(dAsset,"Sounds","APPLAUSE.WAV")}

        self.folders={  "data":path.join(dEvent,"data"),
                        "gifs":path.join(dEvent,"gifs"),
                        "images":path.join(dEvent,"images"),
                        "montages":path.join(dEvent,"montages"),
                        "thumbs":path.join(dEvent,"thumbs")}
        
        
        self.devcam=0

    def camCheck(self): #check for camera and return message if none detected
        print("checking camera exists")
        #check all cameras
        for x in (0,1,2,3):
        	print "Testing camera " + str(x)
        	c=cv2.VideoCapture(x)
        	r=c.read()[0]
        	if r:
        		del(c)
        		return x
        	del(c)
        return ("None found")
        
    def storageCheck(self,vname):
		retval=(False,"Not Tested","Not Found")
		w=False
		print "Filesystem\tMounted on"
		with contextlib.closing(open('/etc/mtab')) as fp: 
		  for m in fp: 
		    fs_spec, fs_file, fs_vfstype, fs_mntops, fs_freq, fs_passno = m.split()
		    if fs_spec.startswith('/'):
		       r = statvfs(fs_file)
		       print "%s\t%s" % (fs_spec, fs_file)
		    if fs_file.find(vname)!=-1:
	           	try:
	           		p=path.join(fs_file,"test")
	           		f=open(p,"w")
	           		f.write("test")
	           		remove(p)
	           		f.close()
	           		w=True
	           	except Exception, e:
	           		print e
	           		w=False
		        retval = (True,w,fs_file)
		return retval #media found,writable,path

    def gpio(self):
        self.inputs = {"init":False}
        #init all GPIO inputs
        
    def __init__(self):
        self.assetPaths()
        self.webConfig()
        self.folderCheck()
        self.devcam=self.camCheck() 
        self.gpio()   