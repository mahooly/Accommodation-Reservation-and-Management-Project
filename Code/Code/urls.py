"""Code URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf.urls.static import static
from Code import settings
from accommodation import views as accommodation_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('registration.urls')),
                  path('', include('accommodation.urls')),
                  path('', include('admin_dashboard.urls')),
                  path('', include('search_index.urls')),
                  path('', include('blog.urls')),
                  path('', include('reservation.urls')),
                  path('', include('review.urls')),
                  path('summernote/', include('django_summernote.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
