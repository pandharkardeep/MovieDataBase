# MovieDataBase Operations 

## Tech Stack Used:
`Python` , `Flask`, `SQLite`

## Accessing API Endpoints:
  1)`GET /movies` : Get all movies.
  
  2)`GET /movies/<movie_id>` : Get a specific movie by ID.
  
  3)`POST /movies` : Add a new movie.
  
  4)`PUT /movies/<movie_id>`: Update an existing movie.
  
  5)`DELETE /actors/<actor_id>`: Delete an actor if not associated with any movies.

## Models:
  The application defines the following models:
  
  - Movie: Represents a movie with attributes like name, year of release, ratings, etc.
  - Genre: Represents a movie genre.
  - Actor: Represents an actor associated with movies.
  - Technician: Represents a technician (e.g., director, producer) associated with movies.

## Setup 
1) Clone the Repository: `git clone https://github.com/pandharkardeep/MovieDataBase.git`
2) Run the Application: `python Rschema.py`
3) Open `http://localhost:5000`
   
