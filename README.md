# EM_BOT
The death count in emergencies is not high because of the people present there 
but also because of the people sent to rescue them. Sending our armed forces 
without proper knowledge of the situation always ends with more casualties than 
we expect. This is where we step in. We have an idea for a small and 
cost-effective rover that can provide a live video feed of the area and can be controlled via a web server.  
We have used the IBM cloud API to store the images we have taken to train the object detection model the object detection model runs using a cloud API on the raspberry pi which also plays a vital role in disaster management and we are also using ultra sonic sensor to make the rover autonomous .Our main aim is to assess situations more accurately before we have to risk any lives.The video is lag free and can also function during pitch darkness. We are also planning to use fire-resistant material if we get our hands on it. It is powered by a power bank and can work for an hour or two independently. It’s sad to say that a rover can be replaced but a human being cannot!! If provided with proper funding, this rover 
can be a revolutionary breakthrough for emergencies.  
Parts/software being used are:  

1. Raspberry pi 3 
2. Pi cam 
3. IBM Cloud
4. Chassis for rover  
5. Motor controller 
6. Web page for rover controls with login page 
7. Developing an app for future purposes and ease in using the rover 
8. Python programming for controls 
9. Html/javascript for web page integration 
10. Vnc viewer 
11. A special module for live video feed through the camera 
12. Ultra Sonic Senosr 


STEPS:-
Step1:- connect Raspberry pi and host laptop to same hotspot or wifi network
Step2:- get the IP address of Raspberry pi, open vnc viewer and connect Raspberrypi using the IP address
Step3:- type ./gpiocreate.cgi in raspberry pi terminal
Step4:- And Open Live Video Feed File and run cam.py file and then go to your IP address in chrome/Any search Engine.
Step5:- Now, if you see on the webpage, which is hosted through our IP address and then you can control the rover using buttons present          on the webpage.
Step6:- Open IBM_CLOUD_STREAM and then run the ibmcloud.py to get live cloud-based object detection.
Step7:- Open the Autonomous_Mode folder and run ultratime.py in Raspberry pi terminal to enable autonomous mode.
Step8:- To get live video stream open the IBM_CLOUD_STREAM and open the stream video browser in terminal to get YOLOv3 object detection.

STEPS:-

