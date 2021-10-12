from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
api = Api(app)
run_with_ngrok(app)


BOOKS = {
    'book0': {'title': 'placeholder', 'author': 'placeholder'}
}


def abort_if_todo_doesnt_exist(book_id):
    if book_id not in BOOKS:
        abort(404, message="Book {} doesn't exist".format(book_id))

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('author')


# Todo
# shows a single todo item and lets you delete a todo item
class Book(Resource):
    def get(self, book_id):
        abort_if_todo_doesnt_exist(book_id)
        return BOOKS[book_id]

    def delete(self, book_id):
        abort_if_todo_doesnt_exist(book_id)
        del BOOKS[book_id]
        return '', 204

    def put(self, book_id):
        args = parser.parse_args()
        book = {'task': args['task']}
        BOOKS[book_id] = book
        return book, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class BooksList(Resource):
    def get(self):
        return BOOKS

    def post(self):
        args = parser.parse_args()
        book_id = int(max(BOOKS.keys()).lstrip('book')) + 1
        book_id = 'book%i' % book_id
        BOOKS[book_id] = {'title': args['title'], 'author': args['author']}
        #'book0': {'title': 'placeholder'},
        return BOOKS[book_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(BooksList, '/books')
api.add_resource(Book, '/books/<book_id>')


if __name__ == '__main__':
    app.run()