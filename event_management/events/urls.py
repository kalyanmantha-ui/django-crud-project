from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("", views.list_events, name="list_events"),  # List all events
    path("create/", views.create_event, name="create_event"),  # Create a new event
    path("update/<int:event_id>/", views.update_event, name="update_event"),  # Update event details
    path("delete/<int:event_id>/", views.delete_event, name="delete_event"),
    path("logout/", views.logout_view, name="logout"),
]
