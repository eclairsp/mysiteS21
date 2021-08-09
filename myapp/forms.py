from django import forms
from django.contrib.auth.forms import UserCreationForm
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
        fields = ['courses']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect()}


class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'courses',  'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect()}
        labels = {'students;': u'Student Name'}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'course': forms.RadioSelect()}
        labels = {'reviewer': 'Please enter a valid email',
                  'rating': 'Rating: An integer between 1 (worst) and 5 (best)'}


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = ["username", "email", "first_name", "last_name", "city", "picture", "interested_in"]
        widgets = {"interested_in": forms.CheckboxSelectMultiple(), 'email': forms.EmailInput(),
                   'picture': forms.FileInput()}
        labels = {'picture': 'Profile Picture'}


class EditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'city', 'picture', 'level', 'address']
        widgets = {
            'picture': forms.FileInput(),
            'level': forms.RadioSelect
        }

        def __init__(self, *args, **kwargs):
            super(EditForm, self).__init__(*args, **kwargs)
            self.fields['level'].required = False


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100, label='Email address of the account:')
