from django.core.management.base import BaseCommand, CommandError
from books.models import Book, Reading, Author
from taggit.models import Tag

import dateparser
from datetime import datetime
import re

from orgtools import parse_org_table
from panda.debug import debug, jprint


# cd ~/d/src/py/django/lists && python manage.py import_from_orgtable

class Command(BaseCommand):
    help = 'Imports data from an org-mode table'

    def add_arguments(self, parser):
        parser.add_argument('--filename', default=None)

    def handle(self, *args, **options):

        Book.objects.all().delete()
        Reading.objects.all().delete()  # TODO: get rid of this...

        # parse file to a list of dicts
        fname = options['filename'] or '/u/a/d/txt/todo/read.txt'
        with open(fname, 'r') as f:
            data = f.read()
            lines = data.split('\n')

        rows = parse_org_table(lines)

        print('%d lines -> %d rows' % (len(lines), len(rows)))

        author_field_map = {'author': 'name'}
        book_field_map = {'title': 'title',
                          'tags': 'tags'}  # org-table field name : django model field name
        # TODO: handle status
        reading_field_map = {'finish date': 'end_date',
                             'start date': 'start_date',
                             'focus': 'focus',
                             'rating': 'rating',
                             'read medium': 'format',
                             'notes': 'notes'}
        other_field_map = {'hugo year': 'hugo'}

        # convert each dict to a set of django objects, save them
        for row in rows:
            row = {k: v for k, v in row.items() if v}
            # parse strings to other types
            if 'finish date' in row:
                row['finish date'], info = parse_date(row['finish date'])
            if 'start date' in row:
                row['start date'], info = parse_date(row['start date'])
            if 'rating' in row:
                row['rating'] = int(row['rating'])

            # split up among models
            translate = lambda row, map: {map[k]: v for k, v in row.items() if k in map}
            book_data = translate(row, book_field_map)
            reading_data = translate(row, reading_field_map)
            author_data = translate(row, author_field_map)
            other_data = translate(row, other_field_map)

            if 'title' not in book_data:
                continue

            print(book_data)
            book, _ = Book.objects.get_or_create(title=book_data['title'])
            if 'tags' in row:
                tagstr = row['tags']
                taglist = tagstr.split(',')
                taglist = [t.strip() for t in taglist]
                book.tags.add(*taglist)

            if 'name' in author_data:
                author, _ = Author.objects.get_or_create(**author_data)
                book.author_id = author.id
                author.save()

            if 'end_date' in reading_data:
                print(reading_data)
                reading, _ = Reading.objects.get_or_create(book_id=book.id, end_date=reading_data['end_date'])
                reading.save()

            book.save()

        debug()


def parse_date(strng):
    date = None
    info = ''
    if '?' in strng:
        info = 'uncertain'
    elif strng == '-':
        info = 'gave up'
    else:
        parts = map(int, strng.split('/'))
        while len(parts) < 3:
            parts.append(1)
        date = datetime(*parts)

    return date, info


# def parse_org_table(lines):
#     # return a list of:
#     #  dict like header:value
#     header_fields = {}
#     rows = []
#     for line in lines:
#         # skip extraneous lines
#         if not line or not line[0] == '|' or line[1] == '-':
#             continue

#         # skip width-limiting lines
#         if re.search('<[0-9]*>', line):
#             continue

#         # get header row
#         fields = line.split('|')
#         fields = [field.strip() for field in fields]
#         if not header_fields:
#             header_fields = fields
#             continue

#         # parse entry lines
#         row = {k: v for k, v in zip(header_fields, fields)}
#         row['raw'] = line
#         rows.append(row)

#     return rows
