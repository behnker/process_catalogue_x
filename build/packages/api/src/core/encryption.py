"""Encryption utilities for sensitive data (API keys, tokens, etc.)."""

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from src.config import settings


def _get_fernet_key() -> bytes:
    """
    Get or derive a Fernet key from settings.

    If ENCRYPTION_KEY is not set, derives one from SECRET_KEY.
    For production, always set a dedicated ENCRYPTION_KEY.
    """
    if settings.ENCRYPTION_KEY:
        key = settings.ENCRYPTION_KEY.encode()
        # If it's not a valid Fernet key, derive one
        if len(key) != 44:  # Fernet keys are 44 chars base64-encoded
            key = base64.urlsafe_b64encode(
                hashlib.sha256(key).digest()
            )
        return key
    else:
        # Derive from SECRET_KEY (fallback for development)
        return base64.urlsafe_b64encode(
            hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        )


def encrypt_sensitive_data(plaintext: str) -> str:
    """
    Encrypt sensitive data using Fernet symmetric encryption.

    Args:
        plaintext: The sensitive string to encrypt

    Returns:
        Base64-encoded encrypted string
    """
    if not plaintext:
        return ""

    fernet = Fernet(_get_fernet_key())
    encrypted = fernet.encrypt(plaintext.encode())
    return encrypted.decode()


def decrypt_sensitive_data(ciphertext: str) -> str:
    """
    Decrypt sensitive data that was encrypted with encrypt_sensitive_data().

    Args:
        ciphertext: The encrypted string

    Returns:
        Decrypted plaintext string

    Raises:
        ValueError: If decryption fails (invalid key or corrupted data)
    """
    if not ciphertext:
        return ""

    try:
        fernet = Fernet(_get_fernet_key())
        decrypted = fernet.decrypt(ciphertext.encode())
        return decrypted.decode()
    except InvalidToken:
        raise ValueError("Failed to decrypt data - invalid key or corrupted ciphertext")


def generate_encryption_key() -> str:
    """
    Generate a new Fernet encryption key.

    Use this to generate a key for the ENCRYPTION_KEY setting.
    Run: python -c "from src.core.encryption import generate_encryption_key; print(generate_encryption_key())"
    """
    return Fernet.generate_key().decode()
