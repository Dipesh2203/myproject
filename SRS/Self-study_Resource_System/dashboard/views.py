from django.shortcuts import render,redirect,get_object_or_404
from . forms import *
from . forms import UserRegistrationForm
from django.contrib import messages
from django.views.generic import DetailView
from .models import Notes,Ebooks,Homework
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
import http.client
import json
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

# Create your views here.

class NotesDetailView(DetailView):
    model = Notes

@login_required
def notes(request):
    if request.method == "POST":
        form = NoteForms(request.POST)
        if form.is_valid():
            notes = Notes(user= request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            form = NoteForms()
        messages.success(request,f"Notes Added from {request.user.username} Successfully!")
    else:
        form = NoteForms()
    notes = Notes.objects.filter(user = request.user)
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_note(request,pk=None):
    note = get_object_or_404(Notes, id=pk, user=request.user)
    note.delete()
    messages.success(request, "Note deleted successfully!")
    return redirect("notes")

@login_required
def edit_note(request, pk=None):
    note = get_object_or_404(Notes,id=pk, user= request.user)
    if request.method == 'POST':
        form = NoteForms(request.POST,instance = note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully!")
            return redirect("notes")
    else:
        form = NoteForms(instance=note)
    context = {'form':form,'note':note}
    # return redirect("notes-detail")
    return render(request,'dashboard/notes.html',context)

@login_required
def home(request):
    # Fetch groups for the logged-in user
    groups = GroupStudy.objects.filter(members=request.user)
    # Pass groups to the context
    context = {'groups': groups}
    return render(request, 'dashboard/home.html', context)

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                document=form.cleaned_data['document'],
                is_finished = finished,
            )
            homeworks.save()
            form = HomeworkForm()
            messages.success(request,f'Homework Added from {request.user.username}!!')
    else:
        form = HomeworkForm()
    homework= Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    incomplete_homework_count = homework.filter(is_finished=False).count()
    total_homework_count = homework.count()

    context = {
        'homeworks':homework,
        'homework_done':homework_done,
        'form':form,
        'incomplete_homework_count': incomplete_homework_count,
        'total_homework_count': total_homework_count,
        }
    return render(request,'dashboard/homework.html',context)


@login_required
def update_homework(request,pk= None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else: 
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def edit_homework(request, pk=None):
    homework = get_object_or_404(Homework,id=pk, user= request.user)
    homework.document.delete()
    if request.method == 'POST':
        form = HomeworkForm(request.POST,request.FILES,instance = homework)
        if form.is_valid():
            form.save()
            messages.success(request, "Homework updated successfully!")
            return redirect("homework")
    else:
        form = HomeworkForm(instance=homework)
    context = {'form':form,'homework':homework}
    # return redirect("notes-detail")
    return render(request,'dashboard/homework.html',context)

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit= 50)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,"dashboard/youtube.html",context)

@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished =='on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            form = TodoForm()
            messages.success(request,f"Todo Added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form':form,
        'todos': todo,
        'todos_done':todos_done
    }
    return render(request,"dashboard/todo.html",context)

@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')
    
@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

@login_required
def edit_todo(request, pk=None):
    todo = get_object_or_404(Todo,id=pk, user= request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST,instance = todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated successfully!")
            return redirect("todo")
    else:
        form = TodoForm(instance=todo)
    context = {'form':form,'todo':todo}
    # return redirect("notes-detail")
    return render(request,'dashboard/todo.html',context)

def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,"dashboard/wiki.html",context)
    else:
        form = DashboardForm()
        context = {
            'form':form
        }
    return render(request,"dashboard/wiki.html",context)


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }

        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
    else:
        form = ConversionForm()
        context = {
            'form':form,
            'input':False
        }
    return render(request,"dashboard/conversion.html",context)


# @login_required
# def login_register_view(request):
#     form = AuthenticationForm()
#     register_form = UserRegistrationForm()


@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos)==0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done': todos_done
    }
    return render(request,"dashboard/profile.html",context)





