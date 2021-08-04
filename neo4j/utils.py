import json

def string_btw_xters(string, initial, terminating)->str:
    '''
    method returns the string in between two characters
    Args:
        string: str
        initial character: str
        terminal character: str
    '''
    start = string.find(initial) + len(initial)
    end = string.find(terminating)
    return string[start:end]

def verify_algo_args(sample_size, seed):
    if isinstance(sample_size, int) and isinstance(seed, int):
            if sample_size >0 and seed >=0:
                return True;
    return False  

def algorithm_response(response):
    result = {}
    if response and len(response) >1:
        for record in response:
            result[record['name']] = record['score']    
    return result

def format_attr_dict(attr_dict):
    attr_dict = attr_dict.split()
    new_attr_dict = ""
    for item in attr_dict:
        if '":' in item:
            new_attr_dict += item.replace('"', ' ')
        elif '[]' in item:
            new_attr_dict += item.replace('[]', '\"\"')
        else:
            new_attr_dict += item
    return new_attr_dict

def retrive_attr_dict_from_event(event):
    attributes = {}
    for attr in list(event.__dict__):
        instvar = getattr(event, attr)
        if isinstance(instvar, dict):
            attributes[attr[1:]] = json.dumps(getattr(event, attr))
        else:
            attributes[attr[1:]] = getattr(event, attr)
        attributes["name"] = event.__class__.__name__ 
    return attributes