from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Applications.RRHH.views import buscaDatosParaInsertarHE, obtener_fecha_hora_actual_con_milisegundos, insertaHorasExtras
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
import datetime 

from django.db import connections
from django.http import JsonResponse

# Create your views here.

### RENDERIZADO DE EMPAQUE
#@login_required
#@permission_required('Empaque.puede_ingresar', raise_exception=True)
def Empaque(request):
    return render (request, 'Empaque/empaque.html')

def HorasExtrasEmpaque(request):
    return render (request, 'Empaque/HorasExtras/horasExtrasEmpaque.html')

def AutorizaHorasExtrasEmpaque(request):
    return render (request, 'Empaque/HorasExtras/autorizaHorasExtras.html')

##LLAMA A LAS HORAS EXTRAS

@csrf_exempt
def cargaLegajosEmpaque(request):
    if request.method == 'GET':
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "SELECT DISTINCT " \
                                                "HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), CONVERT(VARCHAR(5), HorasExtras_Procesadas.Legajo) + ' - ' + TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS DATOS " \
                        "FROM            TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo " \
                        "WHERE (HorasExtras_Procesadas.EstadoEnvia = '3') AND (HorasExtras_Procesadas.Sector = 'E')"
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    data = []
                    for i in consulta:
                        legajo = str(i[0])
                        nombres = str(i[1])
                        datos = {'legajo':legajo, 'nombres':nombres}
                        data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': data})
                else:
                    data = "No se encontraron horas extras procesadas."
                    return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

###BUSCA POR EL LAGJO DEL SPINNER
@csrf_exempt
def mostrarHorasCargadasPorLegajoEmpaque(request):
    if request.method == 'POST':
        legajo = request.POST.get('ComboxTipoLegajoAutorizaEmpaque')
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "SELECT        RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, " \
                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, " \
                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, " \
                                                "RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5), HorasExtras_Procesadas.CantidadHoras) AS HORAS, RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, HorasExtras_Procesadas.ID_HEP AS idHoras " \
                        "FROM            S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                                "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON  " \
                                                "S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado " \
                        "WHERE        (HorasExtras_Procesadas.Legajo = %s) AND (HorasExtras_Procesadas.EstadoEnvia = '3') AND (HorasExtras_Procesadas.Sector = 'E') " \
                        "ORDER BY HorasExtras_Procesadas.Legajo, HorasExtras_Procesadas.FechaHoraDesde"
                cursor.execute(sql, [legajo])
                consulta = cursor.fetchall()
                if consulta:
                    data = []
                    for i in consulta:
                        tipo = str(i[0])
                        legajo = str(i[1])
                        nombres = str(i[2])
                        desde = str(i[3]) + " - " + str(i[4])
                        hasta = str(i[5]) + " - " + str(i[6])
                        motivo = str(i[7])
                        descripcion = str(i[8])
                        horas = str(i[9])
                        idHoras = str(i[11])
                        datos = {'ID':idHoras,'tipo':tipo, 'legajo':legajo, 'nombres':nombres, 'desde':desde, 'hasta':hasta, 'motivo':motivo, 'descripcion':descripcion, 'horas':horas}
                        data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': data})
                else:
                    data = "No se encontrarón horas extras procesadas."
                    return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


@csrf_exempt
def autorizaHorasCargadas(request):
    if request.method == 'POST':
        checkboxes_tildados = request.POST.getlist('idCheck')
        resultados = []
        importe = "0"
        pagada = "N"
        for i in checkboxes_tildados:
            ID_HEP = str(i) 
            fecha_y_hora = str(obtener_fecha_hora_actual_con_milisegundos())
            Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora = buscaDatosParaInsertarHE(ID_HEP) 
            resultado = insertaHorasExtras(ID_HEP,Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora, importe, pagada, fecha_y_hora)
            resultados.append(resultado)

        if 0 in resultados:
            data = "Se produjo un Error en alguna de las inserciones."
            return JsonResponse({'Message': 'Error', 'Nota': data})
        else:
            data = "Las horas se autorizaron correctamente."
            return JsonResponse({'Message': 'Success', 'Nota': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

def autorizaHorasEstadoHEP(ID_HEP):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE HorasExtras_Procesadas SET EstadoEnvia = '1' WHERE ID_HEP = %s"
            cursor.execute(sql, [ID_HEP])
    except Exception as e:
        error = str(e)
        print(error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

def eliminaHorasEstadoHEP(ID_HEP):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE HorasExtras_Procesadas SET EstadoEnvia = '8' WHERE ID_HEP = %s"
            cursor.execute(sql, [ID_HEP])
            
            slq2 = "UPDATE HorasExtras_Sin_Procesar SET Estado='8' WHERE ID_HESP = (SELECT ID_HESP FROM HorasExtras_Procesadas WHERE ID_HEP = %s)"
            cursor.execute(slq2, [ID_HEP])
    except Exception as e:
        error = str(e)
        print(error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

@csrf_exempt
def eliminaHorasSeleccionadas(request):
    if request.method == 'POST':
        checkboxes_tildados = request.POST.getlist('idCheck')
        resultados = []
        for i in checkboxes_tildados:
            ID_HEP = str(i) 
            eliminaHorasEstadoHEP(ID_HEP)

        if 0 in resultados:
            data = "Se produjo un Error en alguna de las inserciones."
            return JsonResponse({'Message': 'Error', 'Nota': data})
        else:
            data = "Las horas se eliminaron correctamente."
            return JsonResponse({'Message': 'Success', 'Nota': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})






































