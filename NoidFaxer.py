import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

FROM = 'finesir6969@gmail.com'
PASS = 'lelelelele'

def sign_in(): #signs into finesir6969's email, returns email obj
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(FROM, PASS)
    return mail

def mime_file(file_loc):
    with open(file_loc, 'rb') as f:
        attatchment = MIMEApplication(f.read())
        file_name = f.name.split('\\')[-1]
        attatchment['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    return attatchment

def mime_text(text):
    return MIMEText(text)

def send_mail(to, text = None, file_loc = None, subject = "GOOD CONTENT"):
    mail = sign_in()
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = FROM
    msg['To'] = to
    if text is not None:
        msg.attach(mime_text(text))
    if file_loc is not None:
        msg.attach(mime_file(file_loc))
    mail.sendmail(FROM, to, msg.as_string())
    mail.close()




'''
def send_file(file_loc, to):
    mail = sign_in()
    mail.sendmail(FROM, to, mime_encode(to, file_loc, 'WIN'))
    mail.close()
'''

'''
def mime_encode(to, file_loc, text):
    msg = MIMEMultipart()
    msg['Subject'] = 'File transfer'
    msg['From'] = FROM
    msg['To'] = to
    with open(file_loc, 'rb') as f:
        attatchment = MIMEApplication(f.read())
        file_name = f.name.split('\\')[-1]
        attatchment['Content-Disposition'] = 'attachment; filename="{}"'.format(fileName)
        msg.attach(attatchment)
    msg.attach(MIMEText(text, 'text'))
    return msg.as_string()
'''
