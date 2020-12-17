from django.db import models

class Categorys(models.Model):
    category_name = models.CharField(max_length=50)
    category_image = models.ImageField(upload_to = 'category_image')

    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=50)
    subcategory_image = models.ImageField(upload_to = 'subcategory_image')
    categorys = models.ForeignKey(Categorys,on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to = 'product_image')
    product_price = models.IntegerField()
    product_desc = models.CharField(max_length=300)
    categorys = models.ForeignKey(Categorys,on_delete= models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Register(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'register'

class Cart(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product =  models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    

    class Meta:
        db_table = 'cart'


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    register = models.ForeignKey(Register,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    
    

class Address(models.Model):
    register = models.ForeignKey(Register,on_delete=models.CASCADE)
    contact = models.IntegerField()
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.IntegerField()

class OrderNumber(models.Model):
    
    order = models.ManyToManyField(Order)
    amount = models.IntegerField()
    date = models.DateTimeField()
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    register = models.ForeignKey(Register,on_delete=models.CASCADE)
