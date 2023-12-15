from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('fruit', user='chris', password='1234', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Fruit(BaseModel):
  name = CharField()
  color = CharField()
  seed = BooleanField()

db.connect()
db.drop_tables([Fruit])
db.create_tables([Fruit])

Fruit(name='Coconut', color='brown', seed= False).save()
Fruit(name='Apple', color='green', seed= True).save()
Fruit(name='Grape', color='purple', seed= False).save()
Fruit(name='Pineapple', color='yellow', seed= False).save()
Fruit(name='Strawberry', color='red', seed= True).save()


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home(id=None):
   if request.method == "GET":
      return "Welcome to the fruit stand!"

@app.route('/fruit/', methods=['GET', 'POST'])
@app.route('/fruit/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Fruit.get(Fruit.id == id)))
    else:
        fruit_list = []
        for fruit in Fruit.select():
            fruit_list.append(model_to_dict(fruit
        ))
        return jsonify(fruit_list)

  if request.method =='PUT':
    body = request.get_json()
    Fruit.update(body).where(Fruit.id == id).execute()
    return "Fruit " + str(id) + " has been updated."

  if request.method == 'POST':
    new_fruit = dict_to_model(Fruit, request.get_json())
    new_fruit.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Fruit.delete().where(Fruit.id == id).execute()
    return "Fruit " + str(id) + " deleted."

app.run(debug=True, port=9000)