from sqlalchemy import create_engine, Column, String, select, update, delete, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSON
import databases
import uuid

from .entities import UserCreate

DATABASE_URL = "sqlite:///./users.db"
database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    full_name = Column(String, index=True)
    verified = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    picture = Column(String, index=True)
    sso_id = Column(String, index=True)
    followers = Column(JSON, default=lambda: [])
    
    @classmethod
    async def get_user_by_email(cls, email: str):
        async with database.transaction():
            query = select(cls).where(cls.email == email)
            user = await database.fetch_one(query)
            return user
        
    @classmethod
    async def get_user_by_id(cls, id: str):
        async with database.transaction():
            query = select(cls).where(cls.id == id)
            user = await database.fetch_one(query)
            return user
        
    
    @classmethod
    async def create_user(cls, user_data: UserCreate):
        async with database.transaction():
            print(user_data)
            id = str(uuid.uuid4())
            query = insert(cls).values(
                id=id,
                username=user_data['email'],
                email=user_data['email'],
                full_name=user_data['name'],
                verified=user_data['verified_email'],
                first_name=user_data['given_name'],
                last_name=user_data['family_name'],
                picture=user_data['picture'],
                sso_id=user_data['id']
            )
            await database.execute(query)
            return id
        
    @classmethod
    async def create_or_update_user(cls, user: dict):
        async with database.transaction():
            # Check if the user already exists
            existing_user = await cls.get_user_by_email(user['email'])

            if existing_user:
                # If user already exists, update the user's information
                await cls.update_user(user)
                return existing_user.id
            else:
                # If user does not exist, create a new user
                return await cls.create_user(user)

    @classmethod
    async def update_user(cls, user: dict):
        async with database.transaction():
            # Update the user's information
            query = update(cls).where(cls.email == user['email']).values(
                username=user['email'],
                full_name=user['name'],
                verified=user['verified_email'],
                picture=user['picture'],
                first_name=user['given_name'],
                last_name=user['family_name'],
                sso_id=user['id']
            )
            await database.execute(query)

    @classmethod
    async def delete_user(cls, email: str):
        async with database.transaction():
            # Delete the user profile
            query = delete(cls).where(cls.email == email)
            await database.execute(query)
            
    @classmethod
    async def append_follower(cls, user_id: str, follower_user_id: str):
        async with database.transaction():
            main_user = await cls.get_user_by_id(user_id)
            if not main_user:
                return "Main user not found"

            follower_user = await cls.get_user_by_id(follower_user_id)
            if not follower_user:
                return "Follower user not found"

            # Extract necessary follower information to append
            follower_data = {
                "id": follower_user["id"],
                "username": follower_user["username"],
                "email": follower_user["email"],
                "full_name": follower_user["full_name"],
                "picture": follower_user["picture"]
            }

            # Update followers list
            current_followers = main_user["followers"] if main_user["followers"] else []
            current_followers.append(follower_data)
            update_query = update(cls).where(cls.id == user_id).values(followers=current_followers)
            await database.execute(update_query)
            return "Follower added successfully"

Base.metadata.create_all(bind=engine)

