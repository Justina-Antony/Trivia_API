import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginated_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)* QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [ques.format() for ques in selection]
    current_page=questions[start:end]

    return current_page

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.route('/')
    def hello():
        return jsonify({
            'message':'hello world jintu'
        })
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.all()

        if len(categories) == 0:
            abort(404)

        formated_categories = [cat.format() for cat in categories]
        return jsonify({
            'success':True,
            'categories': formated_categories,
            'total_categories': len(formated_categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_all_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.all()
        formated_categories = [cat.format() for cat in categories]
        current_questions = paginated_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success':True,
            'questions': list(current_questions),
            'total_questions': len(questions),
            'categories': formated_categories,
            'current_category': None
        })
    


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.all()
            current_questions = paginated_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions':len(Question.query.all())
            })
        except:
            abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def add_questions():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
       

        try:
            question = Question(new_question, new_answer, new_category, new_difficulty)
            question.insert()
            selection = Question.query.all()
            current_questions = paginated_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions':len(Question.query.all())
            })
        except:
            abort(422)
        
        
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def serach_question():
        search_term = request.args.get('search')
        # search_term = 'in'
        question = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        current_questions = paginated_questions(request, question)

        if search_term is None:
            abort(404)

        return jsonify({
            'success':True,
            'questions':list(current_questions),
            'total_questions':len(Question.query.all())
        })
    
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):

        try:
            question = Question.query.filter(Question.category==category_id).all()

            if len(question) == 0:
                abort(404)

            current_questions= paginated_questions(request, question)
            categories = Category.query.all()

            return jsonify({
                'success':True,
                'questions':list(current_questions),
                'total_questions':len(question),
                'current_category': [cat.format() for cat in categories if cat.id == category_id]
            })
        
        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():

        try:
            body = request.get_json()
            selected_category = body.get('quizCategory')
            previous_question = body.get('previousQuestions')
            category_id = selected_category['id']
            ques = None

            if(category_id == 0):
                questions = Question.query.filter(Question.id.notin_(previous_question)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_question), Question.category==category_id).all()

            if(questions):
                ques = random.choice(questions)

            return jsonify({
                'success': True,
                'question':ques.format()
            })
        
        except:
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error":404,
            "message":"resource not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            "success": False,
            "error":422,
            "message":"resource cannot be processed"
        }), 422
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app

app = Flask(__name__)
if __name__ == "__main__":
    app=create_app()
    app.run(debug=True)