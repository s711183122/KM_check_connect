from flask import Flask
from flask_apscheduler import APScheduler
import os
from flask import current_app

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import atexit, requests
from datetime import datetime
from config import *
# fly scale count 1
# flyctl deploy

requests.packages.urllib3.disable_warnings()
#### init ####
BOOL_NEED_SEND_EMAIL = True
BOOL_SERVER_HAS_RETURN = True
rtxt = './receivers.txt'
#### init ####

def get_receivers():
    with open(rtxt, 'r+') as f:
        data = f.readlines()
    try:
        dtmp = []
        for i in data:
            i = i.strip()
            if i != '': dtmp.append(i)
        data = dtmp
    except:
        data = [smtp_acc]
    return data
def send_start_email():
    message = MIMEText(f'線上檢測程式 已開始運行\n目前檢測頻率為每{check_interval_second}秒一次', 'plain', 'utf-8')
    message['From'] = Header(program_name, 'utf-8')
    message['To'] =  Header(receivers_name, 'utf-8')
    
    subject = f'線上檢測程式 已開始運行'
    message['Subject'] = Header(subject, 'utf-8')
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(smtp_acc, smtp_pass)  # 登入寄件者gmail
            receivers = get_receivers()
            smtp.sendmail(sender_email, receivers, message.as_string())
            current_app.logger.info("成功傳送")
            # print("成功傳送")
        except Exception as e:
            # print("Error message: ", e)
            current_app.logger.info(f"Error message: {e}")

def send_email_error(code='', message=''):
    message = MIMEText(f'{error_text}\n\n伺服器無法連線(code={code})\nERROR MESSAGE:\n{message}', 'plain', 'utf-8')
    message['From'] = Header(program_name, 'utf-8')
    message['To'] =  Header(receivers_name, 'utf-8')
    
    subject = f'伺服器無法連線 ({code}) {server_url}'
    message['Subject'] = Header(subject, 'utf-8')
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(smtp_acc, smtp_pass)  # 登入寄件者gmail
            receivers = get_receivers()
            smtp.sendmail(sender_email, receivers, message.as_string())
            # print("成功傳送")
            current_app.logger.info("成功傳送")
        except Exception as e:
            # print("Error message: ", e)
            current_app.logger.info(f"Error message: {e}")
def send_email_close():
    current_app.logger.info(close_text)
    message = MIMEText(close_text, 'plain', 'utf-8')
    message['From'] = Header(program_name, 'utf-8')
    message['To'] =  Header(receivers_name, 'utf-8')
    
    subject = '線上檢測程式已關閉'
    message['Subject'] = Header(subject, 'utf-8')
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(smtp_acc, smtp_pass)  # 登入寄件者gmail
            receivers = [sender_email]
            smtp.sendmail(sender_email, receivers, message.as_string())
            # print("成功傳送")
            current_app.logger.info("成功傳送")
        except Exception as e:
            # print("Error message: ", e)
            current_app.logger.info(f"Error message: {e}")
def do_exit():
    with app.app_context():
        send_email_close()
def send_email_server_is_ok():
    
    current_app.logger.info(re_connect_text)
    # print(text)
    message = MIMEText(re_connect_text, 'plain', 'utf-8')
    message['From'] = Header(program_name, 'utf-8')
    message['To'] =  Header(receivers_name, 'utf-8')
    subject = '伺服器已重新上線'
    message['Subject'] = Header(subject, 'utf-8')
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(smtp_acc, smtp_pass)  # 登入寄件者gmail
            receivers = get_receivers()
            smtp.sendmail(sender_email, receivers, message.as_string())
            # print("成功傳送")
            current_app.logger.info("成功傳送")
        except Exception as e:
            # print("Error message: ", e)
            current_app.logger.info(f"Error message: {e}")
def send_email_alive():
    current_app.logger.info(check_alive_text)
    message = MIMEText(check_alive_text, 'plain', 'utf-8')
    message['From'] = Header(program_name, 'utf-8')
    message['To'] =  Header(receivers_name, 'utf-8')
    subject = '線上檢測程式在線測試'
    message['Subject'] = Header(subject, 'utf-8')
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(smtp_acc, smtp_pass)  # 登入寄件者gmail
            receivers = [sender_email]
            smtp.sendmail(sender_email, receivers, message.as_string())
            # print("成功傳送")
            current_app.logger.info("成功傳送")
        except Exception as e:
            # print("Error message: ", e)
            current_app.logger.info(f"Error message: {e}")

def check_server():
    global BOOL_NEED_SEND_EMAIL, BOOL_SERVER_HAS_RETURN
    nt = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    text = 'check_server'
    try:
        r = requests.get(server_url, verify=False, timeout=5)
        current_app.logger.info(f'Request code = {r.status_code}')
        if str(r.status_code) not in ['200', '201']:
            text = f'{nt} 檢查失敗 code={r.status_code}'
            current_app.logger.info(text)
            BOOL_SERVER_HAS_RETURN = False
            if BOOL_NEED_SEND_EMAIL:
                send_email_error(code=r.status_code, message=text)
                BOOL_NEED_SEND_EMAIL = False
        else:
            text = f'{nt} 檢查成功'
            current_app.logger.info(text)
            BOOL_NEED_SEND_EMAIL = True
            if not BOOL_SERVER_HAS_RETURN:
                send_email_server_is_ok()
                BOOL_SERVER_HAS_RETURN = True
    except Exception as e:
        text = f'{nt} 檢查失敗 code=無法連線'
        # print(text)
        current_app.logger.error(str(e))
        current_app.logger.info(text)
        BOOL_SERVER_HAS_RETURN = False
        if BOOL_NEED_SEND_EMAIL:
            send_email_error(code='無法連線', message=f'{text}\n{e}')
            BOOL_NEED_SEND_EMAIL = False
    return text

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

with app.app_context():
    current_app.logger.info(f'開始執行線上檢測程式 每{check_interval_second}秒檢查一次')
    send_start_email()
    check_server()

@app.route("/")
def main():
    with app.app_context():
        t = check_server()
    return t

@scheduler.task('interval', id='do_job_1', seconds=check_interval_second, misfire_grace_time=300, max_instances=10)
def run():
    with app.app_context():
        check_server()
@scheduler.task('cron', id='do_job_2', day=check_server_alive_para['day'], hour=check_server_alive_para['hour'], minute=check_server_alive_para['minute'], second=check_server_alive_para['second'], max_instances=10)
def check_alive():
    with app.app_context():
        send_email_alive()

if __name__ == '__main__':
    atexit.register(do_exit)
    app.run(
        port=int(os.environ.get("PORT", 8080)),
        host="0.0.0.0",
    )
    