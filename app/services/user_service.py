from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User

def check_user_exists(id):
    return User.query.get(id)

def authenticate_user(id, pw):
    user = check_user_exists(id)

    # id 일치 확인
    if not user:
        return {"success": False, "message": "The user does not exist."}
    # pw 일치 확인
    elif not check_password_hash(user.pw, pw):
        return {"success": False, "message": "The password is incorrect."}

    # 로그인 성공
    return {"success": True, "message": "Login successful.", "user": user}

def id_available(id):
    # id 존재 확인
    if check_user_exists(id):
        return {"success": False, "message": "This ID already exists."}

    # 사용가능한 ID
    return {"success": True, "message": "This ID is available."}

def register_user(id, pw, nickname):
    result = id_available(id)

    # 이미 존재하는 ID
    if not result["success"]:
        return result
    
    # 해시 암호화
    hashed_pw = generate_password_hash(pw)
    # 사용자 생성
    user = User(id=id, pw=hashed_pw, nickname=nickname)

    # DB 업데이트
    db.session.add(user)
    db.session.commit()

    return {"success": True, "message": "User registered successfully."}