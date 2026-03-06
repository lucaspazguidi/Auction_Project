from models.user import User


def validate_username(name):
    user = User.query.filter_by(name=name).first()
    
    if user:
        return False
    else:
        return True