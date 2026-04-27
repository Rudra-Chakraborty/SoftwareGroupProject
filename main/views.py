from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Staff, Team, Department
from django.contrib.auth.hashers import make_password, check_password



# LOGIN

def login_view(request):

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "login":
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user = User.objects.get(email=email)

                if check_password(password, user.password_hash):

                    request.session["user_email"] = user.email
                    request.session["user_id"] = user.user_Id

                    return redirect("dashboard")

                else:
                    messages.error(request, "Wrong password")

            except User.DoesNotExist:
                messages.error(request, "User not found")

        elif action == "register":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            role = request.POST.get("role")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                user = User.objects.create(
                    email=email,
                    password_hash=make_password(password),
                    role=role
                )

                Staff.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name
                )

                messages.success(request, "Account created successfully")

        elif action == "reset":
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user = User.objects.get(email=email)
                user.password_hash = make_password(password)
                user.save()

                messages.success(request, "Password updated")

            except User.DoesNotExist:
                messages.error(request, "User not found")

    return render(request, "login.html")



# DASHBOARD

def dashboard(request):

    email = request.session.get("user_email")
    if not email:
        return redirect("login")

    user = User.objects.get(email=email)

    staff = Staff.objects.filter(user=user).first()

    teams = Team.objects.all()[:4]
    staff_list = Staff.objects.all()[:4]

    return render(request, "dashboard.html", {
        "staff": staff,
        "teams": teams,
        "staff_list": staff_list,
        "user_role": user.role
    })



# ADMIN DASHBOARD

def admin_dashboard(request):

    email = request.session.get("user_email")
    if not email:
        return redirect("login")

    user = User.objects.get(email=email)

    staff = Staff.objects.filter(user=user).first()

    teams = Team.objects.all()
    staff_list = Staff.objects.all()

    return render(request, "admin_dashboard.html", {
        "staff": staff,
        "teams": teams,
        "staff_list": staff_list,
        "user_role": user.role
    })



# PROFILE

def profile_view(request):

    email = request.session.get("user_email")
    if not email:
        return redirect("login")

    user = User.objects.get(email=email)

    staff = Staff.objects.filter(user=user).first()

    return render(request, "profile.html", {
        "staff": staff,
        "user_role": user.role
    })



# DEPARTMENTS

def department_view(request):

    email = request.session.get("user_email")
    if not email:
        return redirect("login")

    user = User.objects.get(email=email)

    staff = Staff.objects.filter(user=user).first()

    q = request.GET.get("q")

    if q:
        departments = Department.objects.filter(
            department_name__icontains=q
        )
    else:
        departments = Department.objects.all()

    return render(request, "department.html", {
        "departments": departments,
        "staff": staff,
        "user_role": user.role
    })