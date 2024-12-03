from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.models import User, Permission, Group
from django.db.models.functions import TruncMinute, Cast
from django.utils.dateformat import DateFormat
from django.db.models import Count
from django.db.models import Sum, F, FloatField
from polls.forms import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required, login_required
from .models import *
from django.utils.timezone import now, timedelta
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db.models.functions import TruncDate
from collections import Counter
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_protect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from .filters import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os



################################################ group 



# view group 
@user_passes_test(lambda u: u.is_superuser) 
def select_group(request):
    # Get all groups
    groups = Group.objects.all()
    selected_group = None
    users = []
    labels = []
    data = []

    if request.method == 'POST':
        group_id = request.POST.get('group')
        if group_id and group_id != '':
            selected_group = Group.objects.get(id=group_id)
            users = selected_group.user_set.all()
            labels.append(selected_group.name)
            data.append(selected_group.user_set.count())
        else:
            for group in groups:
                labels.append(group.name)
                data.append(group.user_set.count())
    else:
        for group in groups:
            labels.append(group.name)
            data.append(group.user_set.count())

    return render(request, 'select_group.html', {
        'groups': groups,
        'labels': labels,
        'data': data,
        'selected_group': selected_group,
        'users': users,
        
    })


# assign employee 

@user_passes_test(lambda u: u.is_superuser)  # Only allow superusers to access this view
def assign_employee(request):
    if request.method == 'POST':
        form = UserGroupAssignmentForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            group = form.cleaned_data['group'] 
            user.groups.add(group)
            return redirect('select_group')  # Redirect to a success page or another relevant view
    else:
        form = UserGroupAssignmentForm()

    return render(request, 'assign_employee.html', {'form': form})





# remove user from a group

 
@user_passes_test(lambda u: u.is_superuser) 
def remove_user_from_group(request):
    groups = Group.objects.all()
    selected_group = None
    users = []
    message = ''

    if request.method == 'POST':
        group_id = request.POST.get('group')
        user_id = request.POST.get('user')

        if group_id:
            selected_group = Group.objects.get(id=group_id)
            users = selected_group.user_set.all()

        if group_id and user_id:
            try:
                group = Group.objects.get(id=group_id)
                user = User.objects.get(id=user_id)
                group.user_set.remove(user)
                message = f'User {user.username} has been removed from group {group.name}.'
            except Group.DoesNotExist:
                message = 'Selected group does not exist.'
            except User.DoesNotExist:
                message = 'Selected user does not exist.'

    return render(request, 'remove_user_from_group.html', {
        'groups': groups,
        'selected_group': selected_group,
        'users': users,
        'message': message,
    })



############################################################## Autentication 

# active user real time 

def active_sessions_count(request):
    # Get the current time
    now = timezone.now()

    # Get all active sessions
    active_sessions = Session.objects.filter(expire_date__gte=now)

    # Only count sessions with an authenticated user
    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')  # Only authenticated users have _auth_user_id
        if user_id and user_id not in user_ids:
            user_ids.append(user_id)

    # Count unique authenticated users with active sessions
    active_users_count = len(user_ids)

    return JsonResponse({'active_users': active_users_count})



# signup page

def signup(request):
    form = creatuserform()
    
    if request.method == 'POST':
        form =creatuserform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_login')
        
    cont = {'reg': form}


    return render(request, 'signup.html', cont)


# login page


def my_login(request):
    form = log()
    if request.method == 'POST':
        form = log(request, data=request.POST)
        if form.is_valid():
            username= request.POST.get('username')
            password= request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('')
    conte = {'log': form}
    return render(request, 'Login.html', conte)



# log out


def log_out(request):
    auth.logout(request)
    return redirect('my_login')


# user profile 

