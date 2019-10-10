#!/usr/bin/env python3
# coding=utf-8
from email.mime.text import MIMEText
from email.utils import formatdate  
from email.header import Header  
from email.mime.multipart import MIMEMultipart

import smtplib
import sys

def send_mail(result):
    default_encoding = 'utf-8'  
    if sys.getdefaultencoding() != default_encoding:  
        reload(sys)  
        sys.setdefaultencoding(default_encoding)
    
    #发送邮件的相关信息，根据你实际情况填写  
    smtpHost = 'smtp.sohu.com'  
    smtpPort = '25'  
    fromMail = 'from@sohu.com'
    toMail   = 'to@sohu.com'
    username = 'shadowsock5'
    password = ''
    
    subject = u'[Wiki敏感信息] 扫描结果'
    #from getpass import getpass
    #password = getpass()
    #password = 'password'
    print('[*] sending mail')
    print(len(result))
    msg = []
    body = ''  # 邮件正文
    data = ''  # 邮件附件内容
    if len(result) > 0:
        for i in result:
            title = i.title
            url = i.url
            excerpt = i.details
            msg.append({'url': url, 'title': title, 'excerpt': excerpt})
        body =  '本次扫描已结束，扫描人: {0}。敏感信息共：{1}条。 <br><br>'.format(fromMail, str(len(result))) 
        base_url = "http://192.168.170.1:8090"
        for i in msg:
            data = data +  '- <a href="{0}">{1}</a>'.format( base_url + i['url'], i['title']) + '<br>' + i['excerpt'] + '<br><br>'
    # print msg   
    else:
        print('长度为0')
    
    #初始化邮件  
    encoding = 'utf-8'
    mail = MIMEMultipart()
    body      = MIMEText(body.encode(encoding),'html', encoding)  # 正文
    mail_data = MIMEText(data.encode(encoding),'html', encoding)  # 附件
    #mail_data.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', u'wiki敏感信息详情.html'.encode('utf-8')) )
    mail['Subject'] = Header(subject,encoding)  
    mail['From'] = fromMail  
    mail['To'] = toMail
    mail['Date'] = formatdate()
    mail.attach(body)
    mail.attach(mail_data)
      
    try:  
       
        #tls加密方式，通信过程加密，邮件数据安全，使用正常的smtp端口  
        smtp = smtplib.SMTP(smtpHost,smtpPort)  
        #smtp.set_debuglevel(True)  
        smtp.ehlo()  
        smtp.starttls()  
        smtp.ehlo()  
        smtp.login(username,password)  
        
        #发送邮件  
        smtp.sendmail(fromMail,toMail,mail.as_string())  
        smtp.close()  
        print('[*] mail sent!')
    except Exception as e:
        print('[-]error!')
        raise e  
