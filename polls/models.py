from django.db import models
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from django.utils import timezone
from datetime import timedelta
import datetime


# User profile 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_image = models.ImageField(blank=True, null=True)
    # Add any other fields you want here

    def __str__(self):
        return self.user.username


# Create your models here.

class books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publish = models.DateTimeField()
    history = HistoricalRecords()

    def __str__(self):
        return self.title



# Accouont table 


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('Savings', 'Savings'),
        ('Checking', 'Checking'),
        ('Fixed Deposit', 'Fixed Deposit')
    ]
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.account_type} - {self.user.username}"
    

# Transaction 

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer')
    ]
    transaction_id = models.AutoField(primary_key=True) 
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_transactions', null=True, blank=True)
    form_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='form_account_transactions', null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
    

# Signal transaction, it update the value of the account

@receiver(post_save, sender=Transaction)
def Transfer_mony(sender, instance, **kwargs):
    # Handle Deposit
    if instance.transaction_type == 'Deposit':
        # Increase the balance of the 'to_account' by the transaction amount
        account = instance.to_account
        if account:
            account.balance += instance.amount
            account.save()

    # Handle Withdrawal
    elif instance.transaction_type == 'Withdrawal':
        # Decrease the balance of the 'form_account' by the transaction amount
        account = instance.form_account
        if account and account.balance >= instance.amount:  # Ensure enough balance
            account.balance -= instance.amount
            account.save()

    # Handle Transfer
    elif instance.transaction_type == 'Transfer':
        # Decrease the balance of the 'form_account'
        from_account = instance.form_account
        to_account = instance.to_account
        if from_account and from_account.balance >= instance.amount:
            from_account.balance -= instance.amount
            from_account.save()

            # Increase the balance of the 'to_account'
            if to_account:
                to_account.balance += instance.amount
                to_account.save()
    

# Saving 


class SavingsAccount(models.Model):
    savings_account_id = models.AutoField(primary_key=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    accumulated_interest = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField()
    history = HistoricalRecords()

    def __str__(self):
        return f"Savings Account - {self.account.user.username}"


# Signal to create a SavingsAccount when an Account of type 'Savings' is created

@receiver(post_save, sender=Account)
def create_savings_account(sender, instance, **kwargs):
    # Check if the account type is 'Savings'
    if instance.account_type == 'Savings':
        SavingsAccount.objects.get_or_create(
            account=instance,
            defaults={
                'interest_rate': 3.50,  # Default interest rate (3.5%)
                'accumulated_interest': 0.00,  # Default accumulated interest
                'start_date': datetime.date.today(),  # Default start date as today
            }
        )   


    
# checking 


class CheckingAccount(models.Model):
    checking_account_id = models.AutoField(primary_key=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    overdraft_limit = models.DecimalField(max_digits=15, decimal_places=2)
    history = HistoricalRecords()

    def __str__(self):
        return f"Checking Account - {self.account.user.name}"


# sending signale from acc to checking acc 



@receiver(post_save, sender=Account)
def Create_Checking(sender, instance, **kwargs):
    if instance.account_type == 'Checking':
        CheckingAccount.objects.get_or_create(
            account=instance,
            defaults={'overdraft_limit': 10}  # Set default overdraft limit
        )

    
# fixed 


class FixedDepositAccount(models.Model):
    fixed_deposit_id = models.AutoField(primary_key=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    deposit_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    maturity_date = models.DateField()
    history = HistoricalRecords()

    def __str__(self):
        return f"Fixed Deposit - {self.account.user.name}"

# Signal to create a FixedDepositAccount when an Account of type 'Fixed Deposit' is created

@receiver(post_save, sender=Account)
def create_fixed_deposit(sender, instance, **kwargs):
    # Check if the account type is 'Fixed Deposit'
    if instance.account_type == 'Fixed Deposit':
        FixedDepositAccount.objects.get_or_create(
            account=instance,
            deposit_amount = instance.amount,
            defaults={
                'interest_rate': 5.00,  # Default interest rate (5%)
                'maturity_date': datetime.date.today() + datetime.timedelta(days=365)  # Default maturity date (1 year from today)
            }
        )

# lone 

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0 )
    collateral = models.OneToOneField('Collateral', on_delete=models.CASCADE, related_name='loan')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2 )
    repayment_schedule = models.IntegerField(null=True)
    start_date = models.DateField(default=timezone.now)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)  # Add this field
    end_date = models.DateTimeField(null=True)  # Allowing nullable end_date
    status = models.CharField(max_length=50, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Loan - {self.user.username}"
    
# loan payment 

class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=50)
    history = HistoricalRecords()  # Paid, Late, etc.

    def __str__(self):
        return f"Payment for Loan {self.loan.loan_id} - {self.status}"
    

