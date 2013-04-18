from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.utils import simplejson
from choice.models import User, Poll, Choice


@csrf_exempt
def login(request):
    result = {'code':0}
    try:
        if request.method == 'POST':
            username = request.POST['username']
    	    password = request.POST['password']
            user = User.objects.get(username=username)
            if user.password == password:
                result['code'] = 1
                result['info'] = 'success'
            else:
                result['info'] = 'invalid password'
        else:
            result['info'] = 'invalid request'
    except User.DoesNotExist:
        result['info'] = 'invalid username'
    
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')     

@csrf_exempt
def register(request):
    result = {'code':0}
    try:
        if request.method == 'POST':
            username = request.POST['username']
    	    password = request.POST['password']
            email = request.POST['email']
            if username is not None and password is not None and email is not None:
                user = User(username=username, password=password, email=email)
                user.save()
                result['code'] = 1
                result['info'] = 'success'
            else:
                result['info'] = 'invalid info'
        else:
            result['info'] = 'invalid request'
    except User.DoesNotExist, IntegrityError:
        result['info'] = 'invalid username'
     
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')


@csrf_exempt
def index(request):
    def trans(poll, username = None):
        dic = {}
        dic['poll_id'] = poll.id
        dic['question'] = poll.question
        dic['pub_date'] = str(poll.pub_date)
        if username == None:
            user = User.objects.get(id=poll.user_id)
            dic['username'] = user.username
        else:
            dic['username'] = username
        return dic

    result = {'code':0}
    try:
        if request.method == 'POST':
            type = request.POST['type']
            if type == 'private':
                username = request.POST['username']
                user = User.objects.get(username=username)
                polls = Poll.objects.filter(user_id=user.id)
                list = [trans(p_item, username) for p_item in polls]
            else:
                polls = Poll.objects.all()
                list = [trans(p_item) for p_item in polls]
            result['list'] = list
            result['code'] = 1
            result['info'] = 'success'
        else:
            result['info'] = 'invalid request'

    except User.DoesNotExist, IntegrityError:
        result['info'] = 'invalid username'

    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')
            

@csrf_exempt
def detail(request):
    def trans(choice):
       #array = []
       #for choice in list:
        dic = {}
        dic['choice_text'] = choice.choice_text
        dic['image_url'] = choice.image_url
        dic['votes'] = choice.votes
        dic['choice_id'] = choice.id
            #array += dic
        return dic

    result = {'code':0}
    try:
        if request.method == 'POST':
            id = int(request.POST['p_id'])
            poll = Poll.objects.get(id=id)
            list = Choice.objects.filter(poll_id=id) 
            result['code'] = 1
            result['p_id'] = id
            result['question'] = poll.question
            result['pub_date'] = str(poll.pub_date)
            result['choices'] = [trans(item) for item in list]
            #result['choices'] = trans(list)
            result['info'] = 'success'
        else:
            result['info'] = 'invalid request'
    
    except Poll.DoesNotExist, Choice.DoesNotExist:
        result['info'] = 'invalid pollid'
    
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')

@csrf_exempt
def post(request):
    result = {'code':0}
    try:
        if request.method == 'POST':
            req = simplejson.loads(request.body)
            username = req['username']
            #print username
            user = User.objects.get(username=username)
            question = req['question']
            #print question
            p = Poll(user_id=user.id, question=question)
            p.save()
            choicelist = req['choice_list']
            #print choicelist
            for choice in choicelist:
                c = Choice(choice_text=choice['choice_text'],image_url=choice['image_url'],poll_id=p.id)             
                c.save()
            result['code'] = 1
            result['info'] = 'success'
        else:
            result['info'] = 'invalid request'

    except User.DoesNotExist,IntegrityError:
        result['info'] = 'invalid choice_id'

    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')

@csrf_exempt
def vote(request):
    result = {'code':0}
    try:
        if request.method == 'POST':
            choice_id = request.POST['choice_id']
            choice = Choice.objects.get(id=choice_id)
            choice.votes += 1
            choice.save()
            result['info'] = 'success'
            result['code'] = 1
        else:
            result['info'] = 'invalid request'

    except Choice.DoesNotExist:
        result['info'] = 'invalid choice_id'

    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')

@csrf_exempt
def profile(request):
    result = {'code':0}
    try:
        if request.method == 'GET':
            username = request.GET['username']
            user = User.objects.get(username=username)
            email = user.email
            result['user'] = username
            result['email'] = email
            result['info'] = 'success'            
            result['code'] = 1
        else:
            result['info'] = 'invalid request'
    except User.DoesNotExist:
        result['info'] = 'invalid username'

    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')
