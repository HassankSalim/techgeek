from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import os
from .models import Questions, Options, User
from home.models import User as HomeUser
from datetime import timedelta
import datetime
from django.conf import settings


# START_TIME = datetime(year=2016,month=9,day=17,hour=0)


# def index(request):
#     if not datetime.now() >= START_TIME:
#         return HttpResponse('comingsoon')
#     return HttpResponse("Welcome to TechGeek 2016")


# @csrf_exempt
# def getRank(request):
#     return HttpResponse(0)

#from home.models import User as HomeUser

def index(request):
	if 'logged_in' in request.session:
		if request.session['logged_in']:
			user_id = request.session['uid']
			if not User.objects.filter(user_id=user_id).exists():
				home_user = HomeUser.objects.get(user_id=user_id)
				# request.session['start_time'] = -1
				# request.session['next_answered_qn'] = -1
				# request.session['today_total_time'] = 0
				User.objects.create(
					user_id = user_id,
					email = home_user.email,
					image_url = home_user.image_url,
					name = home_user.name,
					score = 0, 
					today_score = 0,
					totalTime = 0,
					start_time = -1,
					next_answered_qn = -1,
					today_total_time = 0,
					)
				today = datetime.datetime.now().day
				request.session['session_date'] = today
			else:
				today = datetime.datetime.now().day
				userObj = User.objects.filter(user_id=request.session.get('uid','0'))[0] 
				if 'session_date' in request.session:
					if request.session['session_date'] != today:
						request.session['session_date'] = today
						userObj.start_time = -1
						userObj.next_answered_qn = -1
						userObj.today_total_time = 0
						userObj.today_score = 0
						userObj.save()
				else:
					request.session['session_date'] = today
					userObj.start_time = -1
					userObj.next_answered_qn = -1
					userObj.today_total_time = 0
					userObj.today_score = 0
					userObj.save()

	return JsonResponse({})	


@csrf_exempt
def view_qn(request):
	response = {}
	#next qn
	print request.POST
	next_id = request.POST.get('qns_id')
	# print type(next_id)
	next_id = int(next_id)
	userObj = User.objects.filter(user_id=request.session.get('uid','0'))[0]
	# print userObj
	if userObj.next_answered_qn != -1 and next_id == -1:
		next_id = userObj.next_answered_qn
	# print next_id	
	#for chcking ans
	keySet = request.POST.keys()
	keySet.remove('qns_id')
	keyForAns = keySet[0]
	# print 'keyForAns is %s'%keySet[0], type(keySet[0])
	starting_day = 29 #28th Sept 2016
	user_id = request.session['uid']
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute
	second = datetime.datetime.now().second
	if hour >= 21 and hour <= 23 or True:
		if userObj.start_time == -1:
			time = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+(datetime.datetime.now().second)
			userObj.start_time = time
			userObj.save()
		current_time = datetime.datetime.now()
		minute = datetime.datetime.now().minute
		second = datetime.datetime.now().second
		current_time = (hour*3600)+(minute*60)+(second)
		timeElpasedInSec = current_time - userObj.start_time
		timeElpasedInMin = timeElpasedInSec / 60
		print 'time in min', timeElpasedInMin
		if timeElpasedInMin < 15:
			current_day = datetime.datetime.now().day	
			#############################################
			#checking answer of the current
			ans = request.POST.get(keyForAns)
			if ans != '':
				print 'key is', keyForAns
				ans = request.POST.get(keyForAns)
				print 'ans is%s'%ans
				print len(ans)
				ans = ans.replace('\n', '')
				qnsId = int(keyForAns)
				print qnsId
				print 'Inside key'
				questionObj = Questions.objects.get(id = qnsId)
				questionObj.selected = ans
				ansId = questionObj.ansId
				optionObj = Options.objects.get(id = ansId)
				if optionObj.option == ans:
					print 'CORRET ANS'
					questionObj.selected_ans = ans
					userObj.score += 1
					userObj.today_score += 1
					questionObj.save()
					userObj.save()
				print '2This is the user score', userObj.score		
				userObj.today_total_time = timeElpasedInSec	
				userObj.save()				
			#############################################	


			#############################################
			#response for next qn 

			#getting first qn of the day
			next_id = int(next_id)
			if userObj.next_answered_qn != -2:	
				if next_id == -1:
					questionObj = Questions.objects.filter(day=current_day)[0]
					count = Questions.objects.count()
					# print count
				else:
					questionObj = 	Questions.objects.filter(id=next_id, day=current_day)
					# print next_id
					if len(questionObj):
						# print 'thus here'
						questionObj = questionObj[0]
				if questionObj:
					userObj.next_answered_qn = next_id
					userObj.save()
					next_id = questionObj.id + 1
					print 'Time sent', timeElpasedInSec
					response = {	'qns':questionObj.qns, 'qnsId':int(questionObj.id), 'selected':questionObj.selected_ans, 'next_id':next_id, 'timestamp':timeElpasedInSec}
					optionList = questionObj.options_set.all()
					optList = []
					for i in optionList:
						optList.append(i.option)
					response.update({	'option':optList 	})
				else:
					userObj.next_answered_qn = -2
					userObj.totalTime += userObj.today_total_time
					userObj.save()
					response ={
						'qns':"You have completed today's question set",
						'score':userObj.score,
						'qnsId':-1
					}
				return JsonResponse(response, safe=False) 	
			else:
				response ={
						'qns':"You have completed today's question set",
						'timestamp':899,
						'score':userObj.score,
						'qnsId':-1
					}
				return JsonResponse(response, safe=False)
				#############################################			
		else:
			userObj.totalTime = userObj.today_total_time
			userObj.save()
			print 'reached'
			response ={
				'qns':"Come back tomorrow at 9",
				'score':userObj.score,
				'timestamp':899,
				'qnsId':-1
			}
			return JsonResponse(response, safe=False)
	else:
		response = {
			'qns':"Come back at 9",
			'score':userObj.score,
			'timestamp':900,
			'qnsId':-1
		}		
		return JsonResponse(response, safe=False)



def getRank(request):
    p = User.objects.all().order_by('-score', 'totalTime')
    i = 1
    for t in p:
        if t.user_id == request.session.get('uid', 0):
            return HttpResponse(i)
        i += 1
    return HttpResponse(0)

def top(request):
    return JsonResponse(leaderboardData())

def leaderboardData():
    p=User.objects.all().order_by('-score','totalTime')
    i=1
    l=[]
    for t in p:
        u=HomeUser.objects.get(user_id=t.user_id)
        user = {
        'name': u.name,
        'score': t.score,
        'image_url' : u.image_url,
        }
        l.append(user);
        i+=1

    data_to_send = {
    'leaderboard_data' : l,
    }
    return data_to_send


def add_to_model(request):
	# Options.objects.all().delete()
	# Questions.objects.all().delete()
	count = 0
	print settings.STATIC_ROOT
	noOfDays = 5
	qnsList = []
	for day in range(1, noOfDays+1):
		path = os.path.join(settings.STATIC_ROOT, "tech_geek_static/qns/day%s.txt"%day)
		qns_ans = open(path, 'r').read()
		single_qn_ans = qns_ans.split('||')
		for i in single_qn_ans:
			qns_ans_opt = i.split('#')
			question = qns_ans_opt[0].replace('\n', '').replace('\r', '')
			if question not in qnsList:
				count+=1
				answer = qns_ans_opt[-1].replace('\n', '').replace('\r', '')
				options = qns_ans_opt[1:-1]
				q = Questions()
				q.qns = question
				q.ansId = 0
				q.day = day
				q.selected_ans = ''
				q.save()
				for opt in options:
					optObj = Options()
					refined = opt.replace('\n', '')
					optObj.option = refined.replace('\r', '')
					optObj.qn = q
					optObj.save()
					if optObj.option == answer:
						q.ansId = optObj.id
						q.save()			

	print 'COUNTER', count				
	return render(request, 'asindex.html', {})	

def simpleServe(request):
	return render(request, 'asdindex.html', {})    
