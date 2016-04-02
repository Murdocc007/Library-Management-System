# Full path and name to your csv file

csv_filepathname="/home/aditya/Desktop/Aditya/Database/djangoProjects/Tables/book_loans.csv"
your_djangoproject_home="/home/aditya/Desktop/Aditya/Database/djangoProjects/LMS"

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'LMS.settings'
import django
django.setup()
from polls.models import BOOK_LOANS,BOOK,LIBRARY_BRANCH,BORROWER

import csv

dataReader = csv.reader(open(csv_filepathname), delimiter='\t', quotechar='"')

# for row in dataReader:
#     if row[0] != 'book_id': # Ignore the header row, import everything else
#         book_copies=BOOK_COPIES()
#         book_copies.Book_id=BOOK.objects.get(pk=row[0])
#         book_copies.Branch_id=LIBRARY_BRANCH.objects.get(pk=row[1])
#         book_copies.No_of_copies=int(row[2])
#         book_copies.save()

# for row in dataReader:
#     if row[0] != 'ID0000id': # Ignore the header row, import everything else
#         borrower=BORROWER()
#         borrower.Card_no=row[0]
#         borrower.Ssn=(row[1])
#         borrower.Fname=row[2]
#         borrower.Lname=row[3]
#         borrower.Address=row[5]
#         borrower.Phone=(row[8])
#         borrower.save()


# for row in dataReader:
#         book_loan=BOOK_LOANS()
#         book_loan.Loan_id=int(row[0])
#         book_loan.Isbn=BOOK.objects.get(pk=(row[1]))
#         book_loan.Branch_id=LIBRARY_BRANCH.objects.get(pk=int(row[2]))
#         book_loan.Card_no=BORROWER.objects.get(pk=row[3])
#         book_loan.Date_out=row[4]
#         book_loan.Date_due=row[5]
#         book_loan.Date_in=row[6]
#         book_loan.save()


# for book,author in zip(BOOK.objects.all(),AUTHORS.objects.all()):
#         book_authors=BOOK_AUTHORS()
#         book_authors.Isbn=book
#         book_authors.Author_id=author
#         book_authors.save()



