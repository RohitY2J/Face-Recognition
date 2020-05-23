import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

ImgFileName = "./photos/kiran.jpg"

img_data = open(ImgFileName, 'rb').read()
msg = MIMEMultipart()
msg['Subject'] = 'subject'
msg['From'] = 'rohitkauri20@gmail.com'
From = 'rohitkauri20@gmail.com'
msg['To'] = 'rohitkauri13@gmail.com'
To = 'rohitkauri13@gmail.com'
UserName = "Rohit"
UserPassword = '9843833224'
Port = '587'
Server = 'smtp.gmail.com'
text = MIMEText("test")
msg.attach(text)
image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
msg.attach(image)
s = smtplib.SMTP(Server, Port)
s.ehlo()
s.starttls()
s.ehlo()
s.login(From, UserPassword)
s.sendmail(From, To, msg.as_string())
s.quit()
