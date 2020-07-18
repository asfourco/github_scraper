# TODO

My collectio of some ideas for improvements or fixes that need addressing.

## Issues
1. [Issue] - when looking up a model with dict of data, model.objects.update_or_create() or model.objects.get_or_create() returned multiple of objects causing an exception, despite the models having primary_keys. Either the primary_keys are not recognised by Django or this another configuration error.

## Enhancements
1. [Enhancement] - add user_repo next_url endpoints to have a more complete service
1. [Enhancement] - Investigate other db structures, for example by using MongoDB to store user and their repos without any manipulation of the data, i.e., allow for nesting of sub-documents
1. [Enhancement] - Break up the scraping endpoints eacho into two parts: command start - initiates the scraping, command status - reports on the status of the scraping. Avoids keeping the connection open