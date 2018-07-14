"""nursery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include

from journal.views import KidView, KidsView, JournalView, KidJournalView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('kids/<int:kid_id>/', KidView.as_view()),
    path('kids/', KidsView.as_view(), name='kids'),
    path('journal/', JournalView.as_view(), name='journal'),
    path('journal/<int:kid_id>/', KidJournalView.as_view(), name='kid_journal')
]

