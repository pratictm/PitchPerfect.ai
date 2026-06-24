from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Date
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

# Database connection URL
DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/pitchperfect_db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Authorization fields
    is_active = Column(Boolean, default=True)
    role = Column(String, default="coach") # Roles e.g., 'coach', 'analyst', 'admin'

    # A single user can upload multiple matches
    matches = relationship("Match", back_populates="owner", cascade="all, delete-orphan")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Upload Form Metadata
    team_a_name = Column(String, nullable=False)
    team_b_name = Column(String, nullable=False)
    match_date = Column(Date, nullable=False)
    camera_angle = Column(String)
    
    # System Pipeline Fields
    video_filename = Column(String, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    processing_status = Column(String, default="Pending")

    owner = relationship("User", back_populates="matches")
    logs = relationship("TrackingLog", back_populates="match", cascade="all, delete-orphan")


class TrackingLog(Base):
    __tablename__ = "tracking_logs"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), index=True, nullable=False)
    
    # Computer Vision & Homography Outputs
    frame_number = Column(Integer, index=True)
    player_id = Column(Integer, index=True)
    team_id = Column(String) 
    x_position = Column(Float)
    y_position = Column(Float)
    speed_kmh = Column(Float, nullable=True)

    match = relationship("Match", back_populates="logs")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables for Auth and CV Analytics created successfully!")