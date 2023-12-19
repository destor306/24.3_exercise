"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, connect_db, Cupcake
from forms import CupcakeForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "this is my secret_key"

connect_db(app)


@app.route("/api/cupcakes")
def get_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/search')
def search_cupcakes():
    # Get the search term from the query parameter
    search_term = request.args.get('term', '')
    # Modify this query based on your search criteria
    cupcakes = Cupcake.query.filter(
        Cupcake.flavor.ilike(f'%{search_term}%')).all()
    serialized_cupcakes = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized_cupcakes)


@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"],
                          rating=request.json["rating"], image=request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    resp = jsonify(cupcake=new_cupcake.serialize())
    return (resp, 201)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(msg="deleted")


###################### API ###################


@app.route('/', methods=["GET", "POST"])
def index_page():
    form = CupcakeForm()
    cupcakes = Cupcake.query.all()

    if form.validate_on_submit():
        print("it's valid on submit")
        new_cupcake = Cupcake(
            flavor=form.flavor.data,
            size=form.size.data,
            rating=form.rating.data,
            image=form.image.data
        )
        db.session.add(new_cupcake)
        db.session.commit()
        # Redirect back to the index page
        return redirect('/')
    else:
        print("Form errors", form.errors)

    return render_template('index.html', form=form, )
