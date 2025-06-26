from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.http import HttpResponseRedirect
from .models import Task

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
    
    #block the authenticated user from accessing the register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks' #customise our name insted of object_list
    #looks for "model_list.html"
    #add mixin at first

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False) #count incomplete items
        #we set it at context_object_name

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith = search_input #icontains is other method to filter
            )

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task' #customise name instead of object
    template_name = 'base/task.html'#looks for "model_detail.html" by default 
    #instead now looks for base/task.html

class TaskCreate(LoginRequiredMixin,CreateView):
    #look for template with prefix task
    model = Task
    #already gives a model form view
    fields = ['title', 'description', 'complete'] #list all items in field 
    #or we can create own model form by form_class = TaskForm
    success_url = reverse_lazy('tasks') #redirect on success

    def form_valid(self, form):
        #user field in create task can be set to any user initaily
        #to avoid that we write this function and modify the fields attribute
        #which was earlier set to '__all__'
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task' 
    success_url = reverse_lazy('tasks')
    #look for template with prefix as model anem and suffix _confirm_delete

