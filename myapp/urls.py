from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.RegisterAPI.as_view()),
    path('login/',views.LoginAPI.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('forgot-password/<int:pk>',views.ChangePasswordView.as_view()),
    path('view-profile/<int:pk>',views.ViewProfileAPI.as_view()),
    path('edit-profile/',views.EditProfileAPI.as_view()),

    path('add-post/',views.AddPostAPI.as_view()),
    path('view-post/',views.ViewPostAPI.as_view()),
    path('view-one-post/<int:pk>',views.ViewOnePostAPI.as_view()),
    path('edit-post/<int:pk>',views.EditPostAPI.as_view()),
    path('delete-post/<int:pk>',views.DeletePostAPI.as_view()),


    path('follow/<int:pk>',views.FolowAPI.as_view()),
    path('like/<int:pk>',views.LikeAPI.as_view()),


    path('comment/<int:pk>',views.CommentAPI.as_view()),
    path('view-comment/<int:pk>',views.ViewCommentAPI.as_view()),
]
