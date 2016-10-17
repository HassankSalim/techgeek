from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^add$', views.add_to_model, name='add_to_model'),
	url(r'^getRank$', views.getRank, name='getRank'),
	url(r'^leaderboard$', views.top, name='top10'),
	url(r'^test$', views.simpleServe, name='simpleServe'),
	url(r'^get-question$', views.view_qn, name='view_qn'),
]