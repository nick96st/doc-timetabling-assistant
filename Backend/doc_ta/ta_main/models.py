# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import asp_manipulators

# Create your models here.


selection_levels_choices = [('M','Mandatory'),  # eg: 3rd year group project
                            ('S','Mandatory_Selectable'),  # eg: 3rd year Robotics
                            ('E','Extra')]  # eg: Horizons(non-credit


# compares lowerized since we use choices first lowerized as asp code
def get_verbose_of_choice(current):
    return DayDef.objects.filter(day_asp=int(current)).first().day_string


class TableSizeDef(models.Model):
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    title = models.CharField(max_length=30,unique=True)

    @staticmethod
    def create(daydefs,start_hour,end_hour,name):

        table_size_def = TableSizeDef()
        table_size_def.start_hour = start_hour
        table_size_def.end_hour = end_hour
        table_size_def.title = name
        table_size_def.save()

        i = 1
        for daydef in daydefs:
            curr_daydef = DayDef()
            curr_daydef.day_asp = i
            curr_daydef.day_string = daydef
            curr_daydef.table = table_size_def
            curr_daydef.save()
            curr_daydef.day_asp = i
            curr_daydef.save()
            i = i + 1
            # generate timeslots
            for j in range(start_hour, end_hour):
                time_slot = Timeslot()
                time_slot.hour = j
                time_slot.day = curr_daydef
                time_slot.save()

class SavedTable(models.Model):
    name = models.CharField(max_length=50)
    table_size = models.ForeignKey(TableSizeDef)

    def __str__(self):
        return self.name


class DayDef(models.Model):
    day_string = models.CharField(max_length=20)
    day_asp = models.IntegerField()
    table = models.ForeignKey(TableSizeDef)



class Timeslot(models.Model):
    day = models.ForeignKey(DayDef)
    hour = models.IntegerField()

    def __str__(self):
        return str(self.hour) + ":" + str(self.day.day_string)

    def to_json(self):
        return {"time": self.hour, "day": self.day}

    def to_asp(self):
        return "timeslot(" + str(self.day.day_asp) + "," + str(self.hour) + ")"


# Course
class Subject(models.Model):
    code = models.IntegerField()
    title = models.CharField(max_length=50)
    title_asp = models.CharField(max_length=50)
    # course_year = models.CharField()  # such as C_BEng1,C_MEng4,JMC_BEng3 and etc
    selection_level = models.CharField(choices=selection_levels_choices, max_length=25)
    hours = models.IntegerField() # number of staff hours needed to be taken
    population_estimate = models.IntegerField()

    def __str__(self):
        return str(self.code) + str(self.title)

    # def to_json_for_frontend(self):
    #     return {"course_code": self.code,
    #             "name": self.title,
    #             # "course_year": self.course_year,
    #             }

    def to_asp(self):
        return "subject(" + self.title_asp + "," + str(self.population_estimate) + "," + str(self.hours) + ")"

    def assign_asp_suitable_name(self):
        self.title_asp = self.title.lower().replace(" ", "")

    # generates the string suitable for asp
    def save(self, *args, **kwargs):
        self.assign_asp_suitable_name()
        super(Subject, self).save(*args, **kwargs)


class Room(models.Model):
    room_name = models.CharField(max_length=10)
    room_size = models.IntegerField()

    def __str__(self):
        return self.room_name

    def to_json(self):
        return {"room": self.room_name}

    def to_asp(self):
        return "room(" + self.room_name + "," + str(self.room_size) + ")"


# Object that will defined saved allocated timeslot-lecture
class LectureClass(models.Model):
    time_slot = models.ForeignKey(Timeslot)
    subject = models.ForeignKey(Subject)
    room = models.ForeignKey(Room, null=True)
    # each of this will belong to a saved generated solution
    save_it_belongs_to = models.ForeignKey(SavedTable)
