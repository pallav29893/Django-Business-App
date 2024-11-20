from django.urls import path ,include
from blog.apiviews import CategoryApiView,PostApiView,TagApiView,SignUpApiView,CommentApiView,LoginApiView,ProfileApiView,PostListApiView,PostDetailApiView,CommentListApiView,CommentDetailApiView,UserDetailApiView,UserListApiView,ProfileDetailApiView,ProfileListApiView
from rest_framework import routers


router = routers.SimpleRouter()
router.register('get-categories', CategoryApiView)
router.register('get-comments', CommentApiView)
router.register('get-tags', TagApiView)
router.register('get-posts', PostApiView)
router.register('get-profiles', ProfileApiView)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpApiView.as_view(), name='signup'),
    path('login/', LoginApiView.as_view(), name='signin'),
    path('posts-list/', PostListApiView.as_view(), name='posts'),
    path('posts-list/<int:pk>/', PostDetailApiView.as_view(), name='posts'),
    path('comments-list/', CommentListApiView.as_view(), name='comments'),
    path('comments-list/<int:pk>/', CommentDetailApiView.as_view(), name='comments'),
    path('user/', UserListApiView.as_view(), name='users'),
    path('user/<int:pk>/', UserDetailApiView.as_view(), name='users'),
    path('Profile/', ProfileListApiView.as_view(), name='profiles'),
    path('Profile/<int:pk>/', ProfileDetailApiView.as_view(), name='profiles'),
    path('api-auth/', include('rest_framework.urls')),
]

# urlpatterns = router.urls
