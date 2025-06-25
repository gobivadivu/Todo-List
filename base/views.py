from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks' #customise our name insted of object_list
#looks for "model_list.html"
#add mixin at first
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task' #customise name instead of object
    template_name = 'base/task.html'#looks for "model_detail.html" by default 
    #instead now looks for base/task.html

class TaskCreate(LoginRequiredMixin,CreateView):
    #look for template with prefix task
    model = Task
    #already gives a model form view
    fields = '__all__' #list all items in field 
    #or we can create own model form by form_class = TaskForm
    success_url = reverse_lazy('tasks') #redirect on success

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task' 
    success_url = reverse_lazy('tasks')
    #look for template with prefix as model anem and suffix _confirm_delete