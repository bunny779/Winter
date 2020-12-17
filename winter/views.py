from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.db.models import Sum
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.http import HttpResponse
import json
from django.db import connections
from . import static
from PIL import Image 
import os
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from Paytm.checksum import *

MERCHANT_KEY = '27XwUSfN#JRJDHrZ'

cursor = connections['default'].cursor()


def index(request):
    category = Categorys.objects.all()
    return render(request,'index.html',{'category':category})

# def category_page(request,cat_name):
#     category = Categorys.objects.filter(category_name=cat_name)
#     print(cat_name)
#     product =Product.objects.all()
#     context = {'product':product,'subcategory_name':cat_name}
#     return render(request,'category.html',context)
def category(request,cat_name):
    
    category = Categorys.objects.filter(category_name=cat_name) 
    subcategory= Subcategory.objects.filter(categorys_id = category[0].id)
    product = Product.objects.filter(categorys_id = category[0].id)
    context = {'product':product,'category':category,'subcategory':subcategory,'category_name':cat_name}
    return render(request,'category.html',context)

def single_product(request,pro_details):
    product = Product.objects.filter(product_name= pro_details)
    category = Categorys.objects.filter(id=product[0].categorys_id) 
    subcategory = Subcategory.objects.filter(id=product[0].subcategory_id)
    context = {'product':product,'category_name':category[0].category_name,'subcategory_name':subcategory[0].subcategory_name,'product_name':product[0].product_name}
    return render(request,'single-product.html',context)


def sub_category(request,cat_name,sub_name):
    
    category = Categorys.objects.filter(category_name=cat_name) 
    subcategory1= Subcategory.objects.filter(subcategory_name = sub_name)
    subcategory = Subcategory.objects.filter(categorys_id = category[0].id)
    product = Product.objects.filter(categorys_id = category[0].id,subcategory_id = subcategory1[0].id)
    # print(category)
    # print(subcategory)
    # print(product)

    context = {'product':product,'subcategory_name':sub_name,'category_name':cat_name,'subcategory':subcategory,'category':category}
    return render(request,'category.html',context)

def category_main(request):
    category = Categorys.objects.all()
    context = {'category':category}
    return render(request,'category_main.html',context)


def login(request):
    if request.session.has_key('username'):
        return redirect('/')

    if request.method == 'POST':
        form = loginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        #print(email,password)
        count = Register.objects.filter(email=email,password=password).count()
        
        
        if count > 0:
            request.session['username']=email
            

            return redirect('/')
        else:
            messages.error(request,'invalid user')
            return redirect('/login')

    else:
        form = loginForm()
    context={'form':form}
    return render(request,'login.html',context)  

def register(request):
    if request.session.has_key('username'):
        return redirect('/')
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            try:
                form.save() 
                return redirect('/login')
            except:
                pass
    else:
        form = registerForm()
    return render(request,'register.html',{'form':form})   

def logout(request):
    if request.session.has_key("username"):
        del request.session['username']
        return redirect('/login')
    return redirect('/login')


def cart(request):
    if request.session.has_key('username'):
        user = Register.objects.filter(email=request.session['username'])
        obj1 = Cart.objects.filter(user_id=user[0].id)
        all_prod = []
        total = Cart.objects.filter(user_id=user[0].id).aggregate(totals= Sum('price')).get('totals')
        
        for x in obj1:
            product = Product.objects.filter(id = x.product_id )
            all_prod.extend(product)
        detail = zip(obj1,all_prod)
        return render(request,'cart.html',{'zip':detail,'total':total})
    return redirect('/login')

def add_cart(request,id):
    if request.session.has_key('username'):
        user = Register.objects.filter(email=request.session['username'])
        prod = Product.objects.filter(id = id)
        count = Cart.objects.filter(user_id = user[0].id,product_id=id).count()
        if count > 0:
            cart = Cart.objects.filter(user_id = user[0].id,product_id=id)
            quantity = cart[0].quantity + 1
            price = prod[0].product_price * quantity
            obj = Cart.objects.filter(user_id = user[0].id,product_id=id).update(quantity=quantity,price=price)
            return redirect('/cart')
        else:
            obj = Cart(user_id=user[0].id,product_id=id,price=prod[0].product_price)
            obj.save()
            return redirect('/cart')
    else:
        return redirect('/login')

