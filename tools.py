def list_object_transform(list_data):
    result_data = []
    for item in list_data:
        result_set = item.to_json()
        result_data.append(result_set)
    return result_data
