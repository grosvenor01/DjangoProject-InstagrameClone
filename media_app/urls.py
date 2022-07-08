from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('setting/',views.setting,name='setting'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('follow/',views.follow,name='follow'),
    path('search/',views.search,name='search'),
    path('delete/<uuid:id>',views.delete,name='delete'),
    path('like/',views.likepost,name='likepost'),
    path('logout/',views.logout,name='logout'),
    path('upload/',views.upload,name='upload'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)