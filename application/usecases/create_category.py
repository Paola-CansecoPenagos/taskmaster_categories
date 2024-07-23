from infrastructure.repositories.category_repository import CategoryRepository
from domain.entities.category import Category
from domain.validations.category_validation import validate_category_name

class CreateCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, user_id: str, name: str):
        validate_category_name(name)
        
        category = Category(user_id=user_id, name=name)
        return self.repository.add_category(category)
