import asp_manipulators
import models as ta_models

class basic_constraint():

    def __init__(self, s):
        self.constraint_string = s

    def set_constraint(self, s):
        self.constraint_string = s

    def get_constraint(self):
        return self.constraint_string


def parse_timeslot(day, hour):
    return ' at ' + hour + " on " + ta_models.get_verbose_of_choice(day) + ' '

def metadata_timeslot(day, hour):
    return {"timeslot":{"day":day,"hour":hour}}

def metadata_day(day):
    return {}

# TODO:
def parse_year(course):
    return str(course)


def parse_subject(subject):
    return str(ta_models.Subject.objects.filter(title_asp=subject).first().title)
# TEMPLATE
# class BasicCatchableConstraint():
#
#     def __init__(self, creator, negator, show_string):
#         self.creator = creator            # rule with lefthand side
#         self.negator = negator            # constraint
#         self.show_string = show_string    # "show constraint/n."
#
#     def get_creator(self):
#         return self.creator
#
#     def get_negator(self):
#         return self.negator
#
#     def get_show_string(self):
#         return self.show_string
#
#     def get_metadata(self,params):
#         return None # if no metadata


class HasEnoughHoursConstraint():
    def get_creator(self):
        return "not_class_has_enough_hours(T):- not H { class_with_year(T,_,_,_,_) } H , subject(T,_,H).\n"

    def get_negator(self):
        return ":- not_class_has_enough_hours(T), subject(T,_,_).\n"

    def get_show_string(self):
        return "#show not_class_has_enough_hours/1.\n"

    def constraint_parse(self, params):
        subject_obj = ta_models.Subject.objects.filter(title_asp=params[0]).first()
        return 'Class ' + str(subject_obj.title) + " does not have " + str(subject_obj.hours) + " hours per week."

    def get_metadata(self,params):
        return None # if no metadata


class NoThreeConsecutiveLecture():
    def get_creator(self):
        return "no_three_consecutive_lecture(Y,D,S) :- class_with_year(_,_,D,S,Y), class_with_year(_,_,D,S+1,Y), class_with_year(_,_,D,S+2,Y), timeslot(D,S), course(Y).\n"

    def get_negator(self):
        return ":- no_three_consecutive_lecture(_,_,_).\n"

    def get_show_string(self):
        return "#show no_three_consecutive_lecture/3.\n"

    def constraint_parse(self,params):
        return parse_year(params[0]) + " has 3 or more consequitive hours of lectures starting" + parse_timeslot(params[1],params[2])

    def get_metadata(self, params):
        return metadata_timeslot(params[1], params[2])  # if no metadata


class TwoHourSlot():
    def get_creator(self):
        return "two_hour_slot(T,D,S):- class_with_year(T,_,D,S,Y), class_with_year(T,_,D,S+X,Y), X=2..8.\n"

    def get_negator(self):
        return ":- two_hour_slot(_,_,_).\n"

    def get_show_string(self):
        return "#show two_hour_slot/3.\n"

    def constraint_parse(self,params):
        return 'Subject ' + parse_subject(params[0]) + parse_timeslot(params[1],params[2]) + "violates has lectures not in 2 hours slots."

    def get_metadata(self, params):
        return metadata_timeslot(params[1],params[2])  # if no metadata


class CheckRoomCapacity():
    def get_creator(self):
        return "check_room_capacity(R,D,A):- class_with_year(T,R,D,A,_),room(R,C),subject(T,S,_), C<S. \n"

    def get_negator(self):
        return ":- check_room_capacity(_,_,_). \n"

    def get_show_string(self):
        return "#show check_room_capacity/3.\n"

    def constraint_parse(self,param):
        return 'Room ' + param[0] + ' does not have enough capacity for subject ' + parse_timeslot(param[1], param[2]) + "."

    def get_metadata(self, params):
        return metadata_timeslot(params[1],params[2])  # if no metadata


class LimitDayToFormTwohourSlot():
    def get_creator(self):
        return "limit_day_to_form_2h_slot(T) :- { day_occupied(T,_) } (H+1)/2, subject(T,_,H).\n"
    def get_negator(self):
        return ":- not limit_day_to_form_2h_slot(T), subject(T,_,_).\n"
    def get_show_string(self):
        return "#show limit_day_to_form_2h_slot/1.\n"
    def constraint_parse(self,param):
        return 'Subject ' + parse_subject(param[0]) + " is not in 2 hour daily slots."

    def get_metadata(self, params):
        return None  # if no metadata


class UniqueRoom():
    def get_creator(self):
        return "not_unique_room(R,D,S) :- class_with_year(T,R,D,S,_), class_with_year(Q,R,D,S,_), T!=Q.\n"

    def get_negator(self):
        return ":- not_unique_room(_,_,_).\n"

    def get_show_string(self):
        return "#show not_unique_room/3.\n"

    def constraint_parse(self,param):
        return 'Room ' + param[0] + " has multiple classes at time " + param[2] + " " + param[1] + "."

    def get_metadata(self, params):
        return metadata_timeslot(params[1],params[2])  # if no metadata


