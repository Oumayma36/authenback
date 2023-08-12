from flask_mail import Mail, Message

class MailSender:
    def __init__(self, app):
        self.mail = Mail(app)

    def set_params(self, sender, recipients):
        self.sender = sender
        self.recipients = recipients

    def send(self, subject, body):
        msg = Message(subject, sender=self.sender, recipients=self.recipients)
        msg.body = body
        self.mail.send(msg)