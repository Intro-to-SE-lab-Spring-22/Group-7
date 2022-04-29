from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
import hashlib, math
from .forms import UploadFileForm, handle_uploaded_file
from .models import User, Post, Comment, Friendlink


def index(request):
	start = "login"
	return render(request, 'userpage/index.html', {'error':"none", 'start':start })

def new_acc(request):
	if(request.POST['newname'] != ""):
		try:
			page = get_object_or_404(User, user_name=request.POST['newname'])
			error = "prev_acc"
			start = "signup"
			return render(request, 'userpage/index.html', {'error':error, 'start':start})
		except:
			passstr = request.POST['newpass']
			confpassstr = request.POST['newpassconf']
			if(passstr != confpassstr):
				error = "pass_match"
				start = "signup"
				return render(request, 'userpage/index.html', {'error':error, 'start':start})
			bypass = bytes(passstr, 'utf-8')
			hashpass = hashlib.sha256(bypass).hexdigest()
			u = User(user_name=request.POST['newname'], password = hashpass, start_date=timezone.now())
			u.phone = request.POST['phone']
			u.email = request.POST['email']
			u.birthday = request.POST['birthday']
			gender = request.POST['gender']
			u.gender = gender
			u.save()
			html = HttpResponseRedirect(reverse('page', args=(u.id,))) 
			html.set_cookie('user_cookie', u.id)
			return html
	else:
		error = "blank_signup"
		start = "signup"
		return render(request, 'userpage/index.html', {'error':error, 'start':start})

def sign_in(request):
	if(request.POST['username'] != ""):
		name = request.POST['username']
		passstr = request.POST['password']
		bypass = bytes(passstr, 'utf-8')
		hashpass = hashlib.sha256(bypass).hexdigest()
		try:
			u = get_object_or_404(User, user_name = name)
		except:
			error = "acct_miss"
			start = "login"
			return render(request, 'userpage/index.html', {'error':error, 'start':start})
		if(u.password == hashpass):
			html = HttpResponseRedirect(reverse('page', args=(u.id,))) 
			html.set_cookie('user_cookie', u.id)
			return html
		else:
			error = "pass_fail"
			start = "login"
			return render(request, 'userpage/index.html', {'error':error, 'start':start})
	else:
		error = "user_name_miss"
		start = "login"
		return render(request, 'userpage/index.html', {'error':error, 'start':start})

def post(request, user_id):
	u = get_object_or_404(User, pk=user_id)
	new_text = request.POST['text_input']
	p = u.post_set.create(post_text = new_text, op=u.user_name, pub_date=timezone.now(), src=1, share=0)
	p.src = p.id
	p.save()
	return HttpResponseRedirect(reverse('page', args=(user_id,))) 

def page(request, user_id):
	try:
		user = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
		size = user.list_size
	except:
		user = 1
	page = get_object_or_404(User, pk=user_id)
	max_page = math.ceil(page.post_set.count()/size)
	if max_page == 0:
		max_page = 1
	max_page_prev = max_page - 1
	post_list = page.post_set.order_by('-pub_date')[:size]
	friend_request_get = page.user_get.filter(accepted = False)
	friend_request_send = page.user_send.filter(accepted = False)
	friend_get = page.user_get.filter(accepted = True)
	friend_send = page.user_send.filter(accepted = True)
	try:
		f = Friendlink.objects.filter(sender = user).get(receiver = page)
		friendstat = "True"
	except:
		try:
			f = Friendlink.objects.filter(sender = page).get(receiver = user)
			friendstat = "True"
		except:
			friendstat = "False"
	return render(request, 'userpage/page.html', {'page':page, 'user':user, 'post_list':post_list, 'friend_request_get':friend_request_get, 'friend_request_send':friend_request_send, 'friend_get':friend_get, 'friend_send':friend_send, 'friendstat':friendstat, 'max_page':max_page, 'page_num':1, 'page_num_prev':0, 'page_num_post':2, 'max_page_prev':max_page_prev})

