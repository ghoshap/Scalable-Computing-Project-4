# Scalable-Computing-Project-4
Group 2:
      Team members:
            Aparna Ghosh
            Deepthi Rajappan
            Shubhangi Kukreti
            Antony Helson Chandy

Device Simulation code with 6 sensors.
Each sensor contains the code to act as an Edge Node or Sensor Node.
Each body instance has 6 sensor nodes and anyone of them can also be used as an edge node. 
And each sensor node transmits only the critical values to the edge node, and the edge node encrypts the data with SHA256 bit encryption  before transmitting it out of the body. The transmission from the edge nodes is done using Mqtt.


To Run: 
      Clone the Repository on the local machine.
      Install mosquito.
      Decide the node which you want to act as your Edge Node. for example, if take oximeter, goto Sensors2->oximeter->Component-> Helper->Mqtt open MqttPublisher.py in an editor and change the following line:
                host ='10.6.42.165' 
      replace the content of the quotes with the ip address of the broker(server) or change it to 'localhost' to run locally in only one machine.
  
  
  On OSX: 
  Put all the folders of the sensors in one Folder and name it Sensors2
  1. Open a terminal and navigate to the folder using cd command.
  2. run the shell script test.sh using the following command:
            >>>  sh test.sh
  3. It will ask you for the directory name which contains the code for all the sensors. Type Sensors2 and press enter
              Enter sensor directory..
              Sensors2 
  5.It will ask you which node do you want to act as the edge node.You can enter the name any of  6 sensors for eg. type oximeter and press enter.
              Name the Edge..
              oximeter
  6. 6 new instances of terminal should open and you should be able to see the data that the node is reading and transmitting. the transmissions and denoted as TX, therefore you can see all the data that is being read on the respective terminals but only the data that is critical is being transmitted to the node.
  
  For Windows/other Linux systems:
  1. goto the Edge Node folder and open a command promt in that folder and run Edge.py
           >>> python3 Edge.py
  
  2. In the same folder open a new terminal and run Node.py
           >>>  python3 Node.py
  
  3. Now navigate to each of the sensor folders that you want to run open a new terminal in that folder and run Node.py.
  you should be able to see the data that the node is reading and transmitting. the transmissions and denoted as TX, therefore you can see all the data that is being read on the respective terminals but only the data that is critical is being transmitted to the node.
