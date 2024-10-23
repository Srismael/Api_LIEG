def validate_product(data):
    required_fields = ['name', 'price', 'description', 'stock', 'category']
    for field in required_fields:
        if field not in data:
            return False
        if not isinstance(data[field], str) and field != 'price' and field != 'stock':
            return False
        if field == 'price' or field == 'stock':
            if not isinstance(data[field], (int, float)):
                return False
    return True
