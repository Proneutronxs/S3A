from django.shortcuts import render
from S3A.funcionesGenerales import *
from Applications.Inicio.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.


def inicioSesion(request):
    return render (request, 'Inicio/index.html')

def repassword(request):
    return render (request, 'Inicio/repass.html')


@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)
            
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user)

            if not user_profile.password_changed:
                data = "repassword/"
                return JsonResponse({'Message': 'Change', 'data': data})
            else:
                data = "Se inicio sesion."
                return JsonResponse({'Message': 'success', 'data': data})
            
        else:
            data = "No se pudo iniciar sesión, verifique los datos."
            return JsonResponse({'Message': 'Error', 'data': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required
@csrf_exempt
def cambiar_password(request):
    if request.method == 'POST':
        try:
            user = request.user
            current_password = request.POST.get('currentPassword')
            new_password = request.POST.get('newPassword')
            if not user.check_password(current_password):
                return JsonResponse({'Message': 'Error', 'Nota': 'La contraseña actual es incorrecta.'})
            if current_password == new_password:
                return JsonResponse({'Message': 'Error', 'Nota': 'La contraseña no puede ser igual a la actual.'})
            
            try:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.password_changed = True
                user_profile.save()
                user.set_password(new_password)
                user.save()

                ### REGISTRO INICIO ###

                insertar_registro_pass(user,current_password,new_password)

                ### REGISTRO FIN ###

                data = "Se cambió la contraseña correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': data})
            
            except Exception as e:
                insertar_registro_error_sql("Inicio","Cambiar_Password",request.user,str(e))
                data = "El Usuario no Existe."
                return JsonResponse({'Message': 'Error', 'Nota': data})
            
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        data = "No se pudo resolver la petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
