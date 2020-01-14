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
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)