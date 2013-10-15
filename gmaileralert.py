#!/usr/bin/python

import smtplib

def blue_alert(msg):
    sender = 'email@gmail.com'
    receivers = ['email@mac.com']

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("email@gmail.com","password")
        server.sendmail(sender, receivers, msg)         
        print "Successfully sent email"
    except SMTPException:
        print "Error: unable to send email"
        
if __name__ == "__main__":
    mymsg = "From: Me <email@gmail.com>\nTo: You <email@mac.com>\nSubject: Sensor Error \nThere is a problem with the temperture sensor."
    blue_alert(mymsg)
