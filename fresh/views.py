from typing import ContextManager
from django.core.checks import messages
from django.db.models.fields import DateTimeField
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,FormView,DetailView,ListView,UpdateView
from django.views.generic.edit import UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import password_reset_token
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.http import JsonResponse
import datetime
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
# Create your views here.

class FreshMixin(object):
    def dispatch(self, request,*args, **kwargs):
        cart_id= request.session.get("cart_id") 
        if cart_id:
            cart_obj= Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and  Customer.objects.filter(user=request.user).exists():
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs) 

class HomeView(FreshMixin,TemplateView):
    template_name="home.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['notice']=Notice.objects.all().order_by("-id")[0]
        context['count']=Notice.objects.all().count()
        context['date'] =datetime.date.today().year
        context['updates'] =Update.objects.all() 
        
      

        #pagination
        all_products = Product.objects.all().order_by("id")
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        print(page_number)
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        #check if cart exit 
        cart_id=self.request.session.get("cart_id",None)
        #if cart_id exists
        if cart_id:
            cart= Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart

        return context


class ProductDetailsView(FreshMixin,TemplateView):
    template_name="productdetails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug =self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count +=1
        product.save()
        context['product']=product

        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['notice']=Notice.objects.all().order_by("-id")[0]
        context['count']=Notice.objects.all().count()
        context['date'] =datetime.date.today().year
        context['updates'] =Update.objects.all()

         #check if cart exit 
        cart_id=self.request.session.get("cart_id",None)
        #if cart_id exists
        if cart_id:
            cart= Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart


        return context

class AboutView(FreshMixin,TemplateView):
    template_name="about.html"

    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['notice']=Notice.objects.all().order_by("-id")[0]
        context['count']=Notice.objects.all().count()
        context['date'] =datetime.date.today().year
        context['about'] =About.objects.all()
     
      

       
        #check if cart exit 
        cart_id=self.request.session.get("cart_id",None)
        #if cart_id exists
        if cart_id:
            cart= Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart

        return context

class ServiceView(TemplateView):
    template_name="service.html"

    def get_context_data(self,**kwargs):
            context=super().get_context_data(**kwargs)
            context['bcontact']=BusinessContact.objects.all().order_by("id")
            context['btime']=BusinessTime.objects.all().order_by("id")
            context['notice']=Notice.objects.all().order_by("-id")[0]
            context['count']=Notice.objects.all().count()
            context['date'] =datetime.date.today().year
            context['service'] =Service.objects.all()
        
        

        
            #check if cart exit 
            cart_id=self.request.session.get("cart_id",None)
            #if cart_id exists
            if cart_id:
                cart= Cart.objects.get(id=cart_id)
            else:
                cart=None
            context['cart']=cart

            return context
        

class ContactView(CreateView):
    template_name="contact.html"
    form_class= ContactUsForm
    success_url=reverse_lazy('fresh:contact')
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['notice']=Notice.objects.all().order_by("-id")[0]
        context['count']=Notice.objects.all().count()
        context['date'] =datetime.date.today().year
        context['about'] =About.objects.all()
        #check if cart exit 
        cart_id=self.request.session.get("cart_id",None)
        #if cart_id exists
        if cart_id:
            cart= Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart

        return context


  


   
