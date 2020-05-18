"""training_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from authentication import views as auth_views
from training import views as training_views
from routine import views as routine_views

urlpatterns = [
    path('', training_views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('dashboard/', training_views.dashboard, name='dashboard'),
    path('routine/', routine_views.routine_list, name='routine_list'),
    path('routine/detail/<int:pk>/', routine_views.routine_detail, name='routine_detail'),
    path('routine/create/', routine_views.routine_create, name='routine_create'),
    path('routine/edit/<int:pk>/', routine_views.routine_edit, name='routine_edit'),
    path('routine/<int:pk>/instruction/', routine_views.routine_instruction_list, name='routine_instruction_list'),
    path('routine/<int:pk>/instruction/create/', routine_views.routine_instruction_create,
         name='routine_instruction_create'),
    path('routine/<int:routine_pk>/instruction/edit/<int:instruction_pk>', routine_views.routine_instruction_edit,
         name='routine_instruction_edit'),
    path('training/', training_views.training_list, name='training_list'),
    path('training/create/', training_views.training_create, name='training_create'),
    path('training/delete/<int:pk>/', training_views.training_delete, name='training_delete'),
    path('trainer/dashboard/', training_views.trainer_dashboard, name='trainer_dashboard'),
]
