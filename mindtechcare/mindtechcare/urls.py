from django.contrib import admin
from django.urls import path, include
from .views import HomePageView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('employees.urls')),
    path('api/', include('github.urls')),
    path('api/', include('trello.urls')),
    path("", HomePageView, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
