## Softwares
Docker Engine version v22+
python 3.11
postman

## Dependencies
All in file app/requirements.txt

## DB cache
It will create a folder `mysql` after first running

## Installation for dev
1. Copy `.env.exemple` to `.env` and edit values.
2. Run `docker compose up --build`
3. The container is woring when you see `Quit the server with CONTROL-C.` in docker console.  
4. Create superuser : `docker exec -it django-web python manage.py createsuperuser`
5. Visit `http://localhost:8888` or `http://localhost:8888/admin`
6. Remove the container `docker compose down -v`

## project structure
1. core
    settings: environment varialbes configuration
    urls.py: project routes and urls
2. notes
    migrations: DB migration files
    api_views.py: notes api views
    models.py: model note
    serializers.py: api view serializers
    urls.py: notes routes and urls
3. users
    api_views.py: users api views
    serializers.py: api view serializers
    urls.py: users routes and urls

## DB schema
notes_note: from model note
auth_user: django built-in model 
authtoken_token: django built-in model

## Testing with postman
1. create an auth_user
    url: `http://localhost:8888/api/auth/signup`
    type: POST
    body: raw
    data_type: json
    data_example: {
        "username": "bbb",
        "email": "test@notes.com",
        "password": "12345678", 
        "first_name": "user1",
        "last_name": "user1"
    }

2. login and get the user Token
    url: `http://localhost:8888/api/auth/login`
    type: POST
    body: raw
    data_type: json
    data_example: {
        "username": "bbb",       ## optinal, here could be email
        "password": "12345678"
    }
    Response: {"token": <token>}

3. create all notes (needs Token)
    url: `http://localhost:8888/api/notes/`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: GET
    Response: {
        {"id": 1, "content": "test1"},
        {"id": 2, "content": "test2"},
        ...
    }

4. create a note (needs Token)
    url: `http://localhost:8888/api/notes/`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: POST
    body: raw
    data_type: json
    data_example: {
        "content": "test1"
    }
    Response: {"Create the note: test1 successfully"}

5. get a note (needs Token)
    url: `http://localhost:8888/api/notes/<int:id>`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: GET
    Response: {
        "id": 1,
        "content": "test1"
    }

6. update a note (needs Token)
    url: `http://localhost:8888/api/notes/<int:id>`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: PUT
    body: raw
    data_type: json
    data_example: {
        "content": "test3"
    }
    Response: {""Udate note id: 1 successfully"}

7. delete a note (needs Token)
    url: `http://localhost:8888/api/notes/<int:id>`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: DELETE
    Response: {""DELETE note id: 1 successfully"}

8. share a note with a user (needs Token)
    url: `http://localhost:8888/api/notes/<int:id>/share`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: POST
    body: raw
    data_type: json
    data_example: {
        "username": "<str:username>"
    }
    Response: {"Share the note: test2 with user: bbb successfully"}

9. Search the notes with keywords (needs Token)
    url: `http://localhost:8888/api/search/query`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: GET
    Response: Response: {
        "id": 1,
        "content": "test1"
    }