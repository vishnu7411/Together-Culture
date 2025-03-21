from django.shortcuts import render, redirect
from .models import OngoingEvent
from .forms import MemberForm,OngoingEventForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages

def register(request):
    success_message = None  # Stores the success message

    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.password = make_password(form.cleaned_data['password'])  # Hash password
            member.save()
            messages.success(request, "Registration successful!")
            return redirect("home")  # Redirect to home after successful signup
    else:
        form = MemberForm()

    return render(request, "new_member.html", {"form": form, "success_message": success_message})

def home(request):
    return render(request, "home.html")  # Ensure the correct path


from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")  # Redirect to home page after login
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "members/login.html")  # Ensure the login template exists

def manage_events(request):
    """View to display all ongoing events"""
    events = OngoingEvent.objects.all()
    return render(request, 'members/ongoing_events.html', {'events': events})

def add_ongoing_event(request):
    """View to add a new ongoing event"""
    if request.method == 'POST':
        form = OngoingEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ongoing_events')
    else:
        form = OngoingEventForm()
    return render(request, 'members/add_ongoing_event.html', {'form': form})
    return render(request, "login.html")  # Ensure the login template exists


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Only allow admins
            login(request, user)
            return redirect("admin_dashboard")  # Redirects to the Admin Dashboard
        else:
            return render(request, "admin_login.html", {"error_message": "Invalid credentials or not an admin!"})

    return render(request, "admin_login.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def admin_logout(request):
    logout(request)
    return redirect("admin_login")

from django.shortcuts import render
from .models import Member  # Ensure you have imported your Member model

from django.shortcuts import render
from .models import Member

def registered_members(request):
    members = Member.objects.filter(is_approved=True).values(
        "first_name", "last_name", "email", "membership_type", "gender"
    )
    return render(request, "registered_members.html", {"members": members})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Member  # Import Member model

def pending_members(request):
    """View to display all pending members"""
    members = Member.objects.filter(is_approved=False)  # Get only unapproved members
    return render(request, "pending_members.html", {"members": members})

def approve_member(request, member_id):
    """Approve a member and move them to the registered members list"""
    member = get_object_or_404(Member, id=member_id)
    member.is_approved = True  # Approve the member
    member.save()
    return redirect("pending_members")  # Redirect back to pending list

def reject_member(request, member_id):
    """Reject a member and delete from the database"""
    member = get_object_or_404(Member, id=member_id)
    member.delete()  # Remove from database
    return redirect("pending_members")  # Redirect back to pending list

from django.shortcuts import render, redirect
from .models import Event

def add_event(request):
    if request.method == "POST":
        name = request.POST.get('name')
        event_type = request.POST.get('event_type')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')

        # Save to database
        Event.objects.create(
            name=name,
            event_type=event_type,
            location=location,
            capacity=capacity,
            event_date=event_date,
            event_time=event_time
        )
        return redirect('manage_events')  # Redirect to events page

    return render(request, 'add_event.html')

def manage_events(request):
    events = Event.objects.all()  # Fetch all events
    return render(request, 'manage_events.html', {'events': events})
