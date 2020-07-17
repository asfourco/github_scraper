def get_fields(model):
    return [field.name for field in model._meta.get_fields()]
