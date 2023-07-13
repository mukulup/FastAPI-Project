import logging
from fastapi import APIRouter
# from config.db import *
from app.models.model import UserModel
from app.models.schema import UserSchema
router = APIRouter()

router = APIRouter()

@router.get("")
async def get_data():
    try:
        data = await UserModel.get({})
        if data:
            return data
    except Exception as e:
        logging.info(f"Error while getting data, Error occured: {str(e)}")


@router.post("")
async def create_user(data: UserSchema):
    try:
        data = data.dict()
        created_data = await UserModel.create(data)

        logging.info("User Created Successfully")
        return created_data
    except Exception as e:
        logging.info(f"Error occured while creating new User {str(e)}")


@router.get("/getAll")
async def get_all_data():
    try:
        data = await UserModel.filter()
        if data:
            return data
    except Exception as e:
        logging.info(f"Error while getting data, Error occured: {str(e)}")