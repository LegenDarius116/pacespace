# Credits:
# Project: https://github.com/OrenBen-Meir/Meal-Spot
# Author: orenben-meir (Oren Ben Meir)


# in views, use function to check usertype by 
# user = request.user
# userTypeIs = userTypeChecker(user)
def user_typechecker(user):
    """Checks usertype of user"""
    return lambda user_type: len(user_type.objects.filter(user=user)) > 0


# when parsing request's body, hash to dict and convert symbols
symbol_dict = {
    "%21": "!",
    "%22": "\"",
    "%23": "#",
    "%24": "$",
    "%25": "%",
    "%26": "&",
    "%27": "\'",
    "%28": "(",
    "%29": ")",
    "%40": "@",
    "%E2": ""
}


def parse_req_body(body):
    """Organizes HTTP Request into a python dictionary"""
    body = body.decode('utf-8')
    pair_list = body.split('&')
    parsed_body = {}
    for pair in pair_list:
        pair = pair.split('=')

        for i in range(0,len(pair[1])):
            if i>=len(pair[1]):
                break
            if pair[1][i] == "%":
                symbol_key=""
                for c in range(0,3):
                    symbol_key += pair[1][i+c]
                if symbol_key in symbol_dict: 
                    symbol_map = symbol_dict[symbol_key]
                    pair[1] = pair[1].replace(symbol_key, symbol_map)

        parsed_body[pair[0]] = pair[1].replace('+',' ')
    return parsed_body
