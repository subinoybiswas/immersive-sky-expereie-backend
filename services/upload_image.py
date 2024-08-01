from fastapi import APIRouter, Depends, Body
from starlette import status
from models.users import UserBase
from models.upload_image import AssetBase, AssetScatter
from database.upload_image import AssetDB
import datetime
from utils.auth import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    get_current_active_user,
    is_admin
)
from utils.scale_image import get_scale_value


router = APIRouter()
asset_db = AssetDB()


@router.post('/create', response_description="Create new asset", status_code=status.HTTP_201_CREATED)
async def create_asset(asset: AssetBase = Body(...), current_user: UserBase = Depends(get_current_active_user)):

    asset.user_id = current_user["_id"]
    asset.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_asset = await asset_db.create_asset(asset.model_dump(by_alias=True, exclude=["id"]))
    return new_asset


@router.get("/new", response_description="Get first new asset", status_code=status.HTTP_200_OK, response_model=AssetBase)
async def get_new_asset():
    asset = await asset_db.get_newest_asset()

    return AssetBase(**asset).model_dump(include=("src"))


@router.get('/scatter', response_description="Get all assets for scatter page", status_code=status.HTTP_200_OK)
async def get_assets_scatter():
    assets = await asset_db.get_scatter_assets()

    scatter_assets = []
    for asset in assets:
        asset["scale"] = get_scale_value(asset["created_at"])
        scatter_assets.append(AssetScatter(**asset).model_dump(by_alias=True, include=["src", "scale", "id"]))

    return scatter_assets


@router.get('/{asset_id}', response_description="Get asset by ID", status_code=status.HTTP_200_OK)
async def get_asset(asset_id: str):
    asset = await asset_db.get_asset(asset_id)
    return AssetBase(**asset).model_dump(by_alias=True, exclude=["id"])
