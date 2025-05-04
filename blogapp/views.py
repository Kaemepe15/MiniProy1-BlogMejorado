from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages




class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'

#Al colocar LoginRequiredMixin en las siguientes clases nos aseguramos de la seguridad por autenticación 
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})



class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})

#Generando una Vista para registrar usuario y guardar. Javier A

def register(request):
    if request.method == 'POST': #verifica si la solicitud es con un formulario enviado sino return
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  #esto crea el usuario
            login(request, user) #inicia la sesión automaticamente luego del registro
            messages.success(request, f'Gracias, {user.username}, por crear tu cuenta con nosotros. ¡bienvenido!')
            return redirect('blogapp:blog_list') #envia al usuario a la pag principal
        else:
            messages.error(request, 'Error en el formulario, por favor corregir para continuar')
    else:
        form = UserCreationForm()
    return render(request, 'blogapp/signup.html', {'form': form})   #muestra el formulario vacio

#Vista para inicio de sesion

def user_login(request):
    if request.method == 'POST': #lo mismo que register, verificar form, sino return de formulario vacio
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user)
                messages.success(request, f'Que bueno que volviste {user.username}')
                return redirect('blogapp:blog_list')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor corregir los posibles errores en el formulario')
    else:
        form = AuthenticationForm()
    return render(request, 'blogapp/login.html', {'form': form})

#Vista para Logout 

def user_logout(request):
    logout(request)
    messages.success(request, 'cierre de sesión exitoso')
    return redirect('blogapp:blog_list')
