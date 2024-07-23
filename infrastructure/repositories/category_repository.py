from pymongo import MongoClient
from domain.entities.category import Category

class CategoryRepository:
    def __init__(self, connection_string: str, db_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db['categories']
    
    def find_category(self, user_id: str, name: str):
        return self.collection.find_one({"user_id": user_id, "name": name})
    
    def add_category(self, category: Category):
        if not self.find_category(category.user_id, category.name):
            return self.collection.insert_one(category.dict())
        else:
            raise Exception("La categoría ya existe.")
        
    def find_categories_by_user(self, user_id: str):
        count = self.collection.count_documents({"user_id": user_id})
        if count == 0:
            raise ValueError("No se encontraron categorías o el usuario no existe.")
        categories = self.collection.find({"user_id": user_id})
        return [{**cat, '_id': str(cat['_id'])} for cat in categories] 