import string
import re


# --------------------------------------------------------functions
def is_valid_password(password):
    if len(password) < 8:
        return False, "Too short (min 8 chars)"
    if not any(char.isupper() for char in password):
        return False, "Missing uppercase letter"
    if not any(char.islower() for char in password):
        return False, "Missing lowercase letter"
    if not any(char.isdigit() for char in password):
        return False, "Missing digit"
    if not any(char in string.punctuation for char in password):
        return False, "Missing special character"
    
    return True, "Strong password"

def is_valid_syntax(email):
    # A standard pattern for common email formats
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(pattern, email):
        return True
    return False