from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_ngrok import run_with_ngrok
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
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



class Book(Resource):
    def get(self, book_id):
        """
                Get a specific book
                ---
                tags:
                  - restful
                parameters:
                  - in: path
                    name: book_id
                    required: true
                    description: The specified book.
                    type: string
                    examples: book0
                responses:
                  200:
                    description: Book List
                    schema:
                      id: Book
                      properties:
                        title:
                          type: string
                          default:
                        author:
                          type: string
                          default:
                """
        abort_if_todo_doesnt_exist(book_id)
        return BOOKS[book_id]

    def delete(self, book_id):
        """
               Delete a book
               ---
               tags:
                 - restful
               parameters:
                 - in: path
                   name: book_id
                   required: true
                   description: The ID of the book
                   type: string
               responses:
                 204:
                   description: Book deleted
               """
        abort_if_todo_doesnt_exist(book_id)
        del BOOKS[book_id]
        return '', 204

    def put(self, book_id):
        """
               Update a book's information
               ---
               tags:
                 - restful
               parameters:
                 - in: body
                   name: body
                   schema:
                     $ref: '#/definitions/Book'
                 - in: path
                   name: book_id
                   required: true
                   description: The ID of the book
                   type: string
               responses:
                 201:
                   description: The information has been updated
                   schema:
                     $ref: '#/definitions/Book'
               """
        args = parser.parse_args()
        book = {'title': args['title'], 'author': args['author']}
        BOOKS[book_id] = book
        return book, 201


class BooksList(Resource):
    def get(self):
        return BOOKS

    def post(self):
        """
        Enter book data
        ---
         tags:
           - restful
         parameters:
           - in: body
             name: body
             schema:
               $ref: '#/definitions/Book'
         responses:
           201:
            description: The book information has been updated
            schema:
               $ref: '#/definitions/Book'
        """
        args = parser.parse_args()
        book_id = int(max(BOOKS.keys()).lstrip('book')) + 1
        book_id = 'book%i' % book_id
        BOOKS[book_id] = {'title': args['title'], 'author': args['author']}
        return BOOKS[book_id], 201


api.add_resource(BooksList, '/books')
api.add_resource(Book, '/books/<book_id>')


if __name__ == '__main__':
    app.run()