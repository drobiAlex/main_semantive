from flask import Flask
from flask_restful import Api, Resource, reqparse
from helpers import save_text, save_img
from download import download_file

app = Flask(__name__)
api = Api(app)


class Upload(Resource):
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument("url")
        parser.add_argument("type")

        args = parser.parse_args()

        if args["type"] == "img":
            feed_back = save_img(args["url"])

        elif args["type"] == "text":
            feed_back = save_text(args["url"])

        else:
            return "There is a mistake in type", 400

        return feed_back, 201


class Download(Resource):
    def get(self):

        parser = reqparse.RequestParser()

        parser.add_argument("url")
        parser.add_argument("type")

        download_file(parser)


api.add_resource(Upload, '/upload')
api.add_resource(Download, '/download')

if __name__ == '__main__':
    app.run(debug=1)
