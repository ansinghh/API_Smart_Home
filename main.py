from fastapi import FastAPI, HTTPException, Depends
from uuid import uuid4
from sqlalchemy.orm import Session
import uvicorn

# Local imports
from database import engine, SessionLocal
import models, schemas

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Instantiate the FastAPI app
app = FastAPI()

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- USER ENDPOINTS -------------------
@app.post("/api/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_id = str(uuid4())
    db_user = models.User(id=user_id, name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ------------------- HOUSE ENDPOINTS -------------------
@app.post("/api/houses", response_model=schemas.HouseOut)
def create_house(house: schemas.HouseCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == house.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    house_id = str(uuid4())
    db_house = models.House(id=house_id, user_id=house.user_id, name=house.name, address=house.address)
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

@app.get("/api/houses/{house_id}", response_model=schemas.HouseOut)
def get_house(house_id: str, db: Session = Depends(get_db)):
    db_house = db.query(models.House).filter(models.House.id == house_id).first()
    if not db_house:
        raise HTTPException(status_code=404, detail="House not found")
    return db_house

# ------------------- ROOM ENDPOINTS -------------------
@app.post("/api/houses/{house_id}/rooms", response_model=schemas.RoomOut)
def add_room(house_id: str, room: schemas.RoomCreate, db: Session = Depends(get_db)):
    # Check if house exists
    db_house = db.query(models.House).filter(models.House.id == house_id).first()
    if not db_house:
        raise HTTPException(status_code=404, detail="House not found")

    room_id = str(uuid4())
    db_room = models.Room(
        id=room_id,
        house_id=house_id,
        name=room.name,
        room_type=room.room_type
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@app.get("/api/houses/{house_id}/rooms")
def get_rooms(house_id: str, db: Session = Depends(get_db)):
    db_rooms = db.query(models.Room).filter(models.Room.house_id == house_id).all()
    return {"rooms": db_rooms}

# ------------------- DEVICE ENDPOINTS -------------------
@app.post("/api/rooms/{room_id}/devices", response_model=schemas.DeviceOut)
def add_device(room_id: str, device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    # Check if room exists
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    device_id = str(uuid4())
    db_device = models.Device(
        id=device_id,
        room_id=room_id,
        device_name=device.device_name,
        device_type=device.device_type,
        status=device.status
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@app.get("/api/rooms/{room_id}/devices")
def get_devices(room_id: str, db: Session = Depends(get_db)):
    db_devices = db.query(models.Device).filter(models.Device.room_id == room_id).all()
    return {"devices": db_devices}

@app.post("/api/devices/{device_id}/control")
def control_device(device_id: str, request: schemas.DeviceControlRequest, db: Session = Depends(get_db)):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")

    db_device.status = request.status
    db.commit()
    return {"message": f"Device {device_id} turned {request.status}"}

# Optional entry point to run via `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
