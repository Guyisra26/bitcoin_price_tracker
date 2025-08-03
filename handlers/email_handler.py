import smtplib
from email.message import EmailMessage
from models.config_schema import EmailDataConfig
from logging import Logger


class EmailSender:
    def __init__(self, config: EmailDataConfig, logger: Logger):
        self.config = config
        self.logger = logger

    def send_report(
        self, subject: str, body: str, attachment_path: str | None = None
    ) -> None:
        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = self.config.sender_email
            msg["To"] = self.config.recipient_email
            msg.set_content(body)

            if attachment_path:
                with open(attachment_path, "rb") as f:
                    file_data = f.read()
                    file_name = f.name
                    msg.add_attachment(
                        file_data, maintype="image", subtype="png", filename=file_name
                    )

            with smtplib.SMTP_SSL(self.config.smtp_host, self.config.smtp_port) as smtp:
                smtp.login(self.config.sender_email, self.config.app_password)
                smtp.send_message(msg)

            self.logger.info(
                f"Email sent to {self.config.recipient_email} with attachment {file_name}"
            )
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
