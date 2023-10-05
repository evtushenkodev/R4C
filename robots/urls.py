from django.urls import path

from .views import RobotCreateView, RobotReportView

urlpatterns = [
    path('create_robot/', RobotCreateView.as_view(), name='create_robot'),
    path('robot_report/', RobotReportView.as_view(), name='download_report'),
]
