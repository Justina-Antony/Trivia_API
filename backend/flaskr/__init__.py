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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

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


    @app.route('/questions', methods=['POST'])
    def add_questions():
        body = request.get_json()
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')
       
        if None in (body.get('question'),body.get('answer'), body.get('category'), body.get('difficulty')):
            abort(422)

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
            abort(404)

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