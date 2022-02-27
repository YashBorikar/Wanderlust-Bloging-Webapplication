from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import SignUpForm, CommentForm, CreatePostForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from BlogApp.forms import EmailSendForm
from taggit.models import Tag
from django.contrib.auth.decorators import login_required


def index(request, tag_slug=None):
    post_list=Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request,'BlogApp/index.html',{'post_list':post_list, 'tag':tag})

def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/login/')
    return render(request, 'BlogApp/signup.html', {'form': form})

def logout_view(request):
    return render(request,'BlogApp/logout.html')

def post_detail_view(request,year,month,day,post):
    post = get_object_or_404(Post, slug=post,
                             status = '2',
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)

    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()

    return render(request, 'BlogApp/post_detail.html', {'post': post, 'form': form, 'comments': comments, 'csubmit': csubmit})

@login_required
def createpost(request):
    user=request.user
    form=CreatePostForm()
    if request.method=='POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            create_form = form.save(commit=False)
            create_form.author = user
            create_form.save()
            form.save_m2m()

            form = CreatePostForm()
    return render(request, 'BlogApp/createpost.html', {'form':form})


def mail_send_view(request,id):
    post = get_object_or_404(Post, id=id, status='2')
    sent = False
    if request.method =='POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you to read "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read Post At: \n {}\n\n{}\' Comments:\n{}'.format(post_url, cd['name'], cd['comments'])
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True
    else:
        form = EmailSendForm()
    return render(request, 'BlogApp/sharebymail.html', {'post': post, 'form': form, 'sent': sent})


