# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

API DOCUMENTATION

Getting Started:

1. Base URL: The backend app is hosted at the default port, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
2. Authentication: This application does not require authentication.

Endpoints:

`GET /categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Returns all the available categories, success value, and total number of categories.

Example: `curl --location 'localhost:5000/categories'`

Sample Response:

```json
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        }
    ],
    "success": true,
    "total_categories": 6
}
```

`GET /questions`

- Fetches a dictionary of questions, paginated in group of 10
- Returns a list of all questions, success value, total number of questions, current category and list of all the categories.

Example: `curl --location 'localhost:5000/questions'`

Sample Response:

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    }
  ],
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```

`DELETE /questions/<int:question_id>`

- Delete the selected question based on the question id
- Returns the success value, deleted question id, list of all the questions available paginated in group of 10 and total number of questions.

Example: `curl --location --request DELETE 'localhost:5000/questions/27'`

Sample Response:

```json
{
    "deleted": 27,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

`POST /questions`

- Creates a new question using the submitted question, answer, difficulty and category. 
- Returns the id of the created question, success value, total questions, and list of all the questions available paginated in group of 10

Example: `curl --location 'localhost:5000/questions' \
--header 'Content-Type: application/json' \
--data '{
    "question":"what is your favorite color?",
    "answer":"pink",
    "difficulty": 1,
    "category": 5
}'`

Sample Request:

```json
{
    "question":"what is your favorite sport?",
    "answer":"tennis",
    "difficulty": 1,
    "category": 6
}
```

Sample Response:
```json
{
    "created": 29,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "success": true,
    "total_questions": 22
}
```

`POST /questions/search`

- Fetches a dictionary of questions based on the search term submitted in the frondend
- Returns the list of all questions, success value and total number of questions.

Example: `curl --location --request POST 'localhost:5000/questions/search'`

Sample Response:

```json
{
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "success": true,
    "total_questions": 22
}
```

`GET /categories/<int:category_id>/questions`

- Fetches a dictionary of questions based on the category id
- Returns the list of all questions, success value and total number of questions and current category selected.

Example: `curl --location 'localhost:5000/categories/6/questions'`

Sample Response:

```json
{
    "current_category": [
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```

`POST /quizzes`

- This endpoint takes the selected category and previous question parameters.
- Returns a random questions within the selected category for the quiz and success value. 

Example: `curl --location 'localhost:5000/quizzes' \
--header 'Content-Type: application/json' \
--data '{
    "quizCategory":{
        "id":4
    },
    "previousQuestions":[2,5,9,4]
}'`

Sample Request:

```json
{
    "quizCategory":{
        "id":4
    },
    "previousQuestions":[2,5,9,4]
}
```

Sample Response:

```json
{
    "question": {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
    },
    "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
