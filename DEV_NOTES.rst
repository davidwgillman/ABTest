This is the Abortion Day Tracker project, the all-Django test version in which all the classes are defined in tracker/models.py.

The main application is tracker.  The admin application comes with Django and is defined in <path-to-django>/contrib/admin. 


Flow

In models.py the Flow is defined by these classes that are only viewable by the admin application:

Step			step name and number
StepOutcome		outcome name and value, and reference to Step
NextStepCondition	references to Step and next Step, and the conditions
			that determine the next step
FlagCondition		flag name, reference to StepOutcome, and conditions 				that raise the flag


Requirements

The project is built according to the Django 1.6 tutorial, parts 1-3:
https://docs.djangoproject.com/en/1.6/intro/tutorial01/

The project is built with south, which must be installed:  
http://south.aeracode.org/
South adds the commands
python manage.py schemamigration tracker --auto
python manage.py migrate tracker
These update the db after changes to the model.


