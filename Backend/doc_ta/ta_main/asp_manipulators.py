from exceptions import IndexError, KeyError


# Generates rule for hours per week needed to be taken defined by a Subject model
def number_of_hours_asp(subject_model):
    # TODO: refactor to much hardoded dependencies among objects
    asp_string = "class_has_enough_hours(" + subject_model.title_asp + ') ' + ":- "
    asp_string += str(subject_model.hours) + "{ class(" + subject_model.title_asp + ",_,_,_) } "
    asp_string += str(subject_model.hours) + " .\n"
    return asp_string


# Parses a asp term from id(param,param..) format to a json object
def tokenize_asp_term(term):
    # split to parts before and after opening bracket
    try:
        tokens = term.split('(')
        id = tokens[0]
        # gets everything until closing bracket
        params_string = tokens[1].split(')')
        # tokenizes params from commas
        params = params_string[0].split(',')
        return {"id": id, "params": params}
    except IndexError:
        return None


# Inverse function of tokenize_asp_term
def json_term_to_asp_string(json_term):
    try:
        param_list = json_term["params"]
        params_string = param_list[0]
        for i in range(1,len(param_list)):
            params_string += ',' + str(param_list[i])

        total_string = json_term["id"] + '(' + params_string + ')'
        return total_string
    except KeyError:
        return None

