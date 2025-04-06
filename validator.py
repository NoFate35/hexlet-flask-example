def validate(product_data):
    errors = {}
    if not product_data.get('title'):
        errors['title'] = "Can't be blank"
    if int(product_data.get('price')) < 0:
        errors['price'] = "Can't be negative"
    return errors

SPAM_WORDS = ["spam", "реклама"]
TRIGGER_WORDS = ["http", "https"]


def check_spam(text):
    print("textgggggg:", text )
    text = text.lower()
    return any(word in text for word in SPAM_WORDS)


def check_triggers(text):
    text = text.lower()
    return any(word in text for word in TRIGGER_WORDS)
