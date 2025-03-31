from django.shortcuts import render, redirect
from .forms import MemberForm
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
