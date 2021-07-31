import django
from myapp.models import Topic, Course, Student, Order

# List all the courses in the db.
Course.objects.all()

# List all the students in the db.
Student.objects.all()

# List all the orders in the db.
Order.objects.all()

#List all students whose last name is ‘Jones’
Student.objects.filter(last_name__exact = 'Jones')

# List all topics whose course length is 8 weeks
Topic.objects.filter(length__exact = 8)

# List all students that live on ‘Sunset Avenue’.
Student.objects.filter(address__contains = "Sunset Avenue")

# List all students that live on an ‘Avenue’ and live in province ‘ON’.
Student.objects.filter(address__contains = "Avenue").filter(province__exact = "ON")
# OR
Student.objects.filter(address__contains = "Avenue", province__exact = "ON")

# List all the students that are interested in Topic 'Sports'
sports = Topic.objects.filter(name__exact = "Sports")
Student.objects.filter(interested_in__in = sports)
# OR
sports = Topic.objects.get(name__exact = "Sports")
Student.objects.filter(interested_in = sports)

# List the courses that cost more than $150.00
Course.objects.filter(price__gt = 150.00)

# List the students that do NOT live in ON.
Student.objects.exclude(province__exact = "ON")

# List the Orders placed by a student whose first_name is ‘Chris’.
chris = Student.objects.get(first_name__exact = "Chris")
Order.objects.filter(student__exact = chris)
Order.objects.filter(student__exact = chris)[0].courses.all()
# OR
Order.objects.get(student__exact = chris).courses.all()

# List the courses that are currently NOT for_everyone.
Course.objects.exclude(for_everyone = True)
# OR
Course.objects.filter(for_everyone= False)

# Get the first name of the student of the Order with pk=1.
Order.objects.get(pk=1).student.first_name

# List all topics that the student with username ‘john’ is interested_in.
Student.objects.get(username__exact="john").interested_in.all()
# OR
Student.objects.filter(username__exact="john")[0].interested_in.all()

# List all the courses with a price < $150 and is for_everyone.
Course.objects.filter(price__lt = '150').filter(for_everyone = True)
# OR
Course.objects.filter(price__lt = '150', for_everyone = True)

# List the Topics that the student who ordered a Web Dev Bootcamp is interested_in. Assume there is exactly one order for Web Dev Bootcamp course.
course = Course.objects.filter(title__exact = "Web Dev Bootcamp")
Order.objects.get(courses__in = course).student.interested_in.all()

# Find the length of the courses for the topic that ‘chris’ is interested in. (You may assume that ‘alan’ is interested in exactly one topic.)
Student.objects.get(username__exact = "chris").interested_in.all()[0].length
# OR
Student.objects.get(username__exact = "chris").interested_in.get().length
# OR
print([topic.length for topic in Student.objects.get(username__exact = "chris").interested_in.all()])

# Find the number of courses that ‘chris’ is registered in.
len(Student.objects.get(username__exact = "chris").registered_courses.all())
# OR
Student.objects.get(username__exact = "chris").registered_courses.count()