#   type = Tutorial || Lecture // i don't think it matters to be saved

    def to_json_for_frontend(self):
        result = {"time": self.time_slot.hour,
                  "day":  self.time_slot.day.day_string,
                  "room": self.room.room_name,
                  "name": self.subject.title}
        return result

    def init_from_json(self,json_data):
        # gets the day short version
        x = DayDef.objects.filter(day_string=json_data['day']).first()
        self.time_slot = Timeslot.objects.filter(hour=json_data['time'],day=x).first()
        self.room = Room.objects.get(room_name=json_data['room'])
        self.subject = Subject.objects.get(title=json_data['name'])
        return self

    def to_asp(self):
        json_data = {"id":"class","params":[self.subject.title_asp,
                                            self.room.room_name,
                                            self.time_slot.day.day_asp,
                                            self.time_slot.hour,
                                            ]}
        return asp_manipulators.json_term_to_asp_string(json_data)

    def from_asp(self,data,table):
        self.subject = Subject()
        self.time_slot = Timeslot()
        self.room = Room()
        # gets a
        day_obj = DayDef.objects.filter(day_asp=data["params"][2],table=table).first()
        # TODO: handle uniqueness/not_uniqueness of the title_asp"
        self.subject.title = Subject.objects.filter(title_asp=data["params"][0]).first().title
        self.room.room_name = data["params"][1]
        self.time_slot.day = day_obj
        self.time_slot.hour = data["params"][3]
        return self


class Term(models.Model):
    name = models.CharField(max_length=20)
    number_of_weeks = models.IntegerField()

    def __str__(self):
        return self.name


class ClassTerm(models.Model):
    term = models.ForeignKey(Term)
    subject = models.ForeignKey(Subject)
    # Note:doesnt have to_asp since term is disjoint and everything generated will belong to
    #      exactly 1 term


class Lecturer(models.Model):
    first_name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)

    def __str__(self):
        return str(self.first_name) + " " + str(self.surname)

    def to_asp(self):
        json_data = {"id": "lecturer",
                     "params": [asp_manipulators.string_to_asp_suitable(str(self.__str__())),
                     ]}
        return asp_manipulators.json_term_to_asp_string(json_data)


class Teaches(models.Model):
    lecturer = models.ForeignKey(Lecturer)
    subject = models.ForeignKey(Subject)

    def to_asp(self):
        json_data = {"id": "teaches",
                     "params": [asp_manipulators.string_to_asp_suitable(str(self.lecturer)),
                                self.subject.title_asp],
                     }
        # reads: teaches(lecturer,subject)
        return asp_manipulators.json_term_to_asp_string(json_data)


class CourseYear(models.Model):
    name = models.CharField(max_length=40, null=False)

    def __str__(self):
        return self.name

    def to_asp(self):
        return "course(" + str(self.name) + ")."

class SubjectsCourses(models.Model):
    subject = models.ForeignKey(Subject)
    courseyear = models.ForeignKey(CourseYear)

    # reads: subjectincourse(subject_name,course_name)
    def to_asp(self):
        json_data = {"id": "subjectincourse",
                     "params": [self.subject.title_asp,
                                asp_manipulators.string_to_asp_suitable(self.courseyear.name),
                                ]
                     }
        return asp_manipulators.json_term_to_asp_string(json_data)


class Clash(models.Model):
    subject1  = models.ForeignKey(Subject, related_name="subject1")
    subject2 = models.ForeignKey(Subject, related_name="subject2")

    def __str__(self):
        return str(self.subject) + " can clash with " + str(self.subject2)

    def to_asp(self):
        json_data = {"id":"clash",
                     "params":[self.subject.title_asp,
                               self.subject2.title_asp,
                               ]}
        json_data_inverse = {"id":"clash",
                             "params":[self.subject2.title_asp,
                                       self.subject.title_asp,
                                      ]}
        return asp_manipulators.json_term_to_asp_string(json_data) + '.\n' + \
            asp_manipulators.json_term_to_asp_string(json_data_inverse)
