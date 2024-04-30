from sqladmin import Admin, ModelView

from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order
from models.order_product_association import order_product_association_table




class UserAdmin(ModelView, model=User):
    column_list = ['id', 'username', 'email', 'first_name', 'last_name', 'is_verified']
    column_labels = {
        'id': 'ID',
        'username': 'Username',
        'email': 'Email',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'is_verified': 'Verified'
    }
class ProductAdmin(ModelView, model=Product):
    column_list = ['id', 'name', 'description', 'price', 'quantity', 'picture', 'created_at', 'update_time']
    column_labels = {
        'id': 'ID',
        'name': 'Name',
        'description': 'Description',
        'price': 'Price',
        'quantity': 'Quantity',
        'picture': 'Picture',
        'created_at': 'Created At',
        'update_time': 'Update Time'
    }

class CategoryAdmin(ModelView,model =Category):
    column_list = ['id', 'name']
    column_labels = {
        'id':'ID',
        'name':'Name',
    }