def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        
        # Oxford Dictionaries API credentials
        app_id = '8fa5925f'  # Replace with your actual App ID
        app_key = '0325f1a82d499109effcde867f3764bf'  # Replace with your actual App Key
        
        # Set up the connection to Oxford Dictionaries API
        conn = http.client.HTTPSConnection("od-api-sandbox.oxforddictionaries.com")
        
        # Set up the headers
        headers = {
            'app_id': app_id,
            'app_key': app_key,
            'Accept': 'application/json'
        }
        
        # Construct the API URL
        url = f"/api/v2/entries/en-us/{text}"
        
        # Make the request to the API
        conn.request("GET", url, headers=headers)
        
        # Get the response
        res = conn.getresponse()
        data = res.read()

        # Initialize context dictionary
        context = {
            'form': form,
            'input': text
        }

        # Check if the request was successful (status code 200)
        if res.status == 200:
            # Parse the response data as JSON
            answer = json.loads(data.decode("utf-8"))
            try:
                # Extract the definition from the API response
                definition = answer['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
                
                # Add the definition to the context
                context['definition'] = definition
            except (KeyError, IndexError):
                context['error'] = 'No definition available for this word.'
        else:
            # If the request failed, set an error in context
            context['error'] = f"Error: {res.status} - {data.decode('utf-8')}"
        
        # Close the connection
        conn.close()

        # Return the response with context
        return render(request, "dashboard/dictionary.html", context)
    
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, "dashboard/dictionary.html", context)

@login_required
def group_study_list(request):
    groups = GroupStudy.objects.filter(members=request.user)
    context = {'groups': groups}
    return render(request,'dashboard/home.html', context)

@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            group.members.add(request.user)
            messages.success(request,"Group created successfully!")
            form= GroupForm()
            return redirect("create_group")
            # return render(request, 'dashboard/create_group.html', context)
    else:
        form= GroupForm()
    context = {
        'form': form,
        'groups': GroupStudy.objects.filter(members=request.user),  # Include the list of groups
    }
    return render(request, 'dashboard/create_group.html', context)



@login_required
def group_detail(request,pk):
    group = get_object_or_404(GroupStudy,pk=pk)
    if request.method == "POST":
        form = AddMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                group.members.add(user)
                messages.success(request,f"{username} has been added")
            except User.DoesNotExist:
                messages.success(request,"user not found.")

    else:
        form = AddMemberForm()
    return render(request, 'dashboard/group_detail.html',{'group': group,'form':form})


# ebooks

@login_required
def ebooks(request):
    if request.method == "POST":
        form = EbooksForm(request.POST, request.FILES)
        if form.is_valid():
            ebook = Ebooks(
                user = request.user,
                subject = request.POST['subject'],
                # title = request.POST['title'],
                description = request.POST['description'],
                # due = request.POST['due'],
                document=form.cleaned_data['document'],
                # is_finished = finished,
            )
            ebook.save()
            form = EbooksForm()
            messages.success(request,f'Ebook Added from {request.user.username}!!')
    else:
        form = EbooksForm()
    ebook= Ebooks.objects.filter(user=request.user)
    # if len(homework) == 0:
    #     homework_done = True
    # else:
    #     homework_done = False

    context = {
        'ebook':ebook,
        # 'homework_done':homework_done,
        'form':form,
        }
    return render(request,'dashboard/ebooks.html',context)


# ebook view

@login_required
def ebook_view(request):
    if request.method == 'POST':
        # Handle file upload and saving
        # title = request.POST.get('title')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        document = request.FILES.get('document')

        # Create a new Ebook entry
        Ebooks.objects.create(
            user=request.user,
            # title=title,
            subject=subject,
            description=description,
            document=document
        )

    # Fetch all ebooks for the logged-in user
    ebooks = Ebooks.objects.filter(user=request.user)
    total_ebook_count = ebooks.count()

    return render(request, 'ebooks.html', {
        'ebooks': ebooks,
        'total_ebook_count': total_ebook_count,
    })

