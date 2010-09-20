# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from datadinascita.birthdays.models import Person
from datadinascita.birthdays.forms import AddForm
from google.appengine.api import users
from datetime import *
from google.appengine.ext.blobstore import blobstore
import logging
import forms
import cgi

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
    if (request.method == 'POST'):
        try:
            parse_upload(request)
        except:
            return HttpResponseRedirect('/import')
    else:
        try:
            upload_url = blobstore.create_upload_url('/import/')
        except:
            upload_url = '.'
        return render_to_response('import.html', {'upload_url': upload_url})

def parse_upload(request):
    try:
        uploads = get_uploads(request, 'file')
        logging.info(uploads)
        for upload in uploads:
            file = BlobFile(blob=upload)
            file.save()
    except Exception, e:
        return HttpResponseRedirect("/import")
    return HttpResponse("Ok!")

def get_uploads(request, field_name=None, populate_post=False):
    """
    http://appengine-cookbook.appspot.com/recipe/blobstore-get_uploads-helper-function-for-django-request/

    Get uploads sent to this handler.

    Args:
    field_name: Only select uploads that were sent as a specific field.
    populate_post: Add the non blob fields to request.POST

    Returns:
    A list of BlobInfo records corresponding to each upload.
    Empty list if there are no blob-info records for field_name.
    """

    logging.info(request)
    if hasattr(request,'__uploads') == False:
        request.META['wsgi.input'].seek(0)
        fields = cgi.FieldStorage(request.META['wsgi.input'], environ=request.META)

        request.__uploads = {}
        if populate_post:
            request.POST = {}
        for key in fields.keys():
            field = fields[key]
            if isinstance(field, cgi.FieldStorage) and 'blob-key' in field.type_options:
                request.__uploads.setdefault(key, []).append(blobstore.parse_blob_info(field))
            elif populate_post:
                request.POST[key] = field.value

    if field_name:
        try:
            return list(request.__uploads[field_name])
        except KeyError:
            return []
    else:
        results = []
        for uploads in request.__uploads.itervalues():
            results += uploads
        return results

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
        this_year_birhtday = datetime.date(datetime(today.year, person.birthday.month, person.birthday.day))

        if this_year_birhtday > today:
            bd_year = today.year
        else:
            bd_year = today.year + 1

        next_bd_date = datetime(bd_year, person.birthday.month, person.birthday.day)
        next_bd = datetime.date(next_bd_date) - today

        person.age = int(round((datetime.date(next_bd_date) - person.birthday).days / 365.25))
        person.next_bd = next_bd.days
        pp.append(person)

    return sorted(pp, key=lambda ps: ps.next_bd)