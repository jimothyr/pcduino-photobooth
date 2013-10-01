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
from os import path, makedirs, statvfs, remove
from PIL import ImageTk, Image
import threading, sys, contextlib, time, datetime, cv2
from gpio import GPIO, light_ctrl
from img_proc import make_contact_sheet
from assets import assets

class Application(Frame):
    
    def captureLoop(self):
        #TODO - sound 
        #TODO - Lights
        c = cv2.VideoCapture(self.a.devcam)
        #init countdown video
        
        #init GPIO lights

        #a.inputs("init")=True
    
        # self.vcam.set(3,self.capWidth)
        # self.vcam.set(4,self.capHeight)

        c.set(3,10000)
        c.set(4,10000)

        capWidth =  int(c.get(3))
        capHeight = int(c.get(4))

        ts = datetime.datetime.now().strftime("%Y%m%d%I%M_%s")
        
        self.overlay.itemconfig(self.camtext, text="Ready ...")

        mgeo=self.movie_window.winfo_geometry().split("+")

        
        self.overlay.place(x=mgeo[1],y=mgeo[2],width=mgeo[0].split("x")[0],height=mgeo[0].split("x")[1])
        
        root.update()
        
        self.l.setOn()
     

        thbs=[]
        labels=[]
        fnames=[]

        time.sleep(2)

        for j in [1,2,3,4]:
            ja=j-1

            print "setting file paths"
            fn=path.join(self.a.folders['images'],ts+"_"+str(j)+".jpg")
            fnthb = path.join(self.a.folders['thumbs'],ts+"_"+str(j)+".jpg")
            fnames.append(fn)
            file = fn

            print "showing countdown"

            count=["3","2","1","Smile ya Bastard"]

            for i in count:
                self.overlay.itemconfig(self.camtext, text=i)
                root.update()
                time.sleep(0.5)

            
            print "Taking image " + str(j) + " at " + str(capWidth) + "x" + str(capHeight)
            #get image
            for i in xrange(15):#ramp up to ensure stable image
                temp = c.read()
            _b, camera_capture = c.read()#self.get_image(camera)
            #generate thumb
            cvthb = cv2.resize(camera_capture,(self.imageWidth,self.imageHeight))  
            cvthbcc = cv2.cvtColor(cvthb, cv2.COLOR_RGB2BGR)
                        #imb = Image.fromarray(cvthb)
            #ima=Image.open(fnthb)
           
            #write to imageframe
            thbs.append(ImageTk.PhotoImage(image=Image.fromarray(cvthbcc)))
            for child in self.imgs[ja].winfo_children():#clear out frame in case of hiccup
                child.destroy()
            labels.append(Label(self.imgs[ja],image=thbs[ja]))
            labels[ja].pack()
            #self.imgs[j-1].create_image(0, 0, image= self.thbs[j-1])
            
             # write main image to disk
            cv2.imwrite(file, camera_capture)#main
            cv2.imwrite(fnthb, cvthb)   #thumb

            #time.sleep(3)

            root.update()

        del(c)    
      
        self.overlay.itemconfig(self.camtext, text="All Done, thanks")
        self.webcam=True
        

        #self.hi_there.config(state = NORMAL)
        print "building montage"
        mf = make_contact_sheet(fnames,(1,4),(capWidth,capHeight),(10,10,10,10),10)
        print "saving montage"
        mf.save(path.join(self.a.folders['montages'],ts+".jpg"))
        #time.sleep(3)
        self.overlay.place_forget()
        self.l.setOff()

        self.show_video()

    def quit_me(self,event):
        print "quit asked for"
        self.quit_x=True
        self.webcam=False
        
        #clean up to ensure webcam released
        self.quit()

    def init_capture(self, event):
        print "left mouse button clicked"
        self.webcam=False   

    def show_video(self):
        
        vwin=self.movie_window
        c=cv2.VideoCapture(self.a.devcam)
        #c.set(3,vwin.config("width")[4])
        #c.set(4,vwin.config("height")[4])
        
        while(self.webcam==True):
            (_b,f) = c.read()
            f =cv2.flip(f, 1)
            gray_im = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
            a = Image.fromarray(gray_im)
            b = ImageTk.PhotoImage(image=a)
            vwin.configure(image=b)

            if cv2.waitKey(5)==27:
                break

            root.update()
    
        del(c)
        if (self.quit_x==False):
            self.captureLoop()
        

    def printme(self,event):
        print "hello" + str(event.x)

    def key(self,event):
        print "pressed", repr(event.char)
        if event.char=="q":
            self.quit_me()
    
    def createWidgets(self):
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        #work out best geometry based on screen size and set movie size      
        self.movieHeight=int(h*0.6)
        self.movieWidth=int(self.movieHeight*self.a.camRes[2])
        
        self.imageHeight=int(h*0.2)
        self.imageWidth=int(self.imageHeight*self.a.camRes[2])

        #self.vcam.set(3,self.movieWidth)
        #self.vcam.set(4,self.movieHeight)
       
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
        # t = threading.Thread(target=self.show_video(a.devcam))
        # t.start()
        self.quit_x=False
        self.show_video()

    def __init__(self, master=None):
         #ensure environment is set up and ready to go.
        self.a = assets()
        self.g = GPIO()
        self.l = light_ctrl()
        Frame.__init__(self, master)
        
        self.configure(background='#333',cursor='none')
        master.bind("<Button-1>",self.init_capture)
        master.bind("<Button-3>",self.quit_me)
        self.focus_set()
        self.pack()
        self.webcam=True
        self.capture=False
        self.createWidgets()
        self.populateWidgets()
        

#initialise tk instance
root = Tk()
root.attributes("-fullscreen",1) #set to fullscreen
root.configure(background="#333",cursor="none")


app = Application(master=root)

app.mainloop()

root.destroy()
