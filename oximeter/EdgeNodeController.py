from Component.EdgeController import EdgeController
from Component.Bluetooth import Bluetooth
from Component.Battery import Battery
from Component.oximeterSensor import oximeterSensor
from Component.Handler.eventHook import EventHook
from Component.Helper.JsonHandler import JsonHandler
from Component.Helper.Mqtt.MqttPublisher import MqttPublisher
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import time
import sys

class EdgeNodeController (EdgeController) :

    _characteristicsPath = "Characteristics/oximeterController.json"

    def Setup(self):
        self.bt = Battery(self._ControllerChar['Battery']['CurrentState']['Power'])
        self.ble = Bluetooth(3.0,30)
        self.ble.ToRxMode()

    def __init__(self):
        self.jsonHandler = JsonHandler()
        self._ControllerChar = self.jsonHandler.LoadJson(self._characteristicsPath)
        self.Setup()
        self.ConnectHandlers()
        self._mqttService = MqttPublisher("EdgeNode","PatientMonitoring/Edge3/")
        super().__init__(3.0)

        try:
            while(True):
                self.Run()
        except KeyboardInterrupt:
            self._ControllerChar['Battery']['CurrentState']['Power'] = self.bt.GetCurrentCharge()
            self.__del__()
            exit(1)
    
    def __del__(self):
        self.jsonHandler.WriteJson(self._characteristicsPath,self._ControllerChar)
        self.ble.__del__()
        self.bt.__del__()
        super().__del__()

    def ConnectHandlers(self):
        self.ble._batteryEvent.addHandler(self.bt.Discharging)
        self._batteryEvent.addHandler(self.bt.Discharging)
        self.ble._uartEvent.addHandler(self.UartRx)

    def Run(self):
        pass

    def Encript(self,data):
        password_provided = "password" # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
        message = data.encode()

        f = Fernet(key)
        encrypted = f.encrypt(message)
   
        #print('RX --->>>', str(encrypted))
        return encrypted

    def UartRx(self,**kwargs):
        data = kwargs.get('data')
        self.UartPowerConsumed(data)
        print('RX --->>>', str(data))
        data = str(data).split('| ')
        #temp = int(data[0])
        encdata = self.Encript(data[0])
        self.WifiPowerConsumed(encdata)
        #if(temp>400 or temp<70):
        self._mqttService.Publish(encdata,data[1])

