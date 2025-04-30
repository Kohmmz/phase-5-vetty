from flask_jwt_extended import create_access_token, create_refresh_token

def generate_jwt_token(user):
    access_token = create_access_token(identity={"id": user.id, "role": user.role})
    refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role})
    return access_token, refresh_token