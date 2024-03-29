

def filter_data(_object: list, **kwargs):
    filtered_object = _object
    for k, v in kwargs.items():
        if not v:
            continue
        if k == 'user_id':
            k = 'id'
        filtered_object = [i for i in filtered_object if i[k] == v]
    return filtered_object
