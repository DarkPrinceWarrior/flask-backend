from flask import jsonify
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from DAO.Models.Role_entity import RoleModel
from DAO.database_setup import Base


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(80),nullable=False)
    email = Column(String(80),nullable=False)
    gender = Column(String(80),nullable=False)
    age = Column(Integer,nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    role = relationship("RoleModel", back_populates="user")
    attempt = relationship("UsersAttemptsModel", back_populates="user",
                           cascade="all, delete")

    def dictionarize(self):
        return {
                "id":self.id,
                "login": self.login,
                "email": self.email,
                "gender": self.gender,
                "age": self.age,
                "role_id": self.role_id}






