import datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import Event
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from .models import Event, RSVP

# Create

@login_required
def create_event(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        description = request.POST.get("description")

        # Automatically set the organizer to the logged-in user
        Event.objects.create(
            name=name,
            date=date,
            description=description,
            organizer=request.user  # Assign the logged-in user as the organizer
        )
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
@login_required
def dashboard(request):
    total_events = Event.objects.count()
    registered_events = RSVP.objects.filter(user=request.user).count()
    upcoming_events = Event.objects.filter(date__gte=datetime.date.today()).count()

    return render(request, 'dashboard.html', {
        'total_events': total_events,
        'registered_events': registered_events,
        'upcoming_events': upcoming_events
    })
@login_required
def all_events(request):
    events = Event.objects.all()
    return render(request, 'all_events.html', {'events': events})
@login_required
def event_details(request, event_id):
    # Safely fetch the event or return a 404 if it doesn't exist
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is already registered for the event
    is_registered = RSVP.objects.filter(user=request.user, event=event).exists()

    if request.method == "POST":
        # Handle RSVP registration
        if 'rsvp' in request.POST:
            RSVP.objects.get_or_create(user=request.user, event=event)
            is_registered = True  # Update the variable after RSVP

        # Handle RSVP cancellation
        elif 'cancel_rsvp' in request.POST:
            RSVP.objects.filter(user=request.user, event=event).delete()
            is_registered = False  # Update the variable after cancellation

    # Render the event details template
    return render(request, 'event_details.html', {
        'event': event,
        'is_registered': is_registered
    })
@login_required
def my_events(request):
    # Fetch events created by the logged-in user
    created_events = Event.objects.filter(organizer=request.user)

    # Fetch RSVP details for created events
    # Attach RSVP details to each event for easy access in the template
    for event in created_events:
        event.rsvps = RSVP.objects.filter(event=event).select_related('user')

    # Fetch events the logged-in user has registered for
    registered_events = RSVP.objects.filter(user=request.user).select_related('event')

    return render(request, 'my_events.html', {
        'created_events': created_events,
        'registered_events': registered_events,
    })
@login_required
def profile(request):
    if request.method == "POST":
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.email = request.POST['email']
        request.user.save()

    return render(request, 'profile.html', {'user': request.user})
