"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, render_template, redirect
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException
from admin import setup_admin
from models import db, User
# import Cloudinary as cloudinary_utils
# from Cloudinary.uploader import upload
import cloudinary
import uuid
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user
#from models import Person


class MyModelView(ModelView):
    def is_accessible(self):
        user = User.query.get(1)
        # print(user.is_active())
        return user.active


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(CLOUDINARY_URL=os.environ.get('CLOUDINARY_URL'))
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app, MyModelView)
login = LoginManager(app)
# login.init_app(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return render_template('index.html')

@app.route('/check')
def check():
    user = User.query.get(1)
    return user.serialize()

@app.route('/logout', methods=['PATCH'])
def logout():
    user = User.query.get(1)
    body = request.json
    print(body)
    user.update_user(body)
    try: 
        db.session.commit()
        return "logout", 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        return jsonify({
            "result": f"{error.args}"
        }), 500

@app.route('/login', methods=['POST'])
def login():
    body = request.form.getlist('active')
    password = os.environ.get("ADMIN_PASS")
    if body[0] == password:
        res = {'active': True}
        user = User.query.get(1)
        if user == None:
            new = User.admin("borisbruno88@gmail.com", 1234, True)
            db.session.add(new)
            try: 
                db.session.commit()
                return redirect("http://0.0.0.0:3000/admin", code=302)
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "result": f"{error.args}"
                }), 500
        if user != None:
            user.update_user(res)
            try: 
                db.session.commit()
                return redirect("http://0.0.0.0:3000/admin", code=302)
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "result": f"{error.args}"
                }), 500
    if body[0] == "":
        return jsonify({
            "error" : "error"
        }), 400
    if body[0] != password:
        return jsonify({
            "error" : "not"
        }), 400



@app.route('/images', methods=['POST'])
def handle_images():
        body = request.json
        # image = CloudinaryImage("https://res.cloudinary.com/cormineco/image/upload/v1618091325/cormineco/residuos_waru5q.jpg").image(type="fetch")
        
        if body is None:
            return jsonify({
                "result" : "missing request body"

            }), 400

        if "folder" not in body:
            return jsonify({
                "result": "missing fields in request body"
            }), 400

        if "folder" in body:
            if body["folder"] == "inicio":
                result = cloudinary.Search().expression('folder:"inicio"').max_results('10').execute()
                resources = result["resources"]
                response = []
                for image in resources:
                    response.append({"image_url": image["url"], "name": image["filename"]})
                    
                return jsonify(response), 200
            if body["folder"] == "cormineco":
                result = cloudinary.Search().expression('folder:"cormineco"').max_results('10').execute()
                resources = result["resources"]
                response = []
                for image in resources:
                    response.append({"image_url": image["url"], "name": image["filename"]})
                    
                return jsonify(response), 200
            if body["folder"] == "compromiso":
                result = cloudinary.Search().expression('folder:"compromiso"').max_results('10').execute()
                resources = result["resources"]
                response = []
                for image in resources:
                    response.append({"image_url": image["url"], "name": image["filename"]})
                    
                return jsonify(response), 200
            if body["folder"] == "alcance":
                result = cloudinary.Search().expression('folder:"alcance"').max_results('10').execute()
                resources = result["resources"]
                response = []
                for image in resources:
                    response.append({"image_url": image["url"], "name": image["filename"]})
                    
                return jsonify(response), 200
            if body["folder"] == "contacto":
                result = cloudinary.Search().expression('folder:"contacto"').max_results('10').execute()
                resources = result["resources"]
                response = []
                for image in resources:
                    response.append({"image_url": image["url"], "name": image["filename"]})
                    
                return jsonify(response), 200
        return jsonify({
            "result" : "missing fields in request body folder"
        }), 400



@app.route('/admin', methods=['POST'])
def handle_password():

    request_body = request.json

    print(request_body)

    if request_body is None:
        return jsonify({
            "result" : "missing request body"

        }), 400

    if "pass" not in request_body:
        return jsonify({
            "result": "missing fields in request body"
        }), 400

    if "pass" in request_body:
        unique_id = uuid.uuid4()
        password = os.environ.get("ADMIN_PASS")

        if password == request_body["pass"]:

            return jsonify({
                "id": unique_id
            }), 200

        else:
            return jsonify({
                "error": "password incorrect"
            }), 400

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
