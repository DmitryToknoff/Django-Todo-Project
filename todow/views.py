from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
from django.views.generic import ListViews
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'todowo/home.html')


def singupuser(request):
    if request.method == 'GET':
        return render(request, 'todowo/form.html', {'form': UserCreationForm()})
    if request.POST['password1'] == request.POST['password2']:
        try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('currenttodo')
        except IntegrityError:
            return render(request, 'todowo/form.html', {'form': UserCreationForm(),
                                                        'error': 'Your username has already been taken. Please write '
                                                                 'a new username'})
    else:
        return render(request, 'todowo/form.html', {'form': UserCreationForm(), 'error': 'Your password is not mutch'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todowo/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todowo/loginuser.html',
                          {'form': AuthenticationForm, 'error': 'This user didnt match'})
        login(request, user)
        return redirect('currenttodo')

@login_required
def currenttodo(request):
    todo = Todo.objects.filter(user=request.user, date_complated__isnull=True)
    return render(request, 'todowo/current_task.html', {'todo': todo})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todowo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'todowo/createtodo.html', {'form': TodoForm(), 'error': 'Bad date passed in!'})

@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todowo/view_todo.html', {'todo':todo, 'form':form})
    try:
        form = TodoForm(request.POST, instance=todo)
        form.save()
        return redirect('currenttodo')
    except ValueError:
        return render(request, 'todowo/view_todo.html', {'todo': todo,'form': form, 'error': 'Bad date passed in!'})

@login_required
def complatedtodo(request):
    todo = Todo.objects.filter(user=request.user, date_complated__isnull=False).order_by('-date_complated')
    return render(request, 'todowo/complatedtodo.html', {'todo': todo})

@login_required
def view_complated(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.date_complated = timezone.now()
        todo.save()
        return redirect('currenttodo')

@login_required
def view_deleted(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodo')