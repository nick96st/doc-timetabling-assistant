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
        return "limit_day_to_form_2h_slot(T) :- not { day_occupied(T,_) } (H+1)/2, subject(T,_,H).\n"
    def get_negator(self):
        return ":- limit_day_to_form_2h_slot(T), subject(T,_,_).\n"
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
        result += "reserved_slot(D,S,Y) :- reserved(_,D,S,Y), class_with_year(_,_,D,S,Y).\n"
        return result

    def get_negator(self):
        return ":-reserved_slot(_,_,_).  \n "

    def get_show_string(self):
        return "#show reserved_slot/3. \n"

    def constraint_parse(self,param):
        return "" #TODO

    def get_metadata(self, params):
        return None  # if no metadata

class Concentration():
    #we dont have teaches yet
    #we dont even have information about which lecturer teaches which course or class
    lecturers = []
    def get_creator(self):
        result = ""
        for i in self.lecturers:
            result += "not_concentrate(L) :- teaches(L,S1), teaches(L,S2), class_with_year(S1,_,D1,_,_), class_with_year(S2,_,D2,_,_), D1!=D2, L= %s). \n" % (i)
        return result
    def add_lecturer(self, lecturer):
        self.lecturers.append(lecturer)
    def get_negator(self):
        return ":-not_concentrate(_).  \n "

    def get_show_string(self):
        return "#show not_concentrate/1. \n"

    def constraint_parse(self,param):
        return "" #TODO

    def get_metadata(self, params):
        return None  # if no metadata

class Spreading():
    subjects = ["architecture"]
    def get_creator(self):

        result = ""
        for i in self.subjects:
            result += "not_spreading(T) :-  class_with_year(T,_,D1,_,Y), class_with_year(T,_,D2,_,Y), |D1-D2| < 2, D1 != D2, T = %s .\n" % (i)
        return result

    def add_subject(self, subject):
        self.subjects.append(subject)

    def get_negator(self):
        return ":- not_spreading(_).  \n "

    def get_show_string(self):
        return "#show not_spreading/1. \n"

    def constraint_parse(self,param):
        return "Subject is not spread."

    def get_metadata(self, params):
        return None  # if no metadata

class ConcentrateTwo():
    #we dont have teaches yet
    #we dont even have information about which lecturer teaches which course or class
    lecturers = []
    def get_creator(self):
        result = ""
        for i in self.lecturers:
            result += "not_concentrate_two(L) :- teaches(L,S1), teaches(L,S2), teaches(L,S3)," + \
                      "class_with_year(S1,_,D1,_,_), class_with_year(S2,_,D2,_,_), class_with_year(S3,_,D3,_,_),"+\
                      "D1 != D2 , D2 != D3, D3 != D1 , L = %s. \n" % (i)
        return result
    def add_lecturer(self, lecturer):
        self.lecturers.append(lecturer)
    def get_negator(self):
        return ":- not_concentrate_two(_).  \n "

    def get_show_string(self):
        return "#show not_concentrated_two/1. \n"

    def constraint_parse(self,param):
        return "" #TODO

    def get_metadata(self, params):
        return None  # if no metadata

class NoLecturerDayTime():
    #no lecturer on specific day and time
    #we dont have teaches yet
    #we dont even have information about which lecturer teaches which course or class
    lecturerDayTime = []
    def get_creator(self):
        result = ""
        for i in self.lecturerDayTime:
            result += "no_lecturer_day_time(L,S,D,T) :- teaches(L,S) , class_with_year(S,_,D,T,_), L = %s, D = %s, T = %s.\n" % (i[0],i[1],i[2])
        return result

    def add_no_lecturer_day_time(self, lecturer, day, time):
        ar = [lecturer,day,time]
        self.lecturerDayTime.append(ar)

    def get_negator(self):
        return ":- no_lecturer_day_time(_,_,_,_).  \n "

    def get_show_string(self):
        return "#show no_lecturer_day_time/4. \n"

    def constraint_parse(self,param):
        return "" #TODO

    def get_metadata(self, params):
        return None  # if no metadata

