#from django.shortcuts import render
from string import capwords

from django.http import HttpResponse
from django.core.urlresolvers import resolve
from django.shortcuts import render

from books.models import Book, Reading, Author, BookTable, BookInfoTable

# how to get a nice sortable, searchable table?
# - https://www.datatables.net/manual/installation - nice for frontend
# - https://github.com/bradleyayers/django-tables2/ - nice for backend

# - https://pypi.python.org/pypi/django-sorting-bootstrap
# - https://github.com/shymonk/django-datatable - "mainly for the purpose of learning""

# charts?
# http://www.chartjs.org/


def data_table_view_basic(request):
    # django-tables2
    queryset = Book.objects.all()
    table = BookTable(queryset)
    return render(request, 'datatable-basic.html', {'table': table})


def data_table_view_tweaked(request):
    # django-tables2
    # table can be a list of dicts
    #
    # TODO: change styles
    rows = get_books_info_v2()
    table = BookInfoTable(rows)
    return render(request, 'datatable-tweaked.html', {'table': table})


def simple_table_view(request):
    data = '%s<br>\n' % request.resolver_match.url_name
    data += '%s<br>\n' % request.get_full_path()
    data += 'books<br>\n<hr>\n'

    data += get_books_info_v1()
    return HttpResponse(data)


def index(request):
    # return simple_table_view(request)
    return data_table_view_tweaked(request)


def unread(request):
    rows = get_books_info_v2()
    table = BookInfoTable(rows)
    return render(request, 'datatable-tweaked.html', {'table': table})


def get_books_info_v2():
    rows = []
    for book in Book.objects.all():
        row = {}
        row['title'] = capwords(book.title)

        taglist = [t.name for t in book.tags.all()]
        row['tags'] = ', '.join(taglist)

        if book.author:
            row['author'] = capwords(book.author.name)
        else:
            row['author'] = '?'

        readings = Reading.objects.filter(book_id=book.id)
        if readings:
            last_reading = readings[len(readings) - 1]
            if last_reading.end_date:
                row['status'] = 'done'
                row['last_read'] = last_reading.end_date.strftime('%Y/%m')
            elif not last_reading.end_date and last_reading.start_date:
                started = last_reading.start_date
                row['status'] = 'reading'
            else:
                row['status'] = '???'
        else:
            row['status'] = 'to read'

        rows.append(row)

    return rows


def get_books_info_v1():
    books = Book.objects.all()
    allreadings = Reading.objects.all()

    data = ''
    for book in books:
        readings = [r for r in allreadings if r.book.id == book.id]

        if readings:
            read_str = 'last read %s' % readings[-1].end_date
        else:
            read_str = 'never read'

        data += '%s (%s)<br>\n' % (book.title, read_str)

    return data
