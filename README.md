# groupme-app

## AWS EC2 Flask web app
Groupme provides a simple API to get data from groups on your account

This simple app shows the number of messages for my group 'Large Fry Larrys' and I have plans to add graphs and keep everything LIVE.

## Some Helpful hints for future me
I chose to use an Ubuntu 18.04 server in AWS and host this project in Github

Server disconnects after disconnecting ssh, solved by running linux screen program (keeps things going)

## Installation
To install this application to an AWS or other linux server (raspberry pi?), go into the server via ssh, and run
'''
git clone [the-address-to-the-github]
'''
This will create a folder called groupme-app, which you then can cd into
'''
cd groupme-app
'''
Now you should be in the app folder. Install groupyAPI with pip or pip3
'''
pip3 install GroupyAPI
'''
(eventually use the requirements.txt)

Now to run the server, (screen is a hack to keep the server running after disconnecting the ssh)
'''
screen
sudo python3 main.py
'''

It will say 'running on '0.0.0.0:80' or something similar, which is the local address. To access the website,
find the IPV4 address (on AWS its in the instance description).
