#not using any of the mime libraries just because I'm bored and I wanna know how the mime encoding stuff actually works (yeah I know thats a terrible reason)

import smtplib
import base64 as b64

FROM = 'finesir6969@gmail.com'   #gmail address to send from
PASSWD = 'lelelelele' #password for gmail account


def signIn(): #signs into finesir6969's email, returns email obj
    print('Signing in...')
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(FROM,PASSWD)
    return mail

def insert(string, substr, spacing): #inserts substr in string every spacing
    return substr.join(
            [
                string[i: i+spacing]
                for i in range(0, len(string), spacing)
            ]
        )

def b64encode(s):
    return str(b64.encodestring(s), 'ascii')

def mimeEncode(data):
    headers = '''Content-Type: multipart/mixed; boundary="===============6969696969=="
MIME-Version: 1.0
Subject: WINNING
From: <''' + FROM + '''>

--===============6969696969==
Content-Type: application/octet-stream
MIME-Version: 1.0
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="win.jpeg"

'''
    return headers + b64encode(data) + '--===============6969696969==--\n' #base 64 encode the data, add final boundary
    

def sendImgData(data, to): #sends data to specified address
    mail = signIn()
    mail.sendmail(FROM, to, mimeEncode(data))
    mail.close()

def sendFile(fileLoc, to): #sends the file at fileLoc to specified address
    f = open(fileLoc, 'rb')
    data = f.read()
    f.close()
    sendImgData(data, to)