def page_num(request, user_id, page_num):
	try:
		user = get_object_or_404(User, pk=request.COOKIES.get('user_cookie')) 
		size = user.list_size
	except:
		user = 1
	page = get_object_or_404(User, pk=user_id)
	max_page = math.ceil(page.post_set.count()/size)
	if max_page == 0:
		max_page = 1
	max_page_prev = max_page - 1
	page_num_prev = page_num - 1
	page_num_post = page_num + 1
	post_list = page.post_set.order_by('-pub_date')[(size*(page_num-1)):(size * page_num)]
	friend_request_get = page.user_get.filter(accepted = False)
	friend_request_send = page.user_send.filter(accepted = False)
	friend_get = page.user_get.filter(accepted = True)
	friend_send = page.user_send.filter(accepted = True)
	try:
		f = Friendlink.objects.filter(sender = user).get(receiver = page)
		friendstat = "True"
	except:
		try:
			f = Friendlink.objects.filter(sender = page).get(receiver = user)
			friendstat = "True"
		except:
			friendstat = "False"
	return render(request, 'userpage/page.html', {'page':page, 'user':user, 'post_list':post_list, 'friend_request_get':friend_request_get, 'friend_request_send':friend_request_send, 'friend_get':friend_get, 'friend_send':friend_send, 'friendstat':friendstat, 'max_page':max_page, 'page_num':page_num, 'page_num_prev':page_num_prev, 'page_num_post':page_num_post, 'max_page_prev':max_page_prev})

def search(request):
	try:
		page = get_object_or_404(User, user_name=request.POST['search'])
	except:
		return HttpResponse("page does not exist")
	return HttpResponseRedirect(reverse('page', args=(page.id,))) 

def comment_page(request, post_id):
	user = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
	size = user.list_size
	post = get_object_or_404(Post, pk=post_id)
	page = get_object_or_404(User, pk=post.user.id)
	comment_list = post.comment_set.order_by('-pub_date')[:size]
	max_page = math.ceil(post.comment_set.count()/size)
	if max_page == 0:
		max_page = 1
	max_page_prev = max_page - 1
	friend_request_get = page.user_get.filter(accepted = False)
	friend_request_send = page.user_send.filter(accepted = False)
	friend_get = page.user_get.filter(accepted = True)
	friend_send = page.user_send.filter(accepted = True)
	try:
		f = Friendlink.objects.filter(sender = user).get(receiver = page)
		friendstat = "True"
	except:
		try:
			f = Friendlink.objects.filter(sender = page).get(receiver = user)
			friendstat = "True"
		except:
			friendstat = "False"
	return render(request, 'userpage/post.html', {'page':page, 'post':post, 'comment_list':comment_list, 'user':user, 'friend_request_get':friend_request_get, 'friend_request_send':friend_request_send, 'friend_get':friend_get, 'friend_send':friend_send, 'friendstat':friendstat, 'max_page':max_page, 'page_num':1, 'page_num_prev':0, 'page_num_post':2, 'max_page_prev':max_page_prev}) 

def comment_page_num(request, post_id, page_num):
	user = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
	size = user.list_size
	post = get_object_or_404(Post, pk=post_id)
	page = get_object_or_404(User, pk=post.user.id)
	comment_list = post.comment_set.order_by('-pub_date')[(size*(page_num-1)):(size * page_num)]
	max_page = math.ceil(post.comment_set.count()/size)
	if max_page == 0:
		max_page = 1
	max_page_prev = max_page - 1
	page_num_prev = page_num - 1
	page_num_post = page_num + 1
	friend_request_get = page.user_get.filter(accepted = False)
	friend_request_send = page.user_send.filter(accepted = False)
	friend_get = page.user_get.filter(accepted = True)
	friend_send = page.user_send.filter(accepted = True)
	try:
		f = Friendlink.objects.filter(sender = user).get(receiver = page)
		friendstat = "True"
	except:
		try:
			f = Friendlink.objects.filter(sender = page).get(receiver = user)
			friendstat = "True"
		except:
			friendstat = "False"
	return render(request, 'userpage/post.html', {'page':page, 'post':post, 'comment_list':comment_list, 'user':user, 'friend_request_get':friend_request_get, 'friend_request_send':friend_request_send, 'friend_get':friend_get, 'friend_send':friend_send, 'friendstat':friendstat, 'max_page':max_page, 'page_num':page_num, 'page_num_prev':page_num_prev, 'page_num_post':page_num_post, 'max_page_prev':max_page_prev}) 

def comment_post(request, post_id):
	p = get_object_or_404(Post, pk=post_id)
	new_text = request.POST['text_input']
	p.comment_set.create(user = get_object_or_404(User, pk=request.COOKIES.get('user_cookie')), pub_date=timezone.now(), comment_text = new_text)
	return HttpResponseRedirect(reverse('comment_page', args=(post_id,)))  

def share(request, post_id):
	user = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
	post = get_object_or_404(Post, pk=post_id)
	try:
		user.share_set.get(post=post)
	except:
		share = user.post_set.create(post_text = post.post_text, op=post.user.user_name, src=post.id, pub_date=timezone.now(), share=1)
	return HttpResponseRedirect(reverse('page', args=(user.id,)))
  
def friend(request, user_id):
	try:
		u1 = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
		u2 = get_object_or_404(User, pk=user_id)
		try:
			f = Friendlink.objects.filter(sender = u1).get(receiver = u2)
			f.delete()
			return HttpResponseRedirect(reverse('page', args=(u1.id,)))
		except:
			try:
				f = Friendlink.objects.filter(sender = u2).get(receiver = u1)
				if f.accepted:
					f.delete()
					return HttpResponseRedirect(reverse('page', args=(u1.id,)))
				else:
					if request.POST['friend'] == "1":
						f.delete()
						return HttpResponseRedirect(reverse('page', args=(u1.id,)))
					elif request.POST['friend'] == "0":
						f.accepted = True
						f.save()
						return HttpResponseRedirect(reverse('page', args=(u1.id,)))
					else:
						f.delete()
						return HttpResponseRedirect(reverse('page', args=(u1.id,)))
			except:
				Friendlink.objects.create( sender = u1, receiver = u2 )
				return HttpResponseRedirect(reverse('page', args=(u1.id,)))
	except:
		return HttpResponse('uncaught exception')
            
            

def mesg(request, user_id):
	return HttpResponse('message')

def edit(request, post_id):
	if(request.POST['edit'] == "0"):
		p = get_object_or_404(Post, pk=post_id)
		p.post_text = request.POST['text_input']
		p.save()
		return HttpResponseRedirect(reverse('page', args=(p.user.id,)))
	elif(request.POST['edit'] == "1"):
		p = get_object_or_404(Post, pk=post_id)
		p.post_text = request.POST['text_input']
		p.save()
		return HttpResponseRedirect(reverse('comment_page', args=(post_id,)))
	elif(request.POST['edit'] == "2"):
		c = get_object_or_404(Comment, pk=post_id)
		c.comment_text = request.POST['text_input']
		c.save()
		return HttpResponseRedirect(reverse('comment_page', args=(c.post.id,)))
	else:
		return HttpResponseRedirect(reverse('comment_page', args=(post_id,)))

def delete(request, post_id):
	if(request.POST['del'] == "0"):
		p = get_object_or_404(Post, pk=post_id)
		p.delete()
		return HttpResponseRedirect(reverse('page', args=(p.user.id,)))
	elif(request.POST['del'] == "1"):
		p = get_object_or_404(Post, pk=post_id)
		p.delete()
		return HttpResponseRedirect(reverse('page', args=(p.user.id,)))
	elif(request.POST['del'] == "2"):
		c = get_object_or_404(Comment, pk=post_id)
		c.delete()
		return HttpResponseRedirect(reverse('comment_page', args=(c.post.id,)))
	elif(request.POST['del'] == "3"):
		u = get_object_or_404(User, pk=post_id)
		u.delete()
		return HttpResponseRedirect(reverse('index', args=()))
	else:
		return HttpResponseRedirect(reverse('comment_page', args=(post_id,)))

