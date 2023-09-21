from django.contrib import admin

from .models import Person, Book, BorrowedBook, ReturnBook


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'number_of_available')

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('person', 'book', 'borrowed_date', 'must_return_date', 'actual_return_date', 'is_returned')


####
class BorrowedBookInline(admin.TabularInline):
    model = BorrowedBook
    extra = 0
class PersonAdmin(admin.ModelAdmin):
    inlines = [BorrowedBookInline]
###    

admin.site.register(Person, PersonAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowedBook, BorrowedBookAdmin)
admin.site.register(ReturnBook)