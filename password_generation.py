"""
For generating passwords.
"""
import secrets
import string


def generate_password(lowercase_flag, uppercase_flag, digit_flag, symbol_flag, length) -> str:
    """
    Genrate password containing the specified characters.
    
    Arguments:
        lowercase_flag: Whether to use lowercase characters in the password or not.
        uppercase_flag: Whether to use uppercase characters in the password or not.
        digit_flag: Whether to use numbers in the password or not.
        symbol_flag: Whether to use symbols in the password or not.
    """
    symbols_used = ''
    if lowercase_flag:
        symbols_used += string.ascii_lowercase
    if uppercase_flag:
        symbols_used += string.ascii_uppercase
    if digit_flag:
        symbols_used += string.digits
    if symbol_flag:
        symbols_used += string.punctuation
    password = ''.join(secrets.choice(symbols_used) for _ in range(length))
    return password
