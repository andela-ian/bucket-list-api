def list_object_transform(list_data):
    """Tranforms list of query objects into a dictionary of dictionaries.
    """
    result_data = []
    for item in list_data:
        # import pdb; pdb.set_trace()
        if callable(getattr(item, 'to_json')):
            result_set = item.to_json()
        result_data.append(result_set)
    return result_data
