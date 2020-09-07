# Capstone

In Capstone app you can list movies and actors , you can create new movies and actors and you can update actors and movies.

#Motivations
it is last project of the Udacity Full Stack Nanodegree Course. It covers following:

   - DB modeling with postgres using sqlalchemy (models.py)
   - API for CRUD Operations on DB (app.py)
   - Automated testing with Unittest (see test_app)
   - Authorization & Role with Auth0 (auth.py)
   - Deployment on Heroku

## Getting Started
### Pre-requisites and Local Development

Developers using this project should already have Python3 and pip3 installed in their local machines.

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `root` and running:
```bash
pip3 install -r requirements.txt
```

#### Running the server

Ensure you are working using your created virtual environment.

To export all variables inside setup.sh run:

```bash
source setup.sh
. ./setup.sh
```

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

### Tests
To run the tests, run
```
python3 test_app.py
```

## API Reference

### Getting Started
Base URL:At present this app can only run locally ans is not hosted as a base URL. The backend app is hosted at the defult 
```https://finalud.herokuapp.com/```
    
### Endpoints

#### GET '/actors'
(requires Assistant, Director and Producer permissions)

```$ curl -X GET https://finalud.herokuapp.com/actors```

   - Fetches all actors as objects.  
   - Request Arguments: None.
   - Requires permission: get:actors
   - Return an object with keys actors, current_category and sucess value.
     ```
       {
         'actors': [
              {
              'id': 1
              'name': 'abdo',
              'age': 20,
              'gender': 'man',
              'movies': []

              }, 

              {
              'id': 2,
              'name': 'abdo',
              'age': 25,
              'gender': 'woman',
              'movies': []
              } 
         ],   
         'success': true
       }
     ```
     
#### GET '/movies'
(requires Assistant, Director and Producer permissions)

```$ curl -X GET https://finalud.herokuapp.com/movies```

   - Fetches all movies as objects.  
   - Request Arguments: None.
   - Requires permission: get:movies
   - Return an object with keys movies, current_category and success value.
     ```
       {
          'movies': [
              {
              'id': 1,
              'title': 'movie1',
              'age': 25,
              'start_time': '12/9/2020',
              'actors': []
              },  

              {
              'id': 2,
              'title': 'movie2',
              'age': 20,
              'start_time': '19/9/2020',
              'actors': []
              }
          ],    
         'success': true
       }
     ```
#### DELETE '/actors'
(requires Director and Producer permissions)

```$ curl -X DELETE https://finalud.herokuapp.com/actors/1```

   - Delete a actor with specific id.
   - Request Arguments: actor's id.
   - Requires permission: delete:actor
   - Returns a object with keys actors in which actors objects without deleted actor and success value.
   
     ```
       {
        'actors': [
              {
              'id': 1
              'name': 'abdo',
              'age': 20,
              'gender': 'man',
              'movies': []

              }, 
         ],   
         'success': true
       }
     ```
     
 #### DELETE '/movies'
 (requires Producer permissions)
 
```$ curl -X DELETE https://finalud.herokuapp.com/movies/1```

   - Delete a movie with specific id.
   - Request Arguments: movie's id.
   - Requires permission: delete:movie
   - Returns a object with keys movies in which movies objects without deleted movie and success value.
    
   ```
       {
          'movies': [
              {
              'id': 1,
              'title': 'movie1',
              'age': 25,
              'start_time': '12/9/2020',
              'actors': []
              },  

          ],    
         'success': true
       }
   ```
#### POST '/actors'
 (requires Producer permissions)
 
```$ curl -X POST https://finalud.herokuapp.com/actors```

   - Create new actor and add it to db.
   - Request Arguments:None.
   - Request Headers: (json) 1. string name  2. integer age 3. string gender. 
   - Requires permission: add:actor
   - Returns a object with keys actors in which actors objects with new added actor and success values.
   
      ```
       {
         'actors': [
              {
              'id': 1
              'name': 'abdo',
              'age': 20,
              'gender': 'man',
              'movies': []

              }, 

              {
              'id': 2,
              'name': 'abdo',
              'age': 25,
              'gender': 'woman',
              'movies': []
              },
     
              {
              'id': 3,
              'name': 'abdo',
              'age': 25,
              'gender': 'woman',
              'movies': []
              }  
         ],   
         'success': true
       }
     ```
   
#### POST '/movies'
 (requires Producer permissions)
 
```$ curl -X POST https://finalud.herokuapp.com/movies```

   - Create new movie and add it to db.
   - Request Arguments:None.
   - Request Headers: (json) 1. string title  2. date release_date 
   - Requires permission: add:movie
   - Returns a object with keys movies in which movies objects with new added movies and success value.
   
   ```
       {
        'movies': 
          '1':{
              'title': 'movie1',
              'age': 25,
              'start_time': '12/9/2020',
              'actors': []
              },  

           '2':{
              'title': 'movie2',
              'age': 20,
              'start_time': '19/9/2020',
              'actors': []
              }, 
              
           '3':{
              'title': 'movie3',
              'age': 20,
              'start_time': '19/9/2020',
              'actors': []
              }, 
         'success': true
       }
   ```
#### PATCH '/actors'
 (requires Producer permissions)
 
```$ curl -X PATCH https://finalud.herokuapp.com/actors```

   - Update existing actor in db.
   - Request Arguments: actor's id.
   - Request Headers: (json) 1. string name  2. integer age 3. string gender. 
   - Requires permission: patch:actor  
   - Returns a object with keys actors in which actors objects with updated actor and success value.
   
   
   ```
       {
        'actors': 
          '1':{
              'name': 'mohamed',
              'age': 25,
              'gender': 'man',
              'movies': []

              }, 

           '2':{
              'name': 'abdo',
              'age': 25,
              'gender': 'man',
              'movies': []
              },
              
           '3':{
              'name': 'ahmed',
              'age': 35,
              'gender': 'man',
              'movies': []
              },
         'success': true
       }
   
   ```
 #### PATCH '/movies'
 (requires Producer permissions)

```$ curl -X PATCH https://finalud.herokuapp.com/movies```

   - Update existing movie in db.
   - Request Arguments: movie's id.
   - Request Headers: (json) 1. string title  2. date release_date 
   - Requires permission: patch:movie
   - Returns a object with keys movies in which movies objects with updated movie and success value.
     ```
       {
        'movies': 
          '1':{
              'title': 'movie1',
              'age': 30,
              'start_time': '12/9/2020',
              'actors': []
              },  

           '2':{
              'title': 'movie2',
              'age': 20,
              'start_time': '19/9/2020',
              'actors': []
              }, 
              
           '3':{
              'title': 'movie3',
              'age': 20,
              'start_time': '19/9/2020',
              'actors': []
              }, 
         'success': true
       }
       ```
### Error Handling
Errors are returned as json objects in hte format 
```
{
    'sucess' : False,
    'error' : 400,
    'message' : 'bad request'
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: internal server error
