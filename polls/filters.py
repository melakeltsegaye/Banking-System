import django_filters
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.forms import Select, TextInput
from .models import *

# Branch filter 

class Branch_filter(django_filters.FilterSet):
    branch_id = django_filters.NumberFilter(
        widget=forms.NumberInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Branch ID'
        })
    )
    branch_name = django_filters.CharFilter(
        lookup_expr='iexact',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Branch Name'
        })
    )
    location = django_filters.CharFilter(
        lookup_expr='iexact',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Location'
        })
    )

    class Meta:
        model = Branch
        fields = ['branch_id', 'branch_name', 'location']

# Employee filter 

class Employee_filter(django_filters.FilterSet):
    user = django_filters.CharFilter(
        field_name='user__username',
        lookup_expr='icontains',
        label = 'Employee',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Username'
        })
    )
    address = django_filters.CharFilter(
        lookup_expr='iexact',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Address'
        })
    )
    position = django_filters.CharFilter(
        lookup_expr='iexact',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Position'
        })
    )
    branch = django_filters.CharFilter(
        lookup_expr='iexact',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Branch'
        })
    )

    class Meta:
        model = Employee
        fields = ['user', 'address', 'position', 'branch']


# User filter 

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        lookup_expr='iexact',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 Fe rounded-md shadow-lg focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Username'
        })
    )
    
    email = django_filters.CharFilter(
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 Fe rounded-md shadow-lg focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Email'
        })
    )

    last_login = django_filters.DateFilter(
        lookup_expr='exact',
        label='',
        widget=forms.DateInput(attrs={
            'class': 'block w-full px-3 py-2 Fe rounded-md shadow-lg focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black',
            'type': 'date'
        })
    )

    date_joined = django_filters.DateFilter(
        lookup_expr='exact',
        label='',
        widget=forms.DateInput(attrs={
            'class': 'block w-full px-3 py-2 Fe rounded-md shadow-lg focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black ',
            'type': 'date'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'last_login', 'date_joined']


# task filter 


class TaskFilter(django_filters.FilterSet):
    task_type = django_filters.CharFilter(
        lookup_expr='icontains',
        label='',  # Remove label
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Task Type'
        })
    )
    
    status = django_filters.CharFilter(
        lookup_expr='icontains',
        label='',  # Remove label
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Status'
        })
    )
    
    due_date = django_filters.DateFilter(
        lookup_expr='exact',
        label='',  # Remove label
        widget=forms.DateInput(attrs={
            'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'type': 'date',
            'placeholder': 'Due Date'
        })
    )

    class Meta:
        model = Task
        fields = ['task_type', 'status', 'due_date']


# task assign filter 


class TaskAssignmentFilter(django_filters.FilterSet):
    task = django_filters.CharFilter(
        field_name='task__task_type',  # Filter by the related task's task_type
        lookup_expr='icontains',
        label='',  # Remove label
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Task Type'
        })
    )
    
    employee = django_filters.ModelChoiceFilter(
    field_name='employee',  # Filter by the related employee
    queryset=Employee.objects.all(),  # Populate with Employee choices
    label='',  # Remove label
    widget=forms.Select(attrs={
        'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
        'placeholder': 'Select Employee'
    })
    )
    
    assigned_date = django_filters.DateFilter(
    field_name='assigned_date',
    label='',  # Remove label
    widget=forms.DateInput(attrs={
        'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
        'type': 'date',
        'placeholder': 'Assigned Date'
    })
    )

    class Meta:
        model = TaskAssignment
        fields = ['task', 'employee', 'assigned_date']


###### group filter 


class GroupFilter(django_filters.FilterSet):
    # Customizing the form field widgets with classes
    group = django_filters.ModelChoiceFilter(
        queryset=Group.objects.all(),
        label="Group",
        widget=Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    permission = django_filters.ModelChoiceFilter(
        queryset=Permission.objects.all(),
        label="Permission",
        widget=Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm md:w-10'
        })
    )
    
    username = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),  # Making username a dropdown as requested
        label="Username",
        widget=Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'group', 'permission']


######## fillter account 


