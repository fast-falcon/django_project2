import json
from datetime import datetime

import pytz
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.utils.safestring import mark_safe

from Webeloperss.settings import MEDIA_URL, BASE_DIR
from webapp.models import Meeting


def main(request):
    return render(request, 'index.html')


def signup(request):
    passNotEqual = False
    usernameExists = False
    emailExists = False
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        password2 = request.POST.get('pass2')
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')

        if not password == password2: passNotEqual = True
        if User.objects.filter(username=username).exists(): usernameExists = True
        if User.objects.filter(email=email).exists(): emailExists = True
        if not passNotEqual and not emailExists and not usernameExists:
            staff = request.POST.get("type") == "ostad"
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            is_staff=staff
                                            )
            user.save()
            return HttpResponseRedirect("/")

    return render(request, 'signup.html', {
        "passNotEqual": passNotEqual,
        "usernameExists": usernameExists,
        "emailExists": emailExists
    })


def login_(request):
    error = False
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                error = True
        error = True
    return render(request, 'login.html', {
        "error": error
    })


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")


def contactus(request):
    if request.POST:
        send_mail(request.POST.get("title"),
                  request.POST.get("email") + "\n" + request.POST.get("text"),
                  "eden101010hazard@gmail.com",
                  ["pouriaff7171@gmail.com"]
                  )
        return HttpResponse("درخواست شما ثبت شد")
    return render(request, 'contactus.html')

# @login_required(login_url="/login")
def profile(request):
    mine = True
    userShown = request.user
    if request.GET:
        userShown = User.objects.get(username=request.GET.get('username'))
        if not request.user.username == request.GET.get('user'):
            mine = False
    return render(request, "profile.html", {'userShown': userShown, 'mine': mine, })

@login_required(login_url="/login")
def editprofile(request):
    if request.POST:
        user = User.objects.get(username=request.user.username)
        user.first_name = request.POST.get('first')
        user.last_name = request.POST.get('last')
        tmp_bio = request.POST.get('bio')
        bio = mark_safe(tmp_bio)
        user.profile.bio = bio
        user.profile.gender = request.POST.get('gender')
        if request.FILES and request.FILES['pic']:
            file = request.FILES['pic']
            fs = FileSystemStorage(location=MEDIA_URL)
            filename = fs.save(file.name, file)
            user.profile.picture = filename
        else:
            user.profile.picture = None
        user.save()
        return HttpResponseRedirect('/profile')
    return render(request, "edit_profile.html")


def search(request):
    asatid = {}
    if request.GET and request.GET.get('search_param'):
        param = request.GET.get('search_param')
        src = User.objects.filter(is_staff=True)
        asatid = src.filter(username__icontains=param)
        asatid1 = src.filter(first_name__icontains=param)
        asatid2 = src.filter(last_name__icontains=param)
        asatid = asatid.union(asatid1, asatid2)
    return render(request, "search.html", {'asatid': asatid})


def removeuser(request):
    user = User.objects.filter(username=request.user.username)
    logout(request)
    user.delete()
    User.objects.filter(pk=request.user.pk).update(is_active=False, email=None)
    return HttpResponseRedirect('/')


def createmeeting(request):
    # if not request.user.is_staff:
    #     return HttpResponseRedirect("/")
    falseDate = False
    falseStart = False
    falseEnd = False
    endBeforeStart = False
    intersection = False
    if request.POST:
        date = request.POST.get('date')
        start = request.POST.get('start')
        end = request.POST.get('end')
        capacity = request.POST.get('capacity')
        parsed_date = None
        parsed_start = None
        parsed_end = None
        try:
            parsed_date = validate_date(date)
        except:
            falseDate = True
        try:
            parsed_start = validate_time(start)
        except:
            falseStart = True
        try:
            parsed_end = validate_time(end)
        except:
            falseEnd = True
        if not falseEnd and not falseStart and not falseDate:
            if parsed_start > parsed_end:
                endBeforeStart = True
            if not endBeforeStart:
                parsed_end = pytz.utc.localize(parsed_end)
                parsed_start = pytz.utc.localize(parsed_start)
                parsed_date = pytz.utc.localize(parsed_date)

                for item in request.user.meeting_set.all():
                    if (item.date == parsed_date and not (item.start > parsed_end or parsed_start>item.end)):
                        intersection = True
                        break
                if not intersection:
                    meeting = Meeting.objects.create(date=parsed_date,start=parsed_start,end=parsed_end,capacity=int(capacity),teacher=request.user)
                    return HttpResponseRedirect("/")
    return render(request, "createmeeting.html", {
        'falseDate':falseDate,
        'falseStart':falseStart,
        'falseEnd':falseEnd,
        'endBeforeStart':endBeforeStart,
        'intersection':intersection
    })


def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def validate_time(time_text):
    try:
        return datetime.strptime(time_text, '%H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect data format, should be HH:MM:SS")


def search_teachers(request):
    if request.GET:
        query = request.GET.get('query')
        src = User.objects.filter(is_staff=True)
        asatid = src.filter(username__icontains=query)
        asatid1 = src.filter(first_name__icontains=query)
        asatid2 = src.filter(last_name__icontains=query)
        asatid = asatid.union(asatid1, asatid2)
        records = []
        for ostad in asatid:
            first = ostad.first_name
            last = ostad.last_name
            link = '/profile/?username=' + ostad.username
            record = {'first_name': first, 'last_name': last, 'profile_url': link}
            records.append(record)
        # javab = json.dumps(json.loads(records))
        # javab = serializers.serialize('json',records)
        # seru
        javab=records
        return JsonResponse(javab, safe = False)


def forgot(request):
    error = False
    if request.POST:
        email = request.POST.get("email")
        if not User.objects.get(email=email).exists():
            error = True
        else:
            user = User.objects.get(email=email)
            send_mail("reset password",
                      BASE_DIR + "/reset/?user="+user.username,
                      "eden101010hazard@gmail.com",
                      [email]
                      )
    return render(request,"forgot.html",{'error': error})


def reset(request):
    if request.GET:
        user = request.GET.get('user')
        user = User.objects.get(user=user)
        return render(request, )