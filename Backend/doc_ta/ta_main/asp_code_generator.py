import models as ta_models
import json
import asp_manipulators
from asp_constraints import basic_constraint as constraint
from exceptions import TypeError


class CodeGeneratorException(Exception):
    pass


# PRE: type(current) = string ,
# PRE: new has to_asp() function
def append_new_definition(current, new):
    return current + new.to_asp() + '.\n'


# Generates code from specified objects
class ASPCodeGenerator():
    # define term 1 as programming, MM, discrete, logic, hardware
    term_1 = [120, 145, 142, 140, 112]

    # enough hours
    enough_hour = constraint(":- not class_has_enough_hours(T), subject(T,_,_).")
    # no 3 conseuquitive lectures
    no_three_consecutive_lectures = constraint(":- class(_, _, D, S), class (_, _, D, S+1), class (_, _, D, S+2), timeslot(D, S).")
    # if 2 lectures in a day they must follow one another
    two_hour_slot = constraint(":- class(T,_,D,S), class(T,_,D,S+Y), Y=2..15.")
    # capacity check
    room_capacity = constraint(":- class(T,R,_,_),room(R,C),subject(T,S,_), C<S.")
    # limit 2 days a week to form 2hour time_slot
    max_two_day_a_week = constraint(":- not max_two_day_a_week(T), subject(T,_,_).")
    # unique timeslot for each year, allow clashes if stated
    unique_timeslot_unless_allowed = constraint(":- class_with_year(A,_,D,S,Y), class_with_year(B,_,D,S,Y), A!=B, not clash(A,B).")
    # Students have maximum 6 hours a days
    max_six_hour_a_day = constraint(":- not max_six_hour_a_day(D,Y), timeslot(D,_), course(Y).")
    # Each room is used for one lecture each timeslot
    unique_room = constraint(":- class(T,R1,D,_), class(T,R2,D,_), R1!=R2.")

    constraint_dictionary = { "Each class has enough hour per week" : enough_hour
                            , "No three consecutive lectures" : no_three_consecutive_lectures
                            , "Force two-hour slot" : two_hour_slot
                            , "Check room capacity" : room_capacity
                            , "Each subject two day a week" : max_two_day_a_week
                            , "Room should not have clashes" : unique_room
                            , "Only allow clashes of timeslot if stated" : unique_timeslot_unless_allowed
                            , "Students have max 6 hour a day" : max_six_hour_a_day
                            }


    def __init__(self):
        self.term = ""             # term to be generated on
        self.subjects = []         # subjects which belong to the term
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
        for subject in self.subjects:
                axiom_constraints_string += asp_manipulators.number_of_hours_asp(subject)
        axiom_constraints_string += "class_has_enough_hours(T):- H { class(T,_,_,_) } H , subject(T,_,H)." + \
                                    "max_six_hour_a_day(D,Y):- { class_with_year(_,_,D,_,Y) } 6, timeslot(D,S), course(Y).\n" + \
                                    "in_course(Y) :- class(T,R,D,S), timeslot(D,S), room(R,_), subject(T,_,_), subjectincourse(T,Y), course(Y).\n" + \
                                    "class_with_year(T,R,D,S,Y) :- class(T,R,D,S), subjectincourse(T,Y).\n" + \
                                    "1 { day_occupied(T,D) } 1 :- class(T,_,D,_).\n" + \
                                    "force_2_hour_slot(T) :- { day_occupied(T,_) } (H+1)/2, subject(T,_,H).\n"
        return axiom_constraints_string
        # return "class_has_enough_hours(T):- 3 { class(T,_,_,_) } 3 , subject(T,_,_)."

    def generate_hard_constraints(self):
        # as follows
        # enough hours
        # constraint enough_hour = constraint(":- not class_has_enough_hours(T), subject(T,_,_).")
        # #  at 1 room at a given time exactly 1 course
        #
        # # no 3 conseuquitive lectures
        # constraint no_three_consecutive_lectures = constraint(":- class(_, _, D, S), class (_, _, D, S+1), class (_, _, D, S+2), timeslot(D, S).")
        # # if 2 lectures in a day they must follow one another
        # constraint two_hour_slot = constraint(":- class(T,_,D,S), class(T,_,D,S+Y), Y=2..15.")
        # # capacity check
        # constraint room_capacity = constraint(":- class(T,R,_,_),room(R,C),subject(T,S,_), C<S.")
        # # class should not clash if not allowed
        # constraint no_clashes = constraint(":- class(A,_,D,S),class(B,_,D,S), A!=B.")
        result = ""
        constraints_list = self.constraint_dictionary.values()
        for c in constraints_list:
            result += c.get_constraint() + "\n"

        # return ":- not class_has_enough_hours(T), subject(T,_,_).\n" + \
        #        ":- class(T1,R,D,S), class(T2,R,D,S),room(R,_),T1!=T2.\n" + \
        #         ":- class(_, _, D, S), class (_, _, D, S+1), class (_, _, D, S+2), timeslot(D, S)." +\
        #         ":- class(T,_,D,S), class(T,_,D,S+Y), Y=2..15.\n" + \
        #         ":- class(T,R,_,_),room(R,C),subject(T,S,_), C<S." + \
        #         ":- class(T,X,D,S),class(T,Y,D,S), X!=Y."

        return result

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

        # fetches the model of the term
        selected_term = ta_models.Term.objects.filter(name=self.term).first()
        if selected_term is None:
            raise CodeGeneratorException("Term Does Not Exist")

        subjects_queryset = ta_models.ClassTerm.objects.filter(term=selected_term)
        for class_term in subjects_queryset:
            self.subjects.append(class_term.subject)

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
        return json_solutions


# Returns only result status of a asp
    def get_result_status(self,file_name):
        data = self.read_from_asp_result(file_name)
        data_dict = json.loads(data)
        return data_dict["Result"]


# Build pattern for the code generator to define which constraints
# facts, and object definitions to have
class CodeGeneratorBuilder():
    def __init__(self):
        self.selected_term = ""
        self.result_facts = []
        self.hard_constraints = []
        self.soft_constraints = []
        self.should_generate = True

    def for_term(self,term_name):
        self.selected_term = term_name
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
        return code_generator
