from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from backend.database import get_db
from backend.models.user import User
from backend.auth.security import get_password_hash, verify_password
from backend.auth.jwt import create_access_token
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    codeforces_handle: Optional[str] = None
    leetcode_handle: Optional[str] = None
    codechef_handle: Optional[str] = None
    atcoder_handle: Optional[str] = None

class UserLoginRequest(BaseModel):
    username_or_email: str
    password: str

class UpdateHandlesRequest(BaseModel):
    codeforces_handle: Optional[str] = None
    leetcode_handle: Optional[str] = None
    codechef_handle: Optional[str] = None
    atcoder_handle: Optional[str] = None
    target_rating: Optional[int] = None

@router.post("/register")
async def register(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check if username or email exists
    result = await db.execute(
        select(User).where(or_(User.username == req.username, User.email == req.email))
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    new_user = User(
        username=req.username.strip(),
        email=req.email.strip().lower(),
        hashed_password=get_password_hash(req.password),
        codeforces_handle=req.codeforces_handle.strip() if req.codeforces_handle else None,
        leetcode_handle=req.leetcode_handle.strip() if req.leetcode_handle else None,
        codechef_handle=req.codechef_handle.strip() if req.codechef_handle else None,
        atcoder_handle=req.atcoder_handle.strip() if req.atcoder_handle else None,
        user_overall_elo=1300,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id), "username": new_user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "codeforces_handle": new_user.codeforces_handle,
            "leetcode_handle": new_user.leetcode_handle,
            "codechef_handle": new_user.codechef_handle,
            "atcoder_handle": new_user.atcoder_handle,
        }
    }

@router.post("/login")
async def login(req: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    identifier = req.username_or_email.strip()
    result = await db.execute(
        select(User).where(or_(User.username == identifier, User.email == identifier.lower()))
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )

    token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "codeforces_handle": user.codeforces_handle,
            "leetcode_handle": user.leetcode_handle,
            "codechef_handle": user.codechef_handle,
            "atcoder_handle": user.atcoder_handle,
            "overall_elo": user.user_overall_elo,
        }
    }

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "codeforces_handle": current_user.codeforces_handle,
        "leetcode_handle": current_user.leetcode_handle,
        "codechef_handle": current_user.codechef_handle,
        "atcoder_handle": current_user.atcoder_handle,
        "overall_elo": current_user.user_overall_elo,
        "target_rating": current_user.target_rating,
    }

@router.put("/handles")
async def update_handles(
    req: UpdateHandlesRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if req.codeforces_handle is not None:
        current_user.codeforces_handle = req.codeforces_handle.strip() or None
    if req.leetcode_handle is not None:
        current_user.leetcode_handle = req.leetcode_handle.strip() or None
    if req.codechef_handle is not None:
        current_user.codechef_handle = req.codechef_handle.strip() or None
    if req.atcoder_handle is not None:
        current_user.atcoder_handle = req.atcoder_handle.strip() or None
    if req.target_rating is not None:
        current_user.target_rating = req.target_rating

    await db.commit()
    await db.refresh(current_user)
    return {
        "status": "success",
        "message": "Platform handles updated successfully",
        "handles": {
            "codeforces": current_user.codeforces_handle,
            "leetcode": current_user.leetcode_handle,
            "codechef": current_user.codechef_handle,
            "atcoder": current_user.atcoder_handle,
        }
    }
