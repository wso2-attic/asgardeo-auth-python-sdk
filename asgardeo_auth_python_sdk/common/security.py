"""This module holds the security related functions to facilitate the asgardeo_auth_python_sdk."""

import string
import random

UNICODE_ASCII_CHARACTER_SET = string.ascii_letters + string.digits


def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    """
    Generate a random token.

    Args:
        length : Defaults to 30
        chars : Defaults to UNICODE_ASCII_CHARACTER_SET
    """
    rand = random.SystemRandom()
    return ''.join(rand.choice(chars) for _ in range(length))
