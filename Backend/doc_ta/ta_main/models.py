# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import asp_manipulators

# Create your models here.


# compares lowerized since we use choices first lowerized as asp code
def get_verbose_of_choice(current, choices):
    x = [x[1] for x in choices if x[0].lower() == current][0]
    return x


class SavedTable(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


days_choices = [('M','Monday'),
                ('Tu','Tuesday'),
                ('W','Wednesday'),
                ('Th','Thursday'),
                ('F','Friday')]

selection_levels_choices = [('M','Mandatory'),  # eg: 3rd year group project
                            ('S','Mandatory_Selectable'),  # eg: 3rd year Robotics
                            ('E','Extra')]  # eg: Horizons(non-credit


class Timeslot(models.Model):
    day = models.CharField(choices=days_choices,max_length=2)
    hour = models.IntegerField()

    def __str__(self):
        return str(self.hour) + ":" + str(self.day)

    def to_json(self):
        return {"time": self.hour, "day": self.day}

    def to_asp(self):
        return "timeslot(" + str(self.day) + "," + str(self.hour) + ")"


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
                  "day":  get_verbose_of_choice(self.time_slot.day, days_choices),
                  "room": self.room.room_name,
                  "name": self.subject.title}
        return result

    def init_from_json(self,json_data):
        # gets the day short version
        x = [x[0] for x in days_choices if x[1] == json_data['day']][0]
        self.time_slot = Timeslot.objects.filter(hour=json_data['time'],day=x).first()
        self.room = Room.objects.get(room_name=json_data['room'])
        self.subject = Subject.objects.get(title=json_data['name'])
        return self

    def to_asp(self):
        json_data = {"id":"class","params":[self.subject.title_asp,
                                            self.room.room_name,
                                            self.time_slot.day,
                                            self.time_slot.hour,
                                            ]}
        return asp_manipulators.json_term_to_asp_string(json_data)

    def from_asp(self,data):
        self.subject = Subject()
        self.time_slot = Timeslot()
        self.room = Room()
        # TODO: handle uniqueness/not_uniqueness of the title_asp"
        self.subject.title = Subject.objects.filter(title_asp=data["params"][0]).first().title
        self.room.room_name = data["params"][1]
        self.time_slot.day = data["params"][2]
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

class Lecturer(models.Model):
    first_name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)


class Teaches(models.Model):
    lecturer = models.ForeignKey(Lecturer)
    subject = models.ForeignKey(Subject)

class CourseYear(models.Model):
    mandatory_count = models.IntegerField()
    selective_count = models.IntegerField()
    name = models.CharField(max_length=40)

class SubjectsCourses(models.Model):
    subject = models.ForeignKey(Subject)
    courseyear = models.ForeignKey(CourseYear)

