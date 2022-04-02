
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from DAO.database_setup import Base


class RoleModel(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    user = relationship('UserModel', back_populates='role', cascade='all, delete')


    def dictionarize(self):
        return {
            "id": self.id,
            "name": self.name}
