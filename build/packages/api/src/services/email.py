"""
Email service for sending magic links and notifications.

Supports multiple providers:
- resend: Resend.com (production)
- console: Print to console (development)

Blueprint §6.2.4: Magic link delivery via email.
"""

import logging
from abc import ABC, abstractmethod

import resend

from src.config import settings

logger = logging.getLogger(__name__)


class EmailProvider(ABC):
    """Abstract base for email providers."""

    @abstractmethod
    async def send_magic_link(self, to_email: str, magic_link_url: str) -> bool:
        """Send a magic link email. Returns True on success."""
        pass

    @abstractmethod
    async def send_notification(
        self, to_email: str, subject: str, body_html: str
    ) -> bool:
        """Send a notification email. Returns True on success."""
        pass


class ConsoleEmailProvider(EmailProvider):
    """Development provider that prints to console."""

    async def send_magic_link(self, to_email: str, magic_link_url: str) -> bool:
        logger.info(f"\n{'='*60}")
        logger.info(f"MAGIC LINK EMAIL")
        logger.info(f"To: {to_email}")
        logger.info(f"Link: {magic_link_url}")
        logger.info(f"{'='*60}\n")
        print(f"\n[Magic Link] {to_email}: {magic_link_url}\n")
        return True

    async def send_notification(
        self, to_email: str, subject: str, body_html: str
    ) -> bool:
        logger.info(f"[Console Email] To: {to_email}, Subject: {subject}")
        print(f"\n[Notification] {to_email}: {subject}\n")
        return True


class ResendEmailProvider(EmailProvider):
    """Production provider using Resend.com."""

    def __init__(self, api_key: str, from_email: str):
        self.from_email = from_email
        resend.api_key = api_key

    async def send_magic_link(self, to_email: str, magic_link_url: str) -> bool:
        """Send magic link via Resend."""
        try:
            params = {
                "from": self.from_email,
                "to": [to_email],
                "subject": "Sign in to Process Catalogue",
                "html": self._magic_link_template(magic_link_url),
            }
            response = resend.Emails.send(params)
            logger.info(f"Magic link sent to {to_email}, id: {response.get('id')}")
            return True
        except Exception as e:
            logger.error(f"Failed to send magic link to {to_email}: {e}")
            return False

    async def send_notification(
        self, to_email: str, subject: str, body_html: str
    ) -> bool:
        """Send notification via Resend."""
        try:
            params = {
                "from": self.from_email,
                "to": [to_email],
                "subject": subject,
                "html": body_html,
            }
            response = resend.Emails.send(params)
            logger.info(f"Notification sent to {to_email}, id: {response.get('id')}")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification to {to_email}: {e}")
            return False

    def _magic_link_template(self, magic_link_url: str) -> str:
        """HTML template for magic link emails."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
             margin: 0; padding: 40px 20px; background-color: #f5f5f5;">
    <div style="max-width: 480px; margin: 0 auto; background: white;
                border-radius: 8px; padding: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h1 style="color: #000; font-size: 24px; margin: 0 0 24px 0;">
            Sign in to Process Catalogue
        </h1>
        <p style="color: #333; font-size: 16px; line-height: 1.5; margin: 0 0 24px 0;">
            Click the button below to securely sign in. This link expires in 15 minutes.
        </p>
        <a href="{magic_link_url}"
           style="display: inline-block; background-color: #FBB03B; color: #000;
                  text-decoration: none; padding: 14px 28px; border-radius: 6px;
                  font-weight: 600; font-size: 16px;">
            Sign In
        </a>
        <p style="color: #666; font-size: 14px; line-height: 1.5; margin: 24px 0 0 0;">
            If you didn't request this email, you can safely ignore it.
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 32px 0;">
        <p style="color: #999; font-size: 12px; margin: 0;">
            Process Catalogue — Operating Model Design Platform
        </p>
    </div>
</body>
</html>
"""


def get_email_provider() -> EmailProvider:
    """Factory function to get the configured email provider."""
    if settings.EMAIL_PROVIDER == "resend" and settings.RESEND_API_KEY:
        return ResendEmailProvider(
            api_key=settings.RESEND_API_KEY,
            from_email=settings.EMAIL_FROM,
        )
    else:
        return ConsoleEmailProvider()


# Global instance
email_provider = get_email_provider()


async def send_magic_link_email(to_email: str, magic_link_url: str) -> bool:
    """Convenience function to send a magic link email."""
    return await email_provider.send_magic_link(to_email, magic_link_url)


async def send_notification_email(
    to_email: str, subject: str, body_html: str
) -> bool:
    """Convenience function to send a notification email."""
    return await email_provider.send_notification(to_email, subject, body_html)