class UniqueTimeslotUnlessAllowed():
    def get_creator(self):
        return "clash_when_not_allowed(A,B,D,S) :- class_with_year(A,_,D,S,Y), class_with_year(B,_,D,S,Y), A!=B, not clash(A,B).\n"

    def get_negator(self):
        return ":- clash_when_not_allowed(_,_,_,_).\n"

    def get_show_string(self):
        return "#show clash_when_not_allowed/4.\n"

    def constraint_parse(self,param):
        return 'Clashes between subjects' + parse_timeslot(param[2], param[3]) + '.'

    def get_metadata(self, params):
        return metadata_timeslot(params[2],params[3])  # if no metadata


class MaxSixHourADay():
    def get_creator(self):
        return "max_six_hour_a_day(D,Y):- not { slot_occupied(D,_,Y) } 6, timeslot(D,_), course(Y).\n"

    def get_negator(self):
        return ":- max_six_hour_a_day(D,Y), timeslot(D,_), course(Y).\n"

    def get_show_string(self):
        return "#show max_six_hour_a_day/2.\n"

    def constraint_parse(self,param):
        return 'Course ' + param[1] + " has more than 6 hours a day on " + param[0] + "."

    def get_metadata(self, params):
        return metadata_day(params[0])  # if no metadata


class UniqueRoomLecture():
    def get_creator(self):
        return "not_unique_room_lecture(T,D) :- class_with_year(T,R1,D,_,_), class_with_year(T,R2,D,_,_), R1!=R2.\n"

    def get_negator(self):
        return ":- not_unique_room_lecture(T,D),subject(T,_,_),timeslot(D,_). \n"

    def get_show_string(self):
        return "#show not_unique_room_lecture/2.\n"

    def constraint_parse(self,param):
        return 'Lecture ' + parse_subject(param[0]) + ' is not in the same room on ' + ta_models.get_verbose_of_choice(param[1]) + "."

    def get_metadata(self, params):
        return metadata_day(params[1])  # if no metadata


class LecturerClash():
    def get_creator(self):
        return "lecturer_clash(L,D,S) :- class_with_year(T1,_,D,S,_), class_with_year(T2,_,D,S,_), T1!=T2, teaches(L,T1), teaches(L,T2), lecturer(L).\n"
    def get_negator(self):
        return ":- lecturer_clash(L,D,S). \n"
    def get_show_string(self):
        return "#show lecturer_clash/3. \n"
    def constraint_parse(self,param):
        return 'Lecturer ' + param[0] + 'has clashes on ' + parse_timeslot(param[1], param[2]) + '.\n'

class MaxFourHourADayLecturer():
    def get_creator(self):
        return "max_four_hour_a_day(L,D) :- not { slot_teaches(L,D,_) } 4, timeslot(D,_), lecturer(L). \n"
    def get_negator(self):
        return ":- max_four_hour_a_day(L,D). \n"
    def get_show_string(self):
        return "#show max_four_hour_a_day/2. \n"
    def constraint_parse(self,param):
        return 'Lecturer ' + param[0] + 'has more than four hour on ' + param[1] + "."

class ConstraintHandler():
    # static fields
    constraint_table = {
        "not_class_has_enough_hours": HasEnoughHoursConstraint(),
        "no_three_consecutive_lecture": NoThreeConsecutiveLecture(),
        "two_hour_slot":TwoHourSlot(),
        "check_room_capacity" : CheckRoomCapacity(),
        "limit_day_to_form_2h_slot":LimitDayToFormTwohourSlot(),
        "not_unique_room" : UniqueRoom(),
        "clash_when_not_allowed" : UniqueTimeslotUnlessAllowed(),
        "max_six_hour_a_day" : MaxSixHourADay(),
        "not_unique_room_lecture" : UniqueRoomLecture(),
        "lecturer_clash" : LecturerClash(),
        "max_four_hour_a_day_lecturer" : MaxFourHourADayLecturer()
    }
    constraint_table_parse_verbose = {
        "Each class to have enough hours.": "not_class_has_enough_hours",
        "No three consecutive lecture" : "no_three_consecutive_lecture",
        "Force two-hour slot" : "two_hour_slot",
        "Check Room Capacity" : "check_room_capacity",
        "Limit the number of days have a subject to form 2h slot": "limit_day_to_form_2h_slot",
        "Forbid 2 lecturers in the same room" : "not_unique_room",
        "only allow clashes of time slot if stated" : "clash_when_not_allowed",
        "Students have max 6 hours a day" : "max_six_hour_a_day",
        "Lecture is exactly one room at a day" : "not_unique_room_lecture",
        "Lecturer can only teach one subject at a time" : "lecturer_clash",
        "Lecturer teaches max 4 hour a day" : "max_four_hour_a_day_lecturer"
    }

    @staticmethod
    def constraint_parse(id, params):
        return ConstraintHandler.constraint_table[id].constraint_parse(params)

    @staticmethod
    def constraint_creator(name):
        return ConstraintHandler.constraint_table[ConstraintHandler.constraint_table_parse_verbose[name]].get_creator()

    @staticmethod
    def constraint_negator(name):
        return ConstraintHandler.constraint_table[ConstraintHandler.constraint_table_parse_verbose[name]].get_negator()

    @staticmethod
    def constraint_show(name):
        return ConstraintHandler.constraint_table[ConstraintHandler.constraint_table_parse_verbose[name]].get_show_string()

    @staticmethod
    def constraint_metadata(id, params):
        return ConstraintHandler.constraint_table[id].get_metadata(params)

