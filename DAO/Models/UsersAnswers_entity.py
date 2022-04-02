from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from DAO.Models.AnswerQuestion_entity import AnswerQuestionModel
from DAO.Models.UserAttempt_entity import UsersAttemptsModel
from DAO.Models.User_entity import UserModel
from DAO.database_setup import Base


class UsersAnswersModel(Base):
    __tablename__ = 'user_answer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    choiceId = Column(Integer, ForeignKey("answer_question.id"), nullable=False)
    user_answers = relationship(AnswerQuestionModel,back_populates="choice")
    attemptId = Column(Integer, ForeignKey("user_attempt.id"), nullable=False)
    attempt = relationship("UsersAttemptsModel", back_populates="user_answer")



    def dictionarize(self):
        return {
            "choiceId": self.choiceId,
            "attemptId": self.attemptId
        }

