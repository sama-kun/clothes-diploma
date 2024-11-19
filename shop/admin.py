from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'profile_pic', 'gender']
    radio_fields = {'gender': admin.VERTICAL}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'category', 'price', 'tag', 'product_img']
    list_filter = ['price', 'category', 'tag']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'qty', 'price', 'amount']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'first_name', 'last_name','house_no', 'street', 'city', 'pin', 'state', 'total', 'placed_at']

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order','user' , 'product', 'price', 'qty', 'amount', 'status']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Size)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'position', 'start_date', 'end_date', 'salary', 'is_active')
    list_filter = ('position', 'is_active', 'start_date', 'end_date')
    search_fields = ('user__first_name', 'user__last_name', 'position')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.admin_order_field = 'user__first_name'  # Allows column order sorting
    get_full_name.short_description = 'Full Name'  # Renames column head

admin.site.register(Employee, EmployeeAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'type', 'description')
    list_filter = ('date', 'type')
    search_fields = ('description', 'type')

admin.site.register(Expense, ExpenseAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'total_income', 'total_expense', 'net_profit')
    list_filter = ('type', 'date')
    search_fields = ('type',)

admin.site.register(Report, ReportAdmin)
