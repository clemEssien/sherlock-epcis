
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