
from django.contrib import admin
from django.urls import path,include
from pages import views
from django.conf import settings
from django.conf.urls.static import static


# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',include('pages.urls')),
    path('',views.home,name='index'),
    path('symptomchecker/',include('symptomchecker.urls'))

]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)