from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import stripe

#in production this should be in an environment variable not displayed here in code
stripe.api_key = 'sk_test_51N5oozJkQqpUUj2jyWiZCh7zwHh0vAXburItBiJES8oJUA18ypL2DtC6fG7BLLef3Mo0c9zyTqvgWSFxKgb7Hux500T2C2RaMZ'

# Create your views here.
def index(request):
    return render(request,'fitmaxapp/index-2.html',{})

def pay(request):
    return render(request,'fitmaxapp/pay.html',{})

def plan(request,pk):
     plan = get_object_or_404(FitnessPlan,pk=pk)
     if plan.premium:
          if request.user.is_authenticated:
               try:
                    if request.user.customer.membership:
                         return render(request,'fitmaxapp/pay.html',{'plan':plan})
               except Customer.DoesNotExist:
                    return render(request,'fitmaxapp',{})
          else:
               return render(request,'fitmaxapp/pay.html')
     return render(request,'fitmaxapp/pay.html',{})

                    
   
    
@login_required(login_url='fitMax:login-required') 
def checkout(request):
    coupons = {'halloween':30,'welcome':20}
    if request.method != 'POST':
                            
                            if request.GET.get('stripeToken'):
                                 
                                 stripe_customer = stripe.Customer.create( email = request.user.email,source = request.GET['stripeToken'])
                                 plan = 'price_1N5oqrJkQqpUUj2jEBKkW5EJ'
                                 if request.GET['plan'] == 'yearly':
                                      plan = 'price_1N5oqrJkQqpUUj2jLqodgX7T'
                                 if request.GET['coupon'] in coupons:
                                      percentage = coupons[request.GET['coupon'].lower()]
                                      try:
                                           
                                           coupon = stripe.Coupon.create(duration = 'once',id = request.GET['coupon'].lower(),percentage_off = percentage)
                                      except:
                                           pass
                                      subscription = stripe.Subscription.create(customer=stripe_customer.id,items=[{'plan':plan}],coupon = request.GET['coupon'].lower())
                                 else:
                                      subscription = stripe.Subscription.create(customer=stripe_customer.id,items=[{'plan':plan}])

                                 customer = Customer()
                                 customer.user = request.user
                                 customer.stripeid = stripe_customer.id
                                 customer.membership = True
                                 customer.cancel_at_period_end = False
                                 customer.stripe_subscription_id = subscription.id
                                 customer.save()
                                 messages.success(request,'Your Purchase has been completed successfully')
                                 return HttpResponseRedirect(reverse('fitMax:index'))
                            
                            plan = 'monthly'
                            coupon = 'none'
                            price = 100
                            og_dollar = 0
                            coupon_dollar = 0
                            final_dollar = 10

                            if request.GET.get('plan'):
                                 if request.GET['plan'] == 'yearly':
                                      plan = 'yearly'
                                      price = 10000
                                      og_dollar = 100
                                      final_dollar = 100

                            if request.GET.get('coupon'):
                                 if request.GET['coupon'].lower() in coupons:
                                      coupon = request.GET['coupon'].lower()
                                      percentage = coupons[coupon]
                                      coupon_price = int((percentage/100) * price)
                                      price = price - coupon_price
                                      coupon_dollar = str(coupon_price)[:-2] + '.' + str(coupon_price)[-2:]
                                      final_dollar = str(price)[:-2] + '.' + str(price)[-2:]

                            return render(request,'fitmaxapp/checkout.html',
                                          {'plan':plan,
                                           'coupon':coupon,
                                           'price':price,
                                           'og_dollar':og_dollar,
                                           'coupon_dollar':coupon_dollar,
                                           'final_dollar':final_dollar
                                           }
                                          )
    else:
        messages.success(request,'Your Purchase has been completed successfully')
        return HttpResponseRedirect(reverse('fitMax:index'))

def settings(request):
     membership = False
     cancel_at_period_end =False
     if request.method == 'POST':
          subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
          subscription.cancel_at_period_end = True
          cancel_at_period_end = True
          subscription.save()
          request.user.customer.save()
          pass
     else:
          try:
               if request.user.customer.membership:
                    membership = True
               if request.user.customer.cancel_at_period_end:
                    cancel_at_period_end = True
          except Customer.DoesNotExist:
               membership = False
     return render(request,'fitmaxapp/settings.html',{'membership':membership,'cancel_at_period_end':cancel_at_period_end})
               


def _login(request):
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request,user)
        messages.success(request,'Welcome back {0},we are happy to see you again.'.format(user.first_name))
        return HttpResponseRedirect(reverse('fitMax:index'))
    else:
        messages.warning(request,'Wrong credential combination,please check your credentials and try again.')
        return HttpResponseRedirect(reverse('fitMax:index'))


def sign_up(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    cpass = request.POST['cpassword']

    if password == cpass:
        try:
            user = User.objects.create_user(first_name = fname, last_name = lname, email = email,password = password,username=email)
            user.save()
            login(request,user)
            messages.success(request,'Congratulations {0},You have been successfully registered'.format(fname))
            return HttpResponseRedirect(reverse('fitMax:index'))
        except:
            messages.warning(request,'That username is already taken,please choose another name.')
            return HttpResponseRedirect(reverse('fitMax:index'))
    else:
        messages.warning(request,'Passwords do not match,sign up failed')
        return HttpResponseRedirect(reverse('fitMax:index'))
        
def logout_view(request):
    messages.warning(request,'You have been successfully logged out.')
    logout(request)
    return HttpResponseRedirect(reverse('fitMax:index'))

def required(request):
    messages.warning(request,'Please log in to access this feature')
    return HttpResponseRedirect(reverse('fitMax:index'))