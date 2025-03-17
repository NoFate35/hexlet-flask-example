def validate(product_data):
    errors = {}
    if not product_data.get('title'):
        errors['title'] = "Can't be blank"
    if int(product_data.get('price')) < 0:
        errors['price'] = "Can't be negative"
    return errors
