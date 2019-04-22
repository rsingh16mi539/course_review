from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal



class Course(models.Model):
	course_name = models.CharField(max_length=100, default="")

	def __str__(self):
		return self.course_name


class Teacher(models.Model):
	teacher_name = models.CharField(max_length=100, default="")
	quality = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
	quantity = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
	level_of_difficulty = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
	take_again = models.IntegerField(default=0)
	tough_grader = models.IntegerField(default=0)
	self_study_required = models.IntegerField(default=0)
	participation_matters = models.IntegerField(default=0)
	lot_of_assignment = models.IntegerField(default=0)
	accessible_outside_class = models.IntegerField(default=0)
	skip_class_you_dont_pass = models.IntegerField(default=0)
	impartial = models.IntegerField(default=0)
	test_heavy = models.IntegerField(default=0)
	amazing_lectures = models.IntegerField(default=0)
	lecture_heavy = models.IntegerField(default=0)
	total_reviews = models.IntegerField(default=0)

	def __str__(self):
		return self.teacher_name



class Post(models.Model):
	title = models.CharField(max_length=100)
	grade_received = models.CharField(max_length=15, default="Select Grade")
	#found_useful = models.IntegerField(default=0)
	#didnot_found_useful = models.IntegerField(default=0)
	course_review = models.TextField(default="---")
	teacher_review = models.TextField(default="---")
	study_material = models.TextField(default="---")
	quality_rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
	quantity_rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
	level_of_difficulty_rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
	take_again = models.BooleanField(default=False)
	tough_grader = models.BooleanField(default=False)
	self_study_required = models.BooleanField(default=False)
	participation_matters = models.BooleanField(default=False)
	lot_of_assignment = models.BooleanField(default=False)
	accessible_outside_class = models.BooleanField(default=False)
	skip_class_you_dont_pass = models.BooleanField(default=False)
	impartial = models.BooleanField(default=False)
	test_heavy = models.BooleanField(default=False)
	amazing_lectures = models.BooleanField(default=False)
	lecture_heavy = models.BooleanField(default=False)

	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})	

