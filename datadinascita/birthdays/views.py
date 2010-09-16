# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from datadinascita.birthdays.models import Person
from datadinascita.birthdays.forms import AddForm
from datetime import datetime

def index(request):
    people = Person.all()
    return render_to_response('index.html', {"people": people})

def list(request):
    people = Person.all()
    return render_to_response('list.html', {'people': people})

def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            name = form.clean_data['name']
            birthday = form.clean_data['birthday']
            p = Person(name=name)
            p.birthday = datetime.date(datetime.strptime(birthday, "%d/%m/%Y"))
            p.put()
        return HttpResponseRedirect('/people')

    else:
        form = AddForm()
    return render_to_response('add.html', {'form': form})