def delete_cart(request,id):
    Cart.objects.filter(id=id).delete()
    return redirect('/cart')

def delete_all_cart(request):
    user = Register.objects.filter(email=request.session['username'])
    Cart.objects.filter(user_id=user[0].id).delete()
    return redirect('/cart')

def update_cart(request):
    if request.method == "GET":
        cart = request.GET.get('cart_id')
        quantity = request.GET.get('quantity')

        response_data = {}
        crt = Cart.objects.filter(id=cart)    
        prod = Product.objects.filter(id=crt[0].product_id)
        total = int(prod[0].product_price) * int(quantity)
        obj = Cart.objects.filter(id=cart).update(price=total,quantity=quantity)
        response_data['obj']=obj
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    return HttpResponse(
            json.dumps({"nothing to see":"No"}),
            content_type="application/json"
        )

def all_product(request):   
    category = Categorys.objects.all()
    product = Product.objects.all().order_by('categorys_id')
    subcategory = Subcategory.objects.all()
    context = {'category':category,'product':product,'sucategory':subcategory}
    return render(request,'allproduct.html',context)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        messages = request.POST['message']
        subject = request.POST['subject']
        obj = Contact(name=name,email=email,message=messages,subject=subject)
        obj.save()

        # print(name,email,messages,subject)
        data=" Name :"+name+"\n Email :"+email+"\n Message :"+messages+"\n Subject :"+subject
        send_mail('New Contact Received',data,'bunnysorff@gmail.com',['bunnysroff@gmail.com'])
        # img = Image.open(r'D:\Ecom\ecommerce\winter\b1.jpg')
        html_content = '<div><p>Thank You</p><img src="https://image.shutterstock.com/image-vector/thank-you-hand-drawn-lettering-260nw-780491263.jpg" alt="thak you for contact" style="width:400px;height:400px;"></div>'
        msg = EmailMultiAlternatives('Thank You','Thank You for contacting us','bunnysroff@gmail.com',[email])
        msg.attach_alternative(html_content,"text/html")
        msg.send()

        
    return render(request,'contact.html')


def checkout(request):
    if request.session.has_key('username'):
        user = Register.objects.filter(email=request.session['username'])
        obj1 = Cart.objects.filter(user_id=user[0].id)
        all_prod = []
        subtotal = Cart.objects.filter(user_id=user[0].id).aggregate(totals= Sum('price')).get('totals')
        total = int(subtotal)+ int(100)
        checkout = Address.objects.filter(register_id=user[0].id)
        for x in obj1:
            user = Register.objects.filter(email=request.session['username'])
            product = Product.objects.filter(id = x.product_id )
            all_prod.extend(product)
        detail = zip(obj1,all_prod)
        context = {'zip':detail,'subtotal':subtotal,'userdata':user,'checkout':checkout,'total':total}
        return render(request,'checkout.html',context)
    else:
        return redirect('/login')

#for Paytm implement
@csrf_exempt
def handlerequest(request):       
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]=form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify is True:
        if response_dict['RESPCODE']=='01':
            return redirect('/')
        else:
            return HttpResponse("Error "+response_dict['RESPMSG'])
    else:
        return HttpResponse(response_dict)


