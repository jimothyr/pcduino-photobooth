
#TODO
#autosize to screen
#look for portable storage
#add sounds
#add videocountdown
#web check


from Tkinter import *
#from mplayer import Player
from os import path, makedirs, statvfs, remove
from PIL import ImageTk, Image
import threading, sys, contextlib, time, datetime, cv2


class GPIO():
    def __init__(self):
        #set paths
        GPIO_MODE_PATH=path.normpath("/sys/devices/virtual/misc/gpio/mode")
        GPIO_PIN_PATH=path.normpath("/sys/devices/virtual/misc/gpio/pin")
        GPIO_FILENAME="gpio"
        #init pin arrays
        self.pinMode=[]
        self.pinData=[]
        
        #create pin assignments
        for i in range(0,18):
            self.pinMode.append(path.join(GPIO_MODE_PATH,GPIO_FILENAME+str(i)))
            self.pinData.append(path.join(GPIO_PIN_PATH,GPIO_FILENAME+str(i)))

        #init vals
        self.values={   'HIGH':'1',
                        'LOW':'0',
                        'INPUT':'0',
                        'INPUT_PU':'8',
                        'OUPUT':'1'}
        
        #reset pins to default??
        #on exit reset pins??

    def getData(self,pinId):
        temp=['']
        file = open(self.pinData[pinId],'r')
        # file.seek[0]
        temp[0]=file.read()
        file.close()
        return temp[0]
        #return self.pinData[pinId]

    def setData(self,pinId,Value):
        
        file=open(self.pinData[pinId],'r+')
        file.write(self.values[Value])
        file.close
        return True
    
    
    def getMode(self,pinId):
        temp=['']
        file = open (self.pinMode[self.pinId],'r')
        file.seek[0]
        temp[0]=file.read()
        file.close()
        return temp[0]

    def setMode(self,pinId,Value):  
        file=open(self.pinData[self.pinMode],'r+')
        file.write(self.values[self.Value])
        file.close



