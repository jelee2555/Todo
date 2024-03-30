from django.urls import path

from task import views

urlpatterns = [
    path('', views.TaskAPIView.as_view()),
    path('list/', views.TaskListAPIView.as_view()),

]