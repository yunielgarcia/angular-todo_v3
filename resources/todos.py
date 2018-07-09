from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, inputs,
                           fields, marshal, marshal_with, url_for)

# from auth import auth
import models

todo_fields = {
    'id': fields.Integer,
    'name': fields.String
}


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo name provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        todos = [marshal(todo, todo_fields)
                 for todo in models.Todo.select()]
        return {'todos': todos}

    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        course = models.Todo.create(**args)
        return course, 201, {'Location': url_for('resources.todos.todos')}


# class Course(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument(
#             'title',
#             required=True,
#             help='No course title provided',
#             location=['form', 'json']
#         )
#         self.reqparse.add_argument(
#             'url',
#             required=True,
#             help='No course URL provided',
#             location=['form', 'json'],
#             type=inputs.url
#         )
#         super().__init__()
#
#     @marshal_with(course_fields)
#     def get(self, id):
#         return add_reviews(course_or_404(id))
#
#     @marshal_with(course_fields)
#     @auth.login_required
#     def put(self, id):
#         args = self.reqparse.parse_args()
#         query = models.Course.update(**args).where(models.Course.id == id)
#         query.execute()
#         return (add_reviews(models.Course.get(models.Course.id == id)), 200,
#                 {'Location': url_for('resources.courses.course', id=id)})
#
#     @auth.login_required
#     def delete(self, id):
#         query = models.Course.delete().where(models.Course.id == id)
#         query.execute()
#         return '', 204, {'Location': url_for('resources.courses.courses')}


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
# api.add_resource(
#     Course,
#     '/api/v1/courses/<int:id>',
#     endpoint='course'
# )
