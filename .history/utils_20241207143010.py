import json

def match_x(sentences_file, identifiers_file):
    with open(sentences_file, 'r') as f:
        sentences_data = json.load(f)
    
    with open(identifiers_file, 'r') as f:
        identifiers_data = json.load(f)
    
    matched_data = {}
    for identifier, sentences in sentences_data.items():
        if identifier in identifiers_data:
            matched_data[identifier] = [{"x": sentence} for sentence in sentences]
    return matched_data

def match_y(sentences_file, identifiers_file):

    with open(sentences_file, 'r') as f:
        sentences_data = json.load(f)
    
    with open(identifiers_file, 'r') as f:
        identifiers_data = json.load(f)
    
    matched_data = {}
    for identifier, id_values in identifiers_data.items():
        if identifier in sentences_data:
            matched_data[identifier] = [{"y": id_value} for id_value in id_values]
    return matched_data

def get_data(matched_x, identifier):
    if identifier not in matched_x:
        raise KeyError(f"Identifier '{identifier}' not found in the dataset.")
    return [item["x"] for item in matched_x[identifier]]

def get_labels(matched_y, identifier):
    if identifier not in matched_y:
        raise KeyError(f"Identifier '{identifier}' not found in the dataset.")
    return [item["y"] for item in matched_y[identifier]]




if __name__ == "__main__":
## Test case for getting data and labels, paths are hardcoded
    
    matched_x=match_x(sentences_file='sentences.json', identifiers_file='identifiers.json')
    matched_y=match_y(sentences_file='sentences.json', identifiers_file='identifiers.json')
    print(get_data(matched_x, 'PTgdWWK2SPQ'))
    print(get_labels(matched_y, 'PTgdWWK2SPQ'))