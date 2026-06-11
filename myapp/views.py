from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.paginator import Paginator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers
import logging
from django.utils import timezone


logger = logging.getLogger(__name__)

# # Create your views here.
# @cache_page(60 * 15)
# @vary_on_headers('User-Agent')
def index(request):
    logger.info("fetching all items from the database")
    logger.info(f"User [{timezone.now().isoformat()}]{request.user} requested item list from {request.META.get('REMOTE_ADDR')}")
    item_list = Item.objects.all().order_by('-id')
    logger.debug(f" found {item_list.count()} items")
    paginator = Paginator(item_list,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'myapp/index.html',{'page_obj':page_obj})
# 

# class IndexClassView(LoginRequiredMixin,ListView):
#     model = Item
#     template_name = 'myapp/index.html'
#     context_object_name = 'items'
#     login_url = 'users:login'


@login_required(login_url='users:login')
def detail(request,id):
    logger.info(f"Fetching an item with id:{id}")
    try:
        item = get_object_or_404(Item,pk=id)
        logger.debug(f"Item found {item.item_name} (${item.item_price})")
    except Exception as e:
        logger.error(f"Error fetching the item %s:%s",id,e)
        raise
    return render(request,'myapp/detail.html',{'item':item})

# class FoodDetail(LoginRequiredMixin,DetailView):
#     model = Item
#     template_name = 'myapp/detail.html'
#     context_object_name = 'item'
#     login_url = 'users:login'


# @login_required(login_url='users:login')
# def create_item(request):
#     if request.method == 'POST':
#         fm = ItemForm(request.POST,request.FILES)
#         if fm.is_valid():
#             fm.save()
#             return redirect('/')
#     else:
#         fm = ItemForm()

#     return render(request,'myapp/item_form.html',{'form': fm}) 

class ItemCreateView(LoginRequiredMixin,CreateView):
    model = Item
    form_class = ItemForm
    # fields = ['item_name','item_desc','item_price','item_image']
    template_name = 'myapp/item_form.html'
    login_url = 'users:login'
    # success_url = reverse_lazy('myapp:index')
    def form_valid(self,form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)


# def update_item(request,id):
#     item = get_object_or_404(Item,id=id)
#     if request.method == 'POST':
#         fm = ItemForm(request.POST,request.FILES,instance=item)
#         if fm.is_valid():
#             fm.save()
#             return redirect('myapp:index')
#     else:
#         fm = ItemForm(instance=item)

#     return render(request,'myapp/edit_form.html',{'form':fm})

class UpdateItem(LoginRequiredMixin,UpdateView):
    model = Item
    form_class = ItemForm
    template_name ='myapp/edit_form.html'
    login_url = 'users:login'

    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)





# def delete_item(request,id):
#     item = get_object_or_404(Item,id=id)
#     if request.method == "POST":
#         item.delete()
#         return redirect('myapp:index')
#     return render(request, 'myapp/confirm_delete.html', {'item': item})


class DeleteItem(DeleteView):
    model = Item
    template_name = 'myapp/confirm_delete.html'
    success_url = reverse_lazy('myapp:index')

    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)