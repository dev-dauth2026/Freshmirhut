from django.urls import path
from .views import *

app_name="fresh"
urlpatterns=[
    path('',HomeView.as_view(), name ='home'),
    path('about/',AboutView.as_view(), name="about"),
    path('service/',ServiceView.as_view(), name="service"),
    path('contact-us/',ContactView.as_view(), name="contact"),
    path("product/<slug:slug>",ProductDetailsView.as_view(), name="productdetails"),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("save-<slug:slug>/", SaveView.as_view(), name="save"),
    path("savedlist/", SavedListView.as_view(), name="savedlist"),
    path("my-cart/",MyCartView.as_view(), name="mycart"),
    path('manage-cart/<int:cp_id>',ManageCartView.as_view(),name="managecart"),
    path('manage-save/<int:sv_id>',ManageSavedView.as_view(),name="managesave"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    path("empty-save/", EmptySaveView.as_view(), name="emptysave"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("register/",CustomerRegistrationView.as_view(), name="customerregistration"),
    path("logout/",CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/",CustomerLoginView.as_view(), name="customerlogin"),
    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("password/", ChangePasswordView.as_view(), name="changepassword"),
    path("update-profile", UpdateProfileView.as_view(), name="updateprofile"),
    path("purchase/", MyPurchaseView.as_view(), name="mypurchase"),
    path("notification/", NotificationView.as_view(), name="notification"),
    path("message/", MessageView.as_view(), name="message"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
    path("search/", SearchView.as_view(), name="search"),
    path("forgot-password/", PasswordForgotView.as_view(), name="passworforgot"),
    path("password-reset/<email>/<token>/",PasswordResetView.as_view(), name="passwordreset"),
    path("help-center/",HelpCenterView.as_view(), name="help"),
    path("privacy/",PrivacyView.as_view(), name="privacy"),
    path("career/",CareerView.as_view(), name="career"),
    
    




    #Admin Panel
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(),name="adminorderdetail"),
    path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),
    path("admin-order-<int:pk>-change/",AdminOrderStatuChangeView.as_view(), name="adminorderstatuschange"),
    path("admin-product/list/", AdminProductListView.as_view(),name="adminproductlist"),
    path("admin-product/add/", AdminProductCreateView.as_view(),name="adminproductcreate"),


]