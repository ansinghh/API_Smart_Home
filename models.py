from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    # Relationship to House
    houses = relationship("House", back_populates="owner")

class House(Base):
    __tablename__ = "houses"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Relationship back to User
    owner = relationship("User", back_populates="houses")

    # Relationship to Room
    rooms = relationship("Room", back_populates="house")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(String, primary_key=True, index=True)
    house_id = Column(String, ForeignKey("houses.id"), nullable=False)
    name = Column(String, nullable=False)
    room_type = Column(String, nullable=False)

    # Relationship back to House
    house = relationship("House", back_populates="rooms")

    # Relationship to Device
    devices = relationship("Device", back_populates="room")

class Device(Base):
    __tablename__ = "devices"
    id = Column(String, primary_key=True, index=True)
    room_id = Column(String, ForeignKey("rooms.id"), nullable=False)
    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    status = Column(String, default="off")

    # Relationship back to Room
    room = relationship("Room", back_populates="devices")
