from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from polls.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name=''),
    path('my_login/', my_login, name='my_login'),
    path('signup/', signup, name='signup'),
    path('log_out/', log_out, name='log_out'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('user_profile/', user_profile, name='user_profile'),
    path('active-sessions/', active_sessions_count, name='active_sessions_count'),



    path('select-group/', select_group, name='select_group'),
    path('add_bok/', add_bok, name='add_bok'),
    path('remove-user-from-group/', remove_user_from_group, name='remove_user_from_group'),


    path('create_branch/', create_branch, name='create_branch'),
    path('Branchview/', Branchview, name='Branchview'),
    path('Branch_update/<int:id>/', Branch_update, name='Branch_update'),
    path('Branch_remove/<int:id>/', Branch_remove, name='Branch_remove'),




    path('employee_view', employee_view, name='employee_view'),
    path('employee_update/<int:id>/', employee_update, name='employee_update'),
    path('employee_delete/<int:id>/', employee_delete, name='employee_delete'),


    path('send_notification/<str:room_name>/', send_notification, name='send_notification'),


    path('view_notifications/', view_notifications, name='view_notifications'),
    path('task_assign/', task_assign, name='task_assign'),
    path('create_task/', create_task, name='create_task'),
    path('vew_task_ass/', vew_task_ass, name='vew_task_ass'),



    path('create_acc/', create_acc, name='create_acc'),
    path('Account_view/', Account_view, name='Account_view'),
    path('Transaction_creation/', Transaction_creation, name='Transaction_creation'),
    path('Per_Account/', Per_Account, name='Per_Account'),




    path('Create_loan/', Create_loan, name='Create_loan'),
    path('create_collateral/', create_collateral, name='create_collateral'),
    path('Loan_managment/', Loan_managment, name='Loan_managment'),
    path('loan_payment/', loan_payment, name='loan_payment'),
    path('per_loan/', per_loan, name='per_loan'),



    path('History_log/', History_log, name='History_log'),
    path('branch_log/', branch_log, name='branch_log'),
    path('employee_log/', employee_log, name='employee_log'),
    path('loan_log/', loan_log, name='loan_log'),
    path('task_log/', task_log, name='task_log'),
    path('account_log/', account_log, name='account_log'),
    path('transaction_log/', transaction_log, name='transaction_log'),
    path('loan_payment_log/', loan_payment_log, name='loan_payment_log'),




    path('save_pdf_to_local/', save_pdf_to_local, name='save_pdf_to_local'),



    path('assign_employee/', assign_employee, name='assign_employee'),
    path('temp_employee/', temp_employee, name='temp_employee'),
    path('view_temp_employee_list/', view_temp_employee_list, name='view_temp_employee_list'),
    path('remove_temp_emp/<int:id>/', remove_temp_emp, name='remove_temp_emp'),
    path('approve-temp-employee/<int:pk>/', approve_temp_employee, name='approve_temp_employee'),


    path("__reload__/", include("django_browser_reload.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
