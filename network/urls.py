from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_post', views.new_post, name='new_post'),
    path('friends_posts', views.friends_posts, name='friends_posts'),
    path('following', views.following, name='following'),
    path('followers', views.followers, name='followers'),
    path('liked_posts', views.liked_posts, name='liked_posts'),
    path('profile/<str:profile_username>', views.profile, name='profile'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('follow/<str:profile_username>', views.follow, name='follow'),
    path('unfollow/<str:profile_username>', views.unfollow, name='unfollow'),

    # API routes
    path('like/<int:post_id>', views.like, name='like'),
    path('dislike/<int:post_id>', views.dislike, name='dislike'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post')
]
