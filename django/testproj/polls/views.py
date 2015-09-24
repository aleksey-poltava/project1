from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import socket

from socket import AF_INET, SOCK_DGRAM
import sys
import struct, time

from .models import Choice, Question, roadcar

# REST example

from rest_framework import viewsets
from .serializers import RoadcarSerializer

# Create your views here.
# class IndexView(generic.ListView):
#    model = roadcar
#    template_name = 'polls/index.html'

    # context_object_name = 'latest_question_list'

#    def get_queryset(self):
#        """Count number of records in cars table. It is equal to cars number that passes road"""
#        car_counter = roadcar.objects.count()
#        context = {'car_counter': car_counter}
#        return render(self, 'polls/index.html', context)
        # return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def main(request):
    return render_to_response('polls/ajaxexample.html', context_instance=RequestContext(request))

def ajax(request):
    if request.POST.has_key('client_response'):
        x = request.POST['client_response']
        y = socket.gethostbyname(x)
        response_dict = {}
        response_dict.update({'server_response': y})
        return HttpResponse(json.dumps(response_dict), content_type = 'application/javascript')
    else:
        return render_to_response('polls/ajaxexample.html', context_instance = RequestContext(request))

def realtime(request):
    return render_to_response('polls/real-time.html', context_instance=RequestContext(request))

def getrealtime(request):
    localtime = str(time.strftime("%H:%M:%S"))
    ntptime = str(getNTPTime())
    response_dict = {}
    response_dict.update({'server_response': localtime})
    response_dict.update({'server_response_1': ntptime})
    return HttpResponse(json.dumps(response_dict), content_type = 'application/javascript')

def getNTPTime(host = "pool.ntp.org"):
        port = 123
        buf = 1024
        address = (host,port)
        msg = '\x1b' + 47 * '\0'

        # reference time (in seconds since 1900-01-01 00:00:00)
        TIME1970 = 2208988800L # 1970-01-01 00:00:00

        # connect to server
        client = socket.socket( AF_INET, SOCK_DGRAM)
        client.sendto(msg, address)
        msg, address = client.recvfrom( buf )

        t = struct.unpack( "!12I", msg )[10]
        t -= TIME1970
        return time.ctime(t).replace("  "," ")

# http://www.uswitch.com/mobiles/mobile_tracker/ - mobile phone selling stat
# the most visited places of interest, cities

def index(request):
    car_counter = roadcar.objects.count()
    context = {'car_counter': car_counter}
    return render(request, 'polls/index.html', context)

# serializer REST example

class RoadcarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = roadcar.objects.all()
    serializer_class = RoadcarSerializer
