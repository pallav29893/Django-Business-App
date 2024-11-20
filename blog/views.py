from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404 , HttpResponse
from django.utils import timezone
from blog.models import Post, Comment,Category,Tag
from .forms import PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserSignUpForm
from .forms import userloginForm
from .forms import ProfileForm
from django.contrib.auth.hashers import make_password
from django.urls import reverse



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    category = Category.objects.all()
    tags = Tag.objects.all()
    context = {'posts': posts,'category':category,'tags':tags}
    return render(request, 'blog/post_list.html', context)    

def post_detail(request, slug):
  
    if request.method == "POST":
        reply = request.POST.get('reply',None)
        print(reply, "reply>>>>>>>>>>>>>>>>>")
        parent = request.POST.get('comment',None)
        print(parent, "parent >>>>>>>>>>>>>>>>")
        post = get_object_or_404(Post, slug=slug)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        text = request.POST.get('text', None)
        print(text, 'gdfvsdfsdfasdfd')
        try:
            comment = Comment.objects.filter(id=int(parent)).first()
            print(comment, "comment>>>>>>>>>>>>")
            Comment.objects.create(text=reply, post=post,parent=comment,name=name)
        except Exception as e:
            Comment.objects.create(name=name,email=email,text=text, post=post)

        # if comment is not None:
        #     comment = Comment.objects.filter(id=parent).first()

        #     Comment.objects.create(text=reply, post=post,parent=comment.id,name=name)
        # else:
        #     Comment.objects.create(name=name,email=email,text=text, post=post)
        return redirect(reverse('post_detail', kwargs={'slug': post.slug}))        
    else:
        post = get_object_or_404(Post, slug=slug)
        comment = Comment.objects.filter(post=post,  parent__isnull= True)
        category = Category.objects.all()
        tags = Tag.objects.all()
        context =  {'post': post,'comment':comment,'category':category,'tags':tags}
        return render(request, 'blog/post_detail.html',context)

# def post_detail(request,slug):
#     post = Post.objects.filter(slug=slug).first()
#     if request.method == "POST":
#         parent_id = request.POST.get('commentid',None)
#         comment = Comment.objects.filter(id=parent_id).first()
#         name = request.POST.get('name', None)
#         email = request.POST.get('email', None)
#         text = request.POST.get('text', None)
#         if parent_id:
#             parent_comment = Comment.objects.filter(id=int(parent_id)).first()
#             Comment.objects.create(text=text,post=post,parent=parent_comment,name=name)
#             print(text,'<<<<<<nnnnnnnnn<<<')
#         else:
#             Comment.objects.create(name=name,email=email,text=text,post=post)
#             print(text,'<<<<<aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa<<<<')
#         return redirect(reverse('post_detail',kwargs={'slug': post.slug}))        
#     else:
#         comment = Comment.objects.filter(post=post,parent__isnull=True)
#         category = Category.objects.all()
#         tags = Tag.objects.all()
#         context =  {'category':category,'tags':tags,'post':post,'comment':comment}
#         return render(request, 'blog/post_detail.html',context)
    


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES , instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            post.tags.clear()
            tags = request.POST.getlist('tags', '')
            for tags in tags:
                tags = tags.strip()
                if tags:
                    post.tags.add(tags)


            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# def userSignUpViews(request):
#     if request.method == 'POST':
#         form = UserSignUpForm(request.POST,request.FILES)
#         print(form)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = make_password(user.password)  # Hash the password
#             user.save()
#             login(request, user)
#             return redirect('login')
#     else:
#         form = UserSignUpForm()
#     return render(request, 'blog/signup.html', {'form': form})

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # print(username,password, "password>>>>>>>>>>>>>>>>>")
#         user = authenticate(username=username, password=password)
#         # print(user, "user>>>>>>>>>>>>>>>>>>>>>>>>>")
#         if user is not None:   
#             # print("----====------")
#             login(request,user=user)
#             messages.success(request,"You are now logged in as {username}")
#             return redirect("post_list")
#     form = userloginForm()
#     return render(request, "blog/login.html", {"form": form})

# def logout_view(request):
#     logout(request)
#     messages.success(request, "You have been logged out.")
#     return redirect('post_list') 

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'blog/profile.html',{'user':user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'blog/profile_edit.html', {'form': form})


def category_post_list(request,slug):
    category = get_object_or_404(Category,slug=slug)
    posts = Post.objects.filter(category=category)
    context = {'posts':posts,'category':category}
    return render(request,'blog/category_post_list.html',context)

def tag_post_list(request,slug):
    tags = get_object_or_404(Tag,slug=slug)
    posts = Post.objects.filter(tags=tags)
    context = {'posts':posts,'tags':tags}
    return render(request,'blog/tag_post_list.html',context)
