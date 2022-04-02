from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from DAO.Models.Answer_entity import AnswerModel
from DAO.Models.Question_entity import QuestionModel
from DAO.database_setup import Base




class AnswerQuestionModel(Base):
    __tablename__ = 'answer_question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    questionId = Column(Integer, ForeignKey("question.id"), nullable=False)
    question = relationship(QuestionModel, back_populates="questionToQuestion")
    answerId = Column(Integer, ForeignKey("answer.id"), nullable=False)
    answer = relationship("AnswerModel", back_populates="answerToQuestion")
    question_balls = Column(Integer, nullable=False)
    choice = relationship("UsersAnswersModel", back_populates="user_answers",
                          cascade="all, delete")



    def dictionarize(self):
        return {
            "id":self.id,
            "questionId": self.questionId,
            "answerId": self.answerId,
            "question_balls": self.question_balls
        }