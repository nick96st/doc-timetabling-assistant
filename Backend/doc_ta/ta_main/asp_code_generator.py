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
    # enough hours
    # enough_hour = constraint(":- not class_has_enough_hours(T), subject(T,_,_).")
    # no 3 conseuquitive lectures
    # no_three_consecutive_lectures = constraint(":- class_with_year(_,_,D,S,Y), class_with_year(_,_,D,S+1,Y), class_with_year(_,_,D,S+2,Y), timeslot(D,S), course(Y).")
    # if 2 lectures in a day they must follow one another
    #two_hour_slot = constraint(":- class_with_year(T,_,D,S,Y), class_with_year(T,_,D,S+X,Y), X=2..8.")
    # capacity check
    #room_capacity = constraint(":- class_with_year(T,R,_,_,_),room(R,C),subject(T,S,_), C<S.")
    # limit 2 days a week to form 2hour time_slot
    #max_two_day_a_week = constraint(":- not force_2_hour_slot(T), subject(T,_,_).")
    # unique timeslot for each year, allow clashes if stated
    unique_timeslot_unless_allowed = constraint(":- class_with_year(A,_,D,S,Y), class_with_year(B,_,D,S,Y), A!=B, not clash(A,B).")
    # Students have maximum 6 hours a days
    max_six_hour_a_day = constraint(":- not max_six_hour_a_day(D,Y), timeslot(D,_), course(Y).")
    # Lectures on the same day must be in the same room(OR even hour)
    unique_room_lecture = constraint(":- class_with_year(T,R1,D,_,_), class_with_year(T,R2,D,_,_), R1!=R2.")
    # Every room can have 1 lecture at a time
    unique_room = constraint(":- class_with_year(T,R,D,S,_), class_with_year(Q,R,D,S,_), T!=Q.\n")

    constraint_dictionary = {
                            # "Each class has enough hour per week" : enough_hour,
                            # "No three consecutive lectures" : no_three_consecutive_lectures
                            # "Force two-hour slot" : two_hour_slot
                            # "Check room capacity" : room_capacity
                            # "Each subject two day a week" : max_two_day_a_week
                              "Forbid 2 lectures in the same room" : unique_room
                            , "Only allow clashes of timeslot if stated" : unique_timeslot_unless_allowed
                            , "Students have max 6 hour a day" : max_six_hour_a_day
                            , "Lecture is in exactly one room at a day": unique_room_lecture
                            }

    def __init__(self):
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

        # TODO: perhaps selectable MxN thing
        for timeslot in ta_models.Timeslot.objects.all():
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

        return result_string

    def generate_axiom_constraints(self):
        axiom_constraints_string = " "
        for constraint in self.hard_constraints:
            axiom_constraints_string += Constraints.constraint_creator(constraint)

        axiom_constraints_string += "1 { slot_occupied(D,S,Y) } 1 :- class_with_year(_,_,D,S,Y).\n" + \
                                    "max_six_hour_a_day(D,Y):- { slot_occupied(D,_,Y) } 6, timeslot(D,_), course(Y).\n" + \
                                    "class_with_year(T,R,D,S,Y) :- class(T,R,D,S), subjectincourse(T,Y).\n" + \
                                    "1 { day_occupied(T,D) } 1 :- class_with_year(T,_,D,_,Y).\n"
                                    #"force_2_hour_slot(T) :- { day_occupied(T,_) } (H+1)/2, subject(T,_,H).\n"
                                    #"class_has_enough_hours(T):- not H { class_with_year(T,_,_,_,_) } H , subject(T,_,H).\n"

        return axiom_constraints_string

    def generate_hard_constraints(self):

        result_string = ""
        # generate hard constraint negators if generating
        if self.status == "GENERATE":
            for constraint in self.hard_constraints:
                result_string += Constraints.constraint_negator(constraint)

        # TODO: Comment this out when all the constraints are parsed into new format
        constraints_list = self.constraint_dictionary.values()
        for c in constraints_list:
            result_string += c.get_constraint() + "\n"

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

        command_string = "./asp/clingo --outf=2 <" + './' + input_src + ">" + './' + output_src
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
        code_string += "#show class_with_year/5."
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
                if len(constraint_violations) != 0:
                    parsed_violations = self.parse_violations(constraint_violations)

                json_solutions.append({"violations":parsed_violations})

            return True, json_solutions

        # IF IT IS GENERATING NO NEED TO CHECK FOR CONSTRAINTS
        elif self.status == "GENERATE":
            json_solutions = []
            for solution in tokenized_results:
                result_array = []
                # for every solution parse
                for lecture_class in solution:
                        result_array.append(ta_models.LectureClass().from_asp(lecture_class).to_json_for_frontend())

                json_solutions.append(result_array)
            # code_result = read_from_asp_result('default_001.in')
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


# Build pattern for the code generator to define which constraints
# facts, and object definitions to have
class CodeGeneratorBuilder():
    def __init__(self):
        self.selected_term = ""
        self.result_facts = []
        # Default hard constraints are all the defined keys in the verbose map table
        self.hard_constraints = Constraints.constraint_table_parse_verbose.keys()
        self.soft_constraints = []
        self.should_generate = True
        self.status = ""

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
        return code_generator
