#current state
#gpio light not switched on

#Instructions
#left click initiate capture
#right click quit


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
from gpio import GPIO
from img_proc import make_contact_sheet
from assets import assets

class Application(Frame):
    
    def captureLoop(self,event):


        self.webcam=False
        self.capture=True
        #init countdown video
        
        #init GPIO lights

        #a.inputs("init")=True
    
        self.vcam.set(3,self.capWidth)
        self.vcam.set(4,self.capHeight)

        ts = datetime.datetime.now().strftime("%Y%m%d%I%M_%s")
        
        self.overlay.itemconfig(self.camtext, text="Ready ...")

        mgeo=self.movie_window.winfo_geometry().split("+")

        
        self.overlay.place(x=mgeo[1],y=mgeo[2],width=mgeo[0].split("x")[0],height=mgeo[0].split("x")[1])
        
        root.update()
        
        #switch on lights
        #TODO move this to asset control class... abstract out for different interfaces
        # for l in (14,15,16,17):
        #     try:
        #         g.setData(l,"HIGH")
        #     except Exception, e:
        #         raise e

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
            fn=path.join(a.folders['images'],ts+"_"+str(j)+".jpg")
            fnthb = path.join(a.folders['thumbs'],ts+"_"+str(j)+".jpg")
            self.fnames.append(fn)
            file = fn
            #get image
            for i in xrange(15):##while video is playing wait.
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
         #TODO abstract
        # for l in (14,15,16,17):
        #     try:
        #         g.setData(l,"LOW")
        #     except Exception, e:
        #         raise e

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