def user_profile(request):
    # Check if the user has a UserProfile
    try:
        profile = request.user.userprofile  # Try to access the UserProfile
    except UserProfile.DoesNotExist:
        profile = None  # If no UserProfile exists, set profile to None

    if request.method == 'POST':
        # If profile exists, use it; if not, handle it gracefully
        if profile:
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = UserProfileForm(request.POST, request.FILES)  # Creating a new profile

        if form.is_valid():
            # Save the form, creating or updating the profile
            user_profile = form.save(commit=False)
            user_profile.user = request.user  # Link the profile to the user
            user_profile.save()
            return redirect('')  # Redirect to the profile page

    else:
        # Handle the GET request, either load the profile or show an empty form
        if profile:
            form = UserProfileForm(instance=profile)
        else:
            form = UserProfileForm()

    return render(request, 'user_profile.html', {'form': form})

# remove user 

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    if not request.method == 'POST':
        return redirect('')  # Redirect to a different view if not a POST request
    
    # Get the user object or return a 404 error if not found
    user = get_object_or_404(User, id=user_id)
    
    # Delete the user
    user.delete()
    
    # Redirect to a success page or another view
    return redirect('')  # Redirect to a list of users or another relevant page


################################################# view home 

@login_required(login_url="my_login")
def home(request):
    user = request.user
    group = Group.objects.all()
    logs = LogEntry.objects.filter(content_type__model='employee')
    view_taskassi = TaskAssignment.objects.all()
    task_assignment_filter = TaskAssignmentFilter(request.GET, queryset=view_taskassi)
    view_all_taskassi = TaskAssignment.objects.first()
    pending_tasks = Task.objects.filter(status='Pending') 
    completed_tasks = Task.objects.filter(status='Completed')
    all_tasks = Task.objects.all()
    task_filter = TaskFilter(request.GET, queryset=all_tasks)
    user_filters = UserFilter(request.GET, queryset=User.objects.all())
    active_user_count = User.objects.filter(is_active=True).count()
    total_employees = Employee.objects.count()
    total_position_emp = Employee.objects.values('position').distinct().count()
    total_department_emp = Employee.objects.values('department').distinct().count()
    position_data = Employee.objects.values('position').annotate(total=Count('position'))
    department_data = Employee.objects.values('department').annotate(total=Count('department'))
    temp_employee_data = TempEmployee.objects.values('date_of_hire').annotate(total=Count('employee_id')).order_by('date_of_hire')
    branch_data = Employee.objects.values('branch__branch_name').annotate(total_employees=Count('employee_id')).order_by('branch__branch_name')
    total_branch = Branch.objects.count()
    total_account = Account.objects.count()
    total_trans = Transaction.objects.count()
    total_fixed = Account.objects.filter(account_type='Fixed Deposit').count()
    total_saving = Account.objects.filter(account_type='Savings').count()
    total_cheking = Account.objects.filter(account_type='Checking').count()
    account_type_counts = Account.objects.values('account_type').annotate(count=Count('account_type'))
    account_labels = [account_type['account_type'] for account_type in account_type_counts]
    account_data = [account_type['count'] for account_type in account_type_counts]
    try:
       # Aggregate the total balance for accounts related to the user
       account = Account.objects.filter(user=user)
       Account_amount = account.aggregate(Sum('balance'))['balance__sum'] or 0
       account_ids = account.values_list('account_id', flat=True)

        # Total transactions for this user
       trans = Transaction.objects.filter(Q(to_account_id__in=account_ids) | Q(form_account_id__in=account_ids))
        

        # Calculate the total amount per transaction type
       total_deposit = trans.filter(transaction_type='Deposit').aggregate(Sum('amount'))['amount__sum'] or 0
       total_withdrawal = trans.filter(transaction_type='Withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0
       total_transfer = trans.filter(transaction_type='Transfer').aggregate(Sum('amount'))['amount__sum'] or 0


       total_transactions = total_deposit + total_withdrawal + total_transfer

       data = []
       label = []
       for acc in account:
            data.append(float(acc.balance))
            label.append(acc.account_type)
       
       # Try to get the loan associated with the user
       loan_amount = Loan.objects.get(user=user)  
    except (Account.DoesNotExist, Loan.DoesNotExist):
       # Handle case when either Account or Loan does not exist
       account = None
       loan_amount = None
    
    # Prepare data for the pie chart
    positions = [item['position'] for item in position_data]
    employee_counts = [item['total'] for item in position_data]
    department = [item['department'] for item in department_data]
    employee_department_counts = [item['total'] for item in department_data]
    hire_dates = [DateFormat(item['date_of_hire']).format('Y-m-d') for item in temp_employee_data]
    hire_counts = [item['total'] for item in temp_employee_data]
    branch_names = [item['branch__branch_name'] for item in branch_data]
    employee_counts = [item['total_employees'] for item in branch_data]


    today = now()
    seven_days_ago = today - timedelta(days=7)
    
    
    active_users_by_day = User.objects.filter(
        is_active=True,
        last_login__gte=seven_days_ago
    ).annotate(date=TruncDate('last_login')).values('date').annotate(count=Count('id')).order_by('date')
    
    # Create lists of dates and counts for the chart
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in active_users_by_day]
    counts = [entry['count'] for entry in active_users_by_day]
    

    group_user_counts = {group: group.user_set.count() for group in group}

    data = {'log_entries': logs,  'task_filter': task_filter,
            'task_assignment_filter': task_assignment_filter,
            'all_task': view_all_taskassi,
            'pending_tasks': pending_tasks,
            'completed_tasks': completed_tasks,
            'all_tasks': all_tasks,
            'user': user, 
            'group': group_user_counts,
            'user_filter': user_filters,
            'account_labels': account_labels, 
        'account_data': account_data,  
             'dates': dates,
             'active_user_count': active_user_count,
             'total_employees': total_employees,
             'total_position_emp': total_position_emp,
             'total_department_emp': total_department_emp,
             'positions': positions,
             'total_branch': total_branch,
             'total_trans': total_trans,
             'total_fixed': total_fixed,
             'total_saving': total_saving,
             'total_cheking': total_cheking,
        'employee_counts': employee_counts,
             'department': department,
             'total_account': total_account,
             'branch_names': branch_names,
        'employee_counts': employee_counts,
        'employee_department_counts': employee_department_counts,
        'hire_dates': hire_dates,
        'hire_counts': hire_counts,
        'Account_amount': Account_amount,
        'loan_amount': loan_amount,
        'total_transactions': total_transactions,
        'data': data,
        'label': label,
        'counts': counts,}
    return render(request, 'home.html', data)

