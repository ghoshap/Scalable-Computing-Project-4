from Component.MicroController import MicroController
from Component.Bluetooth import Bluetooth
from Component.Battery import Battery
from Component.oximeterSensor import oximeterSensor
from Component.Handler.eventHook import EventHook
from Component.Helper.JsonHandler import JsonHandler
import time
import sys

class oximeterController (MicroController) :

    _characteristicsPath = "Characteristics/oximeterController.json"

    def Setup(self):
        self.bt = Battery(self._ControllerChar['Battery']['CurrentState']['Power'])
        self.ble = Bluetooth(3.0,30)
        self.ts = oximeterSensor(3.0)

    def __init__(self):
        self.jsonHandler = JsonHandler()
        self._ControllerChar = self.jsonHandler.LoadJson(self._characteristicsPath)
        self.Setup()
        self.ConnectHandlers()
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
        self.ts.__del__()
        self.bt.__del__()
        super().__del__()

    def ConnectHandlers(self):
        self.ble._batteryEvent.addHandler(self.bt.Discharging)
        self.ts._batteryEvent.addHandler(self.bt.Discharging)
        self._batteryEvent.addHandler(self.bt.Discharging)

    def Run(self):
        time.sleep(3)
        temp = self.ReadOxygenLevel()
        #time.sleep(3)
        print("Oximeter---->"+str(temp))
        if (temp < 90):
            self.WriteBluetooth(temp)
        time.sleep(3)

    def ReadOxygenLevel(self):
        self.I2CRead()
        return self.ts.I2CRead()

    def WriteBluetooth(self,data):
        super().I2CWrite()
        data = str(data) + '| OxygenLevel'
        self.ble.Tx(data)