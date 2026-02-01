"""
Email service with Resend integration.

Supports multiple providers via EMAIL_PROVIDER config:
- resend: Production email via Resend API
- console: Development — prints to console
"""

from typing import Protocol

import resend

from src.config import settings


class EmailProvider(Protocol):
    """Protocol for email providers."""

    async def send(
        self,
        to: str,
        subject: str,
        html: str,
        text: str | None = None,
    ) -> bool:
        """Send an email. Returns True if successful."""
        ...


class ResendProvider:
    """Resend API email provider."""

    def __init__(self, api_key: str, from_email: str):
        self.from_email = from_email
        resend.api_key = api_key

    async def send(
        self,
        to: str,
        subject: str,
        html: str,
        text: str | None = None,
    ) -> bool:
        try:
            params: resend.Emails.SendParams = {
                "from": self.from_email,
                "to": [to],
                "subject": subject,
                "html": html,
            }
            if text:
                params["text"] = text
            resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"[Resend] Failed to send email to {to}: {e}")
            return False


class ConsoleProvider:
    """Development provider — prints to console."""

    def __init__(self, from_email: str):
        self.from_email = from_email

    async def send(
        self,
        to: str,
        subject: str,
        html: str,
        text: str | None = None,
    ) -> bool:
        print("\n" + "=" * 60)
        print(f"[EMAIL] From: {self.from_email}")
        print(f"[EMAIL] To: {to}")
        print(f"[EMAIL] Subject: {subject}")
        print("-" * 60)
        print(text or html)
        print("=" * 60 + "\n")
        return True


def get_email_provider() -> EmailProvider:
    """Factory to get configured email provider."""
    if settings.EMAIL_PROVIDER == "resend":
        if not settings.RESEND_API_KEY:
            raise ValueError("RESEND_API_KEY required when EMAIL_PROVIDER=resend")
        return ResendProvider(settings.RESEND_API_KEY, settings.EMAIL_FROM)
    return ConsoleProvider(settings.EMAIL_FROM)


# Singleton instance
_email_provider: EmailProvider | None = None


def get_email() -> EmailProvider:
    """Get the singleton email provider instance."""
    global _email_provider
    if _email_provider is None:
        _email_provider = get_email_provider()
    return _email_provider


# ── Magic Link Email Templates ────────────────────────


def build_magic_link_email(magic_link: str, expires_minutes: int = 15) -> tuple[str, str]:
    """
    Build magic link email content.
    Returns (html, text) tuple.
    """
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px; background-color: #f5f5f5;">
    <div style="background-color: #ffffff; border-radius: 8px; padding: 40px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h1 style="color: #000000; font-size: 24px; margin-bottom: 24px;">Sign in to Process Catalogue</h1>
        <p style="color: #333333; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
            Click the button below to sign in. This link expires in {expires_minutes} minutes.
        </p>
        <a href="{magic_link}"
           style="display: inline-block; background-color: #FBB03B; color: #000000; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-weight: 600; font-size: 16px;">
            Sign In
        </a>
        <p style="color: #666666; font-size: 14px; margin-top: 32px; line-height: 1.5;">
            If you didn't request this email, you can safely ignore it.
        </p>
        <hr style="border: none; border-top: 1px solid #eeeeee; margin: 32px 0;">
        <p style="color: #999999; font-size: 12px;">
            If the button doesn't work, copy and paste this link:<br>
            <a href="{magic_link}" style="color: #FBB03B; word-break: break-all;">{magic_link}</a>
        </p>
    </div>
</body>
</html>
"""

    text = f"""Sign in to Process Catalogue

Click this link to sign in (expires in {expires_minutes} minutes):
{magic_link}

If you didn't request this email, you can safely ignore it.
"""

    return html, text


async def send_magic_link_email(to: str, magic_link: str) -> bool:
    """Send a magic link email to the specified address."""
    html, text = build_magic_link_email(
        magic_link, settings.MAGIC_LINK_EXPIRY_MINUTES
    )
    email = get_email()
    return await email.send(
        to=to,
        subject="Sign in to Process Catalogue",
        html=html,
        text=text,
    )
