from django.shortcuts import render, redirect
from Backend.models import Blogs
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your views here.

# assigning User as our User model i.e. as User_details
User = get_user_model()

def Home(request):
    return render(request,'blogs/home.html')

@login_required
def CreateBlog(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Author = request.user
        new_blog = Blogs.objects.create(Author = Author, title = title, content = content)
        new_blog.save()
        return redirect(reverse('blogs:blog-display',kwargs={'search':str(title)}))
    return render(request,'blogs/create_blog.html')

def BlogDisplay(request,search):
    search = search.split('-')
    search1 = ''
    for i in search:    search1 = search1+' '+i
    print("SEARCH1:",search1)
    result = Blogs.objects.filter(title = search1[1:]).first()
    context = {
        "title":result.title,
        "content":result.content.split('\n'),
    }
    return render(request,'blogs/blog_display.html',context)