from sqlalchemy import Column, Integer, String, text, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=False, unique=True)
	password = Column(String, nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))


class Channel(Base):
	__tablename__ = "channels"
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
	user = relationship("User")


class PlayList(Base):
	__tablename__ = "playlists"
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))


class Video(Base):
	__tablename__ = "videos"
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))


class PlaylistVideos(Base):
	__tablename__ = "playlistvideos"
	id = Column(Integer, primary_key=True)
	playlist_id = Column(Integer, ForeignKey("playlists.id", ondelete="CASCADE"))
	video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"))
	__table_args__ = (UniqueConstraint('playlist_id', 'video_id', name='unique_playlist_video'),)
