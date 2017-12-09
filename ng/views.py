
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import Http404

# Create your views here.
from django.template import loader

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


from django.contrib.auth.models import User

from .models import Experiment,XpConfig,PastInteraction,Score
# ...
import json
import uuid

from django.utils import timezone
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from .forms import NameForm

def create_user(request,username='',name='',cookie_id=''):
    user = User.objects.create_user(username=str(username),first_name=str(name),email=str(cookie_id),password=str(username))
    user.save()

def login_user(request,username=''):
    user = authenticate(request, username=username, password=username)
    if user is not None:
        login(request, user)

def login_view(request):
    username = 'oug'
    return render(request, 'ng/login.html', {
            'username': username,
        })

@csrf_protect
@login_required(login_url='/login')
def home(request):
    return render(request, 'ng/home.html', {})

def create_and_login(request,username=None,name='',cookie_id=None):
    if username is None:
        username = name+str(cookie_id)
    if not User.objects.filter(username=username).exists():
        create_user(request,username,name=name,cookie_id=cookie_id)
    login_user(request,username)
    return render(request,'ng/index.html',{})


def get_name(request):
    # if POST: Form submitted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            name = form.cleaned_data['your_name']
            cookie_id = form.cleaned_data['name_cookie_id']
            create_and_login(request=request,name=name,cookie_id=cookie_id)
            return HttpResponseRedirect('/')

    # else (GET): Form to be presented
    else:
        form = NameForm()

    return render(request, 'ng/main.html', {
        'context': "login",
        'form': form,
    })

#@login_required#(login_url='/accounts/login/')
class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/ng/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'ng/index.html'
    context_object_name = 'latest_experiment_list'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Experiment.objects.all()

#@login_required#(login_url='/accounts/login/')


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/ng/login/'
    redirect_field_name = 'redirect_to'
    model = Experiment
    template_name = 'ng/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Experiment.objects.filter()


class ResultsView(LoginRequiredMixin, generic.DetailView):
    login_url = '/ng/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Experiment
    template_name = 'ng/results.html'



@csrf_protect
@login_required(login_url='/ng/login/')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'ng/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('ng:results', args=(question.id,)))


@login_required(login_url='/ng/login/')
def testdet(request, xp_uuid):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    return render(request, 'ng/detail.html', {
            'experiment': experiment,
            'error_message': "You didn't select a choice.",
        })

@csrf_protect
@login_required(login_url='/ng/login/')
def continue_xp(request, xp_uuid):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    experiment.continue_xp(steps=1)
    #raise IOError(experiment)
    #experiment.update_results()
    experiment.save()
    return render(request, 'ng/detail.html', {
            'experiment': experiment,
            'error_message': "You didn't select a choice.",
        })

@csrf_protect
@login_required(login_url='/ng/login/')
def result_srtheo(request, xp_uuid):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    experiment.update_results()
    experiment.save()
    return render(request, 'ng/results.html', {
            'experiment': experiment,
            'error_message': "You didn't select a choice.",
        })




@csrf_protect
@login_required(login_url='/ng/login/')
def result_hearer(request, xp_uuid, meaning):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    currentgame_json = experiment.get_currentgame_json()
    currentgame_json.update({'mh':int(meaning)})
    ms = currentgame_json['ms']
    w = currentgame_json['w']
    experiment.save_currentgame_json(currentgame_json)
    experiment.continue_xp()
    bool_succ = experiment.get_last_bool_succ()
    past_interaction = PastInteraction(meaning=ms,word=w,bool_succ=bool_succ,time_id=experiment.interaction_counter,role='hearer',experiment=experiment)
    experiment.save()
    past_interaction.save()
    return render(request, 'ng/main.html', {
            'experiment': experiment,
            'bool_succ': bool_succ,
            'role':"hearer",
            'context':"result"
        })

@csrf_protect
@login_required(login_url='/ng/login/')
def result_speaker(request, xp_uuid, meaning, word):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    currentgame_json = experiment.get_currentgame_json()
    ms = int(meaning)
    w = word
    currentgame_json.update({'ms':ms,'w':w})
    experiment.save_currentgame_json(currentgame_json)
    experiment.continue_xp()
    bool_succ = experiment.get_last_bool_succ()
    past_interaction = PastInteraction(meaning=ms,word=w,bool_succ=bool_succ,time_id=experiment.interaction_counter,role='speaker',experiment=experiment)
    experiment.save()
    past_interaction.save()
    #return render(request, 'ng/results_new.html', {
    #        'experiment': experiment,
    #        'bool_succ': bool_succ,
    #    })
    return render(request, 'ng/main.html', {
            'experiment': experiment,
            'bool_succ': bool_succ,
            'role':"speaker",
            'context':"result"

        })


@csrf_protect
@login_required(login_url='/ng/login/')
def none(request):
    return None

@csrf_protect
@login_required(login_url='/ng/login/')
def result_inner(request, xp_uuid, bool_succ):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    past_int = experiment.pastinteraction_set.last()
    return render(request, 'ng/results_toinclude_new.html', {
            'experiment': experiment,
            'bool_succ': past_int.bool_succ,
            'ms':past_int.meaning,
            'word':past_int.word,
            'mh':past_int.meaning_h,
            'role':past_int.role,
            'username':request.user.username
        })


