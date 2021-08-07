from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from .models import Topic, Course, Student, User
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm, ForgetPasswordForm, EditForm
import hashlib
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime


# Create your views here.
# def index(request):
#     top_list = Topic.objects.all().order_by('id')[:10]
#     course_list = Course.objects.all().order_by('-title')[:5]
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of topics: ' + '</p>'
#     response.write(heading1)
#     for topic in top_list:
#         para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
#         response.write(para)
#
#     heading2 = '<p>' + 'List of Courses: ' + '</p>'
#     response.write(heading2)
#     for course in course_list:
#         para = '<p>' + str(course) + ' - ' + str(course.price) + '</p>'
#         response.write(para)
#     return response


def index(request):
    last_login = "at {} UTC".format(datetime.fromisoformat(request.session[
                                                               'last_login'])) if 'last_login' in request.session else "more than one hour ago"
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list, 'last_login': last_login})


# def about(request):
#     response = HttpResponse()
#     heading = "<h1> This is an E-learning Website! Search our Topics to find all available Courses </h1>"
#     response.write(heading)
#     return response
def about(request):
    try:
        cookie = request.COOKIES["about_visits"]
        response = render(request, "myapp/about.html", {'about_visits': int(cookie) + 1})
        response.set_cookie("about_visits", int(cookie) + 1, max_age=5 * 60)
        return response
    except KeyError:
        response = render(request, "myapp/about.html")
        response.set_cookie('about_visits', 1)
        return response


# def details(request, topic_id):
#     response = HttpResponse()
#     topic = get_object_or_404(Topic, pk=topic_id)
#     course_list = Course.objects.filter(topic__exact=topic)
#
#     heading = "<h1>" + topic.name.upper() + " - " + str(topic.length) + " weeks" + "</h1>"
#     response.write(heading)
#
#     for course in course_list:
#         para = '<p>' + str(course) + ' - ' + str(course.price) + '</p>'
#         response.write(para)
#
#     return response


def details(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, "myapp/details.html",
                  {'topic': topic, 'course_list': topic.courses.all(), 'students': topic.student_set.all()})


def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "myapp/course.html",
                  {"course": course, "reviews": course.review_set.all(), "students": course.student_set.all()})


# topic = Topic.objects.get(id==1).


def findcourses(request):
    if request.method == "POST":
        unbound_form = SearchForm()
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            length = data['length']
            price = data["max_price"]
            topics = Topic.objects.filter(length=length) if length != "" else Topic.objects.all()
            course_list = []
            for topic in topics:
                course_list.extend(topic.courses.filter(price__lte=price))
            return render(request, "myapp/results.html",
                          {"name": name, "course_list": course_list, "length": length,
                           "form": unbound_form, "max_price": price})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, "myapp/findcourses.html", {"form": form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=False)
            student = order.student
            status = order.order_status
            order.save()
            form.save_m2m()
            if status == 1:
                for course in order.courses.all():
                    student.registered_courses.add(course)
            # if status == 0:
            #     for course in order.courses.all():
            #         student.registered_courses.remove(course)
            return render(request, "myapp/order_response.html",
                          {"courses": courses, "order": order})
        else:
            return render(request, "myapp/place_order.html", {"form": form})
    else:
        form = OrderForm()
        return render(request, "myapp/place_order.html", {"form": form})


# giving name = " ", because as users specify email while reviewing it could be anyone not necessarily logged in user!
# so to be consistent can also do in form context 'name': username and it would consistent
def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_form = form.save(commit=False)
            course = review_form.course
            review_form.save()
            course.num_reviews = course.num_reviews + 1
            course.save()
            return redirect("myapp:index")
        else:
            return render(request, "myapp/review.html", {'form': form, "errors": "Check again"})
    else:
        form = ReviewForm()
        return render(request, "myapp/review.html", {'form': form})


