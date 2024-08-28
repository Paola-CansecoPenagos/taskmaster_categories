# infrastructure/controllers/create_category_controller.py
from flask import Blueprint, request, jsonify
from application.usecases.create_category import CreateCategoryUseCase
from infrastructure.repositories.category_repository import CategoryRepository
from utils.text_utils import escape_javascript, escape_html, trim_text
from infrastructure.services.rabbitmq_producer import send_verification_request
import threading
import json
from threading import Condition

category_blueprint = Blueprint('category', __name__)
repository = CategoryRepository()
create_category_usecase = CreateCategoryUseCase(repository=repository)

condition = Condition()
verification_result = {}

def handle_user_verification_response(response):
    with condition:
        verification_result['exists'] = response.get('exists', False)
        verification_result['user_id'] = response.get('user_id')
        condition.notify()

@category_blueprint.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    user_token = request.headers.get('Authorization', '').split(' ')[1]

    data['name'] = escape_html(data['name'])
    data['name'] = escape_javascript(data['name'])
    data['name'] = trim_text(data['name'])

    with condition:
        # Start a new thread to handle the asynchronous response
        thread = threading.Thread(target=send_verification_request, args=(
            user_token, 
            'response_queue', 
            handle_user_verification_response
        ))
        thread.start()
        condition.wait(timeout=10)  # wait for the verification to complete or timeout

    if verification_result.get('exists', False):
        try:
            result = create_category_usecase.execute(user_id=verification_result['user_id'], name=data['name'])
            return jsonify({"message": "Categoría creada exitosamente"}), 200
        except ValueError as e:
            print(f"Error de validación: {str(e)}") 
            return jsonify({"error": "La creación de la categoría falló debido a una entrada inválida"}), 400
        except Exception as e:
            print(f"Error inesperado: {str(e)}")  
            return jsonify({"error": "Ocurrió un error inesperado"}), 500
    else:
        return jsonify({"error": "Usuario no encontrado o verificación fallida"}), 404
