from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth2
from app.database import get_db

router = APIRouter(
	prefix="/users",
	tags=["Users"]
)


@router.get("/", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
	users = db.query(models.User).all()
	return users


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.id == id).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} does not exist")
	return user


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def add_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
	try:
		hashed_password = utils.hash(user.password)
		print(user.password, hashed_password)
		user.password = hashed_password
		user_to_add = models.User(**user.dict())
		db.add(user_to_add)
		db.commit()
		db.refresh(user_to_add)
		return user_to_add
	except:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this Email already exist")


@router.put("/", response_model=schemas.UserOut)
def update_user(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
	user_to_edit = db.query(models.User).filter(models.User.id == current_user.id)
	if not user_to_edit.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} does not exist")
	db.commit()
	return user_to_edit.fiuser_to_add


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
	user_to_delete = db.query(models.User).filter(models.User.id == current_user.id)
	if not user_to_delete.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} does not exist")
	user_to_delete.delete(synchronize_session=False)
	db.commit()