def data(request):
    if request.session.has_key('username'):
        user = Register.objects.filter(email=request.session['username'])
        amt =[]
        lst_or = []
        if request.method == 'POST':
            number = request.POST['number']
            address1 = request.POST['add1']
            address2 = request.POST['add2']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zip']
            obj = Address(register_id=user[0].id,contact=number,address1=address1,address2=address2,city=city,state=state,zipcode=zipcode)
            obj.save()

            car = Cart.objects.filter(user_id=user[0].id)
            for c in car:
                
                ord = Order(product_id=c.product_id,register_id=user[0].id,quantity=c.quantity,price=c.price)
                ord.save()
                a = Order.objects.raw('SELECT id FROM winter_order ORDER BY id DESC LIMIT 1')
                lst_or.append(a[0].id)
                amt.append(c.price)
            amts = sum(amt)
            add = Address.objects.raw('SELECT id FROM winter_address ORDER BY id DESC LIMIT 1')
            print(add[0].id)
            r = user[0].id
            addr = add[0].id
            date = datetime.now()
            or_num = OrderNumber(amount=amts,address_id=addr,register_id=r,date=date)
            or_num.save()
            get_on = OrderNumber.objects.raw('select id from winter_ordernumber where id=(select last_insert_rowid())')
            for l in lst_or:
                query = "Insert into winter_ordernumber_order(ordernumber_id,order_id) values("+str(get_on[0].id)+","+str(l)+")"
                cursor.execute(query)
            data = "Order id :"+str(get_on[0].id)
            send_mail('Order Confirm',data,'bunnysroff@gmail.com',[user[0].email])
            Cart.objects.filter(user_id=user[0].id).delete()
            o_id = "INV--"+str(get_on[0].id)
            print(get_on[0].id,amts,user[0].email)
            param_dict = {
            'MID':'CCjQrf50252529085191',
            'ORDER_ID':str(o_id),
            'TXN_AMOUNT':str(amts),
            'CUST_ID':user[0].email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	    	'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest',
            }
            param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, MERCHANT_KEY)
            return render(request,'paytm.html',{'param_dict':param_dict,'order':o_id,'email':user[0].email})
        
        

    return redirect('/login')

def faq(request):
    get_on = OrderNumber.objects.raw('select ordernumber_id from winter_ordernumber_order where order_id=(select last_insert_rowid())')
    return render(request,'faq.html')

def tracking(request):
    
    return render(request,'tracking.html')

def confirmation(request):
    if request.method == "POST":
        order = request.POST['order']
        email = request.POST['email']
        register = Register.objects.filter(email=email)
        count = OrderNumber.objects.filter(id=order,register__email=email).count()
        
        if count > 0:

            user = Register.objects.filter(email=email)
            obj1 = Order.objects.filter(register_id=user[0].id)
            all_prod = []
            subtotal = Order.objects.filter(register_id=user[0].id).aggregate(totals= Sum('price')).get('totals')
            total = int(subtotal) + int(100)
            checkout = Address.objects.filter(register_id=user[0].id)
            get_on = OrderNumber.objects.filter(register_id = user[0].id)
            for x in obj1:
                user = Register.objects.filter(email=email)
                product = Product.objects.filter(id = x.product_id )
                all_prod.extend(product)
            
            context = {'order':obj1,'subtotal':subtotal,'total':total,'userdata':user,'checkout':checkout,'ordernumber':get_on}
            return render(request,'confirmation.html',context)
        else:
            messages.error(request,'No Order Found')
            return redirect("/tracking")
    return redirect("/tracking")
    
def profile(request):
    if request.session.has_key('username'):
        user = Register.objects.filter(email=request.session['username'])
        checkout = Address.objects.filter(register_id=user[0].id)    
        context = {'user':user,'checkout':checkout}    
        return render(request,'profile.html',context)
    else:
        return redirect('/login')

def edit_address(request,id):
    if request.session.has_key('username'):
        user = Register.objects.filter(email=request.session['username'])
        checkout = Address.objects.filter(register_id=user[0].id,id=id)
        context ={'checkout':checkout}
        return render(request,'edit_address.html',context)
    else:
        return redirect('/login')
def update_address(request, id):
    if request.session.has_key("username"):
        user = Register.objects.filter(email=request.session['username'])
        checkout = Address.objects.filter(register_id=user[0].id,id=id)  
        if request.method == 'POST':
            number = request.POST['number']
            address1 = request.POST['add1']
            address2 = request.POST['add2']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zip']
            obj = Address.objects.filter(register_id=user[0].id).update(contact=number,address1=address1,address2=address2,city=city,state=state,zipcode=zipcode)
            
            return redirect("/profile")

        context ={'checkout':checkout}
        return render(request,'edit_address.html',context)
    else:
        return redirect('/login')

def add_address(request):
    if request.session.has_key('username'):
        user = Register.objects.filter(email=request.session['username'])
        checkout = Address.objects.filter(register_id=user[0].id)       
        
        return render(request,'add_address.html')
    else:
        return redirect('/login')