import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRTE")

def sign_jwt(email: str):
    payload = {
        "email": email
    }
    token = jwt.encode(payload, JWT_SECRET)
    return token

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET)

        return decoded_token if decoded_token else None
    except:
        return None
