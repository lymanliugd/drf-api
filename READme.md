## Docker and python
1. Docker Engine version v22+
2. Python 3.11

## Install python 3.11 (MacOS for example)
1. brew install python@3.11
2. Run the command after installation to set path environment variable:
    ```
    echo 'export PATH="/opt/homebrew/bin/python3.11:$PATH"' >> ~/.zshrc
    ```
3. Open a new terminal and test: `python --version`

## Installation for dev
1. Copy `.env.exemple` to `.env` and edit values.
2. Open file 'grant_all.sql', change the username before '@' to the value of SQL_USER in .env
3. Run `docker compose up --build`
4. The container is working when you see `Quit the server with CONTROL-C.` in the ternimal widget.  
5. Create superuser : `docker exec -it drf-api python manage.py createsuperuser`
6. Visit `http://localhost:8888/admin`
7. Notes: To re-build the container: Remove the old container `docker compose down -v`, repeat 3, 4

## DB cache
It will create a folder `mysql` after first running

## Installation trouble shooting
1. Access denied for user '<DB_USERNAME>'@'localhost'
    ```
    Delete or remove the folder 'mysql', the cache.
    Check the file grant_all.sql
    Make sure the username before '@' is the same with the value of SQL_USER in .env
    Re-build or reinstall the container:
        `docker compose down -v`
        `docker compose up --build`
    ```

## Login DB with DB tools (MacOS and Sequel Ace for example)
1. Host: `localhost`
2. Username: <SQL_USER>
3. Password: <SQL_PASSWORD>
4. Port: `3316`

## Project structure
1. core
    ```
    settings.py: environment varialbes configuration
    urls.py: project routes and urls
    ```
2. notes
    ```
    migrations: DB migration files
    api_views.py: notes api views
    models.py: model note
    serializers.py: api view serializers
    tests.py: unit tests and integration tests
    urls.py: notes routes and urls
    ```
3. users
    ```
    api_views.py: users api views
    serializers.py: api view serializers
    tests.py: unit tests and integration tests
    urls.py: users routes and urls
    ```

## DB schema
1. notes_note: mapping model Note
2. auth_user: django built-in model 
3. authtoken_token: django built-in model

## Testing with postman
1. create an auth_user
    ```
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
    Response: 'Signup successfully'
    ```

2. login and get the user Token
    ```
    url: `http://localhost:8888/api/auth/login`
    type: POST
    body: raw
    data_type: json
    data_example: {
        "username": "bbb",       ## optinal, here could be email
        "password": "12345678"
    }
    Response: {"token": <token>}
    ```

3. create all notes (needs Token)
    ```
    url: `http://localhost:8888/api/notes/`
    headers: {Key: `Authorization`, Value: `Token <token>`}  ('Token'+ whitespace + <token>)
    type: GET
    Response: {
        {"id": 1, "content": "test1"},
        {"id": 2, "content": "test2"},
        ...
    }
    ```

4. create a note (needs Token)
    ```
    url: `http://localhost:8888/api/notes/`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: POST
    body: raw
    data_type: json
    data_example: {
        "content": "test1"
    }
    Response: 'Create the note: test1 successfully'
    ```

5. get a note (needs Token)
    ```
    url: `http://localhost:8888/api/notes/<int:id>`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: GET
    Response: {
        "id": 1,
        "content": "test1"
    }
    ```

6. update a note (needs Token)
    ```
    url: `http://localhost:8888/api/notes/<int:id>`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: PUT
    body: raw
    data_type: json
    data_example: {
        "content": "test3"
    }
    Response: {""Udate note id: 1 successfully"}
    ```

7. delete a note (needs Token)
    ```
    url: `http://localhost:8888/api/notes/<int:id>`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: DELETE
    Response: {""DELETE note id: 1 successfully"}
    ```

8. share a note with a user (needs Token)
    ```
    url: `http://localhost:8888/api/notes/<int:id>/share`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: POST
    body: raw
    data_type: json
    data_example: {
        "username": "<str:username>"
    }
    Response: {"Share the note: test2 with user: bbb successfully"}
    ```

9. Search the notes with keywords (needs Token)
    ```
    url: `http://localhost:8888/api/search/query`
    headers: {Key: `Authorization`, Value: `Token <token>`}
    type: GET
    Response: Response: {
        "id": 1,
        "content": "test1"
    }
    ```

## Unit tests and integration tests with pytest
3. Make sure the container 'drf-api' is running
2. Create virtual env folder at the project root directory`python -m venv venv`
3. Login venv: `source venv/bin/activate`
4. `pip install --upgrade pip`
5. `pip install -r requirements.txt`
6. `pytest`
7. Exit venv command: `deactivate`

## Pytest trouble shooting
1. No module named 'django'
    ```
    Delete or remove the folder 'venv', the cache.
    'venv' should sovle this issue. If still meet this problem,
    we coud run this command outside venv:
        pip install pytest-django
    Re-build venv
    ```
2. No module named 'decouple'
    ```
    Delete or remove the folder 'venv', the cache.
    'venv' should sovle this issue. If still meet this problem,
    we coud run this command outside venv:
        pip install python-decouple
    Re-build venv
    ```
3. Unknown MySQL server host 'db'
    ```
    Delete or remove the folder 'mysql', the cache.
    Delete or remove the folder 'venv', the cache.
    docker-compose.yml shoud solve this issue. I still met this
    problem during testing, because I had the other containers which
    was using mysql as well and it caused the conflicts. Make sure stop 
    the other mysql containers. And we need to clear or remove the images
    and volumns cache of the docker.
    Re-build the docker
    Re-build venv
    ```
4. Notes: we should open a new terminal widget after we do an update each time

If there is any problem, please contact me.