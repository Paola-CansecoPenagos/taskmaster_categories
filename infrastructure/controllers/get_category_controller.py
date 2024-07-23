from flask import Blueprint, request, jsonify
from application.usecases.get_category import GetCategoriesUseCase
from infrastructure.repositories.category_repository import CategoryRepository
from infrastructure.services.jwt_service import decode_access_token

get_category_blueprint = Blueprint('get_category', __name__)

repository = CategoryRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterCat')
get_categories_usecase = GetCategoriesUseCase(repository=repository)

@get_category_blueprint.route('/categories', methods=['GET'])
def get_categories():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No se proporcionó ningún token de autorización"}), 401

    token = auth_header.split(' ')[1]
    user_info = decode_access_token(token)
    if not user_info:
        return jsonify({"error": "Token no válido o caducado"}), 401

    user_id = user_info.get('user_id')
    if not isinstance(user_id, str):
        return jsonify({"error": "Formato de ID de usuario no válido"}), 400
    
    try:
        categories = get_categories_usecase.execute(user_id)
        return jsonify(categories), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
