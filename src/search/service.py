from src.dependencies import get_search_machine


def add_to_index(index, model):
    sm = get_search_machine()

    if not sm:
        return

    payload = {}
    field = "text"
    payload[field] = getattr(model, field)
    sm.index(index=index, id=model.id, body=payload)


# def remove_from_index(index, model):
#     if not current_app.elasticsearch:
#         return
#     current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)
#
# def query_index(index, query, page, per_page):
#     if not current_app.elasticsearch:
#         return [], 0
#     search = current_app.elasticsearch.search(
#         index=index, doc_type=index,
#         body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
#               'from': (page - 1) * per_page, 'size': per_page})
#     ids = [int(hit['_id']) for hit in search['hits']['hits']]
#     return ids, search['hits']['total']