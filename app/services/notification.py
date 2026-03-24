from typing import List

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.config import notification_settings

from app.utils import TEMPLATE_DIR
from twilio.rest import Client
from twilio.http.async_http_client import AsyncHttpClient
import logging


class NotificationService:
    def __init__(self,tasks: BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(
                    exclude=["TWILIO_SID","TWILIO_AUTH_TOKEN","TWILIO_NUMBER"]
                ),
                TEMPLATE_FOLDER=TEMPLATE_DIR
            )
        )
        
        self.twilio_client = Client(
            notification_settings.TWILIO_SID,
            notification_settings.TWILIO_AUTH_TOKEN,
           
        )
    
        
    async def send_message(
        self,
        recipients:list[EmailStr],
        subject:str,
        body:str
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            MessageSchema(
                recipients= recipients,
                subject = subject,
                body= body,
                subtype =MessageType.plain
            )
        )
        
    async def send_email_with_template(
        self,
        recipients:list[EmailStr],
        subject:str,
        context:dict|None,
        template_name: str
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            MessageSchema(
                recipients= recipients,
                subject = subject,
                template_body= context,
                subtype =MessageType.html
            ),
            template_name = template_name
            
        )
        
        
   
        
    def send_sms(self, to: str, body: str):
        # This adds the task to the background and continues immediately
        # It does NOT wait for Twilio to respond, so it won't crash the API
        self.tasks.add_task(self._execute_twilio_send, to, body)

   
    
    def _execute_twilio_send(self, to: str, body: str):
        try:
            client = Client(
                notification_settings.TWILIO_SID,
                notification_settings.TWILIO_AUTH_TOKEN
            )
            client.messages.create(
                from_=notification_settings.TWILIO_NUMBER,
                to=to,
                body=body
            )
            print(f"DEBUG: SMS successfully sent to {to}")
            
        except Exception as e:
            # We use str(e) to see the message without the full HTTP dump
            print(f"TWILIO LOG: Could not send SMS to {to}. Reason: {str(e)}")