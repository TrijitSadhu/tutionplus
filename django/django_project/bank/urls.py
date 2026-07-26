from django.conf.urls import url,include
from . import views
from django.contrib.auth import views as auth_views

from django.views.decorators.csrf import csrf_exempt

from django.urls import path, re_path

app_name = 'bank'

urlpatterns = [
    
    re_path(r'^$',(views.index),name='index'),
    
    re_path(r'^logout/$', auth_views.LogoutView, {'next_page': '/'}, name='logout'),
    re_path(r'^signup/$',views.signup,name='signup'),
    
    re_path(r'^login/$',views.login,name='login'),
    re_path(r'^add/$',views.add,name='add'),
    re_path(r'^del/$',views.del_ca,name='del_ca'),

    re_path(r'^dashboard/(?P<string>.+)/$',views.dashboard,name='dashboard'),
    re_path(r'^current-affairs/detail/(?P<user_year_month>.+)/(?P<user_page_no>[0-9]+)/$',views.ca,name='ca'),
    re_path(r'^current/(?P<string>.+)/(?P<params>[0-9]+)/$',views.current,name='current'),
    re_path(r'^cuttent_affirs/(?P<string>.+)/$',views.cuttent_affirs_single,name='cuttent_affirs'),
    re_path(r'^english/word/(?P<string>.+)/(?P<no>[0-9]+)/$',views.word,name='word'),
    path('math/home/', views.math_home, name='math_home'),
    path('math/rules/<str:chapter>/', views.math_rules, name='math_rules'),
    path('math/rules/<str:chapter>/<int:rule_id>/', views.math_rule_detail, name='math_rule_detail'),
    path('math/set-language/', views.math_set_language, name='math_set_language'),
    path('math/translate/<int:math_id>/<str:lang>/', views.math_translate_single, name='math_translate_single'),
    re_path(r'^math/(?P<string>.+)/(?P<params>[0-9]+)/$',views.math_all,name='math'),
    re_path(r'^job/(?P<string>.+)/(?P<after_string>.+)/(?P<params>[0-9]+)/$',views.job_view,name='job'),
    path('reasoning/home/', views.reasoning_home, name='reasoning_home'),
    re_path(r'^reasoning/(?P<string>.+)/(?P<params>[0-9]+)/$',views.reasoning_all,name='reasoning'),
    re_path(r'^reasoning/(?P<string>.+)/$',views.reasoning_single,name='reasoning_single'),
    re_path(r'^closetest/(?P<string>.+)/(?P<params>[0-9]+)/$',views.close_all,name='close'),
     re_path(r'^error_correction/(?P<string>.+)/(?P<params>[0-9]+)/$',views.error_all,name='error'),


     re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    re_path(r'^formula/(?P<string>.+)/$',views.formula,name='formula'),
    
    re_path(r'^gktoday/(?P<subject>.+)/(?P<folder>.+)/(?P<html>.+)/(?P<no>[0-9]+)/$',views.gk,name='gk'),
    re_path(r'^gk/(?P<subject>.+)/$',views.gk_index,name='gk_index'),
    
    re_path(r'^current-affairs/mcq/(?P<user_year_month>.+)/(?P<user_page_no>[0-9]+)/$',views.mcq_current,name='mcq_current'),
    path('subjects/home/', views.subjects_home, name='subjects_home'),
    path('biology/home/',   views.biology_home,   name='biology_home'),
    path('physics/home/',   views.physics_home,   name='physics_home'),
    path('chemistry/home/', views.chemistry_home, name='chemistry_home'),
    path('history/home/',   views.history_home,   name='history_home'),
    path('geography/home/', views.geography_home, name='geography_home'),
    path('polity/home/',    views.polity_home,    name='polity_home'),
    path('economics/home/', views.economics_home, name='economics_home'),
    re_path(r'^subject/(?P<subject>.+)/(?P<topic>.+)/(?P<subtopic>.+)/(?P<chapter>.+)/(?P<user_page_no>[0-9]+)/$',views.subject,name='history'),
    re_path(r'^database/$',views.database,name='database'),
    path('api-docs/', views.api_docs, name='api_docs'),



]
