from flask import Flask,request
from flask_restful import Api,Resource
from security import auth, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.secret_key = '#0#'
api = Api(app)
jwt = JWT(app, auth, identity)#/auth
items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x:x['name'] == name, items), None)
        return{'item':item}
    def post(self, name):
        if next(filter(lambda x:x['name'] == name, items), None):
            return {'message':'item '+name+' exists'}
        data = request.get_json()
        new_item = {'name':name, 'price':data['price']}
        items.append(new_item)
        return new_item
    def delete(self, name):
        global items
        items = list(filter(lambda x:x['name'] != name, items))
        return items
    def put(self, name):
        data = request.get_json()
        items = list(filter(lambda x:x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price':data['price']}
        else:
            items.update(data)

class ItemList(Resource):
    def get(self):
        return{'item':items}

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=8000, debug=True)
