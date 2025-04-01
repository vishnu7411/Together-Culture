from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm

from .models import Member, Event
from .forms import MemberForm

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        email = request.POST['email']
        password = request.POST['password']
        interests = request.POST.get('interests', '')
        membership_type = request.POST.get('membership_type', '')

        if Member.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            Member.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                email=email,
                password=password,
                interests=interests,
                membership_type=membership_type
            )
            messages.success(request, 'Registration successful!')

    return render(request, 'new_member.html')

def home(request):
    return render(request, "home.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")

def manage_events(request):
    events = Event.objects.all()
    return render(request, 'manage_events.html', {'events': events})

def add_event(request):
    if request.method == "POST":
        name = request.POST.get('name')
        event_type = request.POST.get('event_type')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')

        Event.objects.create(
            name=name,
            event_type=event_type,
            location=location,
            capacity=capacity,
            event_date=event_date,
            event_time=event_time
        )
        return redirect('manage_events')

    return render(request, 'add_event.html')

@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Wrong username or password.")

    return render(request, "admin_login.html")

def admin_logout(request):
    logout(request)
    return redirect("admin_login")

def registered_members(request):
    members = Member.objects.filter(is_approved=True)
    return render(request, "registered_members.html", {"members": members})

def pending_members(request):
    members = Member.objects.filter(is_approved=False)
    return render(request, "pending_members.html", {"members": members})

def approve_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.is_approved = True
    member.save()
    return redirect("pending_members")

def reject_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect("pending_members")

def events_page(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            send_mail(
                'Password Reset Request',
                'Click the link below to reset your password.',
                'your-email@gmail.com',
                [email],
                fail_silently=False
            )
            messages.success(request, "Password reset email sent successfully!")
            return redirect('password-reset-done')
        else:
            messages.error(request, "Invalid email address!")
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})


from .forms import OngoingEventForm

def add_ongoing_event(request):
    """View to add a new ongoing event"""
    if request.method == 'POST':
        form = OngoingEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_events')
    else:
        form = OngoingEventForm()
    return render(request, 'add_event.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Member

def user_login(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Get user from User model based on email
            user = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            messages.error(request, "No user with that email.")
            return render(request, 'login.html')

        # Authenticate using username (not email)
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)

            try:
                # Now get matching member
                member = Member.objects.get(email=user.email)
                request.session['member_id'] = member.id
                messages.success(request, f"Welcome, {member.first_name}!")
            except Member.DoesNotExist:
                messages.warning(request, "User logged in, but member profile not found.")

            return redirect('member_dashboard')
        else:
            messages.error(request, "Incorrect password.")

    return render(request, 'login.html')


from django.shortcuts import render, redirect
from .models import Member

def member_dashboard(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('user_login')  # Ensure user is logged in

    member = Member.objects.get(id=member_id)
    return render(request, 'member_dashboard.html', {'member': member})


from django.contrib.auth import logout

def member_logout(request):
    logout(request)
    request.session.flush()  # Clear session
    list(messages.get_messages(request))
    return redirect('home')  # Redirect to home or login

from django.shortcuts import render
from .models import Event, Member

def member_dashboard(request):
    # ✅ Match member by email
    member = Member.objects.get(email=request.user.email)

    # ✅ Get events
    events = Event.objects.all().order_by('event_date', 'event_time')

    return render(request, 'member_dashboard.html', {
        'member': member,
        'events': events,
    })

