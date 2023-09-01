### Prerequisites
Before running this API, ensure you have the following software installed:

- Python 3.x
- SQLite (for the database)

### Installation
- Clone this and move to the folder where you have cloned it
```pip install -r requirements.txt ```

### Curls
- Register or log in a user by providing an email and password. The endpoint returns a JWT token for accessing protected endpoints.
Movies
 ```bash
 curl -X POST -H "Content-Type: application/json" -d '{
  "email": "user@example.com",
  "password": "password"
}' http://localhost:5000/auth```

- Retrieve a list of movies. You can use query parameters to filter and search for movies by name, director, genre, IMDb rating, and popularity.
```bash
curl http://localhost:5000/movies
```

- Add a new movie (authentication required).
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <JWT-access-token>" -d '{
  "99popularity": 88.0,
  "director": "George Lucas",
  "genre": ["Action", "Adventure", "Fantasy", "Sci-Fi"],
  "imdb_score": 8.8,
  "name": "Star Wars"
}' http://localhost:5000/movies/add

```


- Edit an existing movie (authentication required) No need to pass all the values if some fields are not passed it will use the previous ones.

```bash
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <JWT-access-token>" -d '{
  "99popularity": 89.0,
  "director": "George Lucas",
  "genre": ["Action", "Adventure", "Sci-Fi"],
  "imdb_score": 9.0,
  "name": "Star Wars: Updated"
}' http://localhost:5000/movies/edit/<movie_id>

```

- Remove a movie by ID (authentication required).
```bash
curl -X DELETE -H "Authorization: Bearer <JWT-access-token>" http://localhost:5000/movies/remove/<movie_id>
```

- Searching
Search for movies based on various criteria, including name, director, genre, IMDb rating , and popularity/popularity range.

- Search Movies by Name
```bash 
curl "http://localhost:5000/movies?name=Star%20Wars"
```

- Search movies by director:
```bash
curl "http://localhost:5000/movies?director=George%20Lucas"
```

- Search movies by multiple genres or a genre:
```bash
curl "http://localhost:5000/movies?genre=Adventure&genre=Fantasy"
```

Search movies by IMDb rating range or wih just maximum and minimum:
```bash
curl "http://localhost:5000/movies?min_rating=8.0&max_rating=9.0"
```
```bash
curl http://localhost:5000/search?max_rating=9.0
```
```bash
curl http://localhost:5000/search?min_rating=8.0
```
Search movies by popularity range or wih just maximum and minimum:

```bash
curl "http://localhost:5000/movies?min_popularity=80.0&max_popularity=90.0"
```
```bash
curl "http://localhost:5000/movies?min_popularity=80.0
```
```bash
curl "http://localhost:5000/movies?max_popularity=80.0
```
