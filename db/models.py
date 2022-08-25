from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

# User table model
class User(Base):
      __tablename__ = 'user'
      id=Column(Integer(), primary_key=True)
      username=Column(String(30), unique=True, nullable=False)
      email=Column(String(30), nullable=False)
      password=Column(String(200), nullable=False)
      history = relationship('History', back_populates='user')

      def __repr__(self) -> str:
            return f'user: {self.username}, email : {self.email}'

# History table model 
class History(Base):
      __tablename__ = 'history'
      id=Column(Integer, primary_key=True)
      username=Column(String(30), nullable=False, unique=False)
      keyword=Column(String(100), nullable=False)
      date=Column(DateTime(), nullable=False)
      user_id = Column(Integer(), ForeignKey('user.id'))
      user = relationship('User', back_populates='history')

      def __repr__(self):
            return f'<History id {self.id}'
      

      