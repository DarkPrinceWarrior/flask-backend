from flask import jsonify
from flask_restful import reqparse, Resource
from sqlalchemy.orm import sessionmaker

from DAO.Models.User_results import UsersResultsModel
from DAO.database_setup import engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

result_get_args = reqparse.RequestParser()
result_get_args.add_argument("id", type=int, required=True)

result_delete_args = reqparse.RequestParser()
result_delete_args.add_argument("id", type=int, required=True)

result_post_args = reqparse.RequestParser()
result_post_args.add_argument("involvement", type=int, required=True)
result_post_args.add_argument("control", type=int, required=True)
result_post_args.add_argument("risk_taking", type=int, required=True)
result_post_args.add_argument("attemptId", type=int, required=True)

result_put_args = reqparse.RequestParser()
result_put_args.add_argument("involvement", type=int)
result_put_args.add_argument("control", type=int)
result_put_args.add_argument("risk_taking", type=int)
result_put_args.add_argument("attemptId", type=int)


class ResultsList(Resource):

    def get(self):
        results = session.query(UsersResultsModel).all()
        session.close()
        return jsonify(list(x.dictionarize() for x in results))

    def post(self):
        args = result_post_args.parse_args()
        involvement = args['involvement']
        control = args['control']
        risk_taking = args['risk_taking']
        attemptId = args['attemptId']

        results = UsersResultsModel(involvement=involvement,
                                    control=control,
                                    risk_taking=risk_taking,
                                    attemptId=attemptId)

        session.add(results)
        session.commit()
        session.close()
        return {"status": "OK"}


class Result(Resource):

    def get(self, id):
        result = session.query(UsersResultsModel).filter_by(attemptId=id).one()
        session.close()
        return jsonify(result.dictionarize())

    def put(self, id):
        args = result_put_args.parse_args()
        involvement = args['involvement']
        control = args['control']
        risk_taking = args['risk_taking']
        attemptId = args["attemptId"]

        # new_role_id = request.args.get('role_id')

        editedResult = session.query(UsersResultsModel).filter_by(id=id).one()

        editedResult.involvement = involvement
        editedResult.control = control
        editedResult.risk_taking = risk_taking
        editedResult.attemptId = attemptId

        session.add(editedResult)
        session.commit()
        session.close()
        return "Result updated OK"

    def delete(self, id):
        deletedResult = session.query(UsersResultsModel).filter_by(id=id).one()
        session.delete(deletedResult)
        session.commit()
        session.close()
        return "Result deleted OK"
