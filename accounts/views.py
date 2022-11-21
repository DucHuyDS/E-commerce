
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from .forms import AccountForm, RegistrationForm,AccountProfileForm
from .models import Account,AccountProfile
from cart.models import Cart
import random
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from checkout.models import Order,Payment,Contact
from django.core.paginator import Paginator

# Create your views here.


def _send_code(request, user):
    request.session['code'] = random.randint(1000, 9999)
    subject = 'Xác thực tài khoản Email của bạn'
    message = render_to_string('email/account_verification.html', {
        'user': user,
        'code': request.session['code']
    })
    email = user.email
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email]
    )
    request.session['time_out'] = datetime.now().hour*60*60 + \
        datetime.now().minute*60+datetime.now().second+60


def log_in(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
         
            

        else:
            messages.error(request, 'Tài khoản hoặc mật khẩu không hợp lệ')
            return redirect('log_in')
    return render(request, 'accounts/log_in.html')


def log_out(request):
    auth.logout(request)
    messages.success(request,'Đăng xuất thành công')
    return redirect('log_in')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                username = email.split('@')[0]
                user = Account.objects.create_user(
                    email=email, first_name=first_name, last_name=last_name, username=username, password=password)
                user.phone = phone
                user.save()

                user_profile=AccountProfile()
                user_profile.user_id=user.id
                user_profile.profile_picture='account/defaulavatar.jpg'
                user_profile.save()

                user_cart=Cart()
                user_cart.user_id=user.id
                user_cart.save()
                
                request.session['email'] = user.email
                _send_code(request, user)
               
                return redirect('/accounts/verify_email/?email='+user.email)
            else:
                messages.error(request, 'Mật khẩu không trùng khớp')
                return redirect('register')

        else:
            try:
                email=request.POST['email']
                user=Account.objects.get(email__exact=email)
            except Account.DoesNotExist:
                user=None
                
            if user is not None and user.is_active==False:
                request.session['email'] = user.email
                _send_code(request,user)
                return redirect('/accounts/verify_email/?email='+user.email)
            else:
                messages.error(request, 'Email đã tồn tại')
                return redirect('register')

    else:
        form = RegistrationForm()

    context = {
        'form': form,

    }
    return render(request, 'accounts/register.html', context)


def verify_email(request):
    url = request.META.get('HTTP_REFERER')
    request.session['time_now'] = datetime.now().hour*60*60 + \
        datetime.now().minute*60+datetime.now().second
    try:
        email = request.session['email']
        user = Account.objects.get(email__exact=email)
    except Account.DoesNotExist:
        user = None

    if 'code' in request.GET:
        code = request.GET['code']
        if str(code) == str(request.session['code']):
            if str(request.session['time_now']) <= str(request.session['time_out']):
                if user.is_active == False:
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Xác thực thành công')
                    return redirect('log_in')
                else:
                    messages.success(request, 'Xác thực thành công')
                    return redirect('/accounts/reset_password/?email='+user.email)

            
            else:
                messages.error(request, 'Mã xác thực đã hết hạn')
                return redirect(url)
        else:
            messages.error(request, 'Mã xác thực không hợp lệ')
            return redirect(url)
    time_remaining = request.session['time_out'] - request.session['time_now']
    context = {
        'user': user,
        'time_remaining': time_remaining,
    }
    return render(request, 'accounts/verify_email.html', context)


def resend_verify_email(request):
    url = request.META.get("HTTP_REFERER")
    email = request.session['email']
    user = Account.objects.get(email__exact=email)
    _send_code(request, user)
    return redirect(url)


def forgot_password(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            user = Account.objects.get(email__exact=email)
        except:
            user = None

        if user is not None and user.is_active==True:
            request.session['email'] = email
            _send_code(request, user)
            return redirect('/accounts/verify_email/?email='+user.email)
        else:
            messages.error(request, 'Không tìm thấy tài khoản')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.session['email']
        user = Account.objects.get(email__exact=email)
        if password == confirm_password:
            user.set_password(password)
            user.save()
            messages.success(request, 'Tạo mật khẩu thành công')
            return redirect('log_in')
        else:
            messages.error(request, 'Mật khẩu không trùng khớp')
            return redirect('/accounts/reset_password/?email='+user.email)
    return render(request, 'accounts/reset_password.html')

def profile(request):
    user=request.user
    url=request.META.get('HTTP_REFERER')
    user_profile=AccountProfile.objects.get(user_id=user.id)
    if request.method == 'POST':
        accountform=AccountForm(request.POST,instance=user)
        profileform=AccountProfileForm(request.POST,request.FILES,instance=user_profile)
        if accountform.is_valid() and profileform.is_valid():
           
            accountform.save()
            profileform.save()
            messages.success(request,'Cập nhật hồ sơ thành công')
            return redirect('profile')
    else:
        accountform=AccountForm(instance=user)
        profileform=AccountProfileForm(instance=user_profile)

    if '/checkout/' in url:
        return redirect(url)

    context={
        'user_profile':user_profile,
        'accountform':accountform,
        'profileform':profileform
    }
    return render(request,'accounts/profile.html',context)

def dashboard(request):
    user=request.user
    user_profile=AccountProfile.objects.get(user_id=user.id)
    payments=Payment.objects.filter(user_id=user.id)
    total=0
    for payment in payments:
        total+=payment.total_price
    payment_count=payments.count()
    context={
        'user_profile':user_profile,
        'payment_count':payment_count,
        'total':round(total,2)
    }
    return render(request,'accounts/dashboard.html',context)


def my_order(request):
    user=request.user
    user.notification=0
    user.save()
    contacts=Contact.objects.filter(user_id=user.id).order_by('-created_at')
    context={
        'contacts':contacts,
    }
    paginator = Paginator(contacts, 7) 
    contact_number = request.GET.get('page')
    contacts = paginator.get_page(contact_number)
    context={
        'contacts':contacts,
        
    }
    return render(request,'accounts/my_order.html',context)

def order_details(request,payment_id):
    payment=Payment.objects.get(payment_id=payment_id)
    contact=Contact.objects.get(user_id=request.user.id,payment=payment)
    order=Order.objects.filter(payment=payment)
    context={
        'contact':contact,
        'order':order
    }
    return render(request,'accounts/order_details.html',context)

def change_password(request):
    if request.method=='POST':
        password=request.POST['currentpassword']
        new_password=request.POST['newpassword']
        confirm_new_password=request.POST['confirmnewpassword']
        user=request.user
        if new_password==confirm_new_password:
            success=user.check_password(password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Đổi mật khẩu thành công')
                return redirect('log_in')
            else:
                messages.error(request,'Mật khẩu hiện tại không đúng')
                return redirect('change_password')
        else:
            messages.error(request,'Mật khẩu không trùng nhau')
            return redirect('change_password')
    return render(request,'accounts/change_password.html')

