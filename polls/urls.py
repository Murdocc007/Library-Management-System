from django.conf.urls import url,patterns,include
from django.contrib import admin
from polls import views


urlpatterns=patterns('',
        url(r'^$', views.index),
        url(r'^sign_up/$',views.sign_up,name='sign_up'),
        url(r'^sign_in/$',views.sign_in,name='sign_in'),
        url(r'^logout/$',views.logout_view,name='logout'),
        url(r'^borrow/(?P<Book_id>\w{0,30})/(?P<Branch_id>\w{0,30})/$',views.borrow,name='borrow'),
        url(r'^borrowconfirm/(?P<Book_id>\w{0,30})/(?P<Branch_id>\w{0,30})/$',views.borrowConfirm,name='borrowconfirm'),
        url(r'^fine/$',views.getFine,name='fine'),
        url(r'^viewUserFines$',views.viewUserFines,name='userfine'),
        url(r'^viewUserFines/(?P<user_id>\w{0,30})$',views.viewUserFines,name='userfine'),
        url(r'^removeFine/(?P<borrow_id>\w{0,30})$',views.removeFine,name='removefine'),
    )
