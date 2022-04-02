from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from DAO.Models.AnswerQuestion_entity import AnswerQuestionModel
from DAO.Models.UserAttempt_entity import UsersAttemptsModel
from DAO.Models.User_entity import UserModel
from DAO.database_setup import Base


class UsersResultsModel(Base):
    __tablename__ = 'user_result'

    id = Column(Integer, primary_key=True, autoincrement=True)
    involvement = Column(Integer, nullable=False)
    control = Column(Integer, nullable=False)
    risk_taking = Column(Integer, nullable=False)
    attemptId = Column(Integer, ForeignKey("user_attempt.id"), nullable=False)
    attempt = relationship("UsersAttemptsModel", back_populates="user_result")


    def dictionarize(self):
        general_result = self.involvement+self.control+self.risk_taking
        return {
            "id":self.id,
            "General_result":general_result,
            "involvement": self.involvement,
            "control": self.control,
            "risk_taking": self.risk_taking,
            "attemptId": self.attemptId
        }
