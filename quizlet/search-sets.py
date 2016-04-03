url = "https://api.quizlet.com/2.0/search/sets?" + "access_token=TfjqGPPaUTrDqeX33r2QmH8S5KndRBDDMBfnpEqq" + "&whitespace=1" + "&q="

q = "math"

def search_sets(term):
    result = url + q
    return result

