from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from models import *

def index(request):
    return render(request, 'wish_list/index.html')

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/index')
    current_user = User.objects.get(id=request.session['id'])
    items = Item.objects.exclude(wished_by = current_user)
    wish_list = current_user.wish_list.all()
    context = {
        'current_user': current_user,
        'items': items,
        'wish_list': wish_list,
    }
    return render(request, 'wish_list/dashboard.html', context)

def success(request):
    if request.POST['submit'] == 'Register': # Registration
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)
            return redirect('/index')

        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = password, date_hired = request.POST['date_hired'])
        if 'id' not in request.session:
            request.session['id'] = user.id
        else:
            request.session['id'] = user.id
        return redirect('/dashboard')


    if request.POST['submit'] == 'Login': # Login
        user = User.objects.filter(username = request.POST['username'])
        if not user:
            messages.add_message(request, messages.INFO, 'User does not exist')
            return redirect('/index')
        else:
            for user in user:
                user_password = user.password
            if bcrypt.checkpw(request.POST['password'].encode(), user_password.encode()):
                if 'id' not in request.session:
                    request.session['id'] = user.id
                else:
                    request.session['id'] = user.id
                return redirect('/dashboard')
            else:
                messages.add_message(request, messages.INFO, 'Password is incorrect')
                return redirect('/index')
def add(request):
    return render(request, 'wish_list/add.html')

def add_item(request):
    errors = Item.objects.item_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/add')
    else:
        user = User.objects.get(id=request.session['id'])
        item = Item.objects.create(item = request.POST['item'], added_by = user)
        user.wish_list.add(item)
        user.save()

        return redirect('/dashboard')

def logout(request):
    del request.session['id']
    return redirect('/index')

def show(request, item_id):
    item = Item.objects.get(id = item_id)
    items_wished_by_all = item.wished_by.all()
    context = {
        'item': item,
        'items_wished_by_all': items_wished_by_all
    }
    return render(request, 'wish_list/show.html', context)

def delete(request, item_id):
    item = Item.objects.get(id = item_id)
    item.delete()
    return redirect('/dashboard')

def remove(request, item_id):
    current_user = User.objects.get(id = request.session['id'])
    item = Item.objects.get(id = item_id)
    current_user.wish_list.remove(item)
    return redirect('/dashboard')

def add_wish(request, item_id):
    current_user = User.objects.get(id=request.session['id'])
    item = Item.objects.get(id = item_id)
    current_user.wish_list.add(item)
    current_user.save()
    return redirect('/dashboard')
