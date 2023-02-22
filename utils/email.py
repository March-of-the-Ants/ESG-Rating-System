import pandas as pd
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from config import Config
from email.mime.image import MIMEImage

def send_report(sender='yha528@naver.com', receiver='yha528@naver.com', file='대시보드'):
    SMTP_SERVER = 'smtp.naver.com'
    SMTP_PORT = 465
    SMTP_USER = sender
    c = Config()
    SMTP_PASSWORD = c.ACCOUNT['email']
    try:
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        print('서버접속 성공')
        smtp.login(sender, SMTP_PASSWORD)
        print('로그인 성공')
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        date_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y년 %m월 %d일')
        msg['Subject'] = f'ESG 평가 보고서 ({date_str})' 
        
        predict = pd.read_excel('predict.xlsx')
        today = int(datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d'))    
        if predict.TotalGrade[predict.Email == today].values[-1] == 'D':
            contents = "귀사의 ESG 평가 결과, 환경/사회/지배구조 측면의 경영활동 계획 및 이행실적과 리스크 대응능력 등이 [ 양호 ]한 수준입니다. <br> 아래는 ESG 평가 보고서 입니다. <br>"
            static = os.getcwd()
            img_path = [os.path.join(static, i) for i in os.listdir(static) if re.search(file, i) ]
            with open(img_path[-1], 'rb') as img_file:
                mime_img = MIMEImage(img_file.read())
                msg.attach(mime_img)   
                image_for_body = f'<img src="cid:img_cid">'
                mime_img.add_header('Content-ID', '<' + 'img_cid' + '>')
                contents += image_for_body
                contents = MIMEText(contents, 'html')
                msg.attach(contents)        
            smtp.sendmail(sender, receiver, msg.as_string())
            print('전송 성공')
    except Exception as e:
        print('에러')
        print(e)
    finally:
        smtp.close()
        print('창닫기')
