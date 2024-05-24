from django.shortcuts import render,redirect
from django.views.generic import View , ListView , DetailView
from .models import Products,CartItem
from django.db.models import Q
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
class Home(View):
    def get(self,req):
       products = Products.objects.all()
       return  render(req,'home.html',{'products':products})
    
class ProdDetailView(DetailView):
    model = Products
    template_name='prod_details.html'

def mobileFilter(requests):
    queryset = Products.products.mobile()
    context = {
        'products' : queryset
    }
    return render(requests,'home.html',context)

def laptopFilter(requests):
    data = Products.objects.filter(prod_category__iexact='laptop')
    context = {
        'products' : data
    }
    return render(requests,'home.html',context)

def tvFilter(requests):
    queryset = Products.products.tv()
    context = {
        'products' : queryset
    }
    return render(requests,'home.html',context)

def rangeView(req):
    try:
        if req.method=='POST':
            min = req.POST['minInput']
            max = req.POST['maxInput']
            product = Products.objects.filter(prod_price__range=(min,max))
            context = {
            'products' : product
            }
            return render(req,'home.html',context)
        else:
            redirect('/')
    except:
        product = Products.objects.all()
        context = {
            'products' : product,
            'msg':"Don't Leave empty fields"
         }
        return render(req,'home.html',context)


def  sorting(req):
    sort_option = req.GET.get('sort')
    if sort_option == 'high_to_low':
        product = Products.objects.all().order_by('-prod_price')
    elif sort_option == "low_to_high" :
        product = Products.objects.all().order_by('prod_price')
    else:
        product = Products.objects.all()
    context = {
            'products' : product
        }
    return render(req,'home.html',context)

def search(req):
    query = req.POST['searched_term']
    result_products = Products.objects.filter(Q(prod_name__icontains = query)|Q(prod_price__icontains = query)|Q(prod_category__icontains = query))
    context = {
            'products' : result_products
        }
    return render(req,'home.html',context)

def addCart(req,id):
    prodo = Products.objects.get(prod_id=id)
    user = req.user if req.user.is_authenticated else None
    print(user)
    # cart_prodo = CartItem.objects.create(product =prodo)
    if user:
        cart_items,created = CartItem.objects.get_or_create(product =prodo,user = user)
    # print(cart_items.product.prod_name)
    if not created:
        cart_items.quantity +=1
    else:
        cart_items.quantity = 1
    cart_items.save()
    print(cart_items,created)
    return redirect('/viewCart')

def viewCart(req):
    cart_items = CartItem.objects.filter(user=req.user)
   
    total_price=0
    total_quantity = 0
    for i in range(len(cart_items)):
        total_price+=cart_items[i].product.prod_price * cart_items[i].quantity 
    for i in range(len(cart_items)):
        total_quantity+=cart_items[i].quantity 
    context = {
        'products' :cart_items,
        'cost' :total_price,
        'qty' : total_quantity
    }
    return render(req,'cart.html',context)


def deleteCartItems(req,id):
    item_to_delete = CartItem.objects.filter(product_id=id)
    print(item_to_delete)
    item_to_delete.delete()
    return redirect('/viewCart')

def updQty(req,val,item_id):
    ct = CartItem.objects.filter(product_id=item_id,user = req.user)
    print(val,ct)
    if val == 0 :
        temp = ct[0].quantity-1
        ct.update(quantity=temp)
        if temp == 0:
            ct.delete()
       
    else:
        temp = ct[0].quantity+1
        ct.update(quantity=temp)
    context={
        'products' :ct
    }
    return redirect('/viewCart')

def registerForm(req):
    form = CreateUserForm()
    if req.method=='POST':
        form =CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,'User Created')
            return redirect('/login')
        else:
            messages.error(req,'Details Invalid')
    context={
        'form':form
    }
    return render(req,'register.html',context)

def login_user(req):
    if req.method == 'GET':
        return render(req,'login.html')
    else:
        username = req.POST['uname']
        passw = req.POST['upass']
        print(username,passw)
        user = authenticate(req,username=username,password=passw)
        if user is not None:
            login(req,user)
            print("You are in !!!")
            messages.success(req,"Login Succesfull")
            return redirect('home')
        else:
            messages.error(req,"Details are incoorect,Try again!!!")
            return render(req,'login.html')

def logout_user(req):
    logout(req)
    messages.success(req,'You are Loggedout Successfully')
    return redirect('login')

def placeOrders(req):
    cart_items = CartItem.objects.filter(user=req.user)
   
    total_price=0
    total_quantity = 0
    for i in range(len(cart_items)):
        total_price+=cart_items[i].product.prod_price * cart_items[i].quantity 
    for i in range(len(cart_items)):
        total_quantity+=cart_items[i].quantity 
    context = {
        'products' :cart_items,
        'cost' :total_price,
        'qty' : total_quantity
    }
    return render(req,'place_orders.html',context)