from flask import Blueprint
from infrastructure.controllers.create_category_controller import category_blueprint
from infrastructure.controllers.get_category_controller import get_category_blueprint

category_router = Blueprint('category_router', __name__)

category_router.register_blueprint(category_blueprint, url_prefix='/')
category_router.register_blueprint(get_category_blueprint, url_prefix='/')