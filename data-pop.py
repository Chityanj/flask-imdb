import sqlite3
import json
import os

# Read movie data from JSON file
with open('imdb.json', 'r') as file:
    movies_data = json.load(file)

# Create a connection to the database
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'movies.db')
db_connection = sqlite3.connect(db_path)
db_cursor = db_connection.cursor()

# Insert movie data into the movies table
for movie in movies_data:
    db_cursor.execute("INSERT INTO movies (popularity, director, genre, imdb_score, name) VALUES (?, ?, ?, ?, ?)",
                      (movie["99popularity"], movie["director"], ', '.join(movie["genre"]),
                       movie["imdb_score"], movie["name"]))
    db_connection.commit()

# Close the database connection
db_connection.close()

print("Movie data has been populated into the database.")