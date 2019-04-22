from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from .models import Teacher, Course, Post
from .forms import PostForm, SearchForm


def home(request):
	
	context = { 'posts': Post.objects.all() }
	

	return render(request, 'blog/home.html', context)


class PostListView(ListView, FormMixin):
	model = Post
	form_class = SearchForm
	template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html

	context_object_name = 'posts'
	ordering = ['-date_posted']
	# paginate_by = 5

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			t = form.cleaned_data['teacher']
			c = form.cleaned_data['course']

		return render(request, 'blog/home.html', { 't': t, 'c': c , 'posts': Post.objects.all()  , 'form': form } )

	def get_context_data(self):
		context = super(PostListView, self).get_context_data()
		return context


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

class TeacherDetailView(DetailView):
	model = Teacher


class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	# fields = ['title', 'teacher', 'course', 'grade_received', 'course_review', 'teacher_review', 'study_material', 
	# 'quality_rating', 'quantity_rating', 'level_of_difficulty_rating', 'take_again', 'tough_grader', 'self_study_required',
	# 'participation_matters', 'lot_of_assignment', 'accessible_outside_class', 'skip_class_you_dont_pass',
	# 'impartial', 'test_heavy', 'amazing_lectures', 'lecture_heavy' ]

	form_class = PostForm
    

	def form_valid(self, form):
		form.instance.author = self.request.user

		user_posts = Post.objects.filter(author = self.request.user)

		user_post_teacher = user_posts.values('teacher')
		teacher_list = [p['teacher'] for p in user_post_teacher]

		user_post_course = user_posts.values('course')
		course_list = [p['course'] for p in user_post_course]

		form_valid_cond = True

		for t in teacher_list:
			tt = Teacher.objects.filter(id = t).first().teacher_name
			for c in course_list:
				cc = Course.objects.filter(id = c).first().course_name
				if str(form.instance.teacher) == str(tt) and str(form.instance.course) == str(cc):
					form_valid_cond = False
					return self.form_invalid(form)
		
		t = Teacher.objects.filter(teacher_name = str(form.instance.teacher)).first()

		# update teacher table
		
		t.quality = ((t.total_reviews*t.quality) + form.instance.quality_rating )/(t.total_reviews + 1)
		t.quantity = ((t.total_reviews*t.quantity) + form.instance.quantity_rating )/(t.total_reviews + 1)
		t.level_of_difficulty = ((t.total_reviews*t.level_of_difficulty) + form.instance.level_of_difficulty_rating )/(t.total_reviews + 1)
		if form.instance.take_again == True:
			t.take_again = t.take_again + 1
		if form.instance.tough_grader== True:
			t.tough_grader = t.tough_grader + 1
		if form.instance.self_study_required == True:
			t.self_study_required = t.self_study_required + 1
		if form.instance.participation_matters == True:
			t.participation_matters = t.participation_matters + 1
		if form.instance.lot_of_assignment == True:
			t.lot_of_assignment = t.lot_of_assignment + 1
		if form.instance.accessible_outside_class == True:
			t.accessible_outside_class = t.accessible_outside_class + 1
		if form.instance.skip_class_you_dont_pass == True:
			t.skip_class_you_dont_pass = t.skip_class_you_dont_pass + 1
		if form.instance.impartial == True:
			t.impartial = t.impartial + 1
		if form.instance.test_heavy == True:
			t.test_heavy = t.test_heavy + 1
		if form.instance.amazing_lectures == True:
			t.amazing_lectures = t.amazing_lectures + 1
		if form.instance.lecture_heavy == True:
			t.lecture_heavy = t.lecture_heavy + 1

		t.total_reviews = t.total_reviews + 1

		t.save()
		

		return super().form_valid(form)
	

	def form_invalid(self,form):
		messages.error(self.request, f'Post cannot be created! You have already reviewed this Teacher and Course combination')
		return self.render_to_response(self.get_context_data(form=form))



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'course_review', 'teacher_review', 'study_material' ]

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



def about(request):
	return render(request, 'blog/about.html',{'title':'About'})
