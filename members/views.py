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

    return render(request, "members/new_member.html", {"form": form, "success_message": success_message})

def home(request):
    return render(request, "members/home.html")  # Ensure the correct path


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

def ongoing_events(request):
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