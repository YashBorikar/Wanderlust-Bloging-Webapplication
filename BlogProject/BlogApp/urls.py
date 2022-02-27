from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('<int:year>/<int:month>/<int:day>/<str:post>/', views.post_detail_view, name="post_detail"),
    path('create-post/', views.createpost),
    path('<int:id>/share', views.mail_send_view),
    path('tag/<str:tag_slug>', views.index, name='post_list_by_tag_name'),
]