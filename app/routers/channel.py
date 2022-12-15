from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
	prefix="/channels",
	tags=["Channels"]
)


@router.get("/", response_model=List[schemas.ChannelOut])
def get_all_channels(db: Session = Depends(get_db)):
	channels = db.query(models.Channel).all()
	return channels


@router.get("/{id}", response_model=schemas.ChannelOut)
def get_channel(id: int, db: Session = Depends(get_db)):
	channel = db.query(models.Channel).filter(models.Channel.id == id).first()
	if not channel:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Channel with id : {id} does not exist")
	return channel


@router.post("/", response_model=schemas.ChannelOut)
def add_channel(channel: schemas.CreateChannel, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
	current_channel = db.query(models.Channel).filter(models.Channel.owner_id == current_user.id).first()
	if current_channel:
		raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"You already have a channel")
	channel_to_add = models.Channel(owner_id=current_user.id, **channel.dict())
	db.add(channel_to_add)
	db.commit()
	db.refresh(channel_to_add)
	return channel_to_add


@router.put("/{id}", response_model=schemas.ChannelOut)
def update_channel(id: int, updated: schemas.CreateChannel, db: Session = Depends(get_db),
                   current_user=Depends(oauth2.get_current_user)):
	channel_query = db.query(models.Channel).filter(models.Channel.id == id)
	channel_to_update = channel_query.first()
	if not channel_to_update:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Channel with id : {id} does not exist")
	channel_query.update(updated.dict(), synchronize_session=False)
	if channel_to_update.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
	db.commit()
	return channel_to_update


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
	channel_to_delete = db.query(models.Channel).filter(models.Channel.id == id)
	if not channel_to_delete.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Channel with id : {id} does not exist")
	if channel_to_delete.first().owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
	channel_to_delete.delete(synchronize_session=False)
	db.commit()
