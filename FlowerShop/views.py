from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Customer

@login_required
def order_list(request):
    query = request.GET.get('q', '').strip()  # Получаем параметр q, убираем пробелы
    if query:
        customers = Customer.objects.filter(name__icontains=query)  # Фильтруем по имени (без учета регистра)
    else:
        customers = Customer.objects.all()  # Если запрос пустой, показываем всех

    return render(request, 'Flower_Shop/order_list.html', {'customers': customers})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Хешируем пароль
            user.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('order_list')  # Перенаправляем на страницу заказов
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})