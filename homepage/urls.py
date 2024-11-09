from django.urls import path

from homepage.apps import HomepageConfig
from homepage.views import HomePageView

app_name = HomepageConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]