class AddToCartView(FreshMixin,View):
    def get (self,request,*args, **kwargs):     
        #get product id from requested url
        product_id= self.kwargs['pro_id']
        #get product
        product_obj= Product.objects.get(id=product_id)
        #check if cart exits
        cart_id=self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            this_product_in_cart= cart_obj.cartproduct_set.filter(product=product_obj)
            #item alredy exists in cart
            if this_product_in_cart.exists():
                if product_obj.quantity_unit=="Kg":
                    cartproduct=this_product_in_cart.last()
                    cartproduct.rate +=product_obj.selling_price
                    cartproduct.quantity+=0.25
                    cartproduct.count+=1
                    cartproduct.subtotal+=product_obj.selling_price/4
                    cartproduct.save()
                    cart_obj.total+=product_obj.selling_price/4
                    cart_obj.total_count+=1
                    cart_obj.save()
                else:
                    cartproduct=this_product_in_cart.last()
                    cartproduct.rate +=product_obj.selling_price
                    cartproduct.quantity+=1
                    cartproduct.count+=1
                    cartproduct.subtotal+=product_obj.selling_price
                    cartproduct.save()
                    cart_obj.total+=product_obj.selling_price
                    cart_obj.total_count+=1
                    
                    cart_obj.save()
            else:
                if product_obj.quantity_unit=="Kg":
                    cartproduct= CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.selling_price,quantity=0.25,count=1,subtotal=product_obj.selling_price/4)
                    cart_obj.total+=product_obj.selling_price/4
                    cart_obj.total_count+=cartproduct.count
                    cart_obj.save()
                else:
                    cartproduct= CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.selling_price,quantity=1,count=1,subtotal=product_obj.selling_price)
                    cart_obj.total+=product_obj.selling_price
                    cart_obj.total_count+=cartproduct.count
                    cart_obj.save()
        else:
            if product_obj.quantity_unit=="Kg":
                cart_obj=Cart.objects.create(total=0,total_count=0)
                self.request.session['cart_id']=cart_obj.id
                cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.selling_price,quantity=0.25,count=1,subtotal=product_obj.selling_price/4)
                cart_obj.total+=product_obj.selling_price/4
                cart_obj.total_count+=cartproduct.count
                cart_obj.save()
            else:
                cart_obj=Cart.objects.create(total=0,total_count=0)
                self.request.session['cart_id']=cart_obj.id
                cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.selling_price,quantity=1,count=1,subtotal=product_obj.selling_price)
                cart_obj.total+=product_obj.selling_price
                cart_obj.total_count+=cartproduct.count
                cart_obj.save()
        
        messages.success(request,"The item has been added to cart.")
        return redirect('fresh:home')

