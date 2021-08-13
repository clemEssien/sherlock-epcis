from flask.json import load
from flask_mail import Message
from FlaskAPI.init_mail import mail
from dotenv import load_dotenv
from typing import List
import os, sys
load_dotenv()


class MailConnector():

    def __init__(self) -> None:
        self._mail = mail

    @property
    def mail(self) -> object:
        return self._mail

    def send(self, subject: str, recipients: List[str], body: str):
        msg = Message()
        msg.subject = subject
        msg.recipients = recipients
        msg.sender = os.getenv('MAIL_USERNAME')
        msg.body = body

        self._mail.send(msg)

    