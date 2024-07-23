def validate_category_name(name: str):
    if not (3 <= len(name) <= 25):
        raise ValueError("El nombre de la categoría debe tener entre 3 y 25 caracteres.")
