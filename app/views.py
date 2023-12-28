from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from app.forms import *
from app import forms
from django.urls import reverse
from django.contrib import messages,auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
import math
from django.db.models import F
from django.core.mail import send_mail

def index(request):
    user_wallet = UserWallet.objects.get(user=request.user.id)
    current_user = user_wallet.id
    
    transactions = Transaction.objects.filter(sender=current_user).annotate(transaction_type=F('recipient'))
    received_transactions = Transaction.objects.filter(recipient=current_user).annotate(transaction_type=F('sender'))
    all_transactions = transactions.union(received_transactions).order_by('-timestamp')

    return render(request, 'home.html', {
        'user_wallet': user_wallet,
        'all_transactions': all_transactions,
    })

def login_page(request):
    if request.method =='POST':
        name=request.POST.get("username")
        pwd=request.POST.get("Password")
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            
            messages.success(request,"successfully login ")
            return redirect('home')
        else :
            messages.error(request,"Invalid username or password")
            return redirect(reverse("login"))   
    return render(request,"login.html")
    

def register(request):
    form=CustomUserForm()
    
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['email']
            msg='''

"Welcome to Google Pay! 🌟

We're thrilled to have you on board. With Google Pay, you can securely and conveniently make payments, send money to friends, and explore exciting offers.

Feel free to explore the app, and if you have any questions or need assistance, our support team is here to help.

Happy payments!
The Google Pay Team
'''
            send_wel_email(user,msg)
            form.save()
            return redirect('login')

    return render(request,"register.html",{'form':form})



def success(request):
    try:
        sender_profile = request.GET.get('sender_profile')
        rec = request.GET.get('rec')
        amount = request.GET.get('amount')
    except:   pass 


    return render(request, 'success.html', {'sender_profile': sender_profile, 'rec': rec, 'amount': amount})


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully")
    return render(request,"home.html")

def pinchange(request):
    oldpin = UserWallet.objects.get(user=request.user.id)
    if request.method == 'POST':
        new_pin_form = PinChangeForm(request.POST) 
        
        if new_pin_form.is_valid():
            new_pin = new_pin_form.cleaned_data['pin']
            
            oldpin.pin = new_pin
            oldpin.save()
            msg='Your PIN has been successfully changed. You can now use the new PIN for future transactions'
            send_welcome_email(request,msg)


            
            messages.success(request,'pin changed successfully')
            return redirect("home")
    return render(request,"pin.html",{'PinChangeForm':PinChangeForm()})            

 

def send_wel_email(mail,msg):
    subject = 'Google pay Notification'
    message = msg
    from_email = 'vendavenda251@gmail.com'  
    recipient_list = [mail]

    send_mail(subject, message, from_email, recipient_list)   

    return redirect("login")

def phonechange(request):
    oldphone = UserWallet.objects.get(user=request.user.id)
    if request.method == 'POST':
        new_phone_form = NumChangeForm(request.POST) 
        
        if new_phone_form.is_valid():
            new_phone = new_phone_form.cleaned_data['phone']
            
           
            oldphone.phone_number = new_phone
            oldphone.save()
            username = request.user.username
            msg = f'Dear {username},\n\nYour phonenumber has been successfully changed. You can now use the new phonenumber for future logins'
            send_welcome_email(request,msg)
            messages.success(request,'phonenumber changed successfully')
            return redirect("home")

    

    return render(request,"phonenumber.html",{'NumChangeForm':NumChangeForm()})

def passchange(request):
    oldpass= User.objects.get(id=request.user.id)
    if request.method == 'POST':
        new_pass_form = PassChangeForm(request.POST) 
        
        if new_pass_form.is_valid():
            new_pass = new_pass_form.cleaned_data['password']
            
           
            oldpass.set_password(new_pass)
            oldpass.save()
            msg = f'Dear user ,\n\nYour password has been successfully changed. You can now use the new password for future logins'
            send_welcome_email(request,msg)
            messages.success(request,'password changed successfully , Re-login ')
            return redirect("login")

    

    return render(request,"pass.html",{'PassChangeForm':PassChangeForm()})





@login_required
def pay(request,id):
    user_wallet = UserWallet.objects.get(user=id)
    recipient_profile = UserWallet.objects.get(user=id)
    pin_form = PinForm()
    transfer_form = TransferForm()

                
    if request.method == 'POST':
     
        if 'pin_submit' in request.POST:
            pin_form = PinForm(request.POST)
            if pin_form.is_valid():
                entered_pin = pin_form.cleaned_data['pin']
                
                if entered_pin == user_wallet.pin:
                    messages.success(request, 'PIN verified successfully .')
                    pin_verified = True
                    return render(request, 'pay.html', {'transfer_form': transfer_form, 'pin_form': pin_form,  'pin_verified': pin_verified,'recipient_profile':recipient_profile})
                elif entered_pin != user_wallet.pin:
                    messages.error(request, 'Incorrect Pin .')

        elif 'transfer_submit' in request.POST:
            form = TransferForm(request.POST)
            
            if form.is_valid():
                
                
                amount = form.cleaned_data['amount']

                sender_profile = UserWallet.objects.get(user=request.user.id)
                
                
                if sender_profile.account_balance >= amount:
                    with db_transaction.atomic():
                        
                        sender_profile.account_balance -= amount
                        sender_profile.save()

                        msg=f'Dear {sender_profile},\n\nYour Account Debited : {amount} To {recipient_profile} has been successfully .'
                        send_welcome_email(request,msg)
                        
                        recipient_profile.account_balance += amount
                        recipient_profile.save()

                        Transaction.objects.create(sender=sender_profile, recipient=recipient_profile, amount=amount)
                        success_url = reverse('success')
                        success_url += f'?sender_profile={sender_profile}&rec={recipient_profile}&amount={amount}'

                        
                        return redirect(success_url)
                else:
                    messages.error(request, 'You have insuffieint Balance')
                    return redirect('home')
                
    return render(request, 'pay.html', { 'transfer_form': transfer_form, 'pin_form': pin_form ,'recipient_profile':recipient_profile  })
def verifiy(request):
    if request.method == 'POST':
        phone_form =PhoneNumberForm(request.POST, prefix='another')
        user=UserWallet.objects.get(user=request.user.id)

        if phone_form.is_valid():
            phone_number = phone_form.cleaned_data['phone_number']
            current_number = user.phone_number
            

            if phone_number!=current_number:

                try:
                    profile = UserWallet.objects.get(phone_number=phone_number)
                    usertdt=User.objects.get(id=request.user.id)
                    user_verified = True
                    messages.success(request,"User Found ")
                    return render(request, 'verify.html', { 'phone_form': phone_form, 'user_verified': user_verified,'profile':profile })
                   
                    return render(request, 'pay.html', { })

                except UserWallet.DoesNotExist:
                    messages.error(request,"User Not Found")

            else:
                messages.error(request,"You can't make transaction to own account")
                return redirect(reverse("verify"))  
                
                    
    else:
       
        phone_form = PhoneNumberForm(prefix='another')

    return render(request, 'verify.html', { 'phone_form': phone_form})
def send_welcome_email(request,msg):
    subject = 'Google pay Notification'
    message = msg
    from_email = 'vendavenda251@gmail.com'  
    recipient_list = [request.user.email]

    send_mail(subject, message, from_email, recipient_list)  