def user_login(request):
    if request.method == "GET":
        next_page = request.GET.get('next', '/')
        if next_page != '/':
            request.session['login_from'] = next_page
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        password = request.POST["password"]
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session['last_login'] = now().isoformat()
                    request.session.set_expiry(60 * 60)
                    # return redirect("myapp:index")
                    if 'login_from' in request.session:
                        return HttpResponseRedirect(request.session['login_from'])
                    else:
                        return redirect('myapp:index')
                else:
                    response = HttpResponse('Your account is disabled.')
        else:
            response = render(request, "myapp/login.html", {'form': form, "errors": form.errors})
    else:
        '''
        used the built in django login form.
        '''
        form = AuthenticationForm()
        response = render(request, "myapp/login.html", {'form': form})

    # if need to display forget password msg
    if "forgetPassword_msg" in request.COOKIES:
        # even deleted, it will still appear once
        response.delete_cookie("forgetPassword_msg")

    return response


@login_required(login_url='/myapp/login')
def user_logout(request):
    logout(request)
    return redirect('myapp:index')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form.save_m2m()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('myapp:myaccount')
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse("Cannot login currently. Try again!")
        else:
            return render(request, "myapp/register.html", {"form": form})
    else:
        form = RegisterForm()
        return render(request, "myapp/register.html", {"form": form})


@login_required(login_url='/myapp/login')
def myaccount(request):
    courses = []
    interested_in = []
    student_id = request.user.id

    try:
        student = Student.objects.get(pk=student_id)
        # stricter if condition
        # if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
        if request.user.is_authenticated:
            first_name = student.first_name
            last_name = student.last_name
            courses.extend(student.registered_courses.all())
            interested_in.extend(student.interested_in.all())
            return render(request, "myapp/myaccount.html",
                          {'first_name': first_name, 'last_name': last_name, 'courses': courses,
                           'interested_in': interested_in})
        else:
            return render(request, "myapp/myaccount.html", {'error': 'You are not a registered student!'})
    except Student.DoesNotExist:
        return render(request, "myapp/myaccount.html", {'error': 'You are not a registered student!'})


@login_required(login_url='/myapp/login')
def edit_profile(request):
    if request.method == "POST":
        user = Student.objects.get(id=request.user.id)
        form = EditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated {}'s profile".format(request.user.username))
            return redirect("myapp:myaccount")
        else:
            return render(request, "myapp/edit_profile.html", {"form": form})
    else:
        form = EditForm(instance=request.user)
        return render(request, "myapp/edit_profile.html", {"form": form})


@login_required(login_url='/myapp/login')
def change_password(request):
    user = Student.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('myapp:myaccount')
        else:
            return render(request, "myapp/change_password.html", {'form': form})
    else:
        form = PasswordChangeForm(user)
        return render(request, "myapp/change_password.html", {'form': form})

def forget_password(request):
    help_text = 'Please enter the email of your account and we will send you a new password.'

    if request.method == "POST":
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            request_email = form.cleaned_data['email']
            print(request_email)

            try:
                target_user = User.objects.get(email__exact=request_email)
                # generate string for hashing
                random_string = request_email + datetime.now().isoformat()

                # get first 16 chars from the hashed value
                hash_password = hashlib.sha224(random_string.encode()).hexdigest()[:16]

                email_subject = 'Password Reset'
                email_message = "Dear " + target_user.username + ",\n\n" \
                                + "Your new password is:\n" \
                                + hash_password + "\n" \
                                + "Please log in and change your password.\n" \
                                + "Have a very nice day!\n\n" \
                                + "Best Regards,\n" \
                                + "Comp8347 Group 9"
                sender = 'noreply@comp8347group9project.com'
                receiver_list = [request_email]

                send_mail(subject=email_subject,
                          message=email_message,
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=receiver_list,
                          fail_silently=False)
                target_user.set_password(hash_password)
                target_user.save()

                response = redirect("myapp:login")
                response.set_cookie("forgetPassword_msg", "New password sent to email")
                return response

            except:
                response = render(request, "myapp/forget_password.html",
                                  {"form": form, 'helptext': help_text, "local_forgetPassword_msg": "Invalid email"})
                return response

        response = render(request, "myapp/forget_password.html",
                          {"form": form, 'helptext': help_text, "local_forgetPassword_msg": "Invalid form. Try again!"})
        return response

    else:
        form = ForgetPasswordForm()
        return render(request, "myapp/forget_password.html", {"form": form, 'helptext': help_text})
