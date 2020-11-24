# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


API Endpoints


GET '/questions'

- Fetches a dictionary of questions in wich keys are the ids and the   value is the corresponding string of the category.
- Arguments: Page #
- Returns JSON:({
    'success': (true/false)
    'qeuestions': list of paginated questions as dictonaries
    'total_questions': length of qestions
    'categories': categories as dictonaries
})


DELETE '/questions/<question_id>'

- Deletes specific question.
- Arguments: Question id
- Returns JSON:({
    'success': (true/false)
    'question_deleted': id of question deleted

})
    

POST '/questions/add'

-  Adds a new question as a dictonary to the list of question
- Arguments: 
    new_question
    new_answer
    new_difficulty
    new_category

- Returns JSON:({
    'success': (true/false)
    'question_added': Newly created question's id

})
    

POST '/questions/search'

- Fetches a list of questions based on a specific search term.
- Arguments: Search term
- Returns JSON:({
    'success': (true/false)
    'question': queried question matching search term
    'total_questions': integer
    'current_category': current category id

})
    

GET '/categories/<int:category_id>/questions'

- Fetches a dictionary of questions based on a specific category
- Arguments: Category id
- Returns JSON:({
    'success': (true/false)
    'questions': list of paginated questions
    'total_questions': integer
    'current_category': category id

})
    

POST '/quizzes'

- Plays the Trivia game.
- Arguments:
    previous questions: list of question id's already used
    quiz_category: category id picked by user

- Returns JSON:({
    'sucess': (true/false)
    'question': list of paginated questions
    'last_question': (true/false)

})
    

errorhandler(400)

- Bad request error
- Returns JSON:({
    success value: (true/false)
    error: 400
    message: 'bad request'
})

errorhandler(404)

- Not found error
- Returns JSON:({
    success value: (true/false)
    error: 404
    message: 'resource not found'
})

errorhandler(422)

- Unprocessable error
- Returns JSON:({
    success value: (true/false)
    error: 422
    message: 'unprocessable'
})
