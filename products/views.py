from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from products.models import *
from products.utils import *
import os
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def contact(request):
    if request.method == "POST":
        data = request.POST
        e_subject = data.get("subject")
        e_message = data.get("message")
        e_recipient_list = ["rookiehaseeb2005@gmail.com"]
        e_file = request.FILES.get("file")

        if e_subject and e_message and e_file:
            # Save the file temporarily
            file_name = e_file.name
            temp_file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with default_storage.open(temp_file_path, 'wb+') as destination:
                for chunk in e_file.chunks():
                    destination.write(chunk)

            # Save email details to the database
            email_instance = Email_m(
                em_subject=e_subject,
                em_message=e_message,
                em_file=file_name
            )
            email_instance.save()

            # Send the email
            send_email_attachment(
                subject=e_subject,
                message=e_message,
                recipient_list=e_recipient_list,
                file_path=temp_file_path
            )

            # Clean up the temporary file
            os.remove(temp_file_path)
            print(f"Subject: {e_subject}, Message: {e_message}, File: {e_file}")

            return redirect('/contact/')
        else:
            return HttpResponse("Invalid input. Please ensure all fields are filled.")
    return render(request, 'contact.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def purchase_item(request, product_id):
    try:
        product_instance = get_object_or_404(product, pk=product_id)  # Use the product model class here
        print(f'Fetched product: {product_instance.pr_name}')  # Debugging line
    except Exception as e:
        print(f'Error: {e}')  # Debugging line
        raise

    if product_instance.available and product_instance.stock > 0:
        messages.success(request, f'{product_instance.pr_name} has been added to your cart.')
    else:
        messages.error(request, f'{product_instance.pr_name} is not available for purchase.')
    
    return redirect('menu')

@login_required


def menu(request):
    products = product.objects.prefetch_related('meta_field', 'images').all()

    # Handle search query
    search_query = request.GET.get('search')
    if search_query:
        print(search_query)
        products = products.filter(pr_name__istartswith=search_query)

    # Group products by category (after filtering by search)
    appetizers = products.filter(pr_slug__icontains='appetizer')
    main = products.filter(pr_slug__icontains='main')
    desserts = products.filter(pr_slug__icontains='dessert')

    # Debugging
    print("Appetizers:", appetizers)
    print("Main:", main)
    print("Desserts:", desserts)

    context = {
        'appetizers': appetizers,
        'main_courses': main,
        'desserts': desserts,
        'search_results': products if search_query else None,  # Pass search results to the template if search is performed
    }
    
    return render(request, 'menu.html', context)


@login_required
def blog(request):
    if request.method =="POST":
        data = request.POST
        m_name = data.get('title')
        m_desc = data.get('content')
        m_excerpt = data.get('excerpt')
        m_image = request.FILES.get('image')
        BlogPost.objects.create(
            title=m_name,
            content=m_desc,
            excerpt=m_excerpt,
            image=m_image
        )
        return render(request, 'success.html')
    return render(request, 'blog.html')

@login_required
def h_tips(request):
    return render(request, 'health-tips.html')

@login_required
def top5(request):
    return render(request, 'top-5.html')

@login_required
def guide(request):
    return render(request, 'guide.html')


@login_required


def reviews(request):
    if request.method == "POST":
        data = request.POST
        m_review = data.get('review')
        m_rating = data.get('rating')

        # Get the logged-in user's name
        user_name = request.user.get_full_name() or request.user.username
        
        Review.objects.create(
            name=user_name,
            review_text=m_review,
            rating=m_rating
        )
        return redirect('/reviews/')

    queryset = Review.objects.all()
    average_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    context = {
        "reviews": queryset,
        "average_rating": average_rating
    }
    return render(request, 'reviews.html', context=context)

@login_required
def add_meal(request):
    if request.method =="POST":
        data = request.POST
        m_name = data.get('name')
        m_desc = data.get('description')
        m_catg = data.get('category')
        m_image = request.FILES.get('image')
        addmeal.objects.create(
            name=m_name,
            description=m_desc,
            cattegory=m_catg,
            image=m_image
        )
        return redirect('/add-meal/')
    queryset = addmeal.objects.all()
    return render(request, 'add.html', context={"queryset": queryset})

@login_required
def delete_meal(request, id):
    queryset = addmeal.objects.get(id=id)
    queryset.delete()
    return redirect('/add-meal/')

def p_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Invalid username')
            return redirect('/login')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, 'Invalid credentials')
            return redirect('/login')
        
        login(request, user)
        
        # Clear the forced re-login flag
        if 'forced_relogin' in request.session:
            del request.session['forced_relogin']
        
        return redirect('/')
    
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    request.session.flush()  # This will clear the session data
    request.session['forced_relogin'] = True  # Set flag for forced re-login
    return redirect('/login')

def p_register(request):
    if request.method == "POST":
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
         # Render the email template with context
        subject = '🎉 Welcome to Our Wonderful Community! 🎉'
        from_email = 'your_email@example.com'
        to_email = email
        context = {
            'first_name': first_name,
        }
        html_message = render_to_string('email_templates/welcome_email.html', context)

        # Send the welcome email
        email = EmailMessage(subject, html_message, from_email, [to_email])
        email.content_subtype = 'html'  # Important to set this
        email.send(fail_silently=False)


        messages.info(request, 'Account created successfully')
        
        return redirect('/register/')
    return render(request, 'register.html')
