# Internet App / Distributed Sys - COMP 8347 Project
This our final project, which itself was an extension of the application (_mysiteS21/myapp_)  we developed in our labs/assignments.
## Features
We will be listing all the features that we have implemented
### Required

 - [X] In admin.py create a class CourseAdmin(admin.ModelAdmin), register this with the admin site and show the name, topic, price, hours, and for_everyone fields, for each Course, in the admin interface page that lists all Courses. (1)
 - [X] In admin.py write an action add_50_to_hours(…)for CourseAdmin class that will add 10 to the current value of the hours field for the selected courses and save the updated value in the database. (2)
 - [X] In admin.py create a class StudentAdmin(admin.ModelAdmin), register this with the admin site and show the first_name, last_name, city fields. Define upper_case_name(…) function to display the student’s first and last name in uppercase. Make the short description of this function Student Full Name. (2)
 - [X] Add ‘register’ view that allows a user to register as a Student. Update myapp/urls.py and create register.html with suitable content. This feature involves creating a ModelForm named RegisterForm that is based on Student model. The form should include the fields: username, password, first name, last name, city, interested_in. Design the form with labels and widgets as appropriate. Instantiate this form in register() view and pass it to register.html for display. (6)
 - [X] Update the user_login view created in Lab 8 so that if an user who is not logged in goes to url ‘/myapp/myaccount/’ they will be directed to the login page and after successful login they will go directly to the ‘/myapp/myaccount/’ page (instead of the main index page). (2)
 - [X] Update base.html so that if a user is logged in, it will display Logout (myapp/logout) and My Account (myapp/myaccount) links. Otherwise it will display Register Here (myapp/register) and Login (myapp/login) links. Each link should go to the corresponding view function defined earlier (in Lab 8 or in step 4 or 5 above). (3)
 - [X] Update base.html so that if a user is logged in, it will display “Hello ” instead of “Hello User”. Here and are the first name and last name of the user that is currently logged in, respectively. (1)
 - [X] Add a ‘Forgot password’ link on login page. It should email a new password to the user. (3)
 
### Optional
 - [X] Save db in JSON format. Load initial data using fixtures.
 - [X] Add validators for price field in Course model so that it is between 100 and 200. If you’re asked to add validators to one more field, which field you’ll choose.
 - [X] Upload image file. Add an optional field image field for a Student to upload his/her photo.
 - [X] Use Bootstrap to style your pages.
 
### Additional Extra feaures
 - [X] dark mode - users can toggle between dark and light themes sitewide.
 - [X] if  a user has no profile image as it is not required during register, they by default a cat image (robohash is used).
 - [X] users can edit their profile if they are logged in.
 - [X] users can change their password if they are logged in.
 - [X] custom pages for 404 (not found) and 500 (server) errors (works if DEBUG=False) *.
 - [X] logged in students can't place order for other students, and not logged in users can't access the place order form, logged in admin can place orders for every sudent.
 - [X] course page, which shows the price, registered students and reviews for the course.
> *for custom error pages to work please set 
> - DEBUG=False
> - add \[\*] in ALLOWED_HOSTS 
> - If using PyCharm do Run -> Edit Configurations... -> Additional Options = `--insecure`
> otherwise `python manage.py runserver --insecure`
>
> We need to do all this to make sure static assets are correctly served when not in debug mode.

## How to Run

- Clone the repo
- Install all the requirements using the command
```
pip install -r requirements.txt
```
- Then migrate using the command (make sure to cd into the cloned repo)
```
python manage.py migrate
```
>While migrating if you encounter
>```
>CommandError: Conflicting migrations detected; multiple leaf nodes in the migration graph: (0009_alter_student_picture, 0010_student_city in myapp).
>To fix them run 'python manage.py makemigrations --merge'
>```
>please run 
>```
>python manage.py makemigrations --merge
>python manage.py migrate
>```
- Load the data using the command
```
python manage.py loaddata db.json
```
> Here [db.json](fixtures/db.json) is the file located in the fixtures folder 
- Run the project
```
python manage.py runserver
```
## Guide for sending email

This is the installation guide for sending email function.

In this project, the default setting is to send email, but it can also disply email in console if .env file is not available.

In order to enable this function, the following steps should be taken:

   * In setting.py uncomment the "EMAIL_BACKEND" part [line 53](https://github.com/eclairsp/mysiteS21/blob/c68c0a9453f08ed1902234a4157645c5d98cd9ea/mysiteS21/settings.py#L53)

   * Comment out the part after it "env = environ.Env() ... env("EMAIL_HOST_PASSWORD")" [line 56](https://github.com/eclairsp/mysiteS21/blob/c68c0a9453f08ed1902234a4157645c5d98cd9ea/mysiteS21/settings.py#L56) to [line 64](https://github.com/eclairsp/mysiteS21/blob/c68c0a9453f08ed1902234a4157645c5d98cd9ea/mysiteS21/settings.py#L64)

You can also add .env file in mysiteS21 (same directory as the [settings.py](mysiteS21/settings.py) file) directory with two parameters, EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
   * you can create your own .env file with these two parameters
   * set EMAIL_HOST_USER=yougmail@gmail.com
   * set EMAIL_HOST_PASSWORD=yourpassword
   * enable less secure access on https://support.google.com/accounts/answer/6010255?hl=en#zippy=%2Cif-less-secure-app-access-is-on-for-your-account

