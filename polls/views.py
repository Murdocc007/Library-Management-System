from django.utils import timezone
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q,Max
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from forms import bookSearchForm,UserCreateForm,AuthenticateForm
from models import BOOK,BOOK_COPIES,BOOK_AUTHORS,LIBRARY_BRANCH,AUTHORS,User,CurrentlyBorrowed,BORROWER,BOOK_LOANS,UserProfile,FINES
from datetime import  datetime,timedelta



@login_required(login_url='/sign_up/')
def index(request):
    content={}
    form=bookSearchForm()
    content['form']=form
    if  datetime.now() -request.user.date_joined.replace(tzinfo=None)<timedelta(minutes=2):
        messages.info(request, "Welcome "+request.user.first_name+"! Your card number is " +request.user.username
                      +". Use your card number next time to login.")
    if request.method == 'POST':
        if(request.POST['BookName']):
            books=BOOK.objects.filter(Title__contains=request.POST['BookName'])
            content['books']=books
        if(request.POST['ISBN']):
            books=BOOK.objects.filter(Isbn=request.POST['ISBN'])
            if 'books' in content:
                content['books']|=books
            else:
                content['books']=books
        if(request.POST['AuthorName']):
            temp=request.POST['AuthorName']
            authors=AUTHORS.objects.all()
            final_authors=[]
            for a in authors:
                if temp.lower().replace(' ','') in a.__str__().lower().replace(' ',''):
                    final_authors.append(a)
            authors_books=BOOK_AUTHORS.objects.filter(Author_id__in=final_authors)
            books=BOOK.objects.filter(Isbn__in=[x.Isbn_id for x in authors_books])
            if 'books' in content:
                content['books']|=books
            else:
                content['books']=books

        if 'books' in content:
            content['copies'],content['availability'],content['copy']=getCopies(content['books'])
            content['books']=getBooksFromCopies(content['copies'])
            content['branches']=getBranch(content['copies'])
            content['authors']=getAuthors(content['books'])
            content['books']=zip(content['books'],content['authors'],
                                 content['copy'],content['branches'],
                                 content['availability'])

    return render(request,'home.html',content)


def getCopies(books):
    bookcopies=[]
    for b in books:
        bookcopies.extend(list(BOOK_COPIES.objects.filter(Book_id=b.Isbn)))
    available=[]
    copies=[]
    for b in bookcopies:
        copies.append(b.No_of_copies-numberOfCopiesBorrowed(b.Book_id,b.Branch_id))
        if(b.No_of_copies-numberOfCopiesBorrowed(b.Book_id,b.Branch_id)>0):
            available.append(True)
        else:
            available.append(False)
    return bookcopies,available,copies

def getBranch(copies):
    branches=[]
    for c in copies:
        branches.extend(LIBRARY_BRANCH.objects.filter(Branch_id=c.Branch_id))
    return branches

def getBooksFromCopies(copies):
    books=[]
    for c in copies:
        books.extend(list(BOOK.objects.filter(Isbn=c.Book_id)))
    return books

def getAuthors(books):
    authors=[]
    for b in books:
        temp1=BOOK_AUTHORS.objects.filter(Isbn_id=b.Isbn)
        temp2=''
        for t in temp1:
            temp3=AUTHORS.objects.get(Author_id=t.Author_id)
            temp2=temp2+" "+temp3.__str__()
        authors.append(temp2)
    return authors

def sign_in(request, auth_form=None):

    if request.user.is_authenticated():
        redirect('/')
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())

            return redirect('/')
        else:
            return render(request, 'sign_in.html', {'auth_form': form})
    auth_form = AuthenticateForm()
    return render(request, 'sign_in.html', {'auth_form': auth_form})


def sign_up(request, user_form=None, incomplete_form=None):

    if request.method == 'POST' and incomplete_form is None:
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            max_username = User.objects.all().aggregate(Max('username'))['username__max']
            if(max_username!=None and max_username!='admin'):
                temp='ID00'+str(int(max_username[2:])+1)
            else:
                temp='ID001001'
            user_form.cleaned_data['card_no']=temp
            user_form.cleaned_data['username']=temp
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=temp, password=password)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Form invalid")
            return sign_up(request, user_form=user_form, incomplete_form=True)
    if incomplete_form is None or not incomplete_form:
        user_form = UserCreateForm()
    return render(request, 'sign_up.html', {'user_form': user_form})

def logout_view(request):
    logout(request)
    return redirect('/')


def numberOfBooks(Isbn,Branch_id):
    temp=len(BOOK_COPIES.objects.filter(Book_id=Isbn).filter(Branch_id=Branch_id))
    return temp


def numberOfCopiesBorrowed(Isbn,Branch_id):
    temp= len(CurrentlyBorrowed.objects.filter(Book_id=Isbn).filter(Branch_id=Branch_id))
    return temp


