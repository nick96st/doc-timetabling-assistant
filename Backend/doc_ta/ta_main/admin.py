# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models as ta_models


class SavedTableAdmin(admin.ModelAdmin):
    list_display = ['name']


class TimeslotAdmin(admin.ModelAdmin):
    list_display = ['day', 'hour']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'hours', 'population_estimate']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'room_size']


class LectureClassAdmin(admin.ModelAdmin):
    list_display = ['room', 'subject', 'time_slot','save_it_belongs_to']


class ClassTermAdmin(admin.ModelAdmin):
    list_display = ["term", "subject"]


class TermAdmin(admin.ModelAdmin):
    list_display = ["name","number_of_weeks"]


# Register your models here.
admin.site.register(ta_models.SavedTable, SavedTableAdmin)
admin.site.register(ta_models.Timeslot, TimeslotAdmin)
admin.site.register(ta_models.Subject, SubjectAdmin)
admin.site.register(ta_models.Room, RoomAdmin)
admin.site.register(ta_models.LectureClass, LectureClassAdmin)
admin.site.register(ta_models.Term, TermAdmin)
admin.site.register(ta_models.ClassTerm, ClassTermAdmin)

