from django.shortcuts import render, redirect
from .forms import ContactosForm

def contactos(request):
    if request.method == 'POST':
        form = ContactosForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contacto_exito.html')
    else:
        form = ContactosForm()
    return render(request, 'contacto.html', {'form': form})