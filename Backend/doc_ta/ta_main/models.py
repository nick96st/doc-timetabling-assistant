# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.


class SavedTable(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SavedTableAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(SavedTable, SavedTableAdmin)


days_choices = [('M','Monday'),
                ('Tu','Tuesday'),
                ('W','Wednesday'),
                ('Th','Thurday'),
                ('F','Friday')]

selection_levels_choices = [('M','Mandatory'),  # eg: 3rd year group project
                            ('S','Mandatory_Selectable'),  # eg: 3rd year Robotics
                            ('E','Extra')]  # eg: Horizons(non-credit


class Timeslot(models.Model):
    day = models.CharField(choices=days_choices,max_length=2)
    hour = models.IntegerField()

    def __str__(self):
        return str(self.hour) + ":" + self.day

    def to_json(self):
        return {"time": self.hour, "day": self.day}

    def to_asp(self):
        return NotImplementedError


class TimeslotAdmin(admin.ModelAdmin):
    list_display = ['day', 'hour']


admin.site.register(Timeslot,TimeslotAdmin)


# Course
class Subject(models.Model):
    code = models.IntegerField()
    title = models.CharField(max_length=50)
    # course_year = models.CharField()  # such as C_BEng1,C_MEng4,JMC_BEng3 and etc
    selection_level = models.CharField(choices=selection_levels_choices, max_length=25)
    hours = models.IntegerField() # number of staff hours needed to be taken
    population_estimate = models.IntegerField()

    def __str__(self):
        return str(self.code) + self.title

    def to_json_for_frontend(self):
        return {"course_code": self.code,
                "name": self.title,
                # "course_year": self.course_year,
                }

    def to_asp(self):
        return NotImplementedError


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'hours', 'population_estimate']


admin.site.register(Subject, SubjectAdmin)


class Room(models.Model):
    room_name = models.CharField(max_length=10)
    room_size = models.IntegerField()

    def __str__(self):
        return self.room_name

    def to_json(self):
        return {"room": self.room_name}


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'room_size']


admin.site.register(Room, RoomAdmin)


# Object that will defined saved allocated timeslot-lecture
class LectureClass(models.Model):
    time_slot = models.ForeignKey(Timeslot)
    subject = models.ForeignKey(Subject)
    room = models.ForeignKey(Room, null=True)
    # each of this will belong to a saved generated solution
    save_it_belongs_to = models.ForeignKey(SavedTable)
#   type = Tutorial || Lecture // i don't think it matters to be saved

    def to_json_for_frontend(self):
        result = {}
        # .update() extend dict with other dict
        result.update(self.subject.model.to_json())
        result.update(self.time_slot.model.to_json())
        result.update(self.room.model.to_json())
        return result

    def init_from_json(self,json_data):
        # gets the day short version
        x = [x[0] for x in days_choices if x[1] == json_data['day']][0]
        self.time_slot = Timeslot.objects.filter(hour=json_data['time'],day=x).first()
        self.room = Room.objects.get(room_name=json_data['room'])
        self.subject = Subject.objects.get(title=json_data['name'])

    def to_asp(self):
        return self.time_slot.model.to_asp() + self.subject.model.to_json()

    def from_asp(self):
        return NotImplementedError


class LectureClassAdmin(admin.ModelAdmin):
    list_display = ['room', 'subject', 'time_slot','save_it_belongs_to']


admin.site.register(LectureClass,LectureClassAdmin)
