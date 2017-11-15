import asp_manipulators

class basic_constraint():
    constraint_string = ""

    def __init__(self, s):
        self.constraint_string = s

    def set_constraint(self, s):
        self.constraint_string = s

    def get_constraint(self):
        return self.constraint_string

