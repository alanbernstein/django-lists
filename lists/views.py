from django.http import HttpResponse


# Create your views here.
def index(request):
    apps = ['books', 'movies', 'podcasts', 'games']
    resp = ''.join(['<a href="%s">%s</a><br />\n' % (a, a) for a in apps])
    return HttpResponse(resp)
