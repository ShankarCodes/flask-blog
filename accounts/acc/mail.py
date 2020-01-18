import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendmail(fr,to,sub,cnt):
    message = Mail(
        from_email=fr,
        to_emails=to,
        subject=sub,
        html_content=cnt)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)