from __future__ import unicode_literals

from django.db import models

from taggit.managers import TaggableManager
import django_tables2 as tables
# NOTE: need to support these tag operations:
# - get all tags for given CreativeWork
# - get all CreativeWorks for given Tag


# abstract media models
class Creator(models.Model):
    # abstract
    name = models.CharField(max_length=300)

    def __str__(self):
        return '%s' % self.name


class CreativeWork(models.Model):
    # abstract
    title = models.CharField(max_length=300)
    tags = TaggableManager()
    entry_created = models.DateTimeField(auto_now_add=True)  # as opposed to 'work_created'
    entry_updated = models.DateTimeField(auto_now=True)
    # book = Book.objects.create(name='name')
    # book.tags.add('scifi', 'fantasy')
    # book.tags.remove('scifi')
    # book.tags.all()
    # Book.objects.filter(tags__name__in=["red"])

    def __str__(self):
        return '%s' % self.title


# extrinsic property models
class Award(models.Model):
    # maybe a hugo-winner tag would be better?
    source = models.CharField(max_length=300)  # e.g. 'Hugo'
    award_name = models.CharField(max_length=300, default='winner')  # e.g. 'Winner'
    work = models.ForeignKey(CreativeWork)


class Rating(models.Model):
    source = models.CharField(max_length=100)  # e.g. amazon, imdb
    value = models.FloatField()
    work = models.ForeignKey(CreativeWork)


# the good stuff
class Author(Creator):
    pass


class Book(CreativeWork):
    pub_year = models.DateField('year published', null=True, blank=True)
    author = models.ForeignKey(Author, null=True, blank=True)
    have_read = models.NullBooleanField()

    # TODO: add abandoned status
    NOT_READING, ACTIVE, DORMANT, ABANDONED = 0, 1, 2, 3
    STATUS_CHOICES = ((NOT_READING, 'not reading'), (ACTIVE, 'reading'), (DORMANT, 'dormant'), (ABANDONED, 'abandoned'))
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=NOT_READING)

    # priority level?


# this just converts the book model directly to a table structure
class BookTable(tables.Table):
    class Meta:
        model = Book


# this is more finely controlled, combines data from Book and Reading in a smarter way
class BookInfoTable(tables.Table):
    index = tables.Column()
    title = tables.Column()
    author = tables.Column()
    status = tables.Column()
    tags = tables.Column()
    last_read = tables.Column()

    class Meta:
        # html table attributes
        attrs = {'class': 'display', 'id': 'booktable'}
        orderable = False  # disable django-table2's sorting links (using datatables in js instead)


# TODO: inherit from AbstractConsumption or something
class Reading(models.Model):
    # in the sense of 'a reading of a book' - might want to change to 'Read')
    book = models.ForeignKey(Book)
    start_date = models.DateTimeField('start date', null=True, blank=True)
    end_date = models.DateTimeField('end date', null=True, blank=True)
    rating = models.IntegerField(default=-1, null=True, blank=True)  # 0-10, -1=unrated
    notes = models.TextField(null=True, blank=True)

    PAPER, EBOOK, AUDIO = 0, 1, 2
    FORMAT_CHOICES = ((PAPER, 'paper'), (EBOOK, 'ebook'), (AUDIO, 'audiobook'))
    format = models.SmallIntegerField(choices=FORMAT_CHOICES, default=AUDIO)

    LOW, MEDIUM, HIGH = 0, 1, 2
    FOCUS_CHOICES = ((LOW, 'low'), (MEDIUM, 'medium'), (HIGH, 'high'))
    focus = models.SmallIntegerField(choices=FOCUS_CHOICES, default=MEDIUM)

    def __str__(self):
        book = Book.objects.get(id=self.book.id)
        return '%s - %s' % (book.title, self.end_date)



def export_to_org_table(self, fname=None):
    pass



# class AbstractSeries(models.Model):
#     # this could just be a tag?
#     """Represents a logical grouping of media items:
#     - tv series or tv season
#     - movie series
#     - book series
#     - podcast series
#     not mutually exclusive - one item can belong to multiple series"""
#     pass
