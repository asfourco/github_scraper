Some ideas on what other improvements or fixes that need addressing


1. [Issue] - when looking up a model with dict of data, model.objects.update_or_create() or model.objects.get_or_create() returned multiple of objects causing an exception, despite the models having primary_keys. Either the primary_keys are not recognised by Django or this another configuration error.
2. [Enhancement] - add user_repo next_url endpoints to have a more complete service