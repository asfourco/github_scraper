def get_fields_of_model(model):
    return [field.name for field in model._meta.get_fields()]