# delete ebooks

@login_required
def delete_ebook(request,pk=None):
    Ebooks.objects.get(id=pk).delete()
    return redirect("ebook")

@login_required
def edit_ebook(request, pk=None):
    ebooks = get_object_or_404(Ebooks,id=pk, user= request.user)
    ebooks.document.delete()
    if request.method == 'POST':
        form = EbooksForm(request.POST,request.FILES,instance = ebooks)
        if form.is_valid():
            form.save()
            messages.success(request, "Ebook updated successfully!")
            return redirect("ebook")
    else:
        form = EbooksForm(instance=ebooks)
    context = {'form':form,'ebooks':ebooks}
    return render(request,'dashboard/ebooks.html',context)


@login_required
def group_homework(request, pk):
    group = get_object_or_404(GroupStudy, pk=pk)
    homeworks = GroupHomework.objects.filter(group=group)
    if request.user not in group.members.all():
        messages.success(request, "You are not a member of this group.")
        return redirect('home')
    if request.method == "POST":
        group = get_object_or_404(GroupStudy, pk=pk)
        if group.created_by != request.user:
            messages.success(request, "Only the group admin can assign homework.")
            return redirect('group_homework', pk=group.pk)
        form = GroupHomeworkForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            homework = form.save(commit=False)
            homework.user = request.user
            homework.group = group
            homework.save()
            messages.success(request, "Homework assigned successfully!")
            return redirect('group_homework', pk=group.pk)
    else:
        form = GroupHomeworkForm(user=request.user)
        context = {
        'group': group,
        'homeworks': homeworks,
        'form': form,
        }
        # messages.success(request, "1st section loaded.")
        return render(request, 'dashboard/grouphomework.html', context)

    context = {
        'group': group,
        'homeworks': homeworks,
        'form': form,
    }
    # messages.success(request, "2nd section loaded.")
    return render(request, 'dashboard/grouphomework.html', context)




@login_required
def delete_group_homework(request, group_pk=None, homework_pk=None):
    group = get_object_or_404(GroupStudy, pk=group_pk)
    if group.created_by == request.user:
        homework = get_object_or_404(GroupHomework, id=homework_pk)
        homework.delete()
        return redirect("group_homework", pk=group.pk)
    messages.success(request, "Only admin can delete homework")
    return redirect('group_homework', pk=group.pk)

@login_required
def edit_group_homework(request, group_pk=None,homework_pk = None):
    group = get_object_or_404(GroupStudy, pk=group_pk)
    if group.created_by == request.user:
        homework = get_object_or_404(GroupHomework,id=homework_pk)
        # homework.document.delete()
        if request.method == 'POST':
            form = GroupHomeworkForm(request.POST,request.FILES,instance = homework)
            if form.is_valid():
                homework = form.save(commit=False)
                homework.user = request.user
                homework.group = group
                form.save()
                messages.success(request, "Homework updated successfully!")
                return redirect('group_homework', pk=group.pk )
                # return JsonResponse({'status': 'success', 'homework': homework.title})
        else:
            form = GroupHomeworkForm(instance=homework)
        context = {'form':form,'homework':homework}
        return render(request,'dashboard/grouphomework.html',context)
    else:
        messages.success(request, "You don't have permission to edit this homework.")
        return redirect("group_homework", pk=group.pk)
        # return JsonResponse({'status': 'unauthorized'})

def register(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = UserRegistrationForm(request.POST)
            form = AuthenticationForm()
            if register_form.is_valid():
                register_form.save()
                username = register_form.cleaned_data.get('username')
                messages.success(request, f"Account created for {username}!")
                return redirect("register")
        elif 'login1' in request.POST:
            form = AuthenticationForm(request, data=request.POST)
            register_form = UserRegistrationForm()
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
    else:
        register_form = UserRegistrationForm()
        form = AuthenticationForm()

    context = {
        'register_form': register_form,
        'form': form,
    }
    return render(request, "dashboard/login.html", context)

