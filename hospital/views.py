from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Avg

from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMessage, send_mail

from .models import *
from .forms import *
from .decorators import *

def home(request):
    context = {
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
    }
    return render(request, 'hospital/home.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'hospital/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {} 
    return render(request, 'hospital/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

"""
@login_required(login_url='login')
@admin_only
def home(request):
    context = {
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
    }
    return render(request, 'hospital/index.html', context)
"""

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def patient_list(request):
    patients = Patient.objects.all()
    context = {
        'patients': patients, 
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
    }
    return render(request, 'hospital/patient_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def add_patient(request):
    if request.user.groups.filter(name='doctor').exists():
        appointments = Appointment.objects.filter(doctor__user=request.user)
        context = {
            'appointments': appointments,
            'is_doctor': request.user.groups.filter(name='doctor').exists(),
            'is_patient': request.user.groups.filter(name='patient').exists(),
        }
        return render(request, 'hospital/add_patient.html', context)
    else:
        return redirect('home')

# Appointments
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def patient_appointment(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.created_by = request.user
            appointment.save()
            return redirect('home')
    else:
        form = PatientAppointmentForm()
    context = {
        'form': form, 
        'doctors': doctors,
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
    }
    return render(request, 'hospital/patient_appointment.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def accountSettings(request):
	patient = request.user.patient
	form = PatientForm(instance=patient)

	if request.method == 'POST':
		form = PatientForm(request.POST, request.FILES,instance=patient)
		if form.is_valid():
			form.save()

	context = {
        'form': form,
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
    }
	return render(request, 'hospital/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def update_appointment_status(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        new_status = request.POST.get('status')
        appointment.status = new_status
        appointment.save()
        messages.success(request, 'Appointment status updated successfully!')
        return redirect('add_patient')

    return render(request, 'hospital/add_patient.html')

def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                f'Contact Form Submission from {name}',
                message,
                email,
                ['info@hospitalmanagement.com'], 
                fail_silently=False,
            )
            
            return render(request, 'hospital/contact.html', {
                'form': form,
                'success_message': 'Thank you for contacting us! We will get back to you soon.'
            })
    else:
        form = ContactForm()
    context = {
        'form': form,
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
    }
    return render(request, 'hospital/contact.html', context)

def reviews_page(request):
    reviews = Review.objects.all()
    form = ReviewForm()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    context = {
        'reviews': reviews, 
        'form': form,
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
        'average_rating': average_rating,
        }
    return render(request, 'hospital/reviews.html', context)

def blog_list(request):
    posts = BlogPost.objects.all()
    context = {
        'posts': posts,
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
    }
    return render(request, 'hospital/blog_list.html', context)

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('blog_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
        'is_patient': request.user.groups.filter(name='patient').exists(),
    }
    return render(request, 'hospital/blog_detail.html', context)

@login_required
@allowed_users(allowed_roles=['doctor', 'admin'])
def new_post(request):
    if request.user.is_staff or request.user.groups.filter(name='doctor').exists():
        if request.method == 'POST':
            form = BlogPostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                return redirect('blog_list')
        else:
            form = BlogPostForm()
        context = {
            'form': form,
            'is_doctor': request.user.groups.filter(name='doctor').exists(),
            'is_patient': request.user.groups.filter(name='patient').exists(),
        }
        return render(request, 'hospital/new_post.html', context)
    else:
        return redirect('blog_list')