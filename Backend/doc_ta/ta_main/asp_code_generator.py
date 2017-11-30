import models as ta_models
import os
import json
import asp_manipulators
from asp_constraints import basic_constraint as constraint
from exceptions import TypeError
from asp_constraints import ConstraintHandler as Constraints

class CodeGeneratorException(Exception):
    pass


# PRE: type(current) = string ,
# PRE: new has to_asp() function
def append_new_definition(current, new):
    return current + new.to_asp() + '.\n'


# Generates code from specified objects
class ASPCodeGenerator():

    def __init__(self):
        self.table_def = ta_models.TableSizeDef.objects.all().first()
        self.check_subject = "architecture"
        self.term = ""             # term to be generated on
        self.subjects = []         # subjects which belong to the term
        self.result_facts = []
        self.hard_constraints = []
        self.soft_constraints = []
        self.should_generate = True
        self.status = ""
        self.file_name = "default_001"

# define base objects like lectures, timeslots and etc
    def generate_default_object_definitions(self):
        obj_def_string = ""
        # TODO: does not get all rooms but selected
        for room in ta_models.Room.objects.all():
            obj_def_string += room.to_asp() + '.\n'

        # Gets the timeslots asociated with the table size definitions
        all_daydefs = ta_models.DayDef.objects.filter(table=self.table_def)
        timeslots = []
        for daydef in all_daydefs:
            for ts in ta_models.Timeslot.objects.filter(day=daydef):
                timeslots.append(ts)

        for timeslot in timeslots:
            obj_def_string += timeslot.to_asp() + '.\n'

        for course in ta_models.CourseYear.objects.all():
            obj_def_string += course.to_asp();

        for subject in self.subjects:
            obj_def_string += subject.to_asp() + '.\n'

            # finds all the courses this subject belongs to
            courses_it_belongs = ta_models.SubjectsCourses.objects.filter(subject=subject)
            for course in courses_it_belongs:
                obj_def_string = append_new_definition(obj_def_string, course)

            # find all lecturers that teach the course
            teachings = ta_models.Teaches.objects.filter(subject=subject)
            for teaching in teachings:
                obj_def_string = append_new_definition(obj_def_string, teaching)

        # generate clashes
        for clash in ta_models.Clash.objects.all():
                obj_def_string = append_new_definition(obj_def_string, clash)

        return obj_def_string.lower()

# Optional step which is used when you want to define that some
# classes have exactly given positions (for check or when u have partial table set to auto-complete)
    # pre: LectureClass obj array in result_Facts
    def generate_result_facts(self):
        result_string = ""
        for fact in self.result_facts:
            result_string += fact.to_asp().lower() + ".\n"
            # generate blocker for already existing if checking for available slots
            if self.status == "CHECKSLOTS" and fact.subject.title_asp == self.check_subject:
                result_string += 'start_loc(' + str(fact.time_slot.day.day_asp) + ',' + str(fact.time_slot.hour) + ').\n'

        return result_string

    def generate_axiom_constraints(self):
        axiom_constraints_string = " "
        # remove constraint to generate enough hours for all subjects
        if self.status == "CHECKSLOTS":
            self.hard_constraints.remove("Each class to have enough hours.")

        for constraint in self.hard_constraints:
            axiom_constraints_string += Constraints.constraint_creator(constraint)

        axiom_constraints_string += "1 { slot_occupied(D,S,Y) } 1 :- class_with_year(_,_,D,S,Y).\n" + \
                                    "1 { day_occupied(T,D) } 1 :- class_with_year(T,_,D,_,Y).\n"

        if self.status != "CHECKSLOTS":
            axiom_constraints_string += "class_with_year(T,R,D,S,Y) :- class(T,R,D,S), subjectincourse(T,Y).\n"
        else:
            T = self.check_subject
            # has enough hours of subjects
            H = 0 # class hours needed
            # count how many times you have as fact and get 1 more
            for fact in self.result_facts:
                if fact.subject.title_asp == T:
                    H = H +1

            H = H + 1
            H = str(H)
            # class ahs enough hours (1 + existing)
            axiom_constraints_string += "not_class_has_enough_hours("+ T + ") :- not " + H +" { class_with_year(" + T + ",_,_,_,_) } " + H + ".\n "
            axiom_constraints_string += ":- not_class_has_enough_hours("+ T + ").\n"
            # generate only of type subject
            axiom_constraints_string += "0 { class("+T + ",R,D,S) } 1:- room(R,_),timeslot(D,S).\n"
            axiom_constraints_string += "class_with_year(" + T + ",R,D,S,Y) :- class(" + T + ",R,D,S),subjectincourse(" + T +",Y).\n"
            # generate result
            axiom_constraints_string += "possible_locations(D,S):- class_with_year(" + T + ",R,D,S,Y), not start_loc(D,S).\n"
        return axiom_constraints_string

    def generate_hard_constraints(self):

        result_string = ""
        # generate hard constraint negators if generating
        if self.status == "GENERATE" or self.status == "CHECKSLOTS":
            for constraint in self.hard_constraints:
                result_string += Constraints.constraint_negator(constraint)

        return result_string

    def generate_soft_constraints(self):
        return ""

