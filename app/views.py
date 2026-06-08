

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import tasks
from django.contrib.auth.decorators import login_required

def home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    if request.method == 'POST':
        tasks.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            deadline=request.POST.get('deadline'),
            priority=request.POST.get('priority')
        )

        return redirect('home')

    all_tasks = tasks.objects.filter(user=request.user)
    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    high_priority_tasks = all_tasks.filter(priority=3).count()

    task_to_edit = None
    edit_id = request.GET.get('edit')

    if edit_id:
        task_to_edit = tasks.objects.get(id=edit_id)


    return render(request, 'home.html', {
        'tasks': all_tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'high_priority_tasks': high_priority_tasks,
        'task_to_edit': task_to_edit
    })



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "auth.html", {
                "show_signup": True
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect('home')

    return render(request, "auth.html", {
        "show_signup": True
    })



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password")

    return render(request, 'auth.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def complete_task(request, task_id):
    task = tasks.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('home')

def update_task(request, task_id):
    task = tasks.objects.get(id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.deadline = request.POST.get('deadline')
        task.priority = request.POST.get('priority')
        task.save()
        return redirect('home')
    
def delete_task(request, task_id):
    task = tasks.objects.get(id=task_id)
    task.delete()
    return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('home')