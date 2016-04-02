from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import  datetime
from django.db import models
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question,null=False,blank=False)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class BOOK(models.Model):
    Isbn=models.CharField(max_length=200,primary_key=True)
    Title=models.CharField(max_length=200)

class LIBRARY_BRANCH(models.Model):
    Branch_id=models.IntegerField(primary_key=True)
    Branch_name=models.CharField(max_length=200)
    Address=models.CharField(max_length=200)


class BOOK_COPIES(models.Model):
    Book=models.ForeignKey(BOOK,null=False,blank=False)
    No_of_copies=models.IntegerField()
    Branch=models.ForeignKey(LIBRARY_BRANCH,null=False,blank=False)


class AUTHORS(models.Model):
    Author_id=models.AutoField(primary_key=True)
    Title=models.CharField(max_length=200)
    Fname=models.CharField(max_length=200)
    Mname=models.CharField(max_length=200)
    Lname=models.CharField(max_length=200)
    Suffix=models.CharField(max_length=200)

    def __str__(self):
        return self.Title+" "+self.Fname+" "+self.Mname+" "+self.Lname+" "+self.Suffix


class BOOK_AUTHORS(models.Model):
    Isbn=models.ForeignKey(BOOK,null=False,blank=False)
    Author=models.ForeignKey(AUTHORS,null=False,blank=False)

class BORROWER(models.Model):
    Card_no=models.CharField(max_length=200,primary_key=True)
    Ssn=models.CharField(max_length=200)
    Fname=models.CharField(max_length=200)
    Lname=models.CharField(max_length=200)
    Address=models.CharField(max_length=200)
    Phone=models.CharField(max_length=200)

    def __str__(self):
        return self.Fname+" "+self.Lname


class BOOK_LOANS(models.Model):
    Loan_id=models.AutoField(primary_key=True)
    Isbn=models.ForeignKey(BOOK,null=False,blank=False)
    Branch=models.ForeignKey(LIBRARY_BRANCH,null=False,blank=False)
    Card_no=models.ForeignKey(BORROWER,null=False,blank=False)
    Date_out=models.DateField()
    Date_in=models.DateField()
    Date_due=models.DateField()

class FINES(models.Model):
    Loan=models.ForeignKey(BOOK_LOANS,null=False,blank=False)
    fine_amt=models.CharField(max_length=200)
    paid=models.IntegerField()


class UserProfile(models.Model):
    User = models.OneToOneField(User)
    Fname = models.CharField(max_length=15, null=False, blank=False)
    Lname = models.CharField(max_length=60, null=False,default='', blank=False)
    Phone_no = models.CharField(max_length=15, null=False,default='', blank=False)
    Ssn = models.CharField(max_length=60, null=False,default='', blank=False)
    Address = models.CharField(max_length=60, null=False,default='', blank=False)
    Card_no = models.CharField(max_length=60, null=False, blank=False,primary_key=True)
    def __unicode__(self):
        return 'User profile: ' + self.user.username + ', ' + self.user.first_name + ' ' + self.user.last_name


class CurrentlyBorrowed(models.Model):
    Book=models.ForeignKey(BOOK,null=False,blank=False)
    Branch=models.ForeignKey(LIBRARY_BRANCH,null=False,blank=False)
    UserProfile=models.ForeignKey(UserProfile,null=False,blank=False)
    Fine=models.IntegerField(default=0)
    Date_out=models.DateField(_("Date"), default=datetime.date.today,null=False)




