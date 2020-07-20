import telepot
from telepot.loop import MessageLoop
from time import sleep
import reseving_mails_test
import cv2
import time
import datetime
import os
import sound
import full_body_detec
import mail
import PHOTO
import VIDEO
import pir
import temp
import full_body_detec_time
import mail
import threading

commands = ['']
def handle(msg):
    
    PASSword = "654321"
    tryes = 0
    global ALART
    global telegramText
    global chat_id
    # Receiving the message from telegram
    chat_id = msg['chat']['id']
    # Getting text from the message
    telegramText = msg['text']
    print('Message received from ' + str(chat_id))
    if True:
        commands.append(telegramText)
        
        # Comparing the incoming message to send a reply according to it
        print(telegramText)
        if telegramText == '/help':
            bot.sendMessage(chat_id, 'I see you need some help:')
            bot.sendMessage(chat_id, '/pic :its for taking an imidiate photo.')
            bot.sendMessage(chat_id, '/hi : if youre lonly.')
            bot.sendMessage(chat_id, '/time :who needs a watch.')
            bot.sendMessage(chat_id, '/stop :shut-down.')
            bot.sendMessage(chat_id, '/alarm :makes a sound.')
            bot.sendMessage(chat_id, '/readmail :will read your last mail.')
            bot.sendMessage(chat_id, '/vid : will take a short video (MAX 15sec).')
            bot.sendMessage(chat_id, '/enB : will enable the body detection in your house, If i will see a intruder i will send you a notification by email.')
            bot.sendMessage(chat_id, '/enBT : will enable the body detection in your house FOR SHORT TIME, If i will see a intruder i will send you a notification by email.')
            bot.sendMessage(chat_id, '/pass:XXXXXX : enter your special password for diss-arm BUT its a SUB-FUNC of /enB.')
            bot.sendMessage(chat_id, 'And many others soon!')
            
        elif telegramText == '/start':
            bot.sendMessage(chat_id, 'Welcome to my python-project!!')
            bot.sendMessage(chat_id, 'IF you want to check the commands just write down :    /help')
            
        elif telegramText == '/hi':
            bot.sendMessage(chat_id, str("Hi! How can i help?"))
            
        elif telegramText == '/time':
            bot.sendMessage(chat_id, str(datetime.datetime.now()))
            
        elif telegramText == '/stop':
            bot.sendMessage(chat_id, str("Total shutdown!"))
            #os.system("shutdown -h now")
            
        elif telegramText == '/alarm':
            bot.sendMessage(chat_id, str("the alarm is working now"))
            sound.soundd()
            
        
        elif telegramText == '/readmail':
            if reseving_mails_test.reseving_mail():
                bot.sendMessage(chat_id, str("Your last email is from: "+temp.FROM))
                bot.sendMessage(chat_id, str("The subject is :" +temp.SUB))
                bot.sendMessage(chat_id, str("The body of the email is: "+temp.BODY))
            
        elif telegramText == '/pic':
            PHOTO.Photo_()
            bot.sendPhoto(chat_id, photo=open('img.jpg', 'rb'))
            
        elif telegramText == '/enBT':
            bot.sendMessage(chat_id, str("Its on!"))
            if pir.motion_check(pir.pirpin):
                bot.sendMessage(chat_id, str("The motion detector detected something, Checking it"))
                if full_body_detec_time.body_detec():
                    bot.sendMessage(chat_id, str("I saw some-one!! see it your self"))
                    bot.sendPhoto(chat_id, photo=open('intruder.jpg', 'rb'))
                    bot.sendVideo(chat_id = chat_id,video = open('output2.mp4',mode ='rb'))
                else:
                    bot.sendMessage(chat_id, str("I saw nothing, But you can check the video your self"))
                    bot.sendVideo(chat_id = chat_id,video = open('output2.mp4',mode ='rb'))
                    
        elif telegramText == '/enB':
            bot.sendMessage(chat_id, str("Its on, Youre safe!"))
            if pir.motion_check(pir.pirpin):
                bot.sendMessage(chat_id, str("The motion detector detected something, Checking it"))
                if full_body_detec.body_detec():
                    ALART = time.time()
                    mail.mail_sender()
                    bot.sendMessage(chat_id, str("The photo has been sent to the mail"))
                    bot.sendPhoto(chat_id, photo=open('intruder.jpg', 'rb'))
                    bot.sendMessage(chat_id, str("Waiting for password for 5min "))
                    
                    
        elif telegramText == '/vid':
            bot.sendMessage(chat_id, str("What length do you want your video to be?max is 15 sec"))
            #VIDEO.VIDEO_()
            #bot.sendVideo(chat_id = chat_id,video = open('output.mp4',mode ='rb'))
            
        elif telegramText.isdigit():
            if commands.pop() == '/vid':
                num = telegramText
                print(num)
                if ((int(num) >= 1) and (int(num) <= 15)):
                    capture_duration = int(num)
                    VIDEO.VIDEO_(capture_duration)
                    bot.sendVideo(chat_id = chat_id,video = open('output.mp4',mode ='rb'))
                else:
                    bot.sendMessage(chat_id, str("Try again!max is 15sec and the minimum is 1sec"))
        
        else:
            if telegramText[:5] == '/pass':
                print(telegramText[:5])
                pass
            else:
                bot.sendMessage(chat_id, 'Sorry, I dont Understand what youre asking for. try again ! ')
        
        
        if int(ALART) <= int(ALART)+500 and telegramText == "/pass:"+PASSword:    
            PHOTO.Photo_()
            bot.sendPhoto(chat_id, photo=open('img.jpg', 'rb'))
            bot.sendMessage(chat_id, str("OK"))
        
        else:
            tryes +=1
            bot.sendMessage(chat_id, str("Try again!"))
            if tryes == 3:
                sound.soundd()
            
            

print('Listening....')
# Connect to our bot
bot =telepot.Bot('')  
# print(bot.getMe())
# Start listening to the telegram bot and whenever a message is received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
#full_body_detec.body_detec()
