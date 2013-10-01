from os import path

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
 
