from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta

class BookCategory(models.Model):
    name = models.CharField(max_length=100,primary_key=True,blank=False)

# books model
class Book(models.Model): 
    isbn = models.CharField(max_length=13,primary_key=True,blank=False) # International Standard Book Number 
    title = models.CharField(max_length=255,blank=False) # Title of the book
    author = models.CharField(max_length=255,blank=False) # Author(s) of the book
    genre = models.ForeignKey(BookCategory,on_delete=models.CASCADE) # Genre or category of the book
    publication_year = models.IntegerField(blank=False) # Year the book was published
    publisher = models.CharField(max_length=100,blank=False) # Publisher of the book
    shelf_location = models.CharField(max_length=50,blank=False) # Physical location of the book on the library shelf
    is_available = models.BooleanField(default=True) # Indicates whether the book is currently in shelf
    date_added = models.DateField() #Date the book was added to the library
    borrowing_count = models.IntegerField(default=0) # Count of times the book has been borrowed
    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE) # assigned borrower
    book = models.ForeignKey(Book, on_delete=models.CASCADE) # the book borrowed
    borrow_date = models.DateField(null=False) # date borrowed
    due_date = models.DateField(null=False) # the due date
    return_date = models.DateField(null=False, blank=False) # returning date
    overdue_fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) # fine

    def calculate_overdue_fine(self):
        if self.return_date and self.return_date > self.due_date:
            #calculating the overdue days
            overdue_days = (self.return_date - self.due_date).days
            # Assuming the fine is 5 KSH per day
            self.overdue_fine = overdue_days * 5.0
        else:
            # the book is not overdue
            self.overdue_fine = 0.0

    def set_book_unavailable(self):
        # Set the availability status of the book to False when borrowed
        self.book.is_available = False
        self.book.save()

    def increment_borrowing_count(self):
        # Increment the borrowing count of the book
        self.book.borrowing_count += 1
        self.book.save()

    def save(self, *args, **kwargs):
        self.calculate_overdue_fine()
        self.set_book_unavailable()
        self.increment_borrowing_count()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.borrower.username} - {self.book.title} ({self.borrow_date} to {self.due_date})"