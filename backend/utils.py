import os
import re
import smtplib


def send_email(subject, body, recipient):
    server = smtplib.SMTP_SSL('smtp.yandex.com', 465)

    server.login(os.environ.get('EMAIL_HOST_USER'), os.environ.get('EMAIL_HOST_PASSWORD'))

    message = f'Subject: {subject} \n\n{body}'

    server.sendmail(os.environ.get('EMAIL_HOST_USER'), recipient, message)

    print('Email has been sent!')

    server.quit()


def extract_store_name(url):
    result = re.search(r'www\.(\w+)\.', url)

    if result is not None:
        return result.group(1)

    return None