from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from DAO.Models.database_setup import Base



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


class RoleModel(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    user = relationship('UserModel', back_populates='role', cascade='all, delete')


    def dictionarize(self):
        return {
            "id": self.id,
            "name": self.name}




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


