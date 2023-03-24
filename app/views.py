from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import Product, Category, Cart, CartProduct, Category, Customer
from .forms import Checkoutform, CustomerRegistrationForm, login_form
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.contrib import messages

# Create your views here.

def home(request):
    data = Product.objects.all()

    category = Category.objects.all()
    category_name = None
    return render(request, 'app/home.html',{'data':data,'category':category,'category_name':category_name})

def about(request):
    category = Category.objects.all()
    return render(request, 'app/about.html',{'category':category})

def contact(request):
    category = Category.objects.all()
    if request.method == 'POST':
        name = str(request.POST.get('name'))
        mail = request.POST.get('mail')
        msg = request.POST.get('msg')
        subject = 'noreply'
        message=f"This is automatically generated email\nplease don't reply\nThank you Mr/Mrs {name.upper()} for your comments\n"
        try:
            send_mail(subject, message, 'bitf20a529@pucit.edu.pk' , [mail],fail_silently=False)
        except:
            return HttpResponse('<h1>server error!</h1>')
        return HttpResponseRedirect('/')

    return render(request, 'app/contact.html',{'category':category})

def view_product(request,slug):
    data = Product.objects.get(slug=slug)
    category = Category.objects.all()
    return render(request, 'app/view_one_product.html',{'data':data,'category':category})

def category_filter(request, slug):
    c_id = Category.objects.filter(slug=slug)
    data = Product.objects.filter(category=c_id[0].id)
    category = Category.objects.all()
    category_name = c_id[0].title
    return render(request, 'app/view_one_category.html',{'data':data,'category':category,'category_name':category_name})

def add_to_cart(request, product_id):
    data = Product.objects.all()
    category = Category.objects.all()
    category_name = None
    
    product_obj = Product.objects.get(id=product_id)

    cart_id = request.session.get('cart_id',None)
    
    # check if cart exitst
    if cart_id:
        cart_obj = Cart.objects.get(id=cart_id)
        p = cart_obj.cartproduct_set.filter(product=product_obj)
        if p.exists():
            cartproduct = p.last()
            cartproduct.quantity += 1
            cartproduct.subtotal += product_obj.selling_price   
            cartproduct.save()
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
        else:
            cartproduct = CartProduct.objects.create(
                cart=cart_obj,product=product_obj,rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price
            )
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
    else:
        cart_obj = Cart.objects.create(total=0)
        request.session['cart_id'] = cart_obj.id
        cartproduct = CartProduct.objects.create(
            cart=cart_obj,product=product_obj,rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price
        )
        cart_obj.total += product_obj.selling_price
        cart_obj.save()

    return HttpResponseRedirect('/view_cart/')

def view_cart(request):
    category = Category.objects.all()
    cart_id = request.session.get("cart_id",None)
    if cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id)
        except:
            cart = None
    else:
        cart = None
    return render(request, 'app/cart.html',{'category':category,'cart':cart})


def manage_cart(request,cp_id):
    action = request.GET.get("action")
    cp_obj = CartProduct.objects.get(id=cp_id)
    cart = cp_obj.cart
    cart_id = request.session.get("cart_id", None)
    if action == 'inc':
        cp_obj.quantity += 1
        cp_obj.subtotal += cp_obj.rate
        cp_obj.save()
        cart.total += cp_obj.rate
        cart.save()
    elif action == 'dcr':
        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.rate
        cp_obj.save()
        cart.total -= cp_obj.rate
        cart.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
    elif action == 'rmv':
        cart.total -= cp_obj.subtotal
        cart.save()
        cp_obj.delete()
    return HttpResponseRedirect("/view_cart/")

def check_out(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            if len(cart.cartproduct_set.all()) == 0:
                cart = None
            fm = Checkoutform(request.POST)
            if fm.is_valid():
                fm.instance.cart = cart
                fm.instance.subtotal = cart.total
                fm.instance.discount = 0
                fm.instance.total = cart.total
                fm.instance.order_status = "Order Received"
                fm.save()
                del request.session['cart_id']
                return HttpResponseRedirect('/')
        else:
            cart = None
        fm = Checkoutform()    
        return render(request, 'app/checkout.html',{'category':category,'cart':cart,"form":fm})
    else:
        return HttpResponseRedirect('/login/')


def signup(request):
    if not request.user.is_authenticated:
        category = Category.objects.all()
        if request.method == 'POST':
            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                email = request.POST['email']
                user = User.objects.create_user(username,email,password)
                form.instance.user = user
                if form.is_valid():
                    form.save()
                    form = CustomerRegistrationForm()
                    return render(request, 'app/signup.html',{'category':category,'fm':form})
            return render(request, 'app/signup.html',{'category':category,'fm':form})

        form = CustomerRegistrationForm()
        return render(request, 'app/signup.html',{'category':category,'fm':form})
    else:
        return HttpResponseRedirect('/')

def customer_login(request):
    if not request.user.is_authenticated:
        category = Category.objects.all()
        if request.method == 'POST':
            form = login_form(request=request, data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                usr = authenticate(username=username,password=password)
                if usr is not None:
                    do_login(request, usr)
                    return HttpResponseRedirect('/')
            messages.error(request, 'Incorrect username or password', extra_tags='login')
            return render(request, 'app/login.html',{'category':category,'fm':form})

        form = login_form()
        return render(request, 'app/login.html',{'category':category,'fm':form})
    else:
        return HttpResponseRedirect('/')

def logout(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            do_logout(request)
            return HttpResponseRedirect('/login/')
        else:
            return HttpResponse('<h1>404 page not found!</h1>')
    else:
        return HttpResponseRedirect('/login/')