# Method to read from a asp_solutions
    @staticmethod
    def read_from_asp_result(result_src):
        f = open(result_src)
        data = f.read()
        f.close()
        return data

    def run_clingo(self,input_src=None,output_src=None):
        if input_src is None:
            input_src = self.file_name+'.in'
        # takes inputs source and gets the name before "." for the out file
        if output_src is None:
            output_src = str(input_src).split('.')[0] + '.out'
        if self.status != "CHECKSLOTS":
            command_string = "./asp/clingo --outf=2 <" + './' + input_src + ">" + './' + output_src
        else:
            command_string = "./asp/clingo  -n 0 --outf=2 <" + './' + input_src + ">" + './' + output_src
        os.system(command_string)

    def select_subjects_from_term(self):
        # fetches the model of the term
        selected_term = ta_models.Term.objects.filter(name=self.term).first()
        if selected_term is None:
            raise CodeGeneratorException("Term Does Not Exist")

        subjects_queryset = ta_models.ClassTerm.objects.filter(term=selected_term)
        for class_term in subjects_queryset:
            self.subjects.append(class_term.subject)

# method which runs the stages of code generation
    def generate_code(self, file_name=None):
        # if call does not specify the file use the filed defined on creation
        if file_name is None:
            file_name = self.file_name + '.in'

        code_string = ''
        self.select_subjects_from_term()
        code_string += self.generate_default_object_definitions()
        code_string += self.generate_result_facts()
        # checks if we need want to generate classes or just check whether current is ok
        if self.should_generate:
            code_string += "0 { class(T,R,D,S) } 1 :- room(R,_), timeslot(D,S),subject(T,_,_).\n"
        code_string += self.generate_axiom_constraints()
        code_string += self.generate_hard_constraints()
        code_string += self.generate_soft_constraints()
        # generate result we are interested in(class objects)
        if self.status != "CHECKSLOTS":
            code_string += "#show class_with_year/5.\n"
        else: # for CHECKSLOTS show the possible locations
            code_string += "#show possible_locations/2.\n"
        # ask to display facts generated from violations when checking
        if self.status == "CHECK":
            for constraint in self.hard_constraints:
                code_string += Constraints.constraint_show(constraint)
        # writes the code to file
        fd = open(file_name,'w+')
        fd.write(code_string)
        fd.close()

    def run(self,file_name='default_001'):
        self.generate_code()
        # TODO: make run_clingo function call async with cancellation token
        self.run_clingo(file_name + '.in', file_name + '.out')
        # return self.read_from_asp_result(file_name + '.out')


