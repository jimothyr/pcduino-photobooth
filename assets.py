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

  

    def camCheck(self): 
    	#check for camera and return dev id , max res of first found
    	#return message if none detected
        #TODO - check for resolution and aspect ratio.
        print("checking camera exists")
        #check all cameras
        for x in (0,1,2,3):
        	print "Testing for existance of camera " + str(x)
        	c=cv2.VideoCapture(x)
        	r=c.read()[0]
        	if r:
        		del(c)
        		return x
        	del(c)
        return ("None found")

    def camResCheck(self,camId):
    	print "checking resolution of camera " + str(camId)
    	c=cv2.VideoCapture(camId)
    	#set stupidly high values and see what sticks
        Width=10000
        Height=10000
        #set 
        c.set(3,Width)
        c.set(4,Height)
        #check resolution in output file
        # for i in xrange(15):#ramp up to ensure stable image
        #         temp = c.read()
        # _b, camera_capture = c.read()#self.get_image(camera)
        # cv2.imwrite("test.jpg", camera_capture)#main

        res=[int(c.get(3)),int(c.get(4)),c.get(3)/c.get(4)] #width,height,aspect_ratio
        del(c) #release camera

        print "max resolution of " + str(res[0]) + " x " + str(res[1]) + " found"
        return res
      
    	

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
        self.camRes=self.camResCheck(self.devcam)
        self.gpio()   