class Account_fillter(django_filters.FilterSet):
    account_type = django_filters.ChoiceFilter(
        choices=Account.ACCOUNT_TYPES,
        label="Account Type",
        widget=Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    # Filtering by user
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="User Selection",
        widget=Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm space-x-2 empty:text-gray-300'
        })
    )

    # Filtering by balance range
    min_balance = django_filters.NumberFilter(
        field_name='balance', lookup_expr='gte', label='Min Balance',
        widget=TextInput(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Min Balance'
        })
    )
    
    max_balance = django_filters.NumberFilter(
        field_name='balance', lookup_expr='lte', label='Max Balance',
        widget=TextInput(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Max Balance'
        })
    )
    
    class Meta:
        model = Account
        fields = ['account_type', 'user', 'min_balance', 'max_balance']


################# filter transaction 


class Transaction_filter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPES,
        label ='',
        widget=Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )

    to_account = django_filters.ModelChoiceFilter(
        queryset=Account.objects.all(),
        label ='',
        widget=Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )

    form_account = django_filters.ModelChoiceFilter(
        queryset=Account.objects.all(),
        label ='',
        widget=Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'to_account', 'form_account']


################# filter loan 

class Loan_filter(django_filters.FilterSet):

    # loan_id = django_filters.NumberFilter(
    #     field_name='loan_id',
    #     widget=forms.NumberInput(attrs={
    #         'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
    #         'placeholder': 'Loan ID'
    #     })
    # )

    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="User",
        label ='',
        widget=forms.Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )

    amount = django_filters.NumberFilter(
        field_name='amount',
        label ='',
        widget=forms.NumberInput(attrs={
            'class': 'block w-full px-3 py-2  rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Amount'
        })
    )

    # collateral = django_filters.ModelChoiceFilter(
    #     queryset=Collateral.objects.all(),
    #     label="Collateral",
    #     widget=forms.Select(attrs={
    #         'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
    #     })
    # )

    # interest_rate = django_filters.NumberFilter(
    #     field_name='interest_rate',
    #     widget=forms.NumberInput(attrs={
    #         'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
    #         'placeholder': 'Interest Rate'
    #     })
    # )

    # repayment_schedule = django_filters.NumberFilter(
    #     field_name='repayment_schedule',
    #     widget=forms.NumberInput(attrs={
    #         'class': 'block w-full px-3 py-2 Fe rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
    #         'placeholder': 'Repayment Schedule'
    #     })
    # )

    # start_date = django_filters.DateFilter(
    #     field_name='start_date',
    #     label="",
    #     widget=forms.DateInput(attrs={
    #         'class': 'block hidden lg:block px-3 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
    #         'type': 'date',
    #     })
    # )

    # end_date = django_filters.DateFilter(
    #     field_name='end_date',
    #     widget=forms.DateInput(attrs={
    #         'class': 'block w-full px-3 py-2  rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
    #         'type': 'date',
    #         'placeholder': 'End Date'
    #     })
    # )

    status = django_filters.CharFilter(
        field_name='status',
        label ='',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2  rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Status'
        })
    )

    class Meta:
        model = Loan
        fields = ['user', 'amount', 'status']



########## filter Collateral 


class CollateralFilter(django_filters.FilterSet):

    collateral_type = django_filters.CharFilter(
        field_name='collateral_type',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Collateral Type'
        })
    )

    value = django_filters.NumberFilter(
        field_name='value',
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'block w-1/3 px-3 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Collateral Value'
        })
    )

    description = django_filters.CharFilter(
        field_name='description',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Description'
        })
    )

    class Meta:
        model = Collateral
        fields = ['collateral_type', 'value', 'description']


############## loan payment filter 


class LoanPaymentFilter(django_filters.FilterSet):

    loan = django_filters.ModelChoiceFilter(
        queryset=Loan.objects.all(),
        label="Loan",
        empty_label="Select a loan",
        widget=forms.Select(attrs={
            'class': 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )

    payment_date = django_filters.DateFilter(
        field_name='payment_date',
        label='Payment Date',
        widget=forms.DateInput(attrs={
            'class': 'block w-full px-3 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'type': 'date',
            'placeholder': 'Select payment date'
        })
    )

    amount_paid = django_filters.NumberFilter(
        field_name='amount_paid',
        label='Amount Paid',
        widget=forms.NumberInput(attrs={
            'class': 'block w-full px-3 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter amount paid'
        })
    )

    status = django_filters.CharFilter(
        field_name='status',
        label='Status',
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Enter status (Paid, Late, etc.)'
        })
    )

    class Meta:
        model = LoanPayment
        fields = ['loan', 'payment_date', 'amount_paid', 'status']