from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,Message
from .forms import RoomForm,UserForm
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


# Create your views here.

def loginpage(request):
 page='Login'
 if request.user.is_authenticated :
     return redirect('home')
 if request.method=="POST":
     username=request.POST.get("username")
     password=request.POST.get("password")
     try:
       user=User.objects.get(username=username)
     except:
        messages.error(request, "No User can found.")
     user= authenticate(request,username=username, password=password)
     if user is not None:
         login(request,user)
         return redirect ("home")
     else :
         messages.error(request, "No User can found.") 
 context={"page":page}
 return render(request,"base/login_register.html",context)



def logoutuser(request):
    logout(request)
    return redirect('home')
 

def registerpage(request):
 page='Register'
 form=UserCreationForm()
 if request.method =='POST':
      #  print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username  .lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, "No User can found.") 

        
 
 context={"page":page,"form":form}
 return render(request,"base/login_register.html",context)


def home(reqeust):
    q=reqeust.GET.get('q') if reqeust.GET.get('q') != None else "" 
    rooms=Room.objects.filter(Q(topic__name__contains=q)|
                              Q(name__icontains=q))
    room_count=rooms.count()
    
    topic=Topic.objects.all()
    user_message= Message.objects.filter(Q(room__topic__name__contains=q)).order_by("-created")

    return render(reqeust,"base/home.html",{"rooms":rooms,"topic":topic,"room_count":room_count,'user_message':user_message})


def room(reqeust,pk):
    rooms=Room.objects.get(id=pk)
    room_messages=rooms.message_set.all().order_by('-created')
    participants=rooms.participants.all()
    if reqeust.method =='POST':
        message =Message.objects.create(
            user=reqeust.user,
            room=rooms,
            body=reqeust.POST.get('body')
        )
        rooms.participants.add(reqeust.user)
        return redirect('room',pk=rooms.id)


    # room =None
    # for i in rooms:
    #     if i["id"]==int(pk):
    #         room=i
    context={'room':rooms,'room_messages':room_messages,'participants':participants}  
    return render(reqeust,"base/room.html",context)


@login_required(login_url="login")
def createroom(request):
    form =RoomForm()
    topics = Topic.objects.all()

    # if request.user != User.host :
    #     HttpResponse("you are not allowed here")
    if request.method =='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

      #  print(request.POST)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request,"base/room_form.html",context)

    #     form = RoomForm(request.POST)
    #     if form.is_valid():
    #        room= form.save(commit=False)
    #        room.host=request.user 
    #        room.save()
    #        return redirect("home")
    # context={"form":form}
    # return render(request,"base/room_form.html",context)


@login_required(login_url="login")
def update_room(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
            HttpResponse("you are not allowed here")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')


    # if request.method =='POST':
    #     form = RoomForm(request.POST,instance=room)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("home")
                
    context={"form":form,"topics":topics,"room":room}
    return render(request,"base/room_form.html",context)


@login_required(login_url="login")
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        HttpResponse("you are not allowed here")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,"base/delete.html",{"obj":room})


@login_required(login_url="login")
def delete_message(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        HttpResponse("you are not allowed here")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,"base/delete.html",{"obj":message})

@login_required(login_url="login")

def userprofile(request,pk):
 user=User.objects.get(id=pk)
 rooms=user.room_set.all()
 user_message=user.message_set.all()
 topic=Topic.objects.all()
 context={'user':user,"rooms":rooms,"user_message":user_message,"topic":topic}
 return render(request,'base/profile.html',context)

@login_required(login_url="login")
def updateUser(request):
  user= request.user
  form= UserForm(instance=user)
  context={"form":form}
  if request.method=='POST':
      form= UserForm(request.POST,instance=user)
      if form.is_valid():
          form.save()
          return redirect("user_profile" , pk=user.id)
          
  return render (request,'base/update_user.html',context)