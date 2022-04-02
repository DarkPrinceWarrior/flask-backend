from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from DAO.database_setup import Base


class QuestionModel(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(String(250), nullable=False)
    question_type = Column(String(20), nullable=False)
    statement_type = Column(String(20), nullable=False)
    questionToQuestion = relationship("AnswerQuestionModel", back_populates="question",
                                      cascade="all, delete")

    def dictionarize(self):
        return {
            "question_text": self.question_text,
            "question_type": self.question_type,
            "statement_type": self.statement_type
        }
