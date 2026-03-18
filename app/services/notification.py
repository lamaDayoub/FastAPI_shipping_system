from typing import List

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.config import notification_settings
from app.services.base import BaseService


class NotificationService:
    def __init__(self,tasks: BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump()
            )
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
        