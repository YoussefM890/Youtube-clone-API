from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ORMCONFIG(BaseModel):
	class Config:
		orm_mode = True


class CreateUser(BaseModel):
	email: EmailStr
	password: str


class CreateChannel(BaseModel):
	name: str


class CreatePlaylist(BaseModel):
	name: str


class CreateVideo(BaseModel):
	name: str


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class UserOut(ORMCONFIG):
	id: int
	email: EmailStr


class ChannelOut(ORMCONFIG):
	id: int
	name: str
	user: UserOut


class PlaylistOut(ORMCONFIG):
	id: int
	name: str
	owner_id: int
	created_at: datetime


class VideoOut(ORMCONFIG):
	id: int
	name: str
	owner_id: int
	created_at: datetime


class TokenData(BaseModel):
	id: Optional[str] = None


class Token(BaseModel):
	token: str
	token_type: str


class Edit(BaseModel):
	video_id: int
	playlist_id: int


class EditOut(ORMCONFIG):
	playlist_id: int
	video_id: int
