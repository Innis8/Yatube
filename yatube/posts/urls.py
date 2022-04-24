from django.urls import include, path
from rest_framework.routers import DefaultRouter
from posts import views

app_name = 'posts'

# роутер для View-классов на основе viewsets
router = DefaultRouter()

# В качестве аргументов этот метод принимает URL-префикс и название вьюсета,
# для которого создаётся набор эндпоинтов
# В роутере можно зарегистрировать любое количество пар "URL, viewset",
# например,
# router.register('owners', OwnerViewSet)
router.register('v1/posts', views.PostViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path(
        'posts/<post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path('follow/', views.follow_index, name='follow_index'),
    # path('api/v1/posts/', views.api_posts, name='api_posts'),
    # path('api/v1/posts/<int:post_id>/', views.get_post, name='get_post'),
    # path(
    #     'api/v1/posts/<int:post_id>/',
    #     views.api_posts_detail,
    #     name='api_posts_detail'
    # ),
    # для View-классов низкоуровневых
    # path('api/v1/posts/', views.APIPost.as_view()),
    # path('api/v1/posts/<int:post_id>/', views.APIPostDetail.as_view()),

    # для View-классов на основе generics
    # path('api/v1/posts/', views.APIPostList.as_view()),
    # path('api/v1/posts/<int:pk>/', views.APIPostDetail.as_view()),

    # Все зарегистрированные в router пути доступны в router.urls
    # Включим их в головной urls.py
    path('api/', include(router.urls)),
]
