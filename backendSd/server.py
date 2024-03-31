from flask import Flask, jsonify,request,session
from flask_cors import CORS,cross_origin
from flask_bcrypt import Bcrypt

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


from models import db , User , Blog

 
# Initializing flask app
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = "yoga"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "siddhi"  # Change this!
jwt = JWTManager(app)


db.init_app(app)
 
with app.app_context():
    db.create_all()

# CORS(app,resources={r"/api/*":{"origins":"*"}})
CORS(app,supports_credentials=True)



@app.route("/api/login",methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error":"Unauthorized Access"}),401
    
    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({"error":"Unauthorized"}),401

    session["user_id"] = user.id
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "id" : user.id,
        "email" : user.email,
        "access_token":access_token
    })


@app.route('/api/userData',methods=['GET'])
@jwt_required()
def get_user_data():
    user_id=get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({'error':'User not found'}),404

    user_data = {
        'id':user.id,
        'email':user.email,
        'name':user.name
    }

    return jsonify(user_data)


@app.route('/api/register', methods=['POST'])
def register():
    email = request.json["email"]
    name = request.json["name"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    hashed_password = bcrypt.generate_password_hash(password)
   
    
    if user_exists:
        return jsonify({"error" : "Email already exists"}),400
    
    new_user = User(email=email,name=name,password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return jsonify({
        "id" : new_user.id,
        "email" : new_user.email
    })

@app.route('/api/getblogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()

    if not blogs:
        return jsonify({'message': 'No blogs found'}), 404

    blog_list = []
    for blog in blogs:
        blog_data = {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'author_id': blog.author_id,
            'created_at': blog.created_at,
            'updated_at': blog.updated_at
        }
        blog_list.append(blog_data)

    return jsonify(blog_list), 200 


@app.route('/api/blogs', methods=['POST'])
@jwt_required()
def add_blogs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    title = request.json['title']
    content = request.json['content']

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    new_blog = Blog(title=title, content=content, author_id=user.id)

    db.session.add(new_blog)
    db.session.commit()

    return jsonify({
        'id': new_blog.id,
        'title': new_blog.title,
        'content': new_blog.content,
        'author_id': new_blog.author_id,
        'created_at': new_blog.created_at,
        'updated_at': new_blog.updated_at
    }), 201

# Route for seeing a data
@app.route('/api/data',methods=['GET'])
def get_data():
    data = {
        "message":"Hello this is api end point"
    }

    return jsonify(data)


 
    
 
     
# Running app
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)