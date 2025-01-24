from decimal import Decimal

from django.shortcuts import render, redirect
from .models import Car, Order
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входит после регистрации
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    cars_list = Car.objects.all()
    paginator = Paginator(cars_list, 10)  # Показывать 10 машин на странице
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    return render(request, 'home.html', {'cars': cars})

def car_detail(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'car_detail.html', {'car': car})


@login_required
def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart_items = Car.objects.filter(id__in=request.session['cart'])
    total_price = sum(car.price for car in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



@login_required
def add_to_cart(request, car_id):
    if 'cart' not in request.session:
        request.session['cart'] = []
    if car_id not in request.session['cart']:
        request.session['cart'].append(car_id)
        request.session.modified = True
    return redirect('cart')


@login_required
def remove_from_cart(request, car_id):
    if 'cart' in request.session:
        request.session['cart'] = [item for item in request.session['cart'] if item != car_id]
        request.session.modified = True
    return redirect('cart')


@login_required
def checkout(request):
    if request.method == 'POST':
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            total_price=Decimal('0.00')  # Заглушка, пока не считаем общую стоимость
        )
        # Добавляем машины из корзины в заказ
        cart_items = Car.objects.filter(id__in=request.session.get('cart', []))
        for car in cart_items:
            order.cars.add(car)
            order.total_price += car.price
        order.save()
        # Очищаем корзину
        request.session['cart'] = []
        # Перенаправляем на страницу подтверждения оплаты
        return redirect('payment_confirmation')

    # Если метод GET, просто отображаем страницу оформления заказа
    cart_items = Car.objects.filter(id__in=request.session.get('cart', []))
    total_price = sum(car.price for car in cart_items)
    return render(request, 'checkout.html', {'total_price': total_price})


@login_required
def payment_confirmation(request):
    return render(request, 'payment_confirmation.html')
