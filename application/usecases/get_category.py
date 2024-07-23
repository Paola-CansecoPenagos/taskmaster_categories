from infrastructure.repositories.category_repository import CategoryRepository

class GetCategoriesUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, user_id: str):
        return self.repository.find_categories_by_user(user_id)