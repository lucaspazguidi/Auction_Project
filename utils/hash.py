import bcrypt

def hash_password(password):
    password_bytes = password.encode('utf-8')                       # Passwords must be bytes
    salt = bcrypt.gensalt()                                         # Generates a salt and performs the hash
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password.decode('utf-8')                          # Save as string in the database

def verify_password(password_typed, hashed_password):
    password_bytes = password_typed.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)    # Automatically extracts the salt from the stored hash and performs the comparison