from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.loginpage, name="loginpage"),
    path("logout/", views.logoutuser, name="logoutuser"),
    path("register/", views.registerpage, name="registerpage"),
    path("update_user/", views.updateUser, name="update_user"),
    path("profile/<int:pk>", views.userprofile, name="user_profile"),
    path("", views.home, name="home"),
    path("room/<int:pk>/", views.room, name="room"),
    path("createroom", views.createroom, name="create_room"),
    path("updateroom/<int:pk>", views.update_room, name="update_room"),
    path("deleteroom/<int:pk>", views.delete_room, name="delete_room"),
    path("delete_message/<int:pk>", views.delete_message, name="delete_message"),
]
