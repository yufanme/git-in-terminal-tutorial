from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    # my code 👇
    # random_cafe = random.choice(Cafe.query.all())
    # my code 👆

    # angela's code 👇
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    # angela's code 👆

    # write code manually👇
    # return jsonify(cafe={
    #     "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #     "seats": random_cafe.seats,
    #     "has_toilet": random_cafe.has_toilet,
    #     "has_wifi": random_cafe.has_wifi,
    #     "has_sockets": random_cafe.has_sockets,
    #     "can_take_calls": random_cafe.can_take_calls,
    #     "coffee_price": random_cafe.coffee_price,
    # })
    # write code manually👆
    # for column in random_cafe.__table__.columns:
    #     print(getattr(random_cafe, column.name))

    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    cafes_list = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafe=cafes_list)


@app.route("/search")
def search_cafe_at_location():
    # my code 👇
    location = request.args.get("loc")
    cafes_found = Cafe.query.filter_by(location=location).all()
    if cafes_found:
        return jsonify(cafe=[cafe.to_dict() for cafe in cafes_found])
    else:
        return jsonify(error={
                "Not Found": "Sorry, we don't have a cafe at that location."
            }), 404
    # my code 👆

    # # angela's code 👇 maybe wrong
    # query_location = request.args.get("loc")
    # cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    # if cafe:
    #     return jsonify(cafe=cafe.to_dict())
    # else:
    #     return jsonify(error={
    #                 "Not Found": "Sorry, we don't have a cafe at that location."
    #             })
    # # angela's code 👆


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form["name"],
        map_url=request.form["map_url"],
        img_url=request.form["img_url"],
        location=request.form["location"],
        seats=request.form["seats"],
        has_toilet=int(request.form["has_toilet"]),
        has_wifi=int(request.form["has_wifi"]),
        has_sockets=int(request.form["has_sockets"]),
        can_take_calls=int(request.form["can_take_calls"]),
        coffee_price=request.form["coffee_price"],
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={
        "success": "Successfully added the new cafe."
    })


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["GET", "PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = f"£{float(new_price)}"
        db.session.commit()
        return jsonify(success="Successful update the price.")
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["GET", "DELETE"])
def delete_cafe(cafe_id):
    correct_api_key = "TopSecretAPIKey"
    api_key = request.args.get("api_key")
    if api_key == correct_api_key:
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(success="Successful delete the cafe from the database."), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in database."}), 404
    else:
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key."), 403


if __name__ == '__main__':
    app.run(debug=True)
