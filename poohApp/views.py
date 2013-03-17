# Create your views here.
#coding: UTF-8
from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from PoohPy.settings import *
from models import Users
from django.template import RequestContext

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Post
import datetime
import urllib,urllib2,cookielib
from bs4 import BeautifulSoup


from django.conf import settings
from django.core.cache import cache


from forms import ContactForm,RegisterForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError,mail_admins,EmailMultiAlternatives
from threading import Thread







def index(request):
    if request.method == 'POST':
        # save new post
        title = request.POST['title']
        content = request.POST['content']

        post = Post(title=title)
        post.last_update = datetime.datetime.now()
        post.content = content
        post.save()

    # Get all posts from DB
    posts = Post.objects
    return render_to_response('index.html', {'Posts': posts},
                              context_instance=RequestContext(request))



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject=cd['subject']
            message=cd['message']
            from_email=cd.get('from_email', 'noreply@example.com')
            sender=EMAIL_HOST_USER
            try:
                send_mail(subject,[from_email,message],sender,
                          ['poohmeng@sina.com'], fail_silently=False)

                thread = Thread(target=send_mail,args=(subject,message,from_email,['poohmeng@sina.com']))
                thread.start()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/poohApp/thanks/')

    else:
        form = ContactForm(
            initial = {'subject':'I love this one!'}
        )
    c = {}
    c = RequestContext(request, {
        'form':form,
        })
    return render_to_response('contact/contact.html',c)

def thanks(request):
    return render_to_response('contact/thanks.html', {
    }, context_instance=RequestContext(request))

def about(request):
    # req = urllib2.Request("http://www.baidu.com/")
    myCookie = urllib2.HTTPCookieProcessor(cookielib.CookieJar());
    opener = urllib2.build_opener(myCookie)
    htmlSource = urllib2.urlopen("http://www.baidu.com/").read(200000)
    soup = BeautifulSoup(htmlSource)
    print soup
    return render_to_response('contact/about.html', {
    }, context_instance=RequestContext(request,{
        'html':soup,
    }))



def update(request):
    id = eval("request." + request.method + "['id']")
    post = Post.objects(id=id)[0]

    if request.method == 'POST':
        # update field values and save to mongo
        post.title = request.POST['title']
        post.last_update = datetime.datetime.now()
        post.content = request.POST['content']
        post.save()
        template = 'index.html'
        params = {'Posts': Post.objects}

    elif request.method == 'GET':
        template = 'update.html'
        params = {'post':post}

    return render_to_response(template, params, context_instance=RequestContext(request))


def delete(request):
    id = eval("request." + request.method + "['id']")

    if request.method == 'POST':
        post = Post.objects(id=id)[0]
        post.delete()
        template = 'index.html'
        params = {'Posts': Post.objects}
    elif request.method == 'GET':
        template = 'delete.html'
        params = { 'id': id }

    return render_to_response(template, params, context_instance=RequestContext(request))

# def register(request):
#     c={}
#     c.update(csrf(request))
#     if 'name' and 'password' and 'email' in request.POST:
#         name=request.POST['name']
#         password=request.POST['password']
#         email=request.POST['email']
#         Users.create_user(name,password,email)
#     return render_to_response('register.html',c)

# def register(request):
#     if request.method == 'GET':
#         d = {}
#         d.update(csrf(request))
#         return render_to_response('register.html', d)
#     if request.method == 'POST':
#         d = request.POST
#         password = d['password']
#         password_repeat = d['password-repeat']
#         if password == password_repeat:
#             db = func.connect_database()
#
#             username = d['username']
#             if db.users.find_one({'Username':username}):
#                 return HttpResponseRedirect("/poohApp/register.html")
#
#             email = d['email']
#             if db.users.find_one({'Email':email}):
#                 return HttpResponseRedirect("/poohApp/register.html")
#
#             db.users.insert({
#                 'Email':email,
#                 'Username': username,
#                 # 'Password':passwordHash,
#                 'Password':password,
#
#                 })
#             db.connection.disconnect()
#             return HttpResponseRedirect("/poohApp/index.html")
#
#
#
#



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            email = form.clean_email()
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            new_user = form.save(username=email, password=password)
            # new_user = authenticate(username=email, password=password)

            # request.session.set_expiry(0)
            return HttpResponseRedirect('/poohApp/index/')
    else:
        form = RegisterForm()
    return render_to_response("register.html", {
        'form': form,
        })


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")