# Parses json result as list of solutions in json format suitable for frontend display
# Returns: (success, array of solutions if generating/array of violations if checking)
    def parse_result(self,file_name=None):
        # if call does not specify the file use the filed defined on creation
        if file_name is None:
            file_name = self.file_name + '.out'
        data = self.read_from_asp_result(file_name)
        data_dict = json.loads(data)
        # check if there are solutions
        result_status = data_dict["Result"]
        if result_status == "UNSATISFIABLE" or result_status == "UNKNOWN":
            return False, []

        all_results = data_dict["Call"][0]["Witnesses"]

        # gets from string to json format of id and params for each solution
        tokenized_results = []
        for result in all_results:
            asp_terms = []
            for item in result["Value"]:
                asp_terms.append(asp_manipulators.tokenize_asp_term(item))

            tokenized_results.append(asp_terms)

        # IF IT IS CHECKER ONLY NEED TO SEE IF GENERATED CONSTRAINTS
        if self.status == "CHECK":
            json_solutions = []
            constraint_violations = []
            for solution in tokenized_results:
                # for every solution parse
                for lecture_class in solution:
                    if lecture_class["id"] != "class_with_year":
                        constraint_violations.append(lecture_class)
                # parses to readable string the violations the checker has generated
                parsed_violations = []
                metadata = []
                if len(constraint_violations) != 0:
                    parsed_violations = self.parse_violations(constraint_violations)
                    metadata = self.parse_metadata(constraint_violations)
                json_solutions.append({"violations":parsed_violations,"metadata":metadata})

            return True, json_solutions

        # IF IT IS GENERATING NO NEED TO CHECK FOR CONSTRAINTS
        elif self.status == "GENERATE":
            json_solutions = []
            for solution in tokenized_results:
                result_array = []
                # for every solution parse
                for lecture_class in solution:
                        result_array.append(ta_models.LectureClass().from_asp(lecture_class,self.table_def).to_json_for_frontend())

                json_solutions.append(result_array)
            # code_result = read_from_asp_result('default_001.in')
            return True, json_solutions

        elif self.status == "CHECKSLOTS":
            json_solutions = []
            for solution in tokenized_results:
                for possible_slot in solution:
                    json_solutions.append({"day":possible_slot["params"][0],"time":possible_slot["params"][1]})

            return True, json_solutions
# Returns only result status of a asp
    def get_result_status(self,file_name=None):
        if file_name is None:
            file_name = self.file_name + '.out'
        data = self.read_from_asp_result(file_name)
        data_dict = json.loads(data)
        return data_dict["Result"]

    def parse_violations(self,violation_terms):
        notification_list = []

        for violation in violation_terms:
            notification_list.append(Constraints.constraint_parse(violation["id"], violation["params"]))

        return notification_list

    def parse_metadata(self, violation_terms):
        metadata_list = []

        for violation in violation_terms:
            metadata_item = Constraints.constraint_metadata(violation["id"], violation["params"])
            if metadata_item is not None:
                metadata_list.append(metadata_item)

        return metadata_list

# Build pattern for the code generator to define which constraints
# facts, and object definitions to have
class CodeGeneratorBuilder():
    def __init__(self):
        self.table = None
        self.subject_to_check = None
        self.selected_term = ""
        self.result_facts = []
        # Default hard constraints are all the defined keys in the verbose map table
        self.hard_constraints = Constraints.constraint_table_parse_verbose.keys()
        self.soft_constraints = []
        self.should_generate = True
        self.status = ""

    def for_subject(self,subject_name):
        self.subject_to_check = subject_name

    def for_table(self,table_id):
        self.table = ta_models.SavedTable(id=table_id)

    def for_term(self,term_name):
        self.selected_term = term_name
        return self

    def perform(self,action_name):
        self.status = action_name
        return self

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
        code_generator.term = self.selected_term
        code_generator.status = self.status
        if self.subject_to_check is not None:
            code_generator.check_subject = ta_models.Subject.objects.filter(title=self.subject_to_check).first().title_asp
        # code_generator.table_def = self.table.table_size
        return code_generator
