import models as ta_models
import json
import asp_manipulators


# Generates code from specified objects
class ASPCodeGenerator():
    # define term 1 as programming, MM, discrete, logic, hardware
    term_1 = [120, 145, 142, 140, 112]

    def __init__(self):
        self.result_facts = []
        self.hard_constraints = []
        self.soft_constraints = []
        self.should_generate = True

# define base objects like lectures, timeslots and etc
    def generate_default_object_definitions(self):
        obj_def_string = ""
        # TODO: does not get all rooms but selected
        for room in ta_models.Room.objects.all():
            obj_def_string += room.to_asp() + '.\n'

        for timeslot in ta_models.Timeslot.objects.all():
            obj_def_string += timeslot.to_asp() + '.\n'

        for subject in ta_models.Subject.objects.all():
            if subject.code in self.term_1:
                obj_def_string += subject.to_asp() + '.\n'

        return obj_def_string.lower()

# Optional step which is used when you want to define that some
# classes have exactly given positions (for check or when u have partial table set to auto-complete)
    # pre: LectureClass obj array in result_Facts
    def generate_result_facts(self):
        result_string = ""
        for fact in self.result_facts:
            result_string += fact.to_asp().lower() + ".\n"

        return result_string

    def generate_axiom_constraints(self):
        axiom_constraints_string = " "
        # return "0 { class(T,R,D,S) } 1 :- room(R,_), timeslot(D,S),subject(T,_,_)." + \
        for subject in ta_models.Subject.objects.all():
            if subject.code in self.term_1:
                axiom_constraints_string += asp_manipulators.number_of_hours_asp(subject)
        return axiom_constraints_string
        # return "class_has_enough_hours(T):- 3 { class(T,_,_,_) } 3 , subject(T,_,_)."

    def generate_hard_constraints(self):
        return ":- not class_has_enough_hours(T), subject(T,_,_).\n" + \
               ":- class(T1,R,D,S), class(T2,R,D,S),room(R,_),T1!=T2.\n"

    def generate_soft_constraints(self):
        return ""

# Method to read from a asp_solutions
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

# method which runs the stages of code generation
    def generate_code(self, file_name):
        code_string = ''
        code_string += self.generate_default_object_definitions()
        code_string += self.generate_result_facts()
        # checks if we need want to generate classes or just check whether current is ok
        if self.should_generate:
            code_string += "0 { class(T,R,D,S) } 1 :- room(R,_), timeslot(D,S),subject(T,_,_).\n"
        code_string += self.generate_axiom_constraints()
        code_string += self.generate_hard_constraints()
        code_string += self.generate_soft_constraints()
        # generate result we are interested in(class objects)
        code_string += "#show class/4."
        # writes the code to file
        fd = open(file_name,'w+')
        fd.write(code_string)
        fd.close()

    def run(self,file_name='default_001'):
        self.generate_code(file_name)
        # TODO: make run_clingo function call async with cancellation token
        self.run_clingo(file_name + '.in', file_name + '.out')
        return self.read_from_asp_result(file_name + '.out')


# Parses json result as list of solutions in json format suitable for frontend display
    def parse_result(self,file_name):
        data = self.read_from_asp_result(file_name)
        data_dict = json.loads(data)
        all_results = data_dict["Call"][0]["Witnesses"]

        tokenized_results = {"results": []}
        for result in all_results:
            asp_terms = []
            for item in result["Value"]:
                asp_terms.append(asp_manipulators.tokenize_asp_term(item))

            tokenized_results["results"].append(asp_terms)

        json_solutions = []
        for solution in tokenized_results["results"]:
            actual_json = []
            for lecture_class in solution:
                actual_json.append(ta_models.LectureClass().from_asp(lecture_class).to_json_for_frontend())

            json_solutions.append(actual_json)
        # code_result = read_from_asp_result('default_001.in')
        return json.dumps(json_solutions)


# Returns only result status of a asp
    def get_result_status(self,file_name):
        data = self.read_from_asp_result(file_name)
        data_dict = json.loads(data)
        return data_dict["Result"]


# Build pattern for the code generator to define which constraints
# facts, and object definitions to have
class CodeGeneratorBuilder():
    def __init__(self):
        self.result_facts = []
        self.hard_constraints = []
        self.soft_constraints = []
        self.should_generate = True

    def with_result_facts(self, result_facts):
        if not result_facts:
            return
        self.result_facts = result_facts
        self.should_generate = False
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
        code_generator.should_generate = self.should_generate
        return code_generator