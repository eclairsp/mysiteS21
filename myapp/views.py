from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from .models import Topic, Course, Student
from .forms import SearchForm, OrderForm, ReviewForm


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
    last_login = request.session[
        'last_login'] if 'last_login' in request.session else "Your last login was more than one hour ago"
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
    course_list = Course.objects.filter(topic__exact=topic)
    return render(request, "myapp/details.html", {'topic': topic, 'course_list': course_list})


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
            rating = review_form.rating
            course = review_form.course
            if 1 <= rating <= 5:
                review_form.save()
                course.num_reviews = course.num_reviews + 1
                course.save()
                return redirect("myapp:index")
            else:
                return render(request, "myapp/review.html",
                              {'form': form, 'name': ' ', "errors": ["You must enter a rating between 1 and 5!"]})
        else:
            return render(request, "myapp/review.html", {'form': form, 'name': ' ', "errors": ["Check again"]})
    else:
        form = ReviewForm()
        return render(request, "myapp/review.html", {'form': form, 'name': ' '})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = now().isoformat()
                request.session.set_expiry(60 * 60)
                # return redirect("myapp:index")
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse("Invalid login details.")
    else:
        '''
        used the built in django login form.
        otherwise can uncomment the template for a custom form as well.
        '''
        form = AuthenticationForm()
        return render(request, "myapp/login.html", {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('myapp:index')


@login_required()
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
            return render(request, "myapp/myaccount.html", {'errors': ['You are not a registered student!']})
    except Student.DoesNotExist:
        return render(request, "myapp/myaccount.html", {'errors': ['You are not a registered student!']})
