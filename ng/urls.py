from django.conf.urls import url
from django.contrib.auth import views as auth_views
import django

from . import views

app_name = 'ng'
urlpatterns = [
    # User Interactions URLs
    url(r'^login/$', views.get_name, name='login'),  
    url(r'^new_experiment/$', views.new_experiment, name='new_experiment'),
    url(r'^choose_experiment/$', views.choose_experiment, name='choose_experiment'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/ng/login'}, name='logout'),  
    url(r'^$',views.game,name='game'),
    url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/continue/$', views.continue_userxp, name='continue'),

    # Internal Workers URLs
    url(r'^userinfo_$', views.none, name='send_user_info_base'),
    # url(r'^new_experiment/(?P<xp_cfg_name>[0-9a-z]+)$', views.new_experiment, name='new_experiment_cfg'),
    # url(r'^index/$', views.IndexView.as_view(), name='index'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.exp_resume, name='exp_resume'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/results_srtheo/$', views.result_srtheo, name='results_srtheo'),#ResultsView.as_view(), name='results'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})-hearer-(?P<meaning>[0-9a-z]+)/results/$', views.result_hearer, name='results_hearer'),#ResultsView.as_view(), name='results'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})-speaker-(?P<meaning>[0-9a-z]+)-(?P<word>[0-9a-z]+)/results/$', views.result_speaker, name='results_speaker'),#ResultsView.as_view(), name='results'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})-hearer-$', views.result_hearer, name='results_hearer_base'),#ResultsView.as_view(), name='results'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})-speaker-$', views.result_speaker, name='results_speaker_base'),#ResultsView.as_view(), name='results'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/vote/$', views.vote, name='vote'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})-hearer-(?P<meaning>[0-9a-z]+)/results_json/$', views.result_hearer_json, name='results_hearer_json'),#ResultsView.as_view(), name='results'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})-speaker-(?P<meaning>[0-9a-z]+)-(?P<word>[0-9a-z]+)/results_json/$', views.result_speaker_json, name='results_speaker_json'),#ResultsView.as_view(), name='results'),
    # url(r'^results_inner/(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/(?P<bool_succ>(True|False))/$', views.result_inner, name='results_inner'),#ResultsView.as_view(), name='results'),
    # url(r'^results_inner/(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.result_inner, name='results_inner_base'),#ResultsView.as_view(), name='results'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})-speaker-(?P<meaning>[0-9a-z]+)-(?P<word>[0-9a-z]+)/results_json/$', views.result_speaker_json, name='results_speaker_json'),#ResultsView.as_view(), name='results'),
    # url(r'^(?P<xp_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.DetailView.as_view(), name='detail'),
    # url(r'^test/$',views.test,name='test'),
    # url(r'^accounts/profile/$', views.new_experiment, name='new_experiment_2'),
    # url(r'^userinfo_(?P<username>[\w-]+)$', views.create_and_login, name='send_user_info'),
]