def make_contact_sheet(fnames,(ncols,nrows),(photow,photoh),
                       (marl,mart,marr,marb),
                       padding):
    """\
    Make a contact sheet from a group of filenames:

    fnames       A list of names of the image files
    
    ncols        Number of columns in the contact sheet
    nrows        Number of rows in the contact sheet
    photow       The width of the photo thumbs in pixels
    photoh       The height of the photo thumbs in pixels

    marl         The left margin in pixels
    mart         The top margin in pixels
    marr         The right margin in pixels
    marb         The bottom margin in pixels

    padding      The padding between images in pixels

    returns a PIL image object.
    """

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+ marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (ncols*photow+marw+padw,nrows*photoh+marh+padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    inew = Image.new('RGB',isize,white)

    count = 0
    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            try:
                # Read in an image and resize appropriately
                img = Image.open(fnames[count]).resize((photow,photoh))
            except:
                break
            inew.paste(img,bbox)
            count += 1
    return inew




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

class Application(Frame):
    
    def captureLoop(self,event):


        self.webcam=False
        self.capture=True
        #init countdown video
        
        #init GPIO lights

        #a.inputs("init")=True
      
        
        #iWDTH=1680#1920
        #iHGHT=950#1080
        #self.aspectRatio=iWDTH/iHGHT
        self.vcam.set(3,self.capWidth)
        self.vcam.set(4,self.capHeight)

        ts = datetime.datetime.now().strftime("%Y%m%d%I%M_%s")
        
        self.overlay.itemconfig(self.camtext, text="Ready ...")

        mgeo=self.movie_window.winfo_geometry().split("+")

        
        self.overlay.place(x=mgeo[1],y=mgeo[2],width=mgeo[0].split("x")[0],height=mgeo[0].split("x")[1])
        
        root.update()
        
        #switch on lights
        for l in (14,15,16,17):
            try:
                g.setData(l,"HIGH")
            except Exception, e:
                raise e

        self.thbs=[]
        self.labels=[]
        self.fnames=[]

        time.sleep(2)

        for j in [1,2,3,4]:
            ja=j-1
            print("Taking image..." + str(j))

            
            self.overlay.itemconfig(self.camtext, text="3")
            root.update()
            time.sleep(1)

            self.overlay.itemconfig(self.camtext, text="2")
            root.update()
            time.sleep(1)

            self.overlay.itemconfig(self.camtext, text="1")
            root.update()
            time.sleep(1)
            
            self.overlay.itemconfig(self.camtext, text="Smile :)")
            root.update()
            time.sleep(1)
            #some sort of osd thing
            #setup paths
            fn=path.join(a.folders['images'],ts+"_"+str(j)+".png")
            fnthb = path.join(a.folders['thumbs'],ts+"_"+str(j)+".png")
            self.fnames.append(fn)
            file = fn
            #get image
            for i in xrange(5):##while video is playing wait.
                temp = self.vcam.read()
            _b, camera_capture = self.vcam.read()#self.get_image(camera)
            #generate thumb
            cvthb = cv2.resize(camera_capture,(self.imageWidth,self.imageHeight))  
            cvthbcc = cv2.cvtColor(cvthb, cv2.COLOR_RGB2BGR)
                        #imb = Image.fromarray(cvthb)
            #ima=Image.open(fnthb)
           
            #write to imageframe
            self.thbs.append(ImageTk.PhotoImage(image=Image.fromarray(cvthbcc)))
            for child in self.imgs[ja].winfo_children():#clear out frame in case of hiccup
    			child.destroy()
            self.labels.append(Label(self.imgs[ja],image=self.thbs[ja]))
            self.labels[ja].pack()
            #self.imgs[j-1].create_image(0, 0, image= self.thbs[j-1])
            
             # write main image to disk
            cv2.imwrite(file, camera_capture)#main
            cv2.imwrite(fnthb, cvthb)   #thumb

            #time.sleep(3)

            root.update()
      
        self.overlay.itemconfig(self.camtext, text="All Done, thanks")
        self.webcam=True
         #switch off lights
        for l in (14,15,16,17):
            try:
                g.setData(l,"LOW")
            except Exception, e:
                raise e

        #self.hi_there.config(state = NORMAL)
        mf = make_contact_sheet(self.fnames,(1,4),(self.capWidth,self.capHeight),(10,10,10,10),10)
        mf.save(path.join(a.folders['montages'],ts+".jpg"))
        time.sleep(3)
        self.overlay.place_forget()
        self.show_video()

    def quit_me(self,event):
        self.webcam=False #kill webcam loop
        #clean up to ensure webcam released
        try:
            del(self.vcam)
        except Exception, e:
            pass
       
        self.quit()

    def initialise_camera(self):
        #check for camera existing
        self.vcam = cv2.VideoCapture(a.devcam)
        self.capWidth=1680#1920 #preferred image capture size
        self.capHeight=950#1080 
        #set what we can
        self.vcam.set(3,self.capWidth)
        self.vcam.set(4,self.capHeight)
        #check resolution and set image size
        self.vcamWidth=self.vcam.get(3)
        self.vcamHeight=self.vcam.get(4)   
        self.vcamAspect=self.vcamWidth/self.vcamHeight 
        #check for true on read
        #put webcam in video frame
    def show_video(self):
        vwin=self.movie_window

        self.vcam.set(3,vwin.config("width")[4])
        self.vcam.set(4,vwin.config("height")[4])
        
        while(self.webcam==True):
            (_b,f) = self.vcam.read()
            f =cv2.flip(f, 1)
            gray_im = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
            a = Image.fromarray(gray_im)
            b = ImageTk.PhotoImage(image=a)
            vwin.configure(image=b)

            if cv2.waitKey(5)==27:
                break

            root.update()
    
    def printme(self,event):
        print "hello" + str(event.x)

    def key(self,event):
        print "pressed", repr(event.char)
        if event.char=="q":
            self.quit_me()
    
    def createWidgets(self):
        self.initialise_camera()
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        #work out best geometry based on screen size and set movie size      
        self.movieHeight=int(h*0.6)
        self.movieWidth=int(self.movieHeight*self.vcamAspect)
        
        self.imageHeight=int(h*0.2)
        self.imageWidth=int(self.imageHeight*self.vcamAspect)

        self.vcam.set(3,self.movieWidth)
        self.vcam.set(4,self.movieHeight)
        #quit button
        
        # self.QUIT = Button(self)
        # self.QUIT["text"] = "QUIT"
        # self.QUIT["fg"]   = "red"
        # self.QUIT["command"] =  self.quit_me
        # self.QUIT.grid(row=0,column=0)
        #take image
        # self.hi_there = Button(self)
        # self.hi_there["text"] = "click",
        # self.hi_there["command"] = self.captureLoop
        # self.hi_there.grid(row=0,column=1)
        #webcam window
        self.movie_window = Label(self, height=self.movieHeight,  bg="#333")
        self.movie_window.grid(column=1, row=1, rowspan=4, columnspan=2)
        
        #placeholders for taken images
        self.imgs=[]
        self.imglabels=[]


        for j in [0,1,2,3]:
            me = self.imgs.append(Frame(self, width=self.imageWidth, height=self.imageHeight,bg="red"))
            self.imgs[j].grid(column=0,row=j+1,padx=20,pady=20)

        self.overlay=Canvas(self,bg="#333")


        self.camtext = self.overlay.create_text(200, 200, text="Ready", font=("helvetica",60), fill="white")
        
       
    def populateWidgets(self):
        t = threading.Thread(target=self.show_video())
        t.start()
            
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.configure(background='#333',cursor='none')
        master.bind("<Button-1>",self.captureLoop)
        master.bind("<Button-3>",self.quit_me)
        self.focus_set()
        self.pack()
        self.webcam=True
        self.capture=False
        self.createWidgets()
        self.populateWidgets()
        
 #ensure environment is set up and ready to go.
a = assets()
g = GPIO()
#initialise tk instance
root = Tk()
root.attributes("-fullscreen",1) #set to fullscreen
root.configure(background="#333",cursor="none")


app = Application(master=root)

app.mainloop()

root.destroy()
