from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


def enforce_rating(rating):
    if not 1 <= rating <= 5:
        raise ValidationError("You must enter a rating between 1 and 5!")


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.PositiveBigIntegerField(default=12)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree'),
    ]
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, blank=True)
    province = models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return "{0} {1} {2}".format(self.id, self.first_name, self.last_name)


class Order(models.Model):
    ORD_STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Confirmed'), (2, 'On Hold')]
    courses = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORD_STATUS_CHOICES, default=1)
    order_date = models.DateField(default=now)

    def __str__(self):
        status = str(self.ORD_STATUS_CHOICES[self.order_status][1])
        return "{0}'s order for {1} courses at ${2} is {3}".format(self.student.first_name, len(self.courses.all()),
                                                                   self.total_cost(), status.lower())

    def total_cost(self):
        return sum(course.price if course.price else 0 for course in self.courses.all())

    def total_items(self):
        return len(self.courses.all())


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[enforce_rating])
    comments = models.TextField(blank=True)
    date = models.DateField(default=now)

    def __str__(self):
        return "{0} rated {1} by {2}".format(self.course, self.rating, self.reviewer)
