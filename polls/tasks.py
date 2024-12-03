import logging
from datetime import datetime as dt
from celery import shared_task
from decimal import Decimal
from django.utils import timezone
from .models import *
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)

@shared_task
def update_savings_accounts():
    # Get all SavingsAccounts
    savings_accounts = SavingsAccount.objects.all()
    current_time = timezone.now()

    logger.info("Starting the update_savings_accounts task")

    for savings_account in savings_accounts:
        logger.info(f"Processing SavingsAccount ID: {savings_account.savings_account_id}")
        
        # Set start_time to midnight of start_date
        start_time = timezone.make_aware(dt(
            year=savings_account.start_date.year,
            month=savings_account.start_date.month,
            day=savings_account.start_date.day
        ))

        time_elapsed = current_time - start_time
        minutes_elapsed = time_elapsed.total_seconds() / 60

        if minutes_elapsed >= 1:
            # Calculate interest per minute
            interest_rate = savings_account.interest_rate / 100
            account_balance = savings_account.account.balance

            logger.info(f"Interest rate: {interest_rate}, Account balance: {account_balance}")
            
            interest = account_balance * (interest_rate / 60)
            
            logger.info(f"Calculated interest: {interest}")

            # Update account and interest
            savings_account.accumulated_interest += interest
            savings_account.account.balance += interest
            savings_account.account.save()
            savings_account.save()

            logger.info(f"Updated SavingsAccount ID: {savings_account.savings_account_id}")




# @shared_task
# def update_loan():
#     loans = Loan.objects.all()
#     current_time = timezone.now()

#     logger.info("Starting the update_loan task")

#     for loan in loans:
#         logger.info(f"Processing Loan ID: {loan.loan_id}")

#         # Check if start_date is not None
#         if loan.start_date is None or loan.end_date is None:
#             logger.error(f"Loan ID: {loan.loan_id} has no start_date or end_date. Skipping.")
#             continue  # Skip this loan if start_date or end_date is missing

#         # Set start_time to midnight of start_date
#         start_time = timezone.make_aware(dt(
#             year=loan.start_date.year,
#             month=loan.start_date.month,
#             day=loan.start_date.day
#         ))

#         # Convert end_date to datetime at midnight for consistency
#         end_time = timezone.make_aware(dt(
#             year=loan.end_date.year,
#             month=loan.end_date.month,
#             day=loan.end_date.day
#         ))

#         # Calculate repayment interval
#         total_duration = (end_time - start_time).days
#         repayment_interval = total_duration // loan.repayment_schedule

#         # Calculate due dates for each payment
#         next_due_date = start_time + timedelta(days=repayment_interval * (loan.repayment_schedule - 1))

#         # Check if a payment is due
#         if current_time >= next_due_date:
#             room, _ = Room.objects.get_or_create(name=loan.user.username)

#             if loan.status != "Paid":
#                 late_fee = loan.amount * Decimal('0.02')
#                 loan.amount += late_fee
#                 loan.save()

#                 Notification.objects.create(
#                     user=loan.user,
#                     room=room,
#                     message=f"Your payment is overdue! A late fee of {late_fee} has been added.",
#                     date_sent=current_time
#                 )
#                 logger.info(f"Late fee applied for Loan ID: {loan.loan_id}")

#             else:
#                 Notification.objects.create(
#                     user=loan.user,
#                     room=room,
#                     message=f"Your next payment is due on {next_due_date}. Please ensure timely payment.",
#                     date_sent=current_time
#                 )
#                 logger.info(f"Payment reminder sent for Loan ID: {loan.loan_id}")

#         # Escalate case if overdue for too long
#         overdue_duration = current_time - next_due_date
#         if overdue_duration.days > 30:
#             assign_to_law_firm(loan)

#         # Escalate to branch manager if loan amount exceeds a threshold
#         if loan.amount > 50000:
#             escalate_to_manager(loan)        
        
#         payments = LoanPayment.objects.filter(loan=loan)
#     for loan in loans:
#         logger.info(f"Processing Loan ID: {loan.loan_id}")
    
#         # Check if start_date, end_date, and repayment_schedule are valid
#         if loan.start_date is None or loan.end_date is None or loan.repayment_schedule == 0:
#             logger.error(f"Loan ID: {loan.loan_id} has invalid data (missing start_date, end_date, or repayment_schedule is     zero). Skipping.")
#             continue  # Skip this loan if any required field is invalid
    
#         # Set start_time to midnight of start_date
#         start_time = timezone.make_aware(dt(
#             year=loan.start_date.year,
#             month=loan.start_date.month,
#             day=loan.start_date.day
#         ))
    
#         # Convert end_date to datetime at midnight for consistency
#         end_time = timezone.make_aware(dt(
#             year=loan.end_date.year,
#             month=loan.end_date.month,
#             day=loan.end_date.day
#         ))
    
#         # Calculate repayment interval
#         total_duration = (end_time - start_time).days
#         repayment_interval = total_duration // loan.repayment_schedule


#     return "Loan update task completed"


# def assign_to_law_firm(loan):
#     logger.info(f"Assigning Loan ID {loan.loan_id} to law firm for collection.")
#     loan.status = "Assigned to Law Firm"
#     loan.save()

#     room, _ = Room.objects.get_or_create(name=loan.user.username)
#     Notification.objects.create(
#         user=loan.user,
#         room=room,
#         message="Your loan has been assigned to a law firm for collection due to non-payment.",
#         date_sent=timezone.now()
#     )


# def escalate_to_manager(loan):
#     logger.info(f"Escalating Loan ID {loan.loan_id} to branch manager.")

#     # Try to get a branch manager
#     branch_manager = User.objects.filter(is_staff=True, groups__name='Branch Manager').first()

#     if branch_manager:
#         loan.status = "Pending Manager Approval"
#         loan.save()

#         room, _ = Room.objects.get_or_create(name=loan.user.username)
#         Notification.objects.create(
#             user=branch_manager,
#             room=room,
#             message=f"Loan ID {loan.loan_id} exceeds the threshold and requires your approval.",
#             date_sent=timezone.now()
#         )
#         logger.info(f"Notification sent to branch manager for Loan ID {loan.loan_id}")
#     else:
#         logger.error("No branch manager found to escalate the loan.")




# @shared_task
# def update_loan():
#     # Get all SavingsAccounts
#     loan = Loan.objects.all()
#     current_time = timezone.now()

#     logger.info("Starting the update_loan task")

#     for loan in loan:
#         logger.info(f"Processing SavingsAccount ID: {loan.loan_id}")
        
#         # Set start_time to midnight of start_date
#         start_time = timezone.make_aware(dt(
#             year=loan.start_date.year,
#             month=loan.start_date.month,
#             day=loan.start_date.day
#         ))

#         time_elapsed = current_time - start_time
#         minutes_elapsed = time_elapsed.total_seconds() / 60

#         if minutes_elapsed >= 1:
#             # Calculate interest per minute
#             interest_rate = loan.interest_rate / 100
#             loan_amount = loan.amount

#             logger.info(f"Interest rate: {interest_rate}, loan amount: {loan_amount}")
            
#             interest = loan_amount * (interest_rate / 60)
            
#             logger.info(f"Calculated interest: {interest}")

#             # Update account and interest
            
#             loan.amount += interest
#             loan.save()
#             loan.save()

#             logger.info(f"Updated SavingsAccount ID: {loan.loan_id}")



