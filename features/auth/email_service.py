import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # For starttls
        self.sender_email = os.getenv("EMAIL_USER")
        self.sender_password = os.getenv("EMAIL_PASS")

        if not self.sender_email or not self.sender_password:
            raise ValueError("Email credentials not found in .env file. Please set EMAIL_USER and EMAIL_PASS.")

    def send_email(self, recipient_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """
        Send an email via Gmail SMTP.

        Args:
            recipient_email: The recipient's email address.
            subject: The subject of the email.
            body: The body of the email.
            is_html: Whether the body is HTML. Default is False (plain text).

        Returns:
            True if email sent successfully, False otherwise.
        """
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject

            # Attach body
            if is_html:
                message.attach(MIMEText(body, "html"))
            else:
                message.attach(MIMEText(body, "plain"))

            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(
                    self.sender_email, recipient_email, message.as_string()
                )
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def send_welcome_email(self, recipient_email: str, username: str) -> bool:
        """
        Send a welcome email to a newly registered user.

        Args:
            recipient_email: The user's email address.
            username: The user's username.

        Returns:
            True if email sent successfully, False otherwise.
        """
        subject = "Welcome to UniQuery!"
        body = f"""
        Hello {username},

        Welcome to UniQuery! We're excited to have you on board.

        You can now log in to your account and start submitting tickets.

        Best regards,
        The UniQuery Team
        """
        return self.send_email(recipient_email, subject, body, is_html=True)

    def send_password_reset_email(self, recipient_email: str, username: str, reset_link: str) -> bool:
        """
        Send a password reset email.

        Args:
            recipient_email: The user's email address.
            username: The user's username.
            reset_link: The link to reset the password.

        Returns:
            True if email sent successfully, False otherwise.
        """
        subject = "Password Reset Request - UniQuery"
        body = f"""
        Hello {username},

        We received a request to reset your password for your UniQuery account.
        Click the link below to reset your password:

        {reset_link}

        If you did not request this, please ignore this email.

        Best regards,
        The UniQuery Team
        """
        return self.send_email(recipient_email, subject, body, is_html=True)

    def send_ticket_status_update_email(self, recipient_email: str, username: str, ticket_id: int, new_status: str) -> bool:
        """
        Send an email notification when a ticket's status changes.

        Args:
            recipient_email: The user's email address.
            username: The user's username.
            ticket_id: The ID of the ticket.
            new_status: The new status of the ticket.

        Returns:
            True if email sent successfully, False otherwise.
        """
        subject = f"Ticket #{ticket_id} Status Updated - UniQuery"
        body = f"""
        Hello {username},

        The status of your ticket #{ticket_id} has been updated to: {new_status}

        You can log in to your account to view the details.

        Best regards,
        The UniQuery Team
        """
        return self.send_email(recipient_email, subject, body, is_html=True)