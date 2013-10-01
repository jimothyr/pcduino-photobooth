from os import path, makedirs

class GPIO():
    def __init__(self):


        #set paths
        GPIO_MODE_PATH=path.normpath("/sys/devices/virtual/misc/gpio/mode")
        GPIO_PIN_PATH=path.normpath("/sys/devices/virtual/misc/gpio/pin")
        GPIO_FILENAME="gpio"
        #init pin arrays
        self.pinMode=[]
        self.pinData=[]
        
        #check on pcduino?? if not create temporary folder for testing


        if not path.isdir(GPIO_MODE_PATH):
            print "Not on a pcduino .. creating local testing files"
            GPIO_MODE_PATH ="GPIO/mode"
            GPIO_PIN_PATH = "GPIO/pins"
            makedirs(GPIO_MODE_PATH)   
            makedirs(GPIO_PIN_PATH)  

        #create pin assignments
        for i in range(0,18):
            self.pinMode.append(path.join(GPIO_MODE_PATH,GPIO_FILENAME+str(i)))
            self.pinData.append(path.join(GPIO_PIN_PATH,GPIO_FILENAME+str(i)))

            if not path.exists(self.pinMode[i]): 
                open(self.pinMode[i],'a').close()     

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

class light_ctrl():

    def __init__(self):
        #get input/out types and init GPIO
        pass

    def setOn(self):#switch on lightarray
        print "switching on"
           #switch on lights
        #TODO move this to asset control class... abstract out for different interfaces
        # for l in (14,15,16,17):
        #     try:
        #         g.setData(l,"HIGH")
        #     except Exception, e:
        #         raise e
        

    def setOff(self):#switch off lightarray
        print "switching off"
         #switch off lights
         #TODO abstract
        # for l in (14,15,16,17):
        #     try:
        #         g.setData(l,"LOW")
        #     except Exception, e:
        #         raise e
        