class SaveView(FreshMixin,View):
    success_url=reverse_lazy("fresh:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request,*args, **kwargs)
    def get (self,request,*args, **kwargs):
        
        #get product id from requested url
        url_slug =self.kwargs['slug']
        product_obj = Product.objects.get(slug=url_slug)
        this_product_in_savedlist=SavedProduct.objects.filter(product=product_obj)
        if this_product_in_savedlist:
            messages.warning(request,"The item already exits in the savelist.")
        else:    
            #get product
            SavedProduct.objects.create(product=product_obj,rate=product_obj.selling_price)       
            messages.info(request,"The item has been added to savelist.")
        return redirect('fresh:home')

class SavedListView(FreshMixin,TemplateView):
    template_name="save.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['count']=Notice.objects.all().count()
        #check if cart exit 
        
        #if cart_id exists
        
        saved= SavedProduct.objects.all().order_by("-id")
        context['saved']=saved
        return context

class ManageSavedView(FreshMixin,View):
    def get(self, request,*args, **kwargs):
        sv_id= self.kwargs['sv_id']
        action=request.GET.get("action")
        sv_obj=SavedProduct.objects.get(id=sv_id)        
        if action=="rmv":
            
            sv_obj.delete()

        else:
            pass
        return redirect ("fresh:savedlist")

class EmptySaveView(FreshMixin,View):
    def get(self,request,*args,**kwargs):
        saved=SavedProduct.objects.all()
        saved.delete()
        return redirect('fresh:savedlist')

class MyCartView(FreshMixin,TemplateView):
    template_name="mycart.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['count']=Notice.objects.all().count()
        #check if cart exit 
        cart_id=self.request.session.get("cart_id",None)
        #if cart_id exists
        if cart_id:
            cart= Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart
        return context

class ManageCartView(FreshMixin,View):
    def get(self, request,*args, **kwargs):
        cp_id= self.kwargs['cp_id']
        action=request.GET.get("action")
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart
        p_qnt_unit=cp_obj.product.quantity_unit
        
        print (cp_obj.product.id)
        
        if action=="inc":
            if p_qnt_unit=="Kg":
                cp_obj.quantity +=0.25
                cp_obj.count +=1
                cp_obj.subtotal +=cp_obj.rate/4
                cp_obj.save()
                cart_obj.total+=cp_obj.rate/4
                cart_obj.total_count+=1
                cart_obj.save()
            else:
                cp_obj.quantity +=1
                cp_obj.count +=1
                cp_obj.subtotal +=cp_obj.rate
                cp_obj.save()
                cart_obj.total+=cp_obj.rate
                cart_obj.total_count+=1
                cart_obj.save()


        elif action=="dcr":
            if p_qnt_unit=="Kg":
                cp_obj.quantity-=0.25
                cp_obj.count -=1
                cp_obj.subtotal-=cp_obj.rate/4
                cp_obj.save()
                cart_obj.total-=cp_obj.rate/4
                cart_obj.total_count-=1
                cart_obj.save()
                if cp_obj.quantity==0:
                    cp_obj.delete()
            else:
                cp_obj.quantity-=1
                cp_obj.count -=1
                cp_obj.subtotal-=cp_obj.rate
                cp_obj.save()
                cart_obj.total-=cp_obj.rate
                cart_obj.total_count-=1
                cart_obj.save()
                if cp_obj.quantity==0:
                    cp_obj.delete()
            
        elif action=="rmv":
            cart_obj.total-=cp_obj.subtotal
            cart_obj.total_count-=cp_obj.count
            cart_obj.save()
            cp_obj.delete()

        else:
            pass
        return redirect ("fresh:mycart")

class EmptyCartView(FreshMixin,View):
    def get(self,request,*args,**kwargs):
        cart_id=request.session.get("cart_id",None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.total_count=0
            cart.save()
        return redirect('fresh:mycart')

class CheckoutView(FreshMixin,CreateView):
    template_name="checkout.html"
    form_class=CheckOutForm
    success_url=reverse_lazy("fresh:message")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id",None)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")


        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
        else:
            cart_obj=None
        context['cart']=cart_obj
        return context

    
    def form_valid(self,form):
        cart_id=self.request.session.get("cart_id")
        if cart_id:
            cart_obj= Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            form.instance.subtotal=cart_obj.total
            form.instance.discount=0
            form.instance.total=cart_obj.total
            form.instance.order_status= "Order Received"            
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order=form.save()

        else:
            return redirect("fresh:home")
        return super().form_valid(form,)


class CustomerRegistrationView(CreateView):
    template_name="customerregistration.html"
    form_class=CustomerRegistrationForm
    success_url=reverse_lazy('fresh:home')

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        
        return context

    def form_valid(self,form):
        username= form.cleaned_data.get("username")
        password= form.cleaned_data.get("password")
        email =form.cleaned_data.get("email")
        user= User.objects.create_user(username,email,password)
        form.instance.user=user
        login(self.request,user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

    

class CustomerLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('fresh:home')
    
class CustomerLoginView(FormView):
    template_name="customerlogin.html"
    form_class=CustomerLoginForm
    success_url= reverse_lazy('fresh:home')

    def form_valid(self, form):
        uname= form.cleaned_data.get("username")
        pword= form.cleaned_data['password'] 
        usr= authenticate(username=uname, password=pword) 

        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request,usr)
        else:
            return render(self.request, self.template_name,{'form':self.form_class, "error":"Invalid Credential"})

        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        
        return context


    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class CustomerProfileView(FreshMixin,TemplateView):
    template_name="customerprofile.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/") 
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customer=self.request.user.customer
        context['customer'] = customer
        orders= Order.objects.filter(cart__customer=customer).order_by("-id") 
        context['orders'] =orders
        context['count']=Notice.objects.all().count()
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        return context

