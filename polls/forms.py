from django import forms
from .models import *
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.models import  User, Group 
from django.forms.widgets import PasswordInput, TextInput


# create user profile 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Add an image',
            }),
        }


# signup form /

class creatuserform(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={
        'placeholder': 'Username',
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
    }))
    
    email = forms.EmailField(widget=TextInput(attrs={
        'placeholder': 'Email Address',
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
    }))
    
    password1 = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
    }))
    
    password2 = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# login form /
        


class log(AuthenticationForm):
    username= forms.CharField(widget=TextInput(attrs={
            'placeholder': 'Username',
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        }))
    password = forms.CharField(widget=PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        }))


# book form 


class book_form(forms.ModelForm):
    class Meta:
        model = books
        fields = '__all__' 


# Branch creation

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['branch_name', 'location']
        labels = {
            'branch_name': 'Branch Name',  # Setting the label for the 'branch_name' field
            'location': 'Location',        # Setting the label for the 'location' field
        }
        widgets = {
            'branch_name': forms.TextInput(attrs={
                'placeholder': 'Enter branch name',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter location',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
        }

# assign form  for user


class UserGroupAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(employee_profile__isnull=False),  # Only users with associated Employee records
        required=True,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )


# Employee creation form 


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'phone', 'address', 'position', 'salary', 'date_of_hire', 'department', 'branch']
        widgets = {
            'date_of_hire': forms.DateInput(attrs={'type': 'date'}),
        }


# Account creation form 

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['user', 'account_type', 'balance']
        widgets = {
            'user': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'account_type': forms.Select(choices=Account.ACCOUNT_TYPES, attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'balance': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }
        labels = {
            'user': 'Account Holder',
            'account_type': 'Account Type',
            'balance': 'Initial Balance',
        }

# transaction form 


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['to_account', 'form_account', 'transaction_type', 'amount', 'description']
        widgets = {
            'to_account': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'form_account': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'transaction_type': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }
        labels = {
            'to_account': 'To Account',
            'form_account': 'From Account',
            'transaction_type': 'Transaction Type',
            'amount': 'Amount',
            'description': 'Description',
        }


# saving account 


class SavingsAccountForm(forms.ModelForm):
    class Meta:
        model = SavingsAccount
        fields = ['account', 'interest_rate', 'accumulated_interest', 'start_date']
        widgets = {
            'account': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'accumulated_interest': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'start_date': forms.DateInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'type': 'date'})
        }
        labels = {
            'account': 'Account',
            'interest_rate': 'Interest Rate (%)',
            'accumulated_interest': 'Accumulated Interest',
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }


# checking acc 


class CheckingAccountForm(forms.ModelForm):
    class Meta:
        model = CheckingAccount
        fields = ['account', 'overdraft_limit']
        widgets = {
            'account': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'overdraft_limit': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }
        labels = {
            'account': 'Account',
            'overdraft_limit': 'Overdraft Limit',
        }

# fixed Account 


class FixedDepositAccountForm(forms.ModelForm):
    class Meta:
        model = FixedDepositAccount
        fields = ['account', 'deposit_amount', 'interest_rate', 'maturity_date']
        widgets = {
            'account': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'deposit_amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'maturity_date': forms.DateInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'type': 'date'}),
        }
        labels = {
            'account': 'Account',
            'deposit_amount': 'Deposit Amount',
            'interest_rate': 'Interest Rate (%)',
            'maturity_date': 'Maturity Date',
        }


# loan form 



class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['user', 'amount', 'collateral', 'interest_rate', 'repayment_schedule', 'status', 'end_date']
        widgets = {
            'user': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'collateral': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'repayment_schedule': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'rows': 3}),
            'status': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'type': 'datetime-local'}),
        }
        labels = {
            'user': 'User',
            'amount': 'Loan Amount',
            'collateral': 'Collateral',
            'interest_rate': 'Interest Rate (%)',
            'repayment_schedule': 'Repayment Schedule',
            'status': 'Status',
            'end_date': 'End Date',
        }


# loanpayment form 


class LoanPaymentForm(forms.ModelForm):
    class Meta:
        model = LoanPayment
        fields = ['loan', 'payment_date', 'amount_paid', 'status']
        widgets = {
            'loan': forms.Select(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'payment_date': forms.DateTimeInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'type': 'datetime-local'
            }),
            'amount_paid': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'status': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
        }
        labels = {
            'loan': 'Loan',
            'payment_date': 'Payment Date',
            'amount_paid': 'Amount Paid',
            'status': 'Payment Status',
        }


# Collateral form 


class CollateralForm(forms.ModelForm):
    class Meta:
        model = Collateral
        fields = ['collateral_type', 'value', 'description']
        widgets = {
            'collateral_type': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'value': forms.NumberInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }
        labels = {
            'collateral_type': 'Collateral Type',
            'value': 'Value',
            'description': 'Description',
        }

# task form 

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_type', 'description', 'status', 'due_date']
        widgets = {
            'task_type': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'status': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
        }
        labels = {
            'task_type': 'Task Type',
            'description': 'Description',
            'status': 'Status',
            'due_date': 'Due Date',
        }

# taskassignment form 

class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = TaskAssignment
        fields = ['task', 'employee']
        widgets = {
            'task': forms.Select(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'employee': forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }
        labels = {
            'task': 'Task',
            'employee': 'Employee',
        }


# notification form 


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'message']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'user': 'User',
            'message': 'Message',
        }


# tem employee form 

class TempEmployeeForm(forms.ModelForm):
    class Meta:
        model = TempEmployee
        fields = [
            'user','phone','address','position','salary','date_of_hire','department','branch',
        ]
        widgets = {
            'user': forms.Select(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone number',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Address',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'position': forms.TextInput(attrs={
                'placeholder': 'Position',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'salary': forms.NumberInput(attrs={
                'placeholder': 'Salary',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'date_of_hire': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'department': forms.TextInput(attrs={
                'placeholder': 'Department',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'branch': forms.Select(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'mt-1 text-indigo-600 focus:ring-indigo-500'
            }),
        }