def numberOfCopiesAvailable(Isbn,Branch_id):
    return numberOfBooks(Isbn,Branch_id)-numberOfCopiesBorrowed(Isbn,Branch_id)

@login_required(login_url='/sign_up/')
def borrow(request,Book_id,Branch_id):
    content={}
    content['Book_id']=Book_id
    content['Branch_id']=Branch_id
    return render(request,'borrow.html',content)

@login_required(login_url='/sign_up/')
def borrowConfirm(request,Book_id,Branch_id):
    content={}
    if(numberofBookBorrowed(request.user.username)<3):
        CurrentlyBorrowed(Book_id=Book_id,Branch_id=Branch_id,UserProfile_id=request.user.username)\
        .save()
        content['due_date']=(datetime.now()+timedelta(days=14)).date()
    return render(request,'borrowconfirm.html',content)

def numberofBookBorrowed(user_id):
    return len(CurrentlyBorrowed.objects.filter(UserProfile_id=user_id))

@login_required(login_url='/sign_up/')
def getFine(request):
    fine_books=calculateFine(request.user.username)
    content={}
    fine=[]
    for b in fine_books:
        fine.append(0.25*(b.Date_out-datetime.now()))
    if(len(fine)>0):
        content['fine_books']=zip(BOOK.objects.filter(Isbn__in=fine_books.Book_id),fine_books,fine)
    return render(request,'fine.html',content)

def calculateFine(Card_no):
    books=CurrentlyBorrowed.objects.filter(UserProfile_id=Card_no)
    fine_books=[]
    for b in books:
        if((datetime.now().date()-b.Date_out).days>14):
            fine_books.append(b)
    return fine_books


def isadmin(user):
    return  user.username=='admin'




@login_required(login_url='/sign_up/')
@user_passes_test(isadmin)
def viewUserFines(request,user_id=None):
    content={}
    if request.method=='POST' or user_id is not None:
        if(user_id ==None or len(user_id.strip(' '))==0):


            if('Card_no' not in request.POST and 'user_id' not in request.POST and 'user_name' not in request.POST):
                temp=CurrentlyBorrowed.objects.all()
            else:
                temp=CurrentlyBorrowed.objects.filter(UserProfile_id=request.POST['Card_no'])
                temp|=CurrentlyBorrowed.objects.filter(Book_id=request.POST['user_id'])
                temp|=CurrentlyBorrowed.objects.filter(UserProfile_id__in=getUserFromName(request.POST['user_name']))

        else:
            temp=CurrentlyBorrowed.objects.filter(UserProfile_id=user_id)
            print len(user_id.strip(' '))
    else:
        temp=CurrentlyBorrowed.objects.all()
    content['borrowers']=getBorrowersName(temp)
    content['borrowedbooks']=temp
    content['fines']=checkFines(temp)
    content['books']=getBooks(content['borrowedbooks'])
    content['borrowedbooks']=zip(content['books'],content['fines'],content['borrowedbooks'],content['borrowers'])

    return render(request,'userfine.html',content)

def getUserFromName(name):
    name=name.split(' ')
    res=[]
    for temp in name:
        res.extend(UserProfile.objects.filter(Fname=temp))
        res.extend(UserProfile.objects.filter(Lname=temp))
    return res



def getBorrowersName(loans):
    temp=[]
    res=[]
    for b in loans:
        res.extend(BORROWER.objects.filter(Card_no=b.UserProfile_id))
    for i in res:
        temp.append(i.__str__())
    return temp


def checkFines(BorrowedBooks):
    temp=[]
    for b in BorrowedBooks:
        if((b.Date_out-datetime.now().date()).days>14):
            temp.append((b.Date_out-datetime.now().date())*0.25)
        else:
            temp.append(0)
    return temp

@login_required(login_url='/sign_up/')
@user_passes_test(isadmin)
def removeFine(request,borrow_id):
    instance=CurrentlyBorrowed.objects.get(id=borrow_id)
    temp=BOOK_LOANS.objects.create(Isbn_id=instance.Book_id,Branch_id=instance.Branch_id
               ,Card_no_id=instance.UserProfile_id,Date_out=instance.Date_out,Date_in=datetime.now()
               ,Date_due=instance.Date_out+timedelta(days=14)
               )
    temp.save()
    FINES(Loan_id=temp.Loan_id,fine_amt=(datetime.now().date()-instance.Date_out).days*0.25,paid=1).save()
    user_id=instance.UserProfile_id
    instance.delete()
    return redirect('/viewUserFines/')


def getBooks(bookids):
        temp=[]
        for b in bookids:
            temp.extend(BOOK.objects.filter(Isbn=b.Book_id))
        return temp