# collateral 

class Collateral(models.Model):
    collateral_id = models.AutoField(primary_key=True)
    collateral_type = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    history = HistoricalRecords()
    

    def __str__(self):
        return f"Collateral - {self.collateral_type}"


# Employee   

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_hire = models.DateField()
    department = models.CharField(max_length=100)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='employees')
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username
    


# temp employe   

class TempEmployee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='temp_employee_profile')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_hire = models.DateField()
    department = models.CharField(max_length=100)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='temp_employees')
    statuse = models.BooleanField(default=False, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username
    


# signale for employee table 



@receiver(post_save, sender=TempEmployee)
def transfer_to_employee(sender, instance, **kwargs):
    if instance.statuse:
        # Check if the Employee already exists to avoid duplication
        if not Employee.objects.filter(user=instance.user).exists():
            # Transfer data to Employee model
            Employee.objects.create(
                user=instance.user,
                phone=instance.phone,
                address=instance.address,
                position=instance.position,
                salary=instance.salary,
                date_of_hire=instance.date_of_hire,
                department=instance.department,
                branch=instance.branch
            )
    

# task 

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_type = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=50)
    due_date = models.DateField()
    history = HistoricalRecords()

    def __str__(self):
        return f"Task - {self.task_type}"

# task managment 

class TaskAssignment(models.Model):
    task_assignment_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True)
    assigned_date = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()


    def __str__(self):
        return f"Task Assignment - {self.task.task_type} to {self.employee.user}"

# branch 

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        return self.branch_name
    

# room
class Room(models.Model):
    name = models.CharField(max_length=128, null=True)
    online = models.OneToOneField(to=User, blank=True, null=True, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def get_online_count(self):
        return 1 if self.online else 0



    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'



# notification 


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=512, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification - {self.user.username}"



@receiver(post_save, sender=TempEmployee)
def create_task_on_tempemployee_creation(sender, instance, created, **kwargs):
    if created:
        task = Task.objects.create(
            task_type='Employee Approval',
            description=f'Approve or reject temp employee {instance.user.username}',
            status='Pending',
            due_date=instance.date_of_hire + timedelta(days=7)  # Example due date
        )
        # Assign the task to an HR specialist (you may add a way to select this in the admin view)
        hr_specialist = Employee.objects.filter(department='HR').first()
        if hr_specialist:
            TaskAssignment.objects.create(task=task, employee=hr_specialist)


@receiver(post_save, sender=TempEmployee)
def update_task_on_tempemployee_approval(sender, instance, **kwargs):
    if instance.statuse:  # Check if the status is set to True
        task_assignment = TaskAssignment.objects.filter(
            task__description__contains=instance.user.username
        ).first()
        if task_assignment:
            task_assignment.task.status = 'Completed'
            task_assignment.task.save()


# creating room automaticaly
@receiver(post_save, sender=User)
def create_chat_room_for_user(sender, instance, created, **kwargs):
    if created:
        # Check if the Employee already exists to avoid duplication
        if not Room.objects.filter(name=instance.username).exists():
            Room.objects.create(
                name = instance.username,
                online = instance
            )


