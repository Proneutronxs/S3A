from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import *
from django.db import connections
from django.http import JsonResponse
import datetime
from Applications.RRHH.views import buscaDatosParaInsertarHE, obtener_fecha_hora_actual_con_milisegundos, insertaHorasExtras

# Create your views here.


@login_required
@permission_required('Frio.puede_ingresar', raise_exception=True)
def Frio(request):
    return render (request, 'Frio/frio.html')


def HorasExtrasFrio(request):
    return render (request, 'Frio/HorasExtras/horasExtrasFrio.html')

def AutorizaHorasExtrasFrio(request):
    return render (request, 'Frio/HorasExtras/autorizaHorasExtras.html')


@login_required
@csrf_exempt
def cargaCentrosCostosFrio(request):### CAMBIO A CENTRO DE COSTOS MUESTRA LOS CENTROS DE COSTOS CARGADOS
    if request.method == 'GET':
        try:
            data = buscaCentroCostosFrioIDDescripHE()
            if data:
                return JsonResponse({'Message': 'Success', 'Datos': data})
            else:
                data = "No se encontraron Centros de Costos Asignados."
                return JsonResponse({'Message': 'Error', 'Nota': data})                
        except Exception as e:
            data = str(e)
            insertar_registro_error_sql("Frio","cargaCCFrio",request.user,data)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
def buscaCentroCostosFrioIDDescripHE():
    listado =  buscaCentroCostosFrioHE()
    lista_json = []
    for item in listado:
        try:
            with connections['ISISPayroll'].cursor() as cursor:
                sql = "SELECT Regis_CCo, DescrCtroCosto " \
                    "FROM CentrosCostos " \
                    "WHERE Regis_CCo = %s"
                cursor.execute(sql,[item])
                consulta = cursor.fetchone()
                if consulta:
                    ids = str(consulta[0])
                    cc = str(consulta[1])
                    data = {'cc':cc, 'id':ids}
                    lista_json.append(data)
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("Frio","buscaCentroCostosFrioIDDescrip","usuario",error)
            return lista_json
        finally:
            cursor.close()
            connections['ISISPayroll'].close()
    return lista_json

def buscaCentroCostosFrioHE():
    data = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Texto " \
                "FROM Parametros_Aplicativo " \
                "WHERE Codigo = 'APP-F-IDCC'"
            cursor.execute(sql)
            consulta = cursor.fetchone()
            if consulta:
                data = str(consulta[0]).split('-')
                return data
            else:
                return data
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("Frio","buscaCentroCostosFrio","usuario",error)
        return data
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

@login_required
@csrf_exempt
def mostrarHorasCargadasPorCCFrio(request): ### MUESTRA LA TABLA DE HORAS
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Frio.puede_ver')
        if user_has_permission:
            cc = request.POST.get('ComboxTipoCCAutorizaFrio')
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = "SELECT     RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, CONVERT(VARCHAR(10), " \
                                        "HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5), " \
                                        "HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5), HorasExtras_Procesadas.CantidadHoras) AS HORAS, " \
                                        "RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, HorasExtras_Procesadas.ID_HEP AS idHoras, TresAses_ISISPayroll.dbo.CentrosCostos.DescrCtroCosto AS CENTROCOSTOS, (SELECT CONVERT(VARCHAR(21),ApellidoEmple + ' ' + NombresEmple) " \
                                        "FROM TresAses_ISISPayroll.dbo.Empleados " \
                                        "WHERE CodEmpleado = HorasExtras_Procesadas.UsuarioEncargado) AS SOLICITA, HorasExtras_Procesadas.EstadoEnvia " \
                        "FROM        TresAses_ISISPayroll.dbo.CentrosCostos INNER JOIN " \
                                        "S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                        "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                        "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                        "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado ON " \
                                        "TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo = TresAses_ISISPayroll.dbo.Empleados.Regis_CCo " \
                        "WHERE     (TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo = %s) --AND (HorasExtras_Procesadas.EstadoEnvia = '3') " \
                        "ORDER BY LEGAJO, HorasExtras_Procesadas.FechaHoraDesde"
                    cursor.execute(sql, [cc])
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
                            centro = str(i[12])
                            solicita = str(i[13])
                            datos = {'ID':idHoras,'tipo':tipo, 'legajo':legajo, 'nombres':nombres, 'desde':desde, 'hasta':hasta, 'motivo':motivo, 'descripcion':descripcion, 'horas':horas , 'centro': centro, 'solicita': solicita}
                            #print(datos)
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Datos': data})
                    else:
                        data = "No se encontrarón horas extras procesadas."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("Frio","mostrarHorasCargadasPorCCFrio",request.user,error)
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    

def eliminaHorasEstadoHEP(ID_HEP):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE HorasExtras_Procesadas SET EstadoEnvia = '8' WHERE ID_HEP = %s"
            cursor.execute(sql, [ID_HEP])
            
            slq2 = "UPDATE HorasExtras_Sin_Procesar SET Estado='8' WHERE ID_HESP = (SELECT ID_HESP FROM HorasExtras_Procesadas WHERE ID_HEP = %s)"
            cursor.execute(slq2, [ID_HEP])
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("Frio","eliminaHorasEstadoHEP","usuario",error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

@login_required
@csrf_exempt
def eliminaHorasSeleccionadasFrio(request): ### ELIMINA LAS HORAS SELECCIONADAS
    if request.method == 'POST':   ### METODO POST PUT DELETE GET
        user_has_permission = request.user.has_perm('Frio.puede_denegar')
        if user_has_permission:
            checkboxes_tildados = request.POST.getlist('idCheck')
            resultados = []
            for i in checkboxes_tildados:
                ID_HEP = str(i) 
                resultado = eliminaHorasEstadoHEP(ID_HEP)
                resultados.append(resultado)
            if 0 in resultados:
                data = "Se produjo un Error en alguna de las eliminaciones."
                return JsonResponse({'Message': 'Error', 'Nota': data})
            else:
                data = "Las horas se eliminaron correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': data})
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'}) 
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


@login_required
@csrf_exempt
def autorizaHorasCargadas(request): ### INSERTA LAS HORAS SELECCIONADAS
    if request.method == 'POST': 
        user_has_permission = request.user.has_perm('Frio.puede_autorizar') 
        if user_has_permission: 
            usuario = str(request.user)
            checkboxes_tildados = request.POST.getlist('idCheck')
            resultados = []
            importe = "0"
            pagada = "N"
            for i in checkboxes_tildados:
                ID_HEP = str(i) 
                fecha_y_hora = str(obtener_fecha_hora_actual_con_milisegundos())
                Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora = buscaDatosParaInsertarHE(ID_HEP) 
                resultado = insertaHorasExtras(ID_HEP,Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora, importe, pagada, fecha_y_hora,usuario.upper())
                resultados.append(resultado)

            if 0 in resultados:
                data = "Se produjo un Error en alguna de las inserciones."
                return JsonResponse({'Message': 'Error', 'Nota': data})
            else:
                data = "Las horas se autorizaron correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': data})
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'}) 
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

def autorizaHorasEstadoHEP(ID_HEP):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE HorasExtras_Procesadas SET EstadoEnvia = '1' WHERE ID_HEP = %s"
            cursor.execute(sql, [ID_HEP])
            #return True
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("Empaque","autorizaHorasEstadoHEP","usuario",error)
        #return False
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()































