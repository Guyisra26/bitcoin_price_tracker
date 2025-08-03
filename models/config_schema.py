from pydantic import BaseModel, EmailStr, HttpUrl, Field


class CoreDataConfig(BaseModel):
    base_url: HttpUrl
    base: str = Field(..., min_length=3)
    currency: str = Field(..., min_length=3)
    run_minutes: int = Field(..., gt=0)
    interval_seconds: int = Field(..., gt=0)


class EmailDataConfig(BaseModel):
    sender_email: EmailStr
    app_password: str
    recipient_email: EmailStr
    subject: str
    smtp_host: str
    smtp_port: int


class AppConfig(BaseModel):
    core_config: CoreDataConfig
    email_config: EmailDataConfig
