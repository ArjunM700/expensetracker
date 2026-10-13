from .import views
from django.urls import path

urlpatterns =[
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login_user,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('add_expense/',views.add_expense,name='add_expense'),
    path('add_income/',views.add_income,name='add_income'),
    path('add_limit/',views.add_limit,name='add_limit'),
    path('settings/',views.settings,name='settings'),
    path('expenses/', views.all_expenses, name='all_expenses'),
    path('expenses/<int:expense_id>/edit/', views.edit_expense, name='edit_expense'),
    path('profile/', views.view_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('expenses/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
    path('incomes/', views.all_incomes, name='all_incomes'),
    path('incomes/<int:income_id>/edit/', views.edit_income, name='edit_income'),
    path('incomes/<int:income_id>/delete/', views.delete_income, name='delete_income'),
    path('reports/monthly/', views.monthly_reports, name='monthly_reports'),
]