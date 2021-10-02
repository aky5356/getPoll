from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from poll.models import Poll, Option

class PollListView(ListView):
    model = Poll
    template_name = 'poll/main.html'


def singlePollDetail(request, pk):
    poll = Poll.objects.get(pk=pk)
    print(poll)
    return render(request, 'poll/poll_page.html', {'poll': poll})

def poll_data_view(request,pk):
    poll = Poll.objects.get(pk=pk)
    
    ans = []
    for i in poll.get_option():
        ans.append(i.text)
    
    context = {str(poll.question): ans}
    #after a minute pass the time as time--
    return JsonResponse({
        'data': context,
        'time': poll.time
    })


def save_poll_data(request, pk):
    if request.is_ajax():
        data = request.POST
        poll = Poll.objects.get(pk=pk)
        
        for i in poll.get_option():
            if i.text == data[poll.question]:
                i.count += 1
                i.save()
        # i need the all the option here which is associated with this question and
        # then I'll do the count ++ manually of the selected option
    
        
    return JsonResponse({'data': 'this is save poll data' })

def option_count_data(request,pk):
    #using pk we will get the the question then we will see their count;
    poll = Poll.objects.get(pk=pk)

   

    options = {}

    hello = poll.get_option()
       

    context = {'polls': poll, 'hello': hello}
    

    return render(request, 'poll/result.html', context)

