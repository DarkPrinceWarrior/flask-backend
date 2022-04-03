from flask import request, jsonify
from flask_restful import Resource

from DAO.Models.database_setup import db_session
from DAO.Models.models import RoleModel


class RolesList(Resource):

    def get(self):
        role = db_session.query(RoleModel).all()
        return jsonify(list(x.dictionarize() for x in role))

    def post(self):
        name = request.args.get('name')
        role = RoleModel(name=name)
        db_session.add(role)
        db_session.commit()
        return "Role added OK"

    def put(self):
        id = request.args.get('id')
        new_name = request.args.get('name')
        editedRole = db_session.query(RoleModel).filter_by(id=id).one()
        editedRole.name = new_name
        db_session.add(editedRole)
        db_session.commit()
        return "Role updated OK"

    def delete(self):
        id = request.args.get('id')
        deletedRole = db_session.query(RoleModel).filter_by(id=id).one()
        db_session.delete(deletedRole)
        db_session.commit()
        return "Role deleted OK"


