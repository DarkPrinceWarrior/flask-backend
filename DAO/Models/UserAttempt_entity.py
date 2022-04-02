
from sqlite3 import Date

from DAO.database_setup import Base

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref

from DAO.Models.AnswerQuestion_entity import AnswerQuestionModel
from DAO.Models.User_entity import UserModel



class UsersAttemptsModel(Base):
    __tablename__ = 'user_attempt'

    id = Column(Integer, primary_key=True, autoincrement=True)
    attempt_number = Column(Integer,nullable=False)
    userId = Column(Integer, ForeignKey("user.id"), nullable=False)
    passing_time = Column(String(100), nullable=False)
    user_answer = relationship('UsersAnswersModel',
                               back_populates='attempt', cascade='all, delete')
    user = relationship("UserModel", back_populates="attempt")
    user_result = relationship('UsersResultsModel',
                               back_populates='attempt', cascade='all, delete')


    def dictionarize(self):
        return {
            "id": self.id,
            "attempt_number": self.attempt_number,
            "userId": self.userId,
            "passing_time": self.passing_time
        }



