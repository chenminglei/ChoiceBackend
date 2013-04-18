from django.http import HttpResponse
from django.template import Context, loader
from polls.models import Poll
from django.http import Http404
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
from django.contrib import auth
import time


@csrf_exempt
def index(request):
    print "aaa"
    dict = {}
    info = 'success'
    try:
        if request.method == 'POST':
            print request.body
            #req = simplejson.loads(request.body)
            username = request.POST['name']
            print username
            #password = req['passwd']
            #print "user: %s pwd: %s" % (username, password)
            #req = simplejson.loads(request.body)
            #username = req['name']
            #password = req['passwd']
            #print "user: %s pwd: %s" % (username, password)
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])

    dict['message']=info
    dict['create_at']=str(time.ctime())
    json=simplejson.dumps(dict)
    return HttpResponse(json, mimetype='application/json')




    #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    #context = Context({
    #    'latest_poll_list': latest_poll_list,
    #})
    #return HttpResponse(template.render(context))
    #output = ','.join([p.question for p in latest_poll_list])
    #return HttpResponse(output)

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    #return HttpResponse("You are looking at poll %s." % poll_id)
    return HttpResponse(csrf.get_token(request))

@csrf_exempt
def results(request, poll_id):
    print 'results'
    dict = {}
    dict['create_at']=str(time.ctime())
    if request.user.is_authenticated():
        print 'results1'
        dict['message']='alreadylogin'
    else:
        print 'results2'
        username = request.POST['username']
        password = request.POST['password']  
        user = auth.authenticate(username=username, password=password)
        if user.is_authenticated():
            dict['message']='alreadylogin2'

        elif user is not None and user.is_active:
            auth.login(request, user)
            dict['message']='login'
        else:
            dict['message']='none'
    json=simplejson.dumps(dict)
    return HttpResponse(json, mimetype='application/json')

def vote(request, poll_id):
    return HttpResponse("You are voting on poll %s." % poll_id)



