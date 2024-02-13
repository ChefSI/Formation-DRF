from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail, BadHeaderError
from .forms import UserRegisterForm, ContactForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Article


# Create your views here.
def home(request):
    return render(request, 'home.html')

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, '', ['']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("/")
	form = ContactForm()
	return render(request, "contact.html", {'form':form})

@login_required
def articles(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles.html', context)

############### APIs ##################
from rest_framework import generics, permissions
from rest_framework import viewsets
from .serializers import ArticleSerializer, UserSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,) 
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
class UserViewSet(viewsets.ModelViewSet): 
	permission_classes = (permissions.IsAdminUser,) 
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer
