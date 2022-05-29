from src.dependencies import get_search_machine


def add_to_index(index, model):
    if not (sm := get_search_machine()):
        return

    payload = {}
    field = "text"
    payload[field] = getattr(model, field)
    sm.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not (sm := get_search_machine()):
        return
    sm.delete(index=index, doc_type=index, id=model.id)


def query_index(index, query, page, per_page):
    if not (sm := get_search_machine()):
        return [], 0

    search = sm.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']
