"""doc_ta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from ta_main import views
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

# adds Django auto-generated login views
urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'timetable/check', views.check_constraints),
    url(r'timetable/saveas', views.save_timetable),
    url(r'timetable/updatesave',views.update_save),
    url(r'timetable/generate', views.generate_table),
    url(r'timetable/load', views.load_save),
    url(r'timetable/add_constraint', views.add_constraint),
    url(r'timetable/existingsaves', views.get_load_choices),
    url(r'choices/rooms', views.get_room_choices),
    url(r'choices/subjects', views.get_subject_choices),
    url(r'choices/terms', views.get_term_choices),
    url(r'choices/constraints',views.get_constraint_choices),
    url(r'create_table_size', views.create_timeslots_for_table),
    url(r'init_timeslots_doc', views.init_timeslots_DoC),
    url(r'', views.get_index),
]

