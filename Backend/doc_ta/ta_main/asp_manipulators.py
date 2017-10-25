from exceptions import IndexError, KeyError


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


def json_term_to_asp_string(json_term):
    try:
        param_list = json_term["params"]
        params_string = param_list[0]
        for i in range(1,len(param_list)):
            params_string += ',' + param_list[i]

        total_string = json_term["id"] + '(' + params_string + ')'
        return total_string
    except KeyError:
        return None


class ASPCodeGenerator():

    def __init__(self):
        self.result_facts = []
        self.hard_constraints = []
        self.soft_constraints = []

    def generate_default_object_definitions(self):
        return ''

    def generate_result_facts(self):
        result_string = ''
        for fact in self.result_facts:
            result_string += json_term_to_asp_string(fact) + ".\n"

        return result_string

    @staticmethod
    def generate_axiom_constraints():
        return ''

    def generate_hard_constraints(self):
        return ''

    def generate_soft_constraints(self):
        return ''

    @staticmethod
    def read_from_asp_result(result_src):
        f = open(result_src)
        data = f.read()
        f.close()
        return data

    @staticmethod
    def run_clingo(input_src, output_src):
        command_string = "./asp/clingo --outf=2 <" + input_src + ">" + output_src
        os.system(command_string)

    def generate_code(self, file_name):
        code_string = ''
        code_string += self.generate_default_object_definitions()
        code_string += self.generate_result_facts()
        code_string += self.generate_axiom_constraints()
        code_string += self.generate_hard_constraints()
        code_string += self.generate_soft_constraints()
        fd = open(file_name,'w+')
        fd.write(code_string)
        fd.close()

    def run(self,file_name='default_001'):
        self.generate_code(file_name)
        # TODO: make run_clingo function call async with cancellation token
        self.run_clingo(file_name + '.in', file_name + '.out')
        return self.read_from_asp_result(file_name + '.out')


class CodeGeneratorBuilder():

    def __init__(self):
        self.result_facts = []
        self.hard_constraints = []
        self.soft_constraints = []

    def with_result_facts(self,result_facts):
        if not result_facts:
            return
        self.result_facts = result_facts
        return self

    def with_hard_constraints(self, hard_constraints):
        if not hard_constraints:
            return
        self.hard_constraints = hard_constraints
        return self

    def with_soft_constraints(self, soft_constraints):
        if not soft_constraints:
            return
        self.soft_constraints = soft_constraints
        return self

    def build(self):
        code_generator = ASPCodeGenerator()
        code_generator.result_facts = [] + self.result_facts
        code_generator.hard_constraints = [] + self.hard_constraints
        code_generator.soft_constraints = [] + self.soft_constraints
        return code_generator
