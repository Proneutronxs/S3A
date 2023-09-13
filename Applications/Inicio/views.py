from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.


def inicioSesion(request):
    return render (request, 'Inicio/index.html')


@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("INICIO SESION")
            data = "Se inicio sesion."
            #return JsonResponse({'Message': 'success', 'data': data})
            return redirect('rrhh/')  # Reemplaza 'ruta_deseada' por la URL a la que deseas redirigir
        else:
            print("INICIO FALLIDO")
            data = "No se pudo iniciar sesión, verifique los datos."
            return JsonResponse({'Message': 'Error', 'data': data})
    else:
        return render(request, 'tu_template_de_login.html')
