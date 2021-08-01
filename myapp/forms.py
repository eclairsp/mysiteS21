from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from myapp.models import Order, Review, Student


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, label="Student Name", required=False)
    length = forms.TypedChoiceField(widget=forms.RadioSelect, label="Preferred course duration",
                                    choices=LENGTH_CHOICES, required=False, coerce=int)
    max_price = forms.IntegerField(min_value=0, label="Maximum Price")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect()}
        labels = {'student': u'Student Name'}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'course': forms.RadioSelect()}
        labels = {'reviewer': 'Please enter a valid email',
                  'rating': 'Rating: An integer between 1 (worst) and 5 (best)'}


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["username", "password", "first_name", "last_name", "address", "interested_in"]
        widgets = {"interested_in": forms.RadioSelect(), "password": forms.PasswordInput()}