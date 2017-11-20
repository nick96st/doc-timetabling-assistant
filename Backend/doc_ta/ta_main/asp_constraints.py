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
        return "class_has_enough_hours(T):- not H { class_with_year(T,_,_,_,_) } H , subject(T,_,H).\n"

    def get_negator(self):
        return ":- class_has_enough_hours(T), subject(T,_,_)."

    def get_show_string(self):
        return "#show class_has_enough_hours/1."

    def constraint_parse(self, params):
        subject_obj = ta_models.Subject.objects.filter(title_asp=params[0]).first()
        return 'Class ' + str(subject_obj.title) + " does not have " + str(subject_obj.hours) + "hours per week."


class ConstraintHandler():
    # static fields
    constraint_table = {
        "class_has_enough_hours": HasEnoughHoursConstraint()

    }
    constraint_table_parse_verbose = {
        "Each class to have enough hours.": "class_has_enough_hours"
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


