from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
import sqlite3
import os
import bcrypt

app = Flask(__name__)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'd@w@kap*9*=a7fv(+m+(hv+2$m@%1hl6iu6f_b&$0418q7*$d!' # Making it public as it is not critical for our this test api as we will not be storing real user data on this, we can load this from pur secet environment also
jwt = JWTManager(app)

# Create SQLite database connection
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'movies.db')
db_connection = sqlite3.connect(db_path, check_same_thread=False)
db_cursor = db_connection.cursor()

# #Initialize the database (run this only once) i have commented it out as i have already ran it once 
# db_cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         email TEXT UNIQUE,
#         password_hash TEXT
#     )
# ''')
# db_cursor.execute('''
#     CREATE TABLE IF NOT EXISTS movies (
#         id INTEGER PRIMARY KEY,
#         popularity REAL,
#         director TEXT,
#         genre TEXT,
#         imdb_score REAL,
#         name TEXT
#     )
# ''')
# db_connection.commit()

# User auth it will register the user if it doesn't already exist and return jwt if user exists it will check password and return jwt
@app.route('/auth', methods=['POST'])
def register():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # Check if user already exists
    db_cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = db_cursor.fetchone()
    if user:
        # If User exists check password
        password = password.encode('utf-8')
        if bcrypt.checkpw(password, user[2]):
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Incorrect password"}), 401   
    
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert user in database
    db_cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, password_hash))
    db_connection.commit()

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200


@app.route('/movies', methods=['GET'])
def get_movies():
    db_cursor.execute("SELECT * FROM movies")
    movies = db_cursor.fetchall()

    # Convert list of tuples to list of dictionaries
    movie_list = []
    for movie in movies:
        movie_dict = {
            "id": movie[0],
            "99popularity": movie[1],
            "director": movie[2],
            "genre": movie[3].split(', '),  # Convert genre to list
            "imdb_score": movie[4],
            "name": movie[5]
        }
        movie_list.append(movie_dict)

    return jsonify(movie_list), 200

# Add movie endpoint
@app.route('/movies/add', methods=['POST'])
@jwt_required()
def add_movie():
    user_email = get_jwt_identity()
    if user_email:
        data = request.get_json()
        
        # Check for required fields
        required_fields = ['99popularity', 'director', 'genre', 'imdb_score', 'name']
        if not all(field in data for field in required_fields):
            return jsonify(error="Missing required fields"), 400

        try:
            # Attempt to insert the movie data into the database
            db_cursor.execute("INSERT INTO movies (popularity, director, genre, imdb_score, name) VALUES (?, ?, ?, ?, ?)",
                              (data['99popularity'], data['director'], ','.join(data['genre']), data['imdb_score'], data['name']))
            db_connection.commit()
            return jsonify(message="Movie added successfully"), 201
        except Exception as e:
            # Handle database insertion errors
            return jsonify(error="Failed to add the movie. Please check your data."), 500
    return jsonify(message="Unauthorized"), 401

# Edit endpoint
@app.route('/movies/edit/<int:movie_id>', methods=['PUT'])
@jwt_required()
def edit_movie(movie_id):
    user_email = get_jwt_identity()
    if user_email:
        data = request.get_json()
        db_cursor.execute("UPDATE movies SET popularity = ?, director = ?, genre = ?, imdb_score = ?, name = ? WHERE id = ?",
                          (data['99popularity'], data['director'], ','.join(data['genre']), data['imdb_score'], data['name'], movie_id))
        db_connection.commit()
        return jsonify(message="Movie updated successfully"), 200
    return jsonify(message="Unauthorized"), 401

# Remvoe a movie
@app.route('/movies/remove/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def remove_movie(movie_id):
    user_email = get_jwt_identity()
    if user_email:
        db_cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        db_connection.commit()
        return jsonify(message="Movie removed successfully"), 200
    return jsonify(message="Unauthorized"), 401

# Search endpoint
@app.route('/search', methods=['GET'])
def search():
    query_params = request.args

    # Build the SQL query
    query = "SELECT * FROM movies"

    # Apply filters if provided
    filters = []
    if 'name' in query_params:
        filters.append(f"name LIKE '%{query_params['name']}%'")
    if 'director' in query_params:
        filters.append(f"director LIKE '%{query_params['director']}%'")
    if 'genre' in query_params:
        genres = query_params.getlist('genre')
        genres_condition = " OR ".join([f"genre LIKE '%{genre}%'" for genre in genres])
        filters.append(f"({genres_condition})")
    if 'min_rating' in query_params:
        filters.append(f"imdb_score >= {query_params['min_rating']}")
    if 'max_rating' in query_params:
        filters.append(f"imdb_score <= {query_params['max_rating']}")
    if 'min_popularity' in query_params:
        filters.append(f"popularity >= {query_params['min_popularity']}")
    if 'max_popularity' in query_params:
        filters.append(f"popularity <= {query_params['max_popularity']}")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    db_cursor.execute(query)
    movies = db_cursor.fetchall()

    # Convert list of tuples to list of dictionaries
    movie_list = []
    for movie in movies:
        movie_dict = {
            "id": movie[0],
            "99popularity": movie[1],
            "director": movie[2],
            "genre": movie[3].split(', '),
            "imdb_score": movie[4],
            "name": movie[5]
        }
        movie_list.append(movie_dict)

    return jsonify(movie_list), 200


if __name__ == '__main__':
    app.run(debug=True)