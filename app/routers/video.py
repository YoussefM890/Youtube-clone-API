from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
	prefix="/videos",
	tags=["Videos"]
)


@router.get("/all", response_model=List[schemas.VideoOut])
def get_all_videos(db: Session = Depends(get_db)):
	videos = db.query(models.Video).all()
	return videos


@router.get("/", response_model=List[schemas.VideoOut])
def get_all_your_video(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
	videos = db.query(models.Video).filter(models.Video.owner_id == current_user.id).all()
	return videos


@router.get("/{id}", response_model=schemas.VideoOut)
def get_one_video(id: int, db: Session = Depends(get_db)):
	video = db.query(models.Video).filter(models.Video.id == id).first()
	if not video:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Video with id : {id} does not exist")
	return video


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VideoOut)
def add_video(video: schemas.CreateVideo, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
	video_to_add = models.Video(owner_id=current_user.id, **video.dict())
	db.add(video_to_add)
	db.commit()
	db.refresh(video_to_add)
	return video_to_add


@router.put("/{id}", response_model=schemas.VideoOut)
def update_video(id: int, updated: schemas.CreateVideo, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
	video_to_edit = db.query(models.Video).filter(models.Video.id == id)
	if not video_to_edit.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Video with id : {id} does not exist")
	if db.query(models.Video).filter(models.Video.id == id).first().owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
	video_to_edit.update(updated.dict(), synchronize_session=False)
	db.commit()
	return video_to_edit.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
	video_to_delete = db.query(models.Video).filter(models.Video.id == id)
	if not video_to_delete.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Video with id : {id} does not exist")
	if db.query(models.Video).filter(models.Video.id == id).first().owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
	video_to_delete.delete(synchronize_session=False)
	db.commit()