@csrf_protect
@login_required(login_url='/ng/login/')
def result_hearer_json(request, xp_uuid, meaning):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    try:
        currentgame_json = experiment.get_currentgame_json()
    except:
        return render(request, 'ng/result.json', {
            'experiment': experiment,
            'bool_succ': experiment.last_bool_succ,
            'role':"hearer",
            'context':"result",
            'ms':experiment.last_ms,
        })
    currentgame_json.update({'mh':int(meaning)})
    ms = currentgame_json['ms']
    w = currentgame_json['w']
    experiment.save_currentgame_json(currentgame_json)
    experiment.continue_xp()
    bool_succ = experiment.get_last_bool_succ()
    past_interaction = PastInteraction(meaning=ms,word=w,meaning_h=int(meaning),bool_succ=bool_succ,time_id=experiment.interaction_counter,role='hearer',experiment=experiment)
    experiment.save()
    past_interaction.save()
    return render(request, 'ng/result.json', {
            'experiment': experiment,
            'bool_succ': bool_succ,
            'role':"hearer",
            'context':"result",
            'ms':ms,
        })

@csrf_protect
@login_required(login_url='/ng/login/')
def result_speaker_json(request, xp_uuid, meaning, word):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")    
    try:
        currentgame_json = experiment.get_currentgame_json()
    except:
        return render(request, 'ng/result.json', {
            'experiment': experiment,
            'bool_succ': experiment.last_bool_succ,
            'role':"speaker",
            'context':"result",
        })
    ms = int(meaning)
    w = word
    currentgame_json.update({'ms':ms,'w':w})
    experiment.save_currentgame_json(currentgame_json)
    experiment.continue_xp()
    bool_succ = experiment.get_last_bool_succ()
    mh = int(experiment.get_last_mh())
    past_interaction = PastInteraction(meaning=ms,word=w,meaning_h=mh,bool_succ=bool_succ,time_id=experiment.interaction_counter,role='speaker',experiment=experiment)
    experiment.exchange_agent(1, 2)
    experiment.save()
    past_interaction.save()
    #return render(request, 'ng/results_new.html', {
    #        'experiment': experiment,
    #        'bool_succ': bool_succ,
    #    })
    return render(request, 'ng/result.json', {
            'experiment': experiment,
            'bool_succ': bool_succ,
            'role':"speaker",
            'context':"result"

        })

@csrf_protect
@login_required(login_url='/ng/login/')
def choose_experiment(request,xp_cfg_name='normal'):
    return render(request, 'ng/main.html', {
            'context':"choose_xp",
        })

@csrf_protect
@login_required(login_url='/ng/login/')
def new_experiment(request,xp_cfg_name='normal'):
    experiment = Experiment.get_new_xp(user=request.user,xp_cfg_name=xp_cfg_name)
    experiment.save()
    return render(request, 'ng/main.html', {
            'experiment': experiment,
            'textid': "new_xp",
            'context':"new_xp"
        })

@csrf_protect
@login_required(login_url='/ng/login/')
def test(request):
    experiment = Experiment.get_new_xp()
    experiment.save()
    return render(request, 'ng/test.html', {
            'experiment': experiment,
        })

@csrf_protect
@login_required(login_url='/ng/login/')
def continue_userxp(request, xp_uuid):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    if 0 < experiment.max_interaction <= experiment.interaction_counter:
        return score(request, xp_uuid=xp_uuid)
    try:
        experiment.continue_xp(steps=1)
        nb_steps = 1
        try:
            while nb_steps<1000:
                experiment.continue_xp(steps=1)
                nb_steps += 1
            raise IOError('Not skipping more than 1000 steps at a time')
        except IOError as e:
            if str(e) == 'User intervention needed' or str(e) == 'Not skipping more than 1000 steps at a time':
                experiment.last_role = 'skipped'
                experiment.last_nb_skipped = nb_steps
                experiment.last_ms = None
                experiment.last_w = None
                experiment.last_mh = None
                experiment.last_bool_succ = False
                experiment.save()
                return render(request, 'ng/main.html', {
                    'experiment': experiment,
                    'textid': "not_involved",
                    'nb_skipped': nb_steps,
                    'context': 'skipped'
                       })

    except IOError as e:
        if str(e) == 'User intervention needed':
            currentgame_json = experiment.get_currentgame_json()
            experiment.save()
            sp_id = currentgame_json['speaker_id']
            hr_id = currentgame_json['hearer_id']
            experiment.update_meanings()
            experiment.update_words()
            if sp_id == experiment.get_user_agent_uuid():
                return render(request, 'ng/main.html', {
                    'experiment': experiment,
                    'role':"speaker",
                    'context':"question"
                    })
            elif hr_id == experiment.get_user_agent_uuid():
                return render(request, 'ng/main.html', {
                    'experiment': experiment,
                    'word': currentgame_json['w'],
                    'role':"hearer",
                    'context':"question"
                    })
            else:
                raise
        else:
            raise


@csrf_protect
@login_required(login_url='/ng/login/')
def exp_resume(request, xp_uuid):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    return render(request, 'ng/main.html', {
            'experiment': experiment,
            'context':"resume"
            })



@csrf_protect
@login_required(login_url='/ng/login/')
def score(request, xp_uuid):
    experiment = get_object_or_404(Experiment, xp_uuid=xp_uuid)
    if request.user != experiment.user:
        raise ValueError("wrong user")
    request.user.last_name = "test"
    request.user.save()
    try:
        score = Score.objects.get(experiment=experiment)
        score_val = score.score
    except:
        experiment.get_xp()
        srtheo = experiment.xp.graph(method="srtheo")._Y[0][-1]
        score_val = int(srtheo * experiment.meanings.count() * 100)#.all().count()?
        score = Score(experiment=experiment,score=score_val,user=request.user)
        score.save()

    #Test if score exists
    #if not, compute and store object
    #get value
    return render(request, 'ng/main.html', {
            'experiment': experiment,
            'score':score_val,
            'context':"score",
            'user':request.user,
            })