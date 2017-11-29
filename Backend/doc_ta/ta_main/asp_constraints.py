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
    return ' at ' + hour + " on " + ta_models.get_verbose_of_choice(day, ta_models.days_choices) + ' '


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

class NoThreeConsecutiveLecture():
    def get_creator(self):
        return "no_three_lectures_in_row(Y,D,S) :- class_with_year(_,_,D,S,Y), class_with_year(_,_,D,S+1,Y), class_with_year(_,_,D,S+2,Y), timeslot(D,S), course(Y).\n"

    def get_negator(self):
        return ":- no_three_lectures_in_row(_,_,_).\n"

    def get_show_string(self):
        return "#show no_three_lectures_in_row/3.\n"

    def constraint_parse(self,params):
        return parse_year(params[0]) + " has 3 or more consequitive hours of lectures starting" + parse_timeslot(params[1],params[2])

class TwoHourSlot():
    def get_creator(self):
        return "two_hour_slot(T,D,S):- class_with_year(T,_,D,S,Y), class_with_year(T,_,D,S+X,Y), X=2..8.\n"

    def get_negator(self):
        return ":- two_hour_slot(_,_,_).\n"

    def get_show_string(self):
        return "#show two_hour_slot/3.\n"

    def constraint_parse(self,params):
        return 'Subject ' + parse_subject(params[0]) + parse_timeslot(params[1],params[2]) + "violates has lectures not in 2 hours slots."

class CheckRoomCapacity():
    def get_creator(self):
        return "check_room_capacity(R,D,A):- class_with_year(T,R,D,A,_),room(R,C),subject(T,S,_), C<S. \n"

    def get_negator(self):
        return ":-check_room_capacity(_,_,_). \n"

    def get_show_string(self):
        return "#show check_room_capacity/3.\n "

    def constaint_parse(self,param):
        return 'Room ' + param[0] + "does not have enough capacity for subject at time " + param[2] + " " + param[1] + "."

class ForceTwoHourSlot():
    def get_creator(self):
        return "force_2_hour_slot(T) :- not { day_occupied(T,_) } (H+1)/2, subject(T,_,H).\n"

    def get_negator(self):
        return ":- force_2_hour_slot(T), subject(T,_,_).\n"

    def get_show_string(self):
        return "#show force_2_hour_slot/1.\n"

    def constraint_parse(self,param):
        return 'Subject ' + parse_subject(param[0]) + " is not in 2 hour daily slots."

class UniqueRoom():
    def get_creator(self):
        return "not_unique_room(R,D,S) :- class_with_year(T,R,D,S,_), class_with_year(Q,R,D,S,_), T!=Q.\n"

    def get_negator(self):
        return ":- not_unique_room(_,_,_).\n"

    def get_show_string(self):
        return "#show not_unique_room/3.\n"

    def constraint_parse(self,param):
        return 'Room ' + param[0] + " has multiple classes at time " + param[2] + " " + param[1] + "."

class UniqueTimeslotUnlessAllowed():
    def get_creator(self):
        return "clash_when_not_allowed(A,B,D,S) :- class_with_year(A,_,D,S,Y), class_with_year(B,_,D,S,Y), A!=B, not clash(A,B).\n"

    def get_negator(self):
        return ":- clash_when_not_allowed(_,_,_,_).\n"

    def get_show_string(self):
        return "#show clash_when_not_allowed/4.\n"

    def constraint_parse(self,param):
        return 'Clashes between subjects' + parse_timeslot(param[2], param[3]) + '.'

class MaxSixHourADay():
    def get_creator(self):
        return "max_six_hour_a_day(D,Y):- not { slot_occupied(D,_,Y) } 6, timeslot(D,_), course(Y).\n"

    def get_negator(self):
        return ":- max_six_hour_a_day(D,Y), timeslot(D,_), course(Y).\n"

    def get_show_string(self):
        return "#show max_six_hour_a_day/2.\n"

    def constraint_parse(self,param):
        return 'Course ' + param[1] + " has more than 6 hours a day on " + param[0] + "."

class UniqueRoomLecture():
    def get_creator(self):
        return "not_unique_room_lecture(T,D) :- class_with_year(T,R1,D,_,_), class_with_year(T,R2,D,_,_), R1!=R2.\n"

    def get_negator(self):
        return ":- not_unique_room_lecture(T,D),subject(T,_,_),timeslot(D,_). \n"

    def get_show_string(self):
        return "#show not_unique_room_lecture/2.\n"

    def constraint_parse(self,param):
        return 'Lecture ' + parse_subject(param[0]) + ' is not in the same room on ' + ta_models.get_verbose_of_choice(param[1], ta_models.days_choices) + "."

class ReserveSlot():
    #reserve slots (now only for horizon (first three line) and horizon year in europe(below first three lines))
    reserved =  [["horizon","tu",16,"computingy1"],["horizon","tu",17,"computingy1"]]
                #  ["horizon", "m", 17, "computingy2"], ["horizon", "m", 16, "computingy2"]
                #["horizon","th",16,"computingy3"],["horizon","th",17,"computingy3"],["horizon","th",16,"computingy4"],["horizon","th",17, "computingy4"],
                #["horizon","f",12,"computingy1"],["horizon", "f",13,"computingy1"],["horizon","f",12,"computingy2"],["horizon","f",13, "computingy2"]]

    def reserve(self,slot):
        #to add reserved slot
        self.reserved.append(slot)

    def get_creator(self):
        result = ""
        for i in self.reserved:
            result += "reserved(%s,%s,%d,%s). \n" % (i[0],i[1],i[2],i[3])
        result += "reserved_in_use(D,S,Y) :- reserved(_,D,S,Y), class_with_year(_,_,D,S,Y).\n"
        return result

    def get_negator(self):
        return ":-reserved_in_use(_,_,_).  \n "

    def get_show_string(self):
        return "show reserved_in_use/3. \n"

    def constraint_parse(self,param):
        return ""

class Concentration():
    #we dont have teaches yet
    #we dont even have information about which lecturer teaches which course or class
    lecturers = []
    def get_creator(self):
        result = ""
        for i in self.lecturers:
            result += "not_concentrated(L) :- not(teaches(L,S1), teaches(L,S2), subject(S1,_,D1,_,_), subject(S2,_,D2,_,_), D1=D2. L= %s) \n" % (i)
        return result

    def get_negator(self):
        return ":-not_concentarted(_).  \n "

    def get_show_string(self):
        return "show not_concentrated/1. \n"

    def constraint_parse(self,param):
        return ""

class ConstraintHandler():
    # static fields
    constraint_table = {
        "not_class_has_enough_hours": HasEnoughHoursConstraint(),
        "no_three_lectures_in_row": NoThreeConsecutiveLecture(),
        "two_hour_slot":TwoHourSlot(),
        "check_room_capacity": CheckRoomCapacity(),
        "force_2_hour_slot":ForceTwoHourSlot(),
        "not_unique_room": UniqueRoom(),
        "clash_when_not_allowed": UniqueTimeslotUnlessAllowed(),
        "max_six_hour_a_day": MaxSixHourADay(),
        "not_unique_room_lecture": UniqueRoomLecture(),
        "reserve_slot" : ReserveSlot(),
        #"concentration" : Concentration()
    }
    constraint_table_parse_verbose = {
        "Each class to have enough hours.": "not_class_has_enough_hours",
        "No three consecutive lectures": "no_three_lectures_in_row",
        "Force two-hour slot": "two_hour_slot",
        "Check Room Capacity": "check_room_capacity",
        "Max_two_day_a_week": "force_2_hour_slot",
        "Forbid 2 lectures in the same room": "not_unique_room",
        "Only allow clashes of time slot if stated": "clash_when_not_allowed",
        "Students have max 6 hours a day": "max_six_hour_a_day",
        "Lecture is exactly one room at a day": "not_unique_room_lecture",
        "Reserve slot for specific year" : "reserve_slot",
        #"specific lecturer want to teach everything on one day" : "concentration"
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


