from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^success$', views.success),
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^add_item$', views.add_item),
    url(r'^logout$', views.logout),
    url(r'^show/(?P<item_id>\d+)$', views.show),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
    url(r'^remove/(?P<item_id>\d+)$', views.remove),
    url(r'^add_wish/(?P<item_id>\d+)$', views.add_wish),
]
