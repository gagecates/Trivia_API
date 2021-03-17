import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, all_questions):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    page_questions = questions[start:end]

    return page_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder='./starter/frontend/build', static_url_path='/')
    setup_db(app)


    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response


    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    


    @app.route('/play')
    def play():
        console.log('heyyyyy')
        return app.send_static_file('index.html')


    @app.route('/add')
    def add():
        return app.send_static_file('index.html')


    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.type).all()

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    

    @app.route('/questions')
    def retrieve_questions():
        all_questions = Question.query.order_by(Question.id).all()
        page_questions = paginate_questions(request, all_questions)
        categories = Category.query.order_by(Category.type).all()

        if len(page_questions) == 0:
            abort(400)

        return jsonify({
            'success': True,
            'questions': page_questions,
            'total_questions': len(all_questions),
            'categories': {category.id: category.type for category in categories},
        })

    

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                'question deleted': question_id
            })
        except BaseException:
            abort(422)
    

    @app.route('/questions/add', methods=['POST'])
    def add_question():
        try:
            question_data = request.get_json()

            new_question = question_data.get('question')
            new_answer = question_data.get('answer')
            new_difficulty = question_data.get('difficulty')
            new_category = question_data.get('category')

            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category,
            )

            Question.insert(question)

            return jsonify({
                'success': True,
                'question_added': question.id,
            })

        except BaseException:
            abort(422)

    

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_data = request.get_json()
        search_term = search_data.get('searchTerm')

        try:
            all_questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            search_results = paginate_questions(request, all_questions)

            if len(search_results) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': search_results,
                'total_questions': len(all_questions),
                'current_category': None
            })

        except BaseException:
            abort(404)

    

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):

        try:
            all_questions = Question.query.filter(
                Question.category == category_id).all()
            search_results = paginate_questions(request, all_questions)

            return jsonify({
                'success': True,
                'questions': search_results,
                'total_questions': len(all_questions),
                'current_category': category_id
            })

        except BaseException:
            abort(404)

    

    @app.route('/quizzes', methods=['POST'])
    def play_game():

        try:
            request_data = request.get_json()
            category = request_data.get('quiz_category')
            previous_question = request_data.get('previous_questions')

            if category['id'] == 0:
                initial_question_count = len(Question.query.filter.all())
                questions = Question.query.filter(
                            Question.id.notin_(previous_question)).all()

            else:
                initial_question_count = len(Question.query.filter(Question.category == category['id']).all())
                questions = Question.query.filter(
                            Question.category == category['id'],
                            Question.id.notin_(previous_question)).all()

            if len(questions) == 0:
                question = {} 
                last_question = True

            else:
                last_question = False
                question = random.choice(questions).format()
            
            


            return jsonify({

                'success': True,
                'question': question,
                'last_question': last_question

            })

        except:
            abort(400)

    

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'

        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'

        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'

        }), 422

    return app

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