class MyPurchaseView(FreshMixin,TemplateView):
    template_name="purchase.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/purchase/") 
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customer=self.request.user.customer
        context['customer'] = customer
        orders= Order.objects.filter(cart__customer=customer).order_by("-id") 
        context['orders'] =orders
        context['count']=Notice.objects.all().count()
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        return context

class MessageView(FreshMixin,TemplateView):
    template_name="message.html"
    
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/message/") 
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customer=self.request.user.customer
        context['customer'] = customer
        orders= Order.objects.filter(cart__customer=customer).order_by("-id")
        context['orders'] =orders
        context['mcount']=Order.objects.all().count()
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        return context

class NotificationView(FreshMixin,TemplateView):
    template_name="notification.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/notification/") 
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        notification=Notice.objects.all().order_by("-id")
        context['notification'] =notification
        context['count']=Notice.objects.all().count()
        
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        return context
class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("fresh:customerprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['count']=Notice.objects.all().count()
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")

        return context

class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(
            Q(title__icontains=kw) | Q(description__icontains=kw))
        print(results)
        context["results"] = results
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        return context

class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email +\
            "/" + password_reset_token.make_token(user)+ "/"
        send_mail(
            'Password Reset Link | Freshmir Hut',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")

        return context

class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("fresh:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")

        return context

class SettingsView(UpdateView):
    model=User
    form_class=SettingsForm
    template_name="settings.html"
    success_url= reverse_lazy('fresh:customerprofile')

    def get_object(self):
        return self.request.user

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")

        return context

class ChangePasswordView(PasswordChangeView):
    model=User
    form_class=PasswordChangingForm
    template_name="change_password.html"
    success_url=reverse_lazy('fresh:settings')

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")

        return context

class UpdateProfileView(UpdateView):
    model=User
    form_class=UpdateProfileForm
    template_name="update_profile.html"
    success_url= reverse_lazy('fresh:customerprofile')

    def get_object(self):
        return self.request.user.customer

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        #footer
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")

        return context

class HelpCenterView(FreshMixin,TemplateView):
    template_name="help.html"

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['help'] =Help.objects.all().order_by("-id") 
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['notice']=Notice.objects.all().order_by("-id")[0]
        context['count']=Notice.objects.all().count()
        context['date'] =datetime.date.today().year
        context['updates'] =Update.objects.all()
        context['yhelp'] =YoutubeVideo.objects.all().order_by("-id") 
        

        return context   

class PrivacyView(FreshMixin,TemplateView):
    template_name="privacy.html"

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['notice']=Notice.objects.all().order_by("-id")[0]
        context['count']=Notice.objects.all().count()
        context['date'] =datetime.date.today().year
        context['updates'] =Update.objects.all() 
        

        return context 

class CareerView(FreshMixin,TemplateView):
    template_name= "career.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['careers'] =Career.objects.all().order_by("-id")
        context['bcontact']=BusinessContact.objects.all().order_by("id")
        context['btime']=BusinessTime.objects.all().order_by("id")
        context['notice']=Notice.objects.all().order_by("-id")[0]
        context['count']=Notice.objects.all().count()
        context['date'] =datetime.date.today().year
        context['updates'] =Update.objects.all() 
        

        return context


# Admin pages
   
class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("fresh:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data['password']
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)
     
class AdminHomeView(AdminRequiredMixin,TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(order_status="Order Received").order_by("-id")
        return context

class AdminOrderDetailView(AdminRequiredMixin,DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"

    

class AdminOrderStatuChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("fresh:adminorderdetail", kwargs={"pk": order_id}))


class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminproductlist.html"
    queryset = Product.objects.all().order_by("id")
    context_object_name = "allproducts"

class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("fresh:adminproductlist")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        return super().form_valid(form)



