from datetime import datetime, timedelta, timezone
from jose import jwt
from pwdlib import PasswordHash
from sqlalchemy import func, select
from ..core.config import settings
from ..exceptions.app_exception import AppException
from ..models.user import User

pwd = PasswordHash.recommended()


class UserService:
    @staticmethod
    def create(db, data):
        email = str(data.email).lower()
        if db.scalar(select(User).where(func.lower(User.email) == email)):
            raise AppException("Email already exists", 409)
        if data.role not in ("admin", "employee"):
            raise AppException("Role must be admin or employee", 400)
        obj = User(
            name=data.name.strip(),
            email=email,
            password=pwd.hash(data.password),
            role=data.role,
            status="active",
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return UserService.public(obj)

    @staticmethod
    def authenticate(db, email, password):
        obj = db.scalar(select(User).where(func.lower(User.email) == email.lower()))
        if not obj or not pwd.verify(password, obj.password):
            raise AppException("Invalid email or password", 401)
        if obj.status == "inactive":
            raise AppException("Your account is inactive", 403)
        return obj

    @staticmethod
    def token(user):
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(
            {"sub": str(user.id), "exp": exp},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def public(user):
        return {
            "id": user.id,
            "_id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "status": user.status,
        }

    @staticmethod
    def get(db, id):
        obj = db.get(User, id)
        if not obj:
            raise AppException("User not found", 404)
        return obj

    @staticmethod
    def update_profile(db, user, data):
        if data.name is not None:
            if len(data.name.strip()) < 2:
                raise AppException("Name must contain at least 2 characters", 400)
            user.name = data.name.strip()
        if data.email is not None:
            email = str(data.email).lower()
            if db.scalar(
                select(User).where(func.lower(User.email) == email, User.id != user.id)
            ):
                raise AppException("Email already exists", 409)
            user.email = email
        if data.password:
            user.password = pwd.hash(data.password)
        db.commit()
        db.refresh(user)
        return UserService.public(user)

    @staticmethod
    def list(db):
        return [
            UserService.public(x)
            for x in db.scalars(select(User).order_by(User.created_at.desc())).all()
        ]

    @staticmethod
    def update(db, id, data):
        user = UserService.get(db, id)
        if data.name is not None:
            user.name = data.name.strip()
        if data.email is not None:
            user.email = str(data.email).lower()
        if data.password:
            user.password = pwd.hash(data.password)
        db.commit()
        db.refresh(user)
        return UserService.public(user)

    @staticmethod
    def status(db, id, status):
        if status not in ("active", "inactive"):
            raise AppException("Status must be active or inactive", 400)
        u = UserService.get(db, id)
        u.status = status
        db.commit()
        db.refresh(u)
        return UserService.public(u)
