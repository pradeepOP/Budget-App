from django.shortcuts import render, redirect
from .models import Category, Transaction
from .forms import TransactionForm, signUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from collections import defaultdict
# Create your views here.


def calculate_total_budget(request):
    income_transaction = Transaction.objects.filter(
        user=request.user, is_income=True)
    total_income = sum(
        transaction.amount for transaction in income_transaction)

    expense_transaction = Transaction.objects.filter(
        user=request.user, is_income=False)

    total_expense = sum(
        transaction.amount for transaction in expense_transaction)

    total_budget = total_income - total_expense

    return total_budget


@login_required(login_url='login')
def index(request):
    form = TransactionForm()
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('index')

        else:
            form = TransactionForm()

    q = request.GET.get('q', '')
    categories = Category.objects.all()

    transactions = Transaction.objects.filter(
        user=request.user, category__name__icontains=q)[:3]

    budget = calculate_total_budget(request)

    context = {"categories": categories,
               "transactions": transactions, "form": form, "budget": budget}
    return render(request, "core/index.html", context)


@login_required(login_url='login')
def delete_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('index')

    context = {"transaction": transaction}
    return render(request, "core/delete_transaction.html", context)


def loginView(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'username does not exist')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'username or password incorrect')

    return render(request, 'core/login.html')


def signupView(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = signUpForm()
    if request.method == "POST":
        form = signUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            form = signUpForm()

    context = {"form": form}
    return render(request, 'core/signup.html', context)


@login_required(login_url='login')
def logoutView(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, 'core/logout.html')


def transactionView(request):

    transactions = Transaction.objects.filter(user=request.user)

    # transactions_by_day = defaultdict(list)
    # for transaction in transactions:
    #     transactions_by_day[transaction.created_at].append(transaction)

    # print(transactions_by_day)

    context = {"transactions": transactions}
    return render(request, 'core/transactions.html', context)
