from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import jwt
import requests
from .database import User
from pydantic import BaseModel
from typing import List, Optional


from .entities import FollowerOperation


GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    verified: bool
    first_name: str
    last_name: str
    picture: str
    sso_id: str
    followers: Optional[List[str]] = None  # Allow None as a valid value
    
    
@app.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@app.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    
    #create user profile 
    user = await User.create_or_update_user(user_info.json())
    
    access_token = str(jwt.encode({"user_id": user}, JWT_SECRET_KEY, algorithm="HS256"))
    
    frontend_redirect_url = f"http://localhost:3000/token/?token={access_token}&user={user_info.json()}"

    # Redirect the user back to the frontend URL with the access token
    return RedirectResponse(url=frontend_redirect_url)

@app.get("/users/me")
async def get_current_user(token: str):
    try:
        print("Decoding User Token")
        # Decode JWT token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id = payload["user_id"]
        print(id)
        
        # Fetch user from database using email
        user = await User.get_user_by_id(id)
        print("User---", user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/users/me/{user_id}/")
async def get_current_user(user_id: str):
    try:
        user = await User.get_user_by_id(user_id)
        # return UserResponse(**user)
        return user
    except:
        return {}
    

@app.post("/users/append-follower", status_code=status.HTTP_200_OK)
async def append_follower(operation: FollowerOperation):
    try:
        result = await User.append_follower(operation.user_id, operation.follower_user_id)
        if "not found" in result:
            raise HTTPException(status_code=404, detail=result)
        return JSONResponse(content={"message": "Follower added successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @app.put("/users/me")
# async def update_user_profile(user: UserUpdate, current_user: User = Depends(get_current_user)):
#     # Update user profile here if needed
#     return {"message": "User profile updated successfully"}

# @app.delete("/users/me")
# async def delete_user_profile(current_user: User = Depends(get_current_user)):
#     # Delete user profile here if needed
#     return {"message": "User profile deleted successfully"}

