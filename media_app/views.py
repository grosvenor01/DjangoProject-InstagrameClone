
from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import auth,User
from .models import profile as profil
from .models import post,like,followers
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='signin')
def index(request):
    user=User.objects.get(username=request.user.username)
    user_profile=profil.objects.all()
    followed=followers.objects.all()
    user_list=[]
    followed_list=[]
    suggestions_list=[]
    for i in user_profile:
        user_list.append(i.user.username)
    for i in followed:
        followed_list.append(i.followers)
    for i in user_list:
        if i not in followed_list:
            suggestions_list.append(i)
    context={
        'use':user_profile,
        'pst':post.objects.all(),
        'all_profiles':suggestions_list
    }
    return render(request,'index.html',context)
def signup(request):
    if request.method =='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password')
        password2=request.POST.get('passwordconf')
        if User.objects.filter(username=username).exists():
            messages.info(request,'username already token')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email already token')
            return redirect('signup')
        elif password1 != password2 :
            messages.info(request,'password not matching')
            return redirect('signup')
        else:
            new_user=User.objects.create(username=username,email=email,password=password1)
            new_user.set_password(password1)  
            new_user.save()
            user_search=User.objects.get(username=username)
            new_profile=profil.objects.create(user=user_search, id_user=user_search.id )
            new_profile.save()
            return redirect('signin')
    return render(request,'signup.html')
def signin(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
       
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'somthing is wrong')
            return redirect('signin')
    else:
        return render(request,'signin.html')
@login_required(login_url='signin')
def setting(request):
    print(request.user.username)
    user_profile=profil.objects.get(user=request.user)
    context={
        'use':user_profile
    }
    if request.method == 'POST':
        if request.FILES.get('profile_pic') == None:
            image=user_profile.profile_pic
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            location=request.POST.get('location')
            bio=request.POST.get('bio')
            
            user_profile.bio=bio
            user_profile.location=location
            user_profile.pofile_pic=image
            user_profile.save()
        else:
            image=request.FILES.get('profile_pic')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            location=request.POST.get('location')
            bio=request.POST.get('bio')
            
            user_profile.bio=bio
            user_profile.location=location
            user_profile.pofile_pic=image
            user_profile.save()
        
        
    return render(request,'setting.html',context)
def profile(request,pk):
    usi=User.objects.get(username=pk)
    prf=profil.objects.get(user=usi)
    posts=post.objects.filter(user=pk)
    counter_following=followers.objects.filter(user=request.user.username).count()
    counter_followers=followers.objects.filter(followers=request.user.username).count()
    context={
        'data':prf,
        'pst':posts,
        'post':posts.count(),
        'username_profile':pk,
        'path':'/profile/'+pk,
        'follow':counter_following,
        'follow_by':counter_followers
    }
    return render(request,'profile.html',context)
def follow(request):
    if request.method =="POST":
        user_name=request.POST.get('follow')
        follower=request.POST.get('following')
        search_user=followers.objects.filter(user=user_name,followers=follower).first()
        if user_name == follower:
            redirect('profile'+user_name)
        elif search_user is None:
            new_follower=followers.objects.create(user=user_name,followers=follower)  
            new_follower.save()
            return redirect('/profile/'+user_name)
        else:
            search_user.delete()
            return redirect('/')   
        
    else:
        return redirect('profile')
def logout(request):
    auth.logout(request)
    return redirect('signin')
def upload(request):
    if request.method == "POST":
        user=request.user.username
        print(request.FILES.get('post_pic'))
        image=request.FILES.get('post_pic')
        caption=request.POST.get('caption')
        new_post=post.objects.create(image=image,caption=caption,user=user)
        new_post.save()
        return redirect('/')
    return HTTPResponse('upload view')
def likepost(request):
    username=request.user.username
    id=request.GET.get('post_id')
    
    like_post=post.objects.get(id=id)
    like_filter=like.objects.filter(id_post=id,usernam=username).first()
    
    if like_filter == None:
        new_like=like.objects.create(id_post=id,usernam=username)
        new_like.save()
        like_post.nbr_like=like_post.nbr_like+1
        like_post.save()
        return redirect('/')
    else:
        like_filter.delete()
        like_post.nbr_like=like_post.nbr_like-1
        like_post.save()
        return redirect('/')
def search(request):
    if request.method=='GET':
        username=request.GET.get('search_bar')
        user=User.objects.get(username=username)
        if user is not None:
            return redirect('/profile/'+username)
        else:
            return redirect('/')
    return HTTPResponse('somthing wrong')
def delete(request,id):
    
    search_post=post.objects.get(id=id)
    if search_post is not None and request.user.username == search_post.user:
        search_post.delete()
        return redirect('/')
    else:
        return redirect('profile')
        