def like(request, post_id):
	if(request.POST['like'] == "0"):
		try:
			u = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
			p = get_object_or_404(Post, pk=post_id)
			try:
				l = u.like_set.get(post = p)
				l.delete()
				return HttpResponseRedirect(reverse('page', args=(p.user.id,)))
			except:
				l = p.like_set.create(user = u)
			return HttpResponseRedirect(reverse('page', args=(p.user.id,)))
		except:
			return HttpResponseRedirect(reverse('page', args=(p.user.id,))) 
	elif(request.POST['like'] == "1"):
		try:
			u = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
			p = get_object_or_404(Post, pk=post_id)
			try:
				l = u.like_set.get(post = p)
				l.delete()
				return HttpResponseRedirect(reverse('comment_page', args=(post_id,)))
			except:
				l = p.like_set.create(user = u)
			return HttpResponseRedirect(reverse('comment_page', args=(post_id,)))
		except:
			return HttpResponseRedirect(reverse('comment_page', args=(post_id,)))
	elif(request.POST['like'] == "2"):
		try:
			u = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
			c = get_object_or_404(Comment, pk=post_id)
			try:
				l = u.like_set.get(comment = c)
				l.delete()
				return HttpResponseRedirect(reverse('comment_page', args=(c.post.id,)))
			except:
				l = c.like_set.create(user = u)
			return HttpResponseRedirect(reverse('comment_page', args=(c.post.id,)))
		except:
			return HttpResponseRedirect(reverse('comment_page', args=(c.post.id,)))
	else:
		return HttpResponseRedirect(reverse('comment_page', args=(post_id,)))

def chng_pass(request):
	u = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
	passstrold = request.POST['oldpass']
	bypassold = bytes(passstrold, 'utf-8')
	hashpassold = hashlib.sha256(bypassold).hexdigest()
	if(u.password == hashpassold):
		passstrnew = request.POST['newpass']
		passstrconf = request.POST['newpassconf']
		if(passstrnew == passstrconf):
			bypassconf = bytes(passstrconf, 'utf-8')
			hashpassconf = hashlib.sha256(bypassconf).hexdigest()
			u.password = hashpassconf	
			u.save()
			return HttpResponseRedirect(reverse('page', args=(u.id,)))
		else:
			return HttpResponse("1")
	else:
		return HttpResponse("2")

def chng_img(request, user_id):
	context = {}
	if request.method == "POST":
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.cleaned_data.get("title")
			img = form.cleaned_data.get("file")
			user = get_object_or_404(User, pk=request.COOKIES.get('user_cookie'))
			user.title = name
			user.img = img
			user.save()
			print(user.title)
			u = get_object_or_404(User, pk=user_id)
			return HttpResponseRedirect(reverse('page', args=(u.id,)))
	else:
		form = UploadFileForm()
	context['form']= form
	context['user_id'] = user_id
	user = get_object_or_404(User, pk=user_id)
	context['user'] = user
	return render(request, "userpage/home.html", context)

def chng_size(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	size = request.POST['size']
	user.list_size = size
	user.save()
	return HttpResponseRedirect(reverse('page', args=(user.id,)))

def chng_data(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	email = request.POST['email']
	user.email = email
	phone = request.POST['phone']
	user.phone = phone
	gender = request.POST['gender']
	user.gender = gender
	username = request.POST['user_name']
	try:
		get_object_or_404(User, user_name = username)
	except:
		user.user_name = username
	user.save()
	return HttpResponseRedirect(reverse('page', args=(user.id,)))