# create book
@permission_required('polls.add_books', raise_exception=True)
def add_bok(request):
    book = books.objects.first()  # Use the model class here
    
    if request.method == 'POST':
     form = book_form(request.POST)
     if form.is_valid():
        form.save()
        
        return redirect('')
    else: 
     form = book_form()
    data = {'books': book, 'form': form}

    return render(request, 'add_book.html', data)



# add default perm 

@receiver(post_save, sender=User)
def add_default_permissions(sender, instance, created, **kwargs):
    if created:
        # Define the models and their permissions
        models_permissions = {
           'account': 'view_account',
           'savingsaccount': 'view_savingsaccount',
           'checkingaccount': 'view_checkingaccount',
           'fixeddepositaccount': 'view_fixeddepositaccount',
           'notification': 'view_notification',

        } 
        
        for model_name, perm_codename in models_permissions.items():
            content_type = ContentType.objects.get(app_label='polls', model=model_name)
            permission = Permission.objects.get(content_type=content_type, codename=perm_codename)
            instance.user_permissions.add(permission)


# create branch 

@permission_required('polls.add_branch')
def create_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')  # Redirect to a list of branches or another relevant view
    else:
        form = BranchForm()

    return render(request, 'create_branch.html', {'form': form})
    

# tem employee 

@permission_required('polls.add_tempemployee', raise_exception=True)
def temp_employee(request):
    if request.method == 'POST':
        fo = TempEmployeeForm(request.POST)
        if fo.is_valid():
            fo.save()
            return redirect('')  # Redirect to a success page or another relevant view
    else:
        fo = TempEmployeeForm()

    return render(request, 'temp_employee.html', {'fo': fo})


# Approvale 

@permission_required('polls.change_tempemployee')
def approve_temp_employee(request, pk):
    temp_employee = get_object_or_404(TempEmployee, pk=pk)
    temp_employee.statuse = True
    temp_employee.save()
    return redirect('view_temp_employee_list')   # Redirect to an appropriate page









######################### managment view ###################################################


########### branch managment 

# view 

@permission_required('polls.view_branch')
def Branchview(request):
    query = request.GET.get('q')
    branch_id = request.GET.get('branch_id')
    location = request.GET.get('location')
    labels = []
    data = []
    employees = []
    position_labels = []
    position_data = []

    # Filter branches based on query parameters
    f = Branch_filter(request.GET, queryset=Branch.objects.annotate(employee_count=Count('employees')))
    branch_view = f.qs

    # Apply additional filters if necessary
    if query:
        branch_view = branch_view.filter(
            Q(branch_name__icontains=query) | Q(location__icontains=query)
        )

    if branch_id:
        branch_view = branch_view.filter(branch_id=branch_id)

    if location:
        branch_view = branch_view.filter(location=location)

    # Get employees related to the filtered branches
    for branch in branch_view:
        branch_employees = branch.employees.all()
        employees.extend(branch_employees)

    # Count the number of employees in each position
    position_counts = Counter(employee.position for employee in employees)
    position_labels = list(position_counts.keys())
    position_data = list(position_counts.values())

    # Collect branch names and employee counts for the chart
    for b in branch_view:
        labels.append(b.branch_name)
        data.append(b.employee_count)

    context = {
        'branch': branch_view,
        'labels': labels,
        'data': data,
        'employees': employees,
        'position_labels': position_labels,
        'position_data': position_data,
        'filter': f,
    }
    return render(request, 'branch_managment.html', context)



# update 

@permission_required('polls.change_branch')  # Ensure the permission name is correct
def Branch_update(request, id):
    branch_view = get_object_or_404(Branch, branch_id=id)
    if request.method == 'POST':
        form = BranchForm(request.POST, request.FILES, instance=branch_view)
        if form.is_valid():  # Add parentheses here
            form.save()
            return redirect('Branchview')
    else:
        form = BranchForm(instance=branch_view)
    return render(request, 'create_branch.html', {'form': form, 'id': id})

# delete 

@permission_required('polls.remove_Branch')
def Branch_remove(request, id ):
    branch_view = Branch.objects.get(branch_id = id)
    branch_view.delete()
    return redirect('Branchview')




############################################################### Employee managment 


# view 

@permission_required('polls.view_employee')
def employee_view(request):
    empview = Employee.objects.all()

    # Apply the filters
    f = Employee_filter(request.GET, queryset=empview)
    empview = f.qs  # Get the filtered queryset
    labels = []
    data = []

    position_counts = Counter(empview.values_list('position', flat=True))

    labels = list(position_counts.keys())
    data = list(position_counts.values())

    return render(request, 'emp_managent.html', {'emp': empview, 'labels': labels, 'data': data, 'filter': f})


# change

@permission_required('polls.change_employee')
def employee_update(request, id):
    employee_view = get_object_or_404(Employee, employee_id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee_view)
        if form.is_valid():  # Add parentheses here
            form.save()
            return redirect('employee_view')
    else:
        form = EmployeeForm(instance=employee_view)
    return render(request, 'temp_employee.html', {'fo': form, 'id': id})


# delete

@permission_required('polls.remove_employee')
def employee_delete(request, id):
    employee_view = get_object_or_404(Employee, employee_id = id)
    employee_view.delete()
    return redirect(reverse('employee_view'))



###############################################  sending notification


def send_notification(request, room_name):

    room = get_object_or_404(Room, name=room_name)
    ro = Room.objects.all()
    messages = Notification.objects.filter(room=room).order_by('date_sent')
    
    return render(request, 'send_notification.html', {"room_name": room_name, "message": messages, "room": ro, "roo": room})



def view_notifications(request):

    room = Room.objects.all()

    return render(request, 'view_notifications.html', {'room': room})





######################################################## history log 

###### all history log 
@user_passes_test(lambda u: u.is_superuser)
def History_log(request):
    Employee_history = Employee.history.all()
    Tempemployee_history = TempEmployee.history.all()
    Branch_history = Branch.history.all()
    Account_history = Account.history.all()
    Loan_history = Loan.history.all()
    Transaction_history = Transaction.history.all()
    Task_history = Task.history.all()
    TaskAssignment_history = TaskAssignment.history.all()
    FixedDepositAccount_history = FixedDepositAccount.history.all()
    SavingsAccount_history = SavingsAccount.history.all()
    CheckingAccount_history = CheckingAccount.history.all()
    Collateral_history = Collateral.history.all()


    context = {'Tempemployee_history': Tempemployee_history,
               'Branch_history': Branch_history,
               'Employee_history': Employee_history,
               'Account_history': Account_history,
               'Loan_history': Loan_history,
               'Transaction_history': Transaction_history,
               'Task_history': Task_history,
               'TaskAssignment_history': TaskAssignment_history,
               'FixedDepositAccount_history': FixedDepositAccount_history,
               'SavingsAccount_history': SavingsAccount_history,
               'CheckingAccount_history': CheckingAccount_history,
               'Collateral_history': Collateral_history,
               }

    return render(request, 'history.html', context)


######  branch history log


def branch_log(request):
    histo = Branch.history.all()
    return render(request, 'Branch_log.html', {'histo': histo})



######  Employee history log


def employee_log(request):
    histo = Employee.history.all()
    return render(request, 'Employee_log.html', {'histo': histo})



######  loan history log


def loan_log(request):
    histo = Loan.history.all()
    return render(request, 'Loan_log.html', {'histo': histo})



######  task history log


def task_log(request):
    histo = Task.history.all()
    return render(request, 'Task_log.html', {'histo': histo})



######  account history log


def account_log(request):
    histo = Account.history.all()
    return render(request, 'Account_log.html', {'histo': histo})



######  transaction history log


def transaction_log(request):
    histo = Transaction.history.all()
    return render(request, 'Transaction_log.html', {'histo': histo})



######  loan_payment history log


def loan_payment_log(request):
    histo = LoanPayment.history.all()
    return render(request, 'LoanPayment_log.html', {'histo': histo})


###################################################### download file 


def save_pdf_to_local(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="table_data.pdf"'


    p = canvas.Canvas(response, pagesize=letter)

    # Query your data (replace with your table data)
    data = Branch.objects.all()

    x = 100
    y = 750

    p.drawString(x, y, 'branch_id')
    p.drawString(x + 100, y, 'branch_name')
    p.drawString(x + 200, y, 'location')

    y -= 30

    for row in data:
        p.drawString(x, y, str(row.branch_id))
        p.drawString(x + 100, y, str(row.branch_name))
        p.drawString(x + 200, y, str(row.location))
        y -= 20

    p.showPage()
    p.save()

    return response


##################################################### task assignment


# view temp_employee

@permission_required('polls.view_tempemployee')
def view_temp_employee_list(request):
    temp_employees = TempEmployee.objects.filter(statuse=False)
    return render(request, 'view_temp_employee_list.html', {'temp_employees': temp_employees})

def remove_temp_emp(request, id):
    temp_dele = get_object_or_404(TempEmployee, employee_id = id)
    temp_dele.delete()
    return redirect('view_temp_employee_list')


# view task and task_assignmment 
@permission_required('polls.view_task')
def vew_task_ass(request):
    task = Task.objects.all()
    task_fil = TaskFilter(request.GET, queryset=task)
    task_ass = TaskAssignment.objects.all()
    task_ass_fil = TaskAssignmentFilter(request.GET, queryset=task_ass)
    return render(request, 'view_task.html', {'task_fil': task_fil, 'task_ass_fil': task_ass_fil})



# create task 

@permission_required('polls.add_task')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_temp_employee_list')
    else:
        form = TaskForm()
    return render(request, 'task.html', {'form': form})



# creat task_assignment 


@permission_required('polls.add_taskassignment')
def task_assign(request):
    if request.method == 'POST':
        form = TaskAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_temp_employee_list')
    else:
        form = TaskAssignmentForm()
    return render(request, 'task_assign_form.html', {'form': form})





###################################################################### account section 


############## create account 

@permission_required('polls.add_account')
def create_acc(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_acc')
    else:
        form = AccountForm()
    return render(request, 'create_acc.html', {'form': form})


############### view account management

@permission_required('polls.add_account')
def Account_view(request):
    Acc = Account.objects.all()
    trans = Transaction.objects.all()
    account_filter = Account_fillter(request.GET, queryset=Acc)
    Acc = account_filter.qs

    account_type_counts = Acc.values('account_type').annotate(count=Count('account_type'))

    
    account_labels = [account_type['account_type'] for account_type in account_type_counts]
    account_data = [account_type['count'] for account_type in account_type_counts]
    total_transactions = trans.count()

    account_type_data = [(account_type['account_type'], account_type['count']) for account_type in account_type_counts]


    transactions = Transaction.objects.all()
    transaction_filter = Transaction_filter(request.GET, queryset=transactions)
    transactions = transaction_filter.qs

    transaction_type_counts = transactions.values('transaction_type').annotate(count=Count('transaction_type'))


    transaction_labels = [transaction_type['transaction_type'] for transaction_type in transaction_type_counts]
    transaction_data = [transaction_type['count'] for transaction_type in transaction_type_counts]



    return render(request, 'Account.html', {
        'account': Acc,
        'filter': account_filter,
        'transaction': trans,
        'total_transactions': total_transactions,
        'account_labels': account_labels,  # Pass labels for the 
        'account_data': account_data,  
        'account_type_counts': account_type_data, 
        'transactions': transactions,
        'transaction_labels': transaction_labels,
        'transaction_data': transaction_data,
        'transaction_filter': transaction_filter, 
    })


############### personal Account 

@permission_required('polls.view_account')
def Per_Account(request):
    user = request.user

    try:
        # Fetch all accounts for the user
        account = Account.objects.filter(user=user)

        # Total balance for all accounts
        total_balance = account.aggregate(Sum('balance'))['balance__sum'] or 0

        # Account IDs for filtering transactions
        account_ids = account.values_list('account_id', flat=True)

        # Total transactions for this user
        trans = Transaction.objects.filter(Q(to_account_id__in=account_ids) | Q(form_account_id__in=account_ids))
        

        # Calculate the total amount per transaction type
        total_deposit = trans.filter(transaction_type='Deposit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_withdrawal = trans.filter(transaction_type='Withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0
        total_transfer = trans.filter(transaction_type='Transfer').aggregate(Sum('amount'))['amount__sum'] or 0


        total_transactions = total_deposit + total_withdrawal + total_transfer
        # Aggregate transaction data by minute (for charting or other needs)
        transaction_data = (
            trans
            .values(transaction_type_name=F('transaction_type'), month=TruncMinute('date'))
            .annotate(total_amount=Sum('amount', output_field=FloatField()))
            .order_by('month')
        )

        # Prepare data for charting or summary
        labels = []
        deposit_data = []
        withdrawal_data = []
        transfer_data = []

        # Prepare monthly data for chart
        for entry in transaction_data:
            month = entry['month'].strftime('%H:%M')  # Format month as a string
            if month not in labels:
                labels.append(month)
                deposit_data.append(0)
                withdrawal_data.append(0)
                transfer_data.append(0)

            # Fill data according to transaction type
            index = labels.index(month)
            if entry['transaction_type_name'] == 'Deposit':
                deposit_data[index] += entry['total_amount']
            elif entry['transaction_type_name'] == 'Withdrawal':
                withdrawal_data[index] += entry['total_amount']
            elif entry['transaction_type_name'] == 'Transfer':
                transfer_data[index] += entry['total_amount']

        # Account balances for charting
        data = []
        label = []
        for acc in account:
            data.append(float(acc.balance))
            label.append(acc.account_type)

    except Account.DoesNotExist:
        account = None
        data = []
        label = []
        labels = []
        deposit_data = []
        withdrawal_data = []
        transfer_data = []
        total_transactions = 0
        total_deposit = 0
        total_withdrawal = 0
        total_transfer = 0

    return render(request, 'per_account.html', {
        'account': account,
        'total_balance': total_balance,
        'data': data,
        'label': label,
        'labels': labels,
        'deposit_data': deposit_data,
        'withdrawal_data': withdrawal_data,
        'transfer_data': transfer_data,
        'total_transactions': total_transactions,
        'total_deposit': total_deposit,
        'total_withdrawal': total_withdrawal,
        'total_transfer': total_transfer,
    })


############### transaction creation  

@permission_required('polls.add_account')
def Transaction_creation(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_acc')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {'form': form})



###################################################################### Loan section 



##################### create loan 


@permission_required('polls.add_loan')
def Create_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form =  LoanForm()
    return render(request, 'create_loan.html', {'form': form})


##################### create colateral


@permission_required('polls.add_loan')
def create_collateral(request):
    if request.method == 'POST':
        form = CollateralForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Create_loan')
        
    else:
        form= CollateralForm()
    return render(request, 'create_collateral.html', {'form': form})



##################### view loan 



def Loan_managment(request):
    loan = Loan.objects.all()
    fil = Loan_filter(request.GET, queryset=loan)
    collateral = Collateral.objects.all()
    filter_col = CollateralFilter(request.GET, queryset=collateral)
    loan_payment = LoanPayment.objects.all()
    filter_payment = LoanPaymentFilter(request.GET, queryset=loan_payment)
    return render(request, 'loan_managment.html', {'laon': loan, 'collateral': collateral, 'fil': fil, 'filter_col': filter_col, 'loan_payment': loan_payment,'filter_payment': filter_payment})


####################### loan paymet form 


def loan_payment(request):
    if request.method == 'POST':
        form = LoanPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Loan_managment')
    else:
        form= LoanPaymentForm()
    return render(request, 'loan_payment.html', {'form': form})


##################### personal loan managment 

def per_loan(request):
    user = request.user
    try:
        lo = Loan.objects.get(user=user)
        loan_pay = LoanPayment.objects.filter(loan=lo)
        
        # Debug: Print loan details
        print("Loan Details:")
        print("Start Date:", lo.start_date)
        print("End Date:", lo.end_date)
        print("Repayment Schedule:", lo.repayment_schedule)
        
        # Calculate loan payments
        loan_payments = []
        if lo.repayment_schedule and lo.start_date and lo.end_date:
            # Convert end_date to date if necessary
            if isinstance(lo.end_date, datetime.datetime):
                end_date = lo.end_date.date()
            else:
                end_date = lo.end_date

            total_minutes = (end_date - lo.start_date).total_seconds() // 60
            
            # Debug: Check if total_minutes is valid
            print("Total Minutes:", total_minutes)
            
            payment_interval = total_minutes // lo.repayment_schedule
            
            for i in range(lo.repayment_schedule):
                payment_date = lo.start_date + timedelta(minutes=payment_interval * i)
                loan_payments.append({
                    'payment_date': payment_date,
                    'amount_due': lo.amount / lo.repayment_schedule,
                    'status': 'Scheduled'
                })

        # Debug: Print loan payments in the console
        print("Loan Payments:", loan_payments)

    except Loan.DoesNotExist:
        lo = None
        loan_pay = None
        loan_payments = []

    return render(request, 'per_loan.html', {'lo': lo, 'loan_payments': loan_payments, 'loan_pay':loan_pay})