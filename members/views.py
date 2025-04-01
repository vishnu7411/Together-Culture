from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm

from .models import Member, Event
from .forms import MemberForm

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Member

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        email = request.POST['email']
        password = request.POST['password']
        interests = request.POST.get('interests', '')
        membership_type = request.POST.get('membership_type', '')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # ✅ Step 1: Create Django User
            username = email.split('@')[0]
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # ✅ Step 2: Create Member linked to User
            Member.objects.create(
                user=user,  # <- 🔥 THIS is what was missing!
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                email=email,
                interests=interests,
                membership_type=membership_type
            )

            # ✅ Step 3: Log in and redirect
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('register')

    return render(request, 'new_member.html')

def home(request):
    return render(request, "home.html")

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Member

def user_login(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('username')
        password = request.POST.get('password')

        # Allow login via email
        try:
            user = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return render(request, 'login.html')

        # Authenticate securely
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            try:
                # Get linked Member
                member = Member.objects.get(email=user.email)

                if not member.is_approved:
                    messages.error(request, "Admin approval is required before you can login. Please try again later.")
                    return render(request, 'login.html')

                # If approved, login user
                login(request, user)
                messages.success(request, f"Welcome, {member.first_name}!")
                return redirect('member_dashboard')

            except Member.DoesNotExist:
                messages.error(request, "Your user account has no member profile.")
        else:
            messages.error(request, "Incorrect password.")

    return render(request, 'login.html')


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

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Member

def approve_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.is_approved = True
    member.save()

    # ✅ Send approval email
    subject = 'Your Together Culture account has been approved!'
    message = f"""
    Hi {member.first_name},

    🎉 Great news! Your Together Culture account has been approved by the admin.

    You can now log in and start exploring events, spaces, and the community.

    👉 Login here: http://127.0.0.1:8000/login/

    See you inside!
    - Together Culture Team
    """
    send_mail(subject, message, 'vivekvardhan378@gmail.com', [member.email], fail_silently=False)

    messages.success(request, f"{member.first_name}'s account has been approved and notified via email.")
    return redirect("pending_members")


from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Member

def reject_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    # ✅ Send rejection email
    subject = 'Update on Your Together Culture Membership'
    message = f"""
    Hi {member.first_name},

    Thank you for your interest in joining Together Culture. 
    Unfortunately, your membership request was not approved at this time.

    If you believe this was a mistake or would like to reapply in the future, feel free to reach out.

    We appreciate your enthusiasm and wish you all the best.

    - Together Culture Team
    """
    send_mail(subject, message, 'vivekvardhan378@gmail.com', [member.email], fail_silently=False)

    member.delete()
    messages.success(request, f"{member.first_name}'s membership was rejected and notified via email.")
    return redirect("pending_members")
