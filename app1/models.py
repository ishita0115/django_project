from django.db import models

class Category(models.Model):
    categoryname=models.CharField(max_length=200)
    img=models.ImageField(upload_to='category')


    def __str__(self):
        return self.categoryname

class Product(models.Model):
        Category=models.ForeignKey(Category, on_delete=models.CASCADE)
        name=models.CharField(max_length=200)
        img=models.ImageField(upload_to='product')
        price = models.IntegerField()
        description= models.TextField()
        quantity=models.IntegerField()

        def __str__(self):
            return self.name

        def average_rating(self):
            reviews = self.reviews.all()
            if reviews:
                return round(sum(r.rating for r in reviews) / len(reviews), 1)
            return 0


class UserRegister(models.Model):
    name=models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    address= models.CharField(max_length=200)
    phone= models.IntegerField()

class Contactus(models.Model):
    name=models.CharField(max_length=200)
    email = models.EmailField()
    phone= models.IntegerField()
    message=models.TextField()

class Ordermodel(models.Model):
    productid=models.CharField(max_length=200 ,default="0")
    productqty=models.CharField(max_length=200,default="0")
    userId = models.CharField(max_length=200)
    userName = models.CharField(max_length=200)
    userEmail = models.EmailField()
    userContact = models.IntegerField()
    address = models.CharField(max_length=200)
    orderAmount = models.IntegerField()
    paymentMethod = models.CharField(max_length=200)
    transactionId = models.CharField(max_length=200)
    orderDate = models.DateTimeField(auto_created=True,auto_now=True)

    def __str__(self) :
        return self.userName


class Cart(models.Model):
    user_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user_email} - {self.product.name}"


class Wishlist(models.Model):
    user_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_email', 'product')

    def __str__(self):
        return f"{self.user_email} - {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_email = models.EmailField()
    user_name = models.CharField(max_length=200)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_email', 'product')

    def __str__(self):
        return f"{self.user_name} - {self.product.name} ({self.rating}/5)"



