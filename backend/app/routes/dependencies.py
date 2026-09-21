from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..core.config import settings
from ..core.database import get_db
from ..exceptions.app_exception import AppException
from ..models.user import User

security=HTTPBearer(auto_error=False)

def current_user(credentials: HTTPAuthorizationCredentials|None=Depends(security), db: Session=Depends(get_db)):
    if not credentials: raise AppException("Authentication required",401)
    try:
        payload=jwt.decode(credentials.credentials,settings.JWT_SECRET,algorithms=[settings.JWT_ALGORITHM])
        user_id=int(payload.get("sub"))
    except (JWTError,TypeError,ValueError): raise AppException("Invalid or expired token",401)
    user=db.get(User,user_id)
    if not user or user.status!="active": raise AppException("User not found or inactive",401)
    return user

def require_roles(*roles):
    def dependency(user=Depends(current_user)):
        if user.role not in roles: raise AppException("You do not have permission for this action",403)
        return user
    return dependency
