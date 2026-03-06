from models.user import User
from email_validator import validate_email, EmailNotValidError

def valid_email(email):
    try:
        v_email = validate_email(email)
        return True
    
    except EmailNotValidError:
        return False
