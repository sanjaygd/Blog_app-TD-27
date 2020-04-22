from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect


from .models import Post
from .forms import PostForm

def post_list(request):
    queryset = Post.objects.all() #.order_by('-timestamp')
    paginator = Paginator(queryset, 5) # Show 5 contents per page.
   

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list' : page_obj,
        'page_obj': page_obj
    }
    return render(request,'blog_app/post_list.html',context)


def post_details(request,pk=None):
    instance = get_object_or_404(Post,pk=pk)
    context = {
        'obj_details':instance
    }
    return render(request,'blog_app/post_details.html',context)


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'Succesfuly created')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request,'Not succesfully created')    
    context = {
        'form':form
    }
    return render(request, 'blog_app/post_create.html',context)



def post_update(request,id=None):
    instance = get_object_or_404(Post,id=id) #This instance should pass through form to update
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'<a href="">Item</a> Succesfuly changed',extra_tags='html_safe') #extra tag is used to create different classes in html
        return HttpResponseRedirect(instance.get_absolute_url()) #redirecting the url is must and should once after saved the form
    # else:
    #     messages.error(request,'Not succesfully changed')

    context = {
        'form':form
    }
    return render(request, 'blog_app/post_create.html',context)


def post_delete(request,id=None):
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request, "Succesfully deleted")
    return redirect('blog_app:post_list')



