from django.core.exceptions import ViewDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, ListView


def index(request):
    return HttpResponse("Hello there, store e-commerce front coming  here...")


@csrf_exempt  # bez tego postman wali nam 403 na post zamiast 404 - django jest zabezpieczone wiec jak chcemy wyslac post to to dajemy
# @cache_page(900) # uwaga to działa kiepsko - do tego trzeba memcache server!!!!!
@gzip_page #gzip - obsluga wszystkich przegladarek, templatki mogą wtedy być przesyłane w zipie (szybciej działa - szybsze przesyłanieu )
@require_http_methods(["GET"])  # blokowanie inneych metod niz GET
def electronics(request):
    items = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
    print('dupa')
    if request.method == 'GET':
        paginator = Paginator(items, 2)  # dzielenie na podstrony
        pages = request.GET.get('page', 1)  # wysylamy requesta o pobranie pierwszej strony
        try:
            items = paginator.page(pages)
        except PageNotAnInteger:
            items = paginator.page(1)

        return render(request, 'my_store/list.html', {'items': items})
        # przekazujemy obiekt typu page dlatego item.has_other_pages atrybut jest w nim
    elif request.method == 'POST':
        return HttpResponseNotFound("Page not  Found")


def detail(request):
    return HttpResponse("Hello there, store e-commerce detail page...")


#
# def error_handler(request, exception=None):
#     return HttpResponseNotFound('<h1> Page not Found </h1>', status=404)
#
#
# # TODO check required params
# def page_not_found(request, exception):
#     raise ViewDoesNotExist
class ElectronicsView(View):

    def get(self, request):
        items = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
        paginator = Paginator(items, 2)  # dzielenie na podstrony
        pages = request.GET.get('page', 1)  # wysylamy requesta o pobranie pierwszej strony
        self.process()
        try:
            items = paginator.page(pages)
        except PageNotAnInteger:
            items = paginator.page(1)

        return render(request, 'my_store/list.html', {'items': items})

    @staticmethod
    def process():
        print('Electronic')


class ElectronicsView2(TemplateView):
    template_name = 'my_store/list.html'

    def get_context_data(self, **kwargs):
        items = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
        context = {"items": items}
        return context


class ElectronicsView3(ListView):
    template_name = 'my_store/list.html'
    queryset = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
    context_object_name = 'items'
    paginate_by = 2


class ComputerView(ElectronicsView):
    @staticmethod
    def process():
        print('Computer')


class MobileView():
    @staticmethod
    def process():
        print('Mobile')


class EquipmentView(MobileView, ComputerView):
    @staticmethod
    def process():
        print('Equipment')