class NoLecturerDay():
    #no lecturer on specific day and time
    #we dont have teaches yet
    #we dont even have information about which lecturer teaches which course or class
    lecturerDay = []
    def get_creator(self):
        result = ""
        for i in self.lecturerDay:
            result += "no_lecturer_day(L,S,D) :- teaches(L,S) , class_with_year(S,_,D,_,_), L = %s, D = %s.\n" % (i[0],i[1])
        return result

    def add_no_lecturer_day_time(self, lecturer, day):
        ar = [lecturer,day]
        self.lecturerDay.append(ar)

    def get_negator(self):
        return ":- no_lecturer_day(_,_,_).  \n "

    def get_show_string(self):
        return "#show no_lecturer_day/3. \n"

    def constraint_parse(self,param):
        return "" #TODO

    def get_metadata(self, params):
        return None  # if no metadata

class NoLecturerTime():
    #no lecturer on specific day and time
    #we dont have teaches yet
    #we dont even have information about which lecturer teaches which course or class
    lecturerTime = []
    def get_creator(self):
        result = ""
        for i in self.lecturerTime:
            result += "no_lecturer_time(L,S,T) :- teaches(L,S) , class_with_year(S,_,_,T,_), L = %s, T = %s.\n" % (i[0],i[1])
        return result

    def add_no_lecturer_day_time(self, lecturer, time):
        ar = [lecturer,time]
        self.lecturerTime.append(ar)

    def get_negator(self):
        return ":- no_lecturer_time(_,_,_).  \n "

    def get_show_string(self):
        return "#show no_lecturer_time/3. \n"

    def constraint_parse(self,param):
        return "" #TODO

    def get_metadata(self, params):
        return None  # if no metadata


class No9to5():
    def get_creator(self):
        return "no_9_to_5(D,Y) :- class_with_year(_,_,D,S1,Y), class_with_year(_,_,D,S2,Y), S1<10, S2>16. \n"
    def get_negator(self):
        return ":- no_9_to_5(_,Y), course(Y). \n"
    def get_show_string(self):
        return "#show no_9_to_5/2. \n"
    def constraint_parse(self,param):
        return 'Year ' +param[1] + 'on day ' + param[0] + ' has classes from 9am to 6pm.\n'

class ThreeConsecutiveHourForLecturer():
    def get_creator(self):
        return "three_consecutive_hour_for_lecturer(L,D) :- class_with_year(S1,_,D,S,_), class_with_year(S2,_,D,S+1,_), class_with_year(S3,_,D,S+2,_), teaches(L,S1),teaches(L,S2), teaches(L,S3), lecturer(L). \n"
    def get_negator(self):
        return ":- three_consecutive_hour_for_lecturer(L,D), lecturer(L), timeslot(D,_) \n."
    def get_show_string(self):
        return "#show three_consecutive_hour_for_lecturer/2. \n"
    def constraint_parse(self,param):
        return 'Lecturer ' + param[0] + ' on day ' + param[1] + ' has 3 consecutive hours. \n'


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
        "max_four_hour_a_day_lecturer" : MaxFourHourADayLecturer(),
        "reserve_slot": ReserveSlot(),
        # "not_concentration" : Concentration(),
        # "not_concentrate_two" : ConcentrateTwo(),
        "not_spreading": Spreading(),
        # "no_lecturer_day_time" : NoLecturerDayTime(),
        # "no_lecturer_day": NoLecturerDay(),
        # "no_lecturer_time" : NoLecturerTime()
        "no_9_to_5": No9to5(),
        "three_consecutive_hour_for_lecturer": ThreeConsecutiveHourForLecturer(),
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
        "Lecturer teaches max 4 hour a day" : "max_four_hour_a_day_lecturer",
        "Reserve specific slot for specific year" : "reserve_slot",
        #"specific lecturer want to teach everything on one day" : "not_concentration",
        #"specific lecturer want all teaching in two days" : "not_concentrate_two",
        "specific class spread out during a week(at least one day break)" : "not_spreading",
        #"specific lecturer cannot teach on specific day and specific time" : "no_lecturer_day_time",
        #"specific lecturer cannot teach on specific day" : "no_lecturer_day",
        #"specific lecturer cannot teach on specific time" : "no_lecturer_time",
        "Forbid early morning and late afternoon on same day.": "no_9_to_5",
        "Lecturer can't have 3 consequitive hours of tutoring.": "three_consecutive_hour_for_lecturer"
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
