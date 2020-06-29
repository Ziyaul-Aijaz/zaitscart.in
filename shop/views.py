from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
# Create your views here.
def index(request):
	allProds=[]
	ctgprods=Product.objects.values('category', 'id')

	ctgs={item['category'] for item in ctgprods}
	for ctg in ctgs:
		prod=Product.objects.filter(category=ctg)
		n=len(prod)
		nSlides=n//4 + ceil((n/4)-(n//4))
		allProds.append([prod, range(1, nSlides), nSlides])
	params={'allProds':allProds}
	return render(request, 'shop/index.htm', params)
    #products = Product.objects.all()
    #print(products)
    #n = len(products)
    #nSlides = n//4 + ceil((n/4)-(n//4))
    #[products, range(1,nSlides), nSlides],
    #[products, range(1,nSlides), nSlides]]
    #params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
	
def productview(request, myid):
	#fetch the product using id
	product=Product.objects.filter(id=myid)
	
	return render(request, 'shop/productview.htm', {'product':product[0]})

def searchMatch(query, item):
	''' returntrue only if query matches the item '''
	if query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
		return True
	else:	
		return False

def search(request):
	query= request.GET.get('search')
	allProds=[]
	ctgprods=Product.objects.values('category', 'id')
	ctgs={item['category'] for item in ctgprods}
	for ctg in ctgs:
		prodtemp=Product.objects.filter(category=ctg)
		prod=[item for item in prodtemp if searchMatch(query,item)]
		n=len(prod)
		nSlides=n//4 + ceil((n/4)-(n//4))
		if len(prod)!=0:
			allProds.append([prod, range(1, nSlides), nSlides])
	params={'allProds':allProds, "msg": ""}
	if len(allProds) == 0:
		params={'msg': "Sorry! for the problem faced, but currently we do not have the requested item"}

	return render(request, 'shop/search.htm', params)	
	

def about(request): 
	return render(request,'shop/about.htm')
def contact(request):
	thank=False
	if request.method=="POST":
		name=request.POST.get('name', '')
		email=request.POST.get('email', '')
		phone=request.POST.get('phone', '')
		desc=request.POST.get('desc', '')
		contact=Contact(name=name, email=email, phone=phone, desc=desc)
		contact.save()	
		thank = True
	return render(request,'shop/contact.htm',{'thank':thank})	
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')

        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates,order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.htm')


def category(request):
	return render(request,'shop/category.htm')


def feedback(request):


	
	return render(request,'shop/feedback.htm')

def checkout(request):   
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount=request.POST.get('amount','')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.htm', {'thank':thank, 'id': id})

    return render(request, 'shop/checkout.htm')
        
	