from bookb.celery import app

@app.task
def send_email():
    """
        param:subject: subject of the mail
        param:html_content: formatted html content
        param:recipients: list of recipients
    """

    print('Testing ')