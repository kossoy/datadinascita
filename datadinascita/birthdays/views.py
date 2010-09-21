import logging
from datetime import *

from datadinascita.birthdays.models import Person
from datadinascita.birthdays.forms import AddForm

from google.appengine.api import users
from google.appengine.ext import blobstore

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def test(request):
    return render_to_response('test.html', {})

def search(request):
    return render_to_response('search.html', {})

def auth_user(back):
    user = users.get_current_user()
    if user:
        auth_url = users.create_logout_url(back)
    else:
        auth_url = users.create_login_url(back)

    return auth_url

def list(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url('/people'))

    people = modify_people(Person.all().filter("owner =", users.get_current_user()))

    return render_to_response('list.html', {'people': people, 'count': len(people), 'auth_url': auth_user('/people')})

def csv_upload(request):
    try:
        upload_url = blobstore.create_upload_url('/upload_csv/')
    except:
        upload_url = '.'
    return render_to_response('import.html', {'upload_url': upload_url})

def add(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url('/add'))

    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            try:
                name = form.clean_data['name']
                birthday = form.clean_birthday()
                p = Person(name=name)
                p.owner = users.get_current_user()
                p.birthday = datetime.date(datetime.strptime(birthday, "%m/%d/%Y"))
            except:
                return show_new_person(form)

            a = p.put()
            logging.info(a)
        else:
            return show_new_person(form)

        return HttpResponseRedirect('/people')
    else:
        form = AddForm()

    return show_new_person(form)

def show_new_person(form):
    people = modify_people(Person.all().filter("owner =", users.get_current_user()))
    return render_to_response('add.html',
                              {'form': form, 'people': people, 'count': len(people),
                               'auth_url': auth_user('/add')})

def modify_people(people):
    pp = []
    for person in people:
        logging.info(person.birthday)
        today = datetime.date(datetime.today())
        this_year_birthday = datetime.date(datetime(today.year, person.birthday.month, person.birthday.day))

        if this_year_birthday > today:
            bd_year = today.year
        else:
            bd_year = today.year + 1

        next_bd_date = datetime(bd_year, person.birthday.month, person.birthday.day)
        next_bd = datetime.date(next_bd_date) - today

        person.age = int(round((datetime.date(next_bd_date) - person.birthday).days / 365.25))
        person.next_bd = next_bd.days
        pp.append(person)

    return sorted(pp, key=lambda ps: ps.next_bd)
