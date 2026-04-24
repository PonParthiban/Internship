from flask import Flask
from flask_restful import Api, Resource

app = Flask("__name__")
api = Api(app)

names = {"parthi": {"age": 19, "gender":"male"},
         "jim": {"age": 32, "gender":"male"}}


class helloworld(Resource):
      def get(self,name):
          return names[name]
      
      def post(self):
           return {"data" : "data posted"}

api.add_resource(helloworld, "/helloworld/<string:name>")


if __name__ == "__main__":
    app.run(debug=True)