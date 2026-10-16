from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request,'index.html')
def register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name','').strip()
        last_name=request.POST.get('last_name','').strip()
        username=request.POST.get('username','').strip()
        email=request.POST.get('email','').strip()
        password=request.POST.get('password','')

        # Validate required fields
        if not username or not email or not password or not first_name or not last_name:
            messages.error(request, 'All fields are required. Please fill in every field.')
            return render(request,'register.html')

        # Validate password length
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request,'register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'An account with that username already exists. Please choose a different one.')
            return render(request,'register.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with that email address already exists. Try logging in instead.')
            return render(request,'register.html')

        try:
            user= User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('login')
        except Exception:
            messages.error(request, 'Something went wrong while creating your account. Please try again.')
            return render(request,'register.html')

    return render(request,'register.html')

def login_user(request):
    if request.method == 'POST':
        username=request.POST.get('username','').strip()
        password=request.POST.get('password','')

        # Validate required fields
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request,'login.html')

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'No account found with that username.')
            return render(request,'login.html')

        user= authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return render(request,'login.html')
    return render(request,'login.html')

from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Expense, Income
from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Expense, Income

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    today = timezone.localdate()

    # User's querysets
    user_expenses = Expense.objects.filter(user=request.user).order_by('-date')
    user_incomes = Income.objects.filter(user=request.user)

    # 1. Totals & Balance
    total_income = user_incomes.aggregate(total=Sum('amount'))['total'] or 0
    all_time_expense = user_expenses.aggregate(total=Sum('amount'))['total'] or 0
    balance_amount = total_income - all_time_expense

    # 2. Today's Expenses
    today_expenses = user_expenses.filter(date__date=today)
    todays_total = today_expenses.aggregate(total=Sum('amount'))['total'] or 0

    # 3. Current Calendar Week (Monday through Sunday)
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)          # Sunday
    week_expenses = user_expenses.filter(date__date__range=[start_of_week, today])
    weekly_total = week_expenses.aggregate(total=Sum('amount'))['total'] or 0

    # 4. Current Calendar Month (Full current month)
    month_expenses = user_expenses.filter(date__year=today.year, date__month=today.month)
    monthly_total = month_expenses.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'user': request.user,
        'expenses': user_expenses[:10],
        'total_income': total_income,
        'all_time_expense': all_time_expense,
        'balance_amount': balance_amount,
        
        # Today
        'todays_total': todays_total,
        'today_count': today_expenses.count(),
        
        # Current Week
        'weekly_total': weekly_total,
        'week_count': week_expenses.count(),
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        
        # Current Month
        'monthly_total': monthly_total,
        'month_count': month_expenses.count(),
        'current_month_name': today.strftime('%B'),
    }
    return render(request, 'home.html', context)
from django.shortcuts import render, redirect
from .forms import ExpenseForm,IncomeForm,LimitForm

def add_expense(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user 
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})
def add_income(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  
            income.save()
            return redirect('home')
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})
from django.shortcuts import render, redirect
from .forms import LimitForm
from .models import Limit  

def add_limit(request):
    if not request.user.is_authenticated:
        return redirect('login')


    limit_instance = Limit.objects.filter(user=request.user).first()

    if request.method == 'POST':
      
        form = LimitForm(request.POST, instance=limit_instance)
        if form.is_valid():
            limit = form.save(commit=False)
            limit.user = request.user
            limit.save()
            return redirect('home')
    else:
 
        form = LimitForm(instance=limit_instance)

    return render(request, 'add_limit.html', {'form': form})
def logout(request):
    request.session.flush()
    return redirect('login')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserProfileForm

def view_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'profile.html', {'user': request.user})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
def settings(request):
    return render(request,'settings.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from .models import Expense

def all_expenses(request):
    if not request.user.is_authenticated:
        return redirect('login')

    expenses = Expense.objects.filter(user=request.user)

    # 1. Amount Threshold Filter
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    if min_amount:
        try:
            expenses = expenses.filter(amount__gte=float(min_amount))
        except ValueError:
            pass
    if max_amount:
        try:
            expenses = expenses.filter(amount__lte=float(max_amount))
        except ValueError:
            pass

    # 2. Date Range Filters (Before / After)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        parsed_start = parse_date(start_date)
        if parsed_start:
            expenses = expenses.filter(date__date__gte=parsed_start)
    if end_date:
        parsed_end = parse_date(end_date)
        if parsed_end:
            expenses = expenses.filter(date__date__lte=parsed_end)

    # 3. Sorting Options
    # Options: date_desc (newest), date_asc (oldest), amount_desc (largest), amount_asc (smallest)
    sort_by = request.GET.get('sort', 'date_desc')
    sort_mapping = {
        'date_desc': '-date',
        'date_asc': 'date',
        'amount_desc': '-amount',
        'amount_asc': 'amount',
    }
    ordering = sort_mapping.get(sort_by, '-date')
    expenses = expenses.order_by(ordering)

    context = {
        'expenses': expenses,
        'min_amount': min_amount or '',
        'max_amount': max_amount or '',
        'start_date': start_date or '',
        'end_date': end_date or '',
        'sort_by': sort_by,
    }
    return render(request, 'all_expenses.html', context)

def edit_expense(request, expense_id):
    if not request.user.is_authenticated:
        return redirect('login')


    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('all_expenses')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {
        'form': form,
        'expense': expense,

    })


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Expense

def delete_expense(request, expense_id):
    if not request.user.is_authenticated:
        return redirect('login')


    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
    
    return redirect('all_expenses')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Income
from .forms import IncomeForm

def all_incomes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    incomes = Income.objects.filter(user=request.user).order_by('-id')
    return render(request, 'all_incomes.html', {'incomes': incomes})


def edit_income(request, income_id):
    if not request.user.is_authenticated:
        return redirect('login')

    income = get_object_or_404(Income, id=income_id, user=request.user)

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully.')
            return redirect('all_incomes')
    else:
        form = IncomeForm(instance=income)

    return render(request, 'edit_income.html', {
        'form': form,
        'income': income,
    })


def delete_income(request, income_id):
    if not request.user.is_authenticated:
        return redirect('login')

    income = get_object_or_404(Income, id=income_id, user=request.user)

    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income entry removed successfully.')

    return redirect('all_incomes')

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import defaultdict
from .models import Expense, Income
from django.shortcuts import render, redirect
from django.db.models import Sum
from collections import defaultdict
from datetime import date
from .models import Expense, Income

def monthly_reports(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_expenses = Expense.objects.filter(user=request.user)
    user_incomes = Income.objects.filter(user=request.user)

    # 1. Calculate All-Time Totals
    overall_income = user_incomes.aggregate(total=Sum('amount'))['total'] or 0
    overall_expense = user_expenses.aggregate(total=Sum('amount'))['total'] or 0
    overall_net = overall_income - overall_expense

    # 2. Group records by (year, month) tuple: (YYYY, MM)
    reports_map = defaultdict(lambda: {'income': 0, 'expense': 0})

    # Aggregate Incomes
    for inc in user_incomes:
        if inc.date:
            m_key = (inc.date.year, inc.date.month)
            reports_map[m_key]['income'] += inc.amount

    # Aggregate Expenses
    for exp in user_expenses:
        if exp.date:
            m_key = (exp.date.year, exp.date.month)
            reports_map[m_key]['expense'] += exp.amount

    # 3. Format rows sorted newest month first
    reports = []
    for (yr, mo) in sorted(reports_map.keys(), reverse=True):
        inc_val = reports_map[(yr, mo)]['income']
        exp_val = reports_map[(yr, mo)]['expense']
        net_val = inc_val - exp_val
        savings_rate = round((net_val / inc_val) * 100, 1) if inc_val > 0 else 0

        # Create a date object representing the 1st of that month
        month_obj = date(yr, mo, 1)

        reports.append({
            'month_label': month_obj.strftime('%B %Y'),
            'income': inc_val,
            'expense': exp_val,
            'net': net_val,
            'savings_rate': savings_rate,
        })

    context = {
        'reports': reports,
        'overall_income': overall_income,
        'overall_expense': overall_expense,
        'overall_net': overall_net,
    }
    return render(request, 'monthly_reports.html', context)