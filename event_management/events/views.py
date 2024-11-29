from django.shortcuts import get_object_or_404, render, redirect
from .models import Event
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create

@login_required
def create_event(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        description = request.POST.get("description")
        Event.objects.create(name=name, date=date, description=description)
        return redirect("list_events")
    return render(request, "create_event.html")

# Read

@login_required
def list_events(request):
    events = Event.objects.all()
    return render(request, "list_events.html", {"events": events})

# Update

@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # Retrieve event by ID or return 404 if not found
    if request.method == "POST":
        event.name = request.POST.get("name")
        event.date = request.POST.get("date")
        event.description = request.POST.get("description")
        event.save()  # Save updated event
        return redirect("list_events")  # Redirect to the list view

    return render(request, "update_event.html", {"event": event})  # Render update form

# Delete

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # Retrieve event by ID or return 404 if not found
    if request.method == "POST":
        event.delete()  # Delete the event
        return redirect("list_events")  # Redirect to the list view

    return render(request, "delete_event.html", {"event": event})  # Render delete confirmation

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "User created successfully! Please log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("signup")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("list_events")  # Redirect to the homepage
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")