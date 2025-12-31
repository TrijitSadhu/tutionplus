from django.contrib import admin
from .models import current_affairs_slide
from .models import current_affairs
from .models import the_hindu_word_Header1
from .models import the_hindu_word_list1
from .models import the_hindu_word_Header2
from .models import the_hindu_word_list2
from .models import the_economy_word_Header1
from .models import the_economy_word_list1
from .models import the_economy_word_Header2
from .models import the_economy_word_list2
from .models import total
from .models import total_english

from .models import job
from .models import total_job
from .models import total_job_category
from .models import total_job_state
from .models import home
from .models import user_save
from .models import reasoning
from .models import total_reasoning
from .models import topic
from .models import total_error
from .models import error
from .models import total_close
from .models import close

from .models import total_math
from .models import math
from .models import mcq
from .models import mcq_info_2018
from .models import mcq_info_2019
from .models import mcq_info_2020
from .models import current_affairs_info_2020
from .models import current_affairs_info_2018
from .models import current_affairs_info_2019

from .models import total_mcq
from .models import polity
from .models import total_polity
from .models import history
from .models import total_history
from .models import geography
from .models import total_geography
from .models import economics
from .models import total_economics
from .models import physics
from .models import total_physics
from .models import chemistry
from .models import total_chemistry
from .models import biology
from .models import total_biology



from django import forms
from django.db import models
from django.forms import TextInput, Textarea

class MessageAdminForm(forms.ModelForm):
    class Meta:
        model = current_affairs
        description = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100})) 
        fields = '__all__'
        exclude = ()

class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
  

# Register your models here.
admin.site.register(current_affairs_slide)
admin.site.register(mcq)
admin.site.register(total_mcq)
admin.site.register(mcq_info_2018)
admin.site.register(mcq_info_2019)
admin.site.register(mcq_info_2020)
admin.site.register(current_affairs_info_2020)
admin.site.register(current_affairs_info_2019)
admin.site.register(current_affairs_info_2018)


admin.site.register(current_affairs,MessageAdmin)

admin.site.register(total)
admin.site.register(the_hindu_word_Header1)
admin.site.register(the_hindu_word_list1)
admin.site.register(the_hindu_word_Header2)
admin.site.register(the_hindu_word_list2)
admin.site.register(the_economy_word_Header1)
admin.site.register(the_economy_word_list1)
admin.site.register(the_economy_word_Header2)
admin.site.register(the_economy_word_list2)
admin.site.register(total_english)
admin.site.register(math)
admin.site.register(total_math)
admin.site.register(job)
admin.site.register(total_job)
admin.site.register(total_job_category)
admin.site.register(total_job_state)

admin.site.register(home)


admin.site.register(user_save)
admin.site.register(topic)


admin.site.register(total_reasoning)
admin.site.register(reasoning)

admin.site.register(total_close)
admin.site.register(close)

admin.site.register(total_error)
admin.site.register(error)

admin.site.register(total_polity)
admin.site.register(polity)

admin.site.register(total_history)
admin.site.register(history)

admin.site.register(total_geography)
admin.site.register(geography)

admin.site.register(total_economics)
admin.site.register(economics)

admin.site.register(total_physics)
admin.site.register(physics)
admin.site.register(total_chemistry)
admin.site.register(chemistry)
admin.site.register(total_biology)
admin.site.register(biology)

