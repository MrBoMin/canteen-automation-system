from django.shortcuts import render,get_object_or_404
from .models import MenuItem

def menu_list_view(request):
    all_menu_items = MenuItem.objects.all()
    return render(request, 'menu/menu.html', {'menu_items': all_menu_items})


def menu_detail_view(request, pk): 
    menu_item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'menu/menuDetail.html', {'menu_item': menu_item})

def footer_view(request):
    return render(request, 'footer.html')


def header_view(request):
    return render(request, 'header.html')

