# schemas.py
from pydantic import BaseModel

# ------------------- USER -------------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        from_attributes = True

# ------------------- HOUSE -------------------
class HouseCreate(BaseModel):
    user_id: str
    name: str
    address: str

class HouseOut(BaseModel):
    id: str
    user_id: str
    name: str
    address: str

    class Config:
        orm_mode = True

# ------------------- ROOM -------------------
class RoomCreate(BaseModel):
    house_id: str
    name: str
    room_type: str

class RoomOut(BaseModel):
    id: str
    house_id: str
    name: str
    room_type: str

    class Config:
        orm_mode = True

# ------------------- DEVICE -------------------
class DeviceCreate(BaseModel):
    room_id: str
    device_name: str
    device_type: str
    status: str = "off"

class DeviceOut(BaseModel):
    id: str
    room_id: str
    device_name: str
    device_type: str
    status: str

    class Config:
        orm_mode = True

class DeviceControlRequest(BaseModel):
    status: str
