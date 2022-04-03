import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


Database_name = "Database.sqlite"
engine = create_engine(f'sqlite:///{Database_name}')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()

# create the db
def init_db():
    from DAO.Models.models import QuestionModel
    from DAO.Models.models import AnswerQuestionModel
    from DAO.Models.models import UsersAnswersModel
    from DAO.Models.models import UsersAttemptsModel
    from DAO.Models.models import UsersResultsModel
    from DAO.Models.models import UserModel
    from DAO.Models.models import RoleModel
    from DAO.Models.models import AnswerModel
    Base.metadata.create_all(engine)
