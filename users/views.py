from django.shortcuts import render, redirect
from users import forms
from django.contrib.auth.models import User
from django.contrib import auth
from users.models import account, item
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

def index(request):
	return render(request, 'users/index.html')

def aboutus(request):
	return render(request, 'users/aboutus.html')

# Search
 
def search(request):
	
	query = request.GET.get('q')
	results = item.objects.filter(Q(title__icontains = query) | Q(description__icontains = query) | Q(price__icontains = query))

	n = len(results)
	
	collist = [[],[],[],[]]

	for i in range(n):
		collist[i%4].append(results[i])
	
	print("This is the collist")
	print(collist)

	context = { 
		'collist':collist,	
	 }


	return render(request,'users/buy.html', context)

	
# Buy views

def buy(request):

	item_all = item.objects.all().order_by('-createdAt')

	n = len(item_all)
	
	collist = [[],[],[],[]]

	for i in range(n):
		collist[i%4].append(item_all[i])
	
	print("This is the collist")
	print(collist)

	context = { 
		'allitems': item_all,
		'collist':collist,	
	 }

	return render(request, 'users/buy.html', context)


def categorybuy(request, cat = 'OT'):
	print("category:" + cat)

	item_all = item.objects.filter(category = cat).order_by('-createdAt') 
	
	n = len(item_all)
	
	collist = [[],[],[],[]]

	for i in range(n):
		collist[i%4].append(item_all[i])
	
	print("This is the collist")
	print(collist)

	context = { 
		'allitems': item_all,
		'collist':collist,	
	 }


	return render(request,'users/buy.html', context)



# Login, Logout, Register, Profile views
@login_required
def register(request):

	if request.method == "POST":

		phnum = request.POST['phone']
		address = request.POST['address']
		user = request.user	

		if phnum == '':
			return render(request, 'users/register.html', {'error': "Phone Number is required"})

				
		newaccount = account(phone_num = phnum, address = address, user = user)
		newaccount.save()
	
		return redirect('profile')



	return render(request, 'users/register.html')


'''
def login(request):
	if request.method == "POST":

		user = 	auth.authenticate(username= request.POST['uname'], password = request.POST['pass'] )
		if user is not None :
			auth.login(request,user)
			return redirect('profile')
		else:
			return render(request, 'users/login.html', {'error': "Invalid login credentials"})

	return render(request, 'users/login.html')
'''

@login_required
def logout(request):
	auth.logout(request)
	return redirect('buy')


@login_required
def profile(request):

	useraccount = account.objects.filter(user = request.user)
	items = []

	registered = False

	for u in useraccount:
		registered = True
	

	if(registered == False):
		return redirect('register')
		
	for u in useraccount:
		items = u.item_set.all()


	n = len(items)
	collist = [[],[],[],[]]

	for i in range(n):
		collist[i%4].append(items[i])


	context = {
		'data': useraccount,
		'items': items,
		'collist':collist
	}

	return render(request, 'users/profile.html',context)


# Add Items view

@login_required
def additem(request):

	itemform = forms.ItemForm()

	registered = False
	useraccount = account.objects.filter(user = request.user)

	for u in useraccount:
		registered = True

	if(registered == False):
		return redirect('register')


	if request.method == 'POST':

		#print('Arjun JOshi')

		
		itemform = forms.ItemForm(request.POST, request.FILES)

		#print("HEY THIS IS THE ITEMFORM")
		#print(itemform)


		if itemform.is_valid():

			#print("ARjun is soooo coool")

			title = itemform.cleaned_data['title']
			price = itemform.cleaned_data['price']
			description = itemform.cleaned_data['description']
			image = itemform.cleaned_data['image']
			category = itemform.cleaned_data['category']
			
			owner = 0
			for u in useraccount:
				owner = u

			newitem = item(title = title, price = price, description = description, category = category, owner = owner, image = image)
			newitem.save()

			return redirect('profile')
			#print('Item is saved')



	context = {
		'form': itemform,
	}

	return render(request, 'users/additem.html',context)


def delitem(request, it = 0):
	#print('Hey this is delitems')


	if request.method == 'POST':
		ditem = item.objects.get(id = it)
		ditem.image.delete(save = True)
		ditem.delete()

	return redirect('profile')


def viewitem(request, it = 0):
	#print("Hey this is viewitem")

	context = {}

	if request.method == 'POST':

		vitem = item.objects.get(id = it)
		context = {'item': vitem}

	return render(request, 'users/viewitem.html', context)