import asp_manipulators
import models as ta_models

class basic_constraint():

    def __init__(self, s):
        self.constraint_string = s

    def set_constraint(self, s):
        self.constraint_string = s

    def get_constraint(self):
        return self.constraint_string


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
        #why is this not NOT?
        return ":- not_class_has_enough_hours(T), subject(T,_,_).\n"

    def get_show_string(self):
        return "#show not_class_has_enough_hours/1.\n"

    def constraint_parse(self, params):
        subject_obj = ta_models.Subject.objects.filter(title_asp=params[0]).first()
        return 'Class ' + str(subject_obj.title) + " does not have " + str(subject_obj.hours) + "hours per week."

class NoThreeConsecutiveLecture():
    def get_creator(self):
        #no axiom generator
        #(Do we leave it blank or we can generate an axiom for all those that dont have one)
        return ""

    def get_negator(self):
        return ":- class_with_year(_,_,D,S,Y), class_with_year(_,_,D,S+1,Y), class_with_year(_,_,D,S+2,Y), timeslot(D,S), course(Y).\n"

    def get_show_string(self):
        #no axiom generate therefore no show function
        return ""

    def constraint_parse(self,params):
        #Yotov please add in the constraint_parse implementations
        #I am not sure about the structure and dont want to mess it up
        return ""

class TwoHourSlot():
    def get_creator(self):
        #no axiom generator
        return ""

    def get_negator(self):
        return ":- class_with_year(T,_,D,S,Y), class_with_year(T,_,D,S+X,Y), X=2..8.\n"

    def get_show_string(self):
        #no axiom generate therefore no show string
        return ""

    def constraint_parse(self,params):
        return ""

class CheckRoomCapacity():
    def get_creator(self):
        return ""
    def get_negator(self):
        return ":- class_with_year(T,R,_,_,_),room(R,C),subject(T,S,_), C<S. \n"

    def get_show_string(self):
        return ""

    def constaint_parse(self,param):
        return ""

class ForceTwoHourSlot():
    def get_creator(self):
        return "force_2_hour_slot(T) :- { day_occupied(T,_) } (H+1)/2, subject(T,_,H).\n"

    def get_negator(self):
        return ":- not force_2_hour_slot(T), subject(T,_,_).\n"

    def get_show_string(self):
        return "#show force_2_hour_slot/1.\n"

    def constraint_parse(self,param):
        return ""

class UniqueRoom():
    def get_creator(self):
        return ""

    def get_negator(self):
        return ":- class_with_year(T,R,D,S,_), class_with_year(Q,R,D,S,_), T!=Q.\n"

    def get_show_string(self):
        return ""

    def constraint_parse(self,param):
        return ""

class UniqueTimeslotUnlessAllowed():
    def get_creator(self):
        return ""

    def get_negator(self):
        return ":- class_with_year(A,_,D,S,Y), class_with_year(B,_,D,S,Y), A!=B, not clash(A,B).\n"

    def get_show_string(self):
        return ""

    def constraint_parse(self,param):
        return ""

class MaxSixHourADay():
    def get_creator(self):
        return "max_six_hour_a_day(D,Y):- { slot_occupied(D,_,Y) } 6, timeslot(D,_), course(Y).\n"

    def get_negator(self):
        return ":- not max_six_hour_a_day(D,Y), timeslot(D,_), course(Y).\n"

    def get_show_string(self):
        return "#show max_six_hour_a_day/2.\n"

    def constraint_parse(self,param):
        return ""

class UniqueRoomLecture():
    def get_creator(self):
        return ""

    def get_negator(self):
        return ":-  class_with_year(T,R1,D,_,_), class_with_year(T,R2,D,_,_), R1!=R2. \n"

    def get_show_string(self):
        return ""

    def constraint_parse(self,param):
        return ""

class ConstraintHandler():
    # static fields
    constraint_table = {
        "not_class_has_enough_hours": HasEnoughHoursConstraint(),
        "no_three_consecutive_lecture" : NoThreeConsecutiveLecture(),
        "two_hour_slot":TwoHourSlot(),
        "check_room_capacity" : CheckRoomCapacity(),
        "force_2_hour_slot":ForceTwoHourSlot(),
        "unique_room" : UniqueRoom(),
        "unique_timeslot_unless_allowed" : UniqueTimeslotUnlessAllowed(),
        "max_six_hour_a_day" : MaxSixHourADay(),
        "unique_room_lecture" : UniqueRoomLecture()
    }
    constraint_table_parse_verbose = {
        "Each class to have enough hours.": "not_class_has_enough_hours",
        "No three consecutive lectures": "no_three_consecutive_lecture",
        "Force two-hour slot": "two_hour_slot",
        "Check Room Capacity": "check_room_capacity",

        #force_2_hour_slot? a bit confusing makesure this is right please
        "Max_two_day_a_week": "force_2_hour_slot",

        "Forbid 2 lecturers in the same room": "unique_room",
        "only allow clashes of time slot if stated": "unique_timeslot_unless_allowed",
        "Students have max 6 hours a day": "max_six_hour_a_day",
        "Lecture is exactly one room at a day": "unique_room_lecture"
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


