from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User

def register_user(id, pw, nickname):
    # 사용자 중복 확인
    if User.query.filter_by(id=id).first():
        return {"success": False, "message": "User ID already exists."}
    
    # 비밀번호 해시 처리 후 사용자 추가
    hashed_pw = generate_password_hash(pw)
    new_user = User(id=id, pw=hashed_pw, nickname=nickname)
    db.session.add(new_user)
    db.session.commit()
    return {"success": True, "message": "User registered successfully."}

def authenticate_user(id, pw):
    # 사용자 조회
    user = User.query.filter_by(id=id).first()
    if user and check_password_hash(user.pw, pw):
        return {"success": True, "message": "Login successful.", "user": user}
    return {"success": False, "message": "Invalid ID or password."}


def authenticate_user_plain(id, pw):
    """
    평문 비밀번호를 사용하여 사용자 인증 (테스트용)
    """
    # DB에서 사용자 조회
    user = User.query.filter_by(id=id).first()

    if not user:
        return {"success": False, "message": "The user does not exist."}
    
    if user.pw != pw:
        return {"success": False, "message": "The password is incorrect."}

    return {"success": True, "message": "Login successful.", "user": user}

def register_user(id, pw, nickname):
    # 사용자 중복 확인
    existing_user = User.query.filter_by(id=id).first()

    if existing_user:
        return {"success": False, "message": "User ID already exists."}
    
    # 사용자 생성
    hashed_pw = generate_password_hash(pw)
    new_user = User(id=id, pw=hashed_pw, nickname=nickname)
    db.session.add(new_user)
    db.session.commit()
    return {"success": True, "message": "User registered successfully."}