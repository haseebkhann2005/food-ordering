from django.db import models
import uuid
from django.contrib.auth.models import User
from faker import Faker
import random
from django.core.exceptions import ValidationError

fake = Faker()

def generate_unique_slug(slug_base):
    """Generate a unique slug by appending a random number."""
    while True:
        slug = f"{slug_base}-{random.randint(1, 10000)}"
        if not product.objects.filter(pr_slug=slug).exists():
            return slug

def fake_pr(n=100) -> None:
    for _ in range(n):
        # Generate fake data for the product
        pr_name = fake.word()
        pr_desc = fake.text(max_nb_chars=200)
        pr_price = random.randint(100, 2000)
        pr_demo_price = random.randint(100, 2000)
        stock = random.randint(0, 30)
        available = fake.boolean()
        pr_slug_base = random.choice(['appetizers', 'desserts', 'main'])
        pr_slug = generate_unique_slug(pr_slug_base)
        
        # Create and save a product instance
        product_instance = product.objects.create(
            pr_name=pr_name,
            pr_slug=pr_slug,
            pr_desc=pr_desc,
            pr_price=pr_price,
            pr_demo_price=pr_demo_price,
            stock=stock,
            available=available
        )
        
        # Generate and save a productmetafield instance
        pr_measuring = random.choice(["kg", "ml", "L", None])
        pr_quantity = str(random.randint(1, 100)) if pr_measuring else None
        is_restrict = fake.boolean()
        restricted_quantity = random.randint(0, 10) if is_restrict else 0
        
        productmetafield.objects.create(
            product=product_instance,
            pr_measuring=pr_measuring,
            pr_quantity=pr_quantity,
            is_restrict=is_restrict,
            restricted_quantity=restricted_quantity
        )
        
        # Generate and save a product_images instance
        product_images.objects.create(
            product=product_instance,
            pr_images=fake.image_url()  # You may want to replace this with a valid image file path or URL
        )

# Django Models

class basefield(models.Model):
    pr_uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class product(basefield):
    pr_name = models.CharField(max_length=100)
    pr_slug = models.SlugField(unique=True)
    pr_desc = models.TextField()
    pr_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pr_demo_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

class productmetafield(models.Model):
    product = models.OneToOneField(product, related_name="meta_field", on_delete=models.CASCADE)
    pr_measuring = models.CharField(max_length=100, null=True, blank=True, choices=[("kg", "kg"), ("ml", "ml"), ("L", "L"), (None, None)])
    pr_quantity = models.CharField(max_length=100, null=True, blank=True)
    is_restrict = models.BooleanField(default=False)
    restricted_quantity = models.IntegerField(default=0)

class product_images(basefield):
    product = models.ForeignKey(product, related_name="images", on_delete=models.CASCADE)
    pr_images = models.ImageField(upload_to="products")


class user(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
class addmeal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False,blank=False)
    cattegory = models.CharField(max_length=50)
    image = models.ImageField(upload_to="image")
    
class Review(models.Model):
    name = models.CharField(max_length=255)
    review_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)  # Rating from 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} Stars"
    
class Email_m(models.Model):
    em_subject = models.CharField(max_length=100)
    em_message = models.TextField()
    em_file  = models.FileField()
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    excerpt = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title