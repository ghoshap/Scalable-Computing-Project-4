import json
import matplotlib.pyplot as plt
s1 = list();
k2=list();
with open('BatteryLog.json') as json_file:
    data = json.load(json_file)
    for p in data['Log']:
        s1.append(p['CurrentPower']); 
        k2.append(p['TimeStamp'][11:]);
 
nlen=list()
h=len(s1)
for j in range(h):
	nlen.append(j);
	  
x = k2 
y = s1
plt.plot(x, y,color='red') 
plt.xlabel('TimeStamp') 
plt.ylabel('EMGSensor I2C')  
plt.title('Power Consumed') 
plt.show() 
