from django import forms
from .models import Teacher, Course, Post


t1 = Teacher.objects.all()
t2 = [ k.teacher_name for k in t1 ]
TEACHER = [ ('Select', 'Select') ] + [ (k,k) for k in t2 ]

c1 = Course.objects.all()
c2 = [ k.course_name for k in c1 ]
COURSE = [ ('Select', 'Select') ] + [(k,k) for k in c2 ]

GRADES = (('', 'Choose...'), ('A', 'A'), ('AB', 'AB'), ('B', 'B'), ('BC', 'BC'), ('C', 'C'), ('D', 'D'), ('F', 'F'))
RATING = [('-1','Rating is given out of 5' ), (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter a title that describes your post'}))
    # teacher = forms.ChoiceField(choices=TEACHER.values('teacher_name'))
    # course = forms.ChoiceField(choices=COURSE.values('course_name'))

    grade_received = forms.ChoiceField(choices=GRADES)
    course_review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type your descriptive review of the selected course here...'}))
    teacher_review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type your descriptive review of the teacher here...'}))
    study_material = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Suggest some study material for the course...'}))
    quality_rating = forms.ChoiceField(choices=RATING)
    quantity_rating = forms.ChoiceField(choices=RATING)
    level_of_difficulty_rating = forms.ChoiceField(choices=RATING)
    take_again = forms.BooleanField(required=False)
    tough_grader = forms.BooleanField(required=False)
    self_study_required = forms.BooleanField(required=False)
    participation_matters = forms.BooleanField(required=False)
    lot_of_assignment = forms.BooleanField(required=False)
    accessible_outside_class = forms.BooleanField(required=False)
    skip_class_you_dont_pass = forms.BooleanField(required=False)
    impartial = forms.BooleanField(required=False)
    test_heavy = forms.BooleanField(required=False)
    amazing_lectures = forms.BooleanField(required=False)
    lecture_heavy = forms.BooleanField(required=False)

    # NumberInput(attrs={'min': '0', 'class': 'yourClass', 'id': 'blah'})
    class Meta:
        model = Post
        fields = ['title', 'teacher', 'course', 'grade_received', 'course_review', 'teacher_review', 'study_material',
        'quality_rating', 'quantity_rating', 'level_of_difficulty_rating', 'take_again', 'tough_grader', 'self_study_required', 
        'participation_matters', 'lot_of_assignment', 'accessible_outside_class', 'skip_class_you_dont_pass', 
        'impartial', 'test_heavy', 'amazing_lectures', 'lecture_heavy' ]


class SearchForm(forms.Form):
    teacher = forms.ChoiceField(choices=TEACHER)
    course = forms.ChoiceField(choices=COURSE)