from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from DAO.database_setup import Base


class AnswerModel(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    answer_text = Column(String(250),nullable=False)
    answerToQuestion = relationship("AnswerQuestionModel", back_populates="answer",
                                    cascade="all, delete")


    def dictionarize(self):
        return {
            "answer_text": self.answer_text
        }