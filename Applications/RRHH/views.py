from django.shortcuts import render
from S3A.funcionesGenerales import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime 

from django.db import connections
from django.http import JsonResponse

def funcionGeneralPermisos(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Empaque.puede_ver')
        if user_has_permission:
            pass
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

# Create your views here.
### RENDERIZADO DE RRHH 
@login_required
def RRHH(request):
    return render (request, 'RRHH/rrhh.html')

### RENDERIZADO DE HORAS EXTRAS
def horasExtras(request):
    return render (request, 'RRHH/HorasExtras/horasExtras.html')

### RENDERIZADO DE HORAS EXTRAS TRANSFERENCIA
def transferenciaHorasExtras(request):
    return render (request, 'RRHH/HorasExtras/transferirhe.html')

def obtener_fecha_hora_actual_con_milisegundos():
    now = datetime.datetime.now()
    fecha_hora_actual = now.strftime("%Y-%m-%dT%H:%M:%S")
    hora = str(fecha_hora_actual) + ".000"
    return hora

@login_required
@csrf_exempt
def mostrarHorasCargadas(request): ### MUESTRA HORAS PROCESADAS POR SECTOR Y TIPO DE HORA
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('RRHH.puede_ver')
        if user_has_permission:
            tipo = request.POST.get('ComboxTipoHoraTransf')
            sector =request.POST.get('ComboxSectorHEHoras')
            if tipo == 'N50':
                try:
                    with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                        sql = "SELECT        RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), " \
                                                    "TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, TresAses_ISISPayroll.dbo.CentrosCostos.DescrCtroCosto AS CENTRO_COSTOS, CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE,  " \
                                                    "CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5),  " \
                                                    "HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5),  " \
                                                    "HorasExtras_Procesadas.CantidadHoras) AS HORAS, RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, HorasExtras_Procesadas.ID_HEP AS idHoras, (SELECT CONVERT(VARCHAR(21),ApellidoEmple + ' ' + NombresEmple) FROM TresAses_ISISPayroll.dbo.Empleados WHERE CodEmpleado = HorasExtras_Procesadas.UsuarioEncargado) AS SOLICITA, ISNULL(ImpArreglo, '0') AS ImpArreglo " \
                            "FROM            TresAses_ISISPayroll.dbo.CentrosCostos INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                    "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                    "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON  " \
                                                    "S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado ON TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo = TresAses_ISISPayroll.dbo.Empleados.Regis_CCo " \
                            "WHERE        (HorasExtras_Procesadas.Sector = 'C') AND (HorasExtras_Procesadas.TipoHoraExtra = 'N') AND (DATEPART(WEEKDAY, HorasExtras_Procesadas.FechaHoraDesde) >= 2 AND DATEPART(WEEKDAY, HorasExtras_Procesadas.FechaHoraDesde) <= 6) " \
                            "AND (HorasExtras_Procesadas.EstadoEnvia = '1') " \
                            "ORDER BY LEGAJO, HorasExtras_Procesadas.FechaHoraDesde"
                        cursor.execute(sql)
                        consulta = cursor.fetchall()
                        if consulta:
                            data = []
                            for i in consulta:
                                tipo = str(i[0])
                                legajo = str(i[1])
                                nombres = str(i[2])
                                centro = str(i[3])
                                desde = str(i[4]) + " - " + str(i[5])
                                hasta = str(i[6]) + " - " + str(i[7])
                                motivo = str(i[8])
                                descripcion = str(i[9])
                                horas = str(i[10])
                                idHoras = str(i[12])
                                solicita = str(i[13])
                                importe = str(i[14])
                                datos = {'ID':idHoras,'tipo':tipo, 'legajo':legajo, 'nombres':nombres, 'centro': centro, 'desde':desde, 'hasta':hasta, 'motivo':motivo, 'descripcion':descripcion, 'horas':horas, 'importe': importe, 'solicita': solicita}
                                data.append(datos)
                            return JsonResponse({'Message': 'Success', 'Datos': data})
                        else:
                            data = "No se encontrarón horas extras procesadas."
                            return JsonResponse({'Message': 'Error', 'Nota': data})
                except Exception as e:
                    insertar_registro_error_sql("RRHH","mostrarHorasCargadas",request.user,str(e))
                    data = str(e)
                    return JsonResponse({'Message': 'Error', 'Nota': data})
                finally:
                    connections['TRESASES_APLICATIVO'].close()
            if tipo == 'N100':
                try:
                    with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                        sql = "SELECT        RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), " \
                                                    "TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, TresAses_ISISPayroll.dbo.CentrosCostos.DescrCtroCosto AS CENTRO_COSTOS, CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE,  " \
                                                    "CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5),  " \
                                                    "HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5),  " \
                                                    "HorasExtras_Procesadas.CantidadHoras) AS HORAS, RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, HorasExtras_Procesadas.ID_HEP AS idHoras, (SELECT CONVERT(VARCHAR(21),ApellidoEmple + ' ' + NombresEmple) FROM TresAses_ISISPayroll.dbo.Empleados WHERE CodEmpleado = HorasExtras_Procesadas.UsuarioEncargado) AS SOLICITA, ISNULL(ImpArreglo, '0') AS ImpArreglo  " \
                            "FROM            TresAses_ISISPayroll.dbo.CentrosCostos INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                    "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                    "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON  " \
                                                    "S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado ON TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo = TresAses_ISISPayroll.dbo.Empleados.Regis_CCo " \
                            "WHERE        (HorasExtras_Procesadas.Sector = 'C') AND (HorasExtras_Procesadas.TipoHoraExtra = 'N') AND (DATEPART(WEEKDAY, HorasExtras_Procesadas.FechaHoraDesde) IN (1, 7)) " \
                            "AND (HorasExtras_Procesadas.EstadoEnvia = '1') " \
                            "ORDER BY LEGAJO, HorasExtras_Procesadas.FechaHoraDesde"
                        cursor.execute(sql)
                        consulta = cursor.fetchall()
                        if consulta:
                            data = []
                            for i in consulta:
                                tipo = str(i[0])
                                legajo = str(i[1])
                                nombres = str(i[2])
                                centro = str(i[3])
                                desde = str(i[4]) + " - " + str(i[5])
                                hasta = str(i[6]) + " - " + str(i[7])
                                motivo = str(i[8])
                                descripcion = str(i[9])
                                horas = str(i[10])
                                idHoras = str(i[12])
                                solicita = str(i[13])
                                importe = str(i[14])
                                datos = {'ID':idHoras,'tipo':tipo, 'legajo':legajo, 'nombres':nombres, 'centro': centro, 'desde':desde, 'hasta':hasta, 'motivo':motivo, 'descripcion':descripcion, 'horas':horas, 'importe': importe, 'solicita': solicita}
                                data.append(datos)
                            return JsonResponse({'Message': 'Success', 'Datos': data})
                        else:
                            data = "No se encontrarón horas extras procesadas."
                            return JsonResponse({'Message': 'Error', 'Nota': data})
                except Exception as e:
                    insertar_registro_error_sql("RRHH","mostrarHorasCargadas",request.user,str(e))
                    data = str(e)
                    return JsonResponse({'Message': 'Error', 'Nota': data})
                finally:
                    connections['TRESASES_APLICATIVO'].close()

            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = "SELECT        RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), " \
                                                    "TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, TresAses_ISISPayroll.dbo.CentrosCostos.DescrCtroCosto AS CENTRO_COSTOS, " \
                                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, CONVERT(VARCHAR(10), " \
                                                    "HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, " \
                                                    "RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5), HorasExtras_Procesadas.CantidadHoras) AS HORAS, RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, " \
                                                    "HorasExtras_Procesadas.ID_HEP AS idHoras, (SELECT CONVERT(VARCHAR(21),ApellidoEmple + ' ' + NombresEmple) FROM TresAses_ISISPayroll.dbo.Empleados WHERE CodEmpleado = HorasExtras_Procesadas.UsuarioEncargado) AS SOLICITA, ISNULL(ImpArreglo, '0') AS ImpArreglo  " \
                            "FROM            TresAses_ISISPayroll.dbo.CentrosCostos INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                    "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                    "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON " \
                                                    "S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado ON TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo = TresAses_ISISPayroll.dbo.Empleados.Regis_CCo " \
                            "WHERE        (HorasExtras_Procesadas.Sector = %s ) AND (HorasExtras_Procesadas.TipoHoraExtra = %s) AND (HorasExtras_Procesadas.EstadoEnvia = '1') " \
                            "ORDER BY LEGAJO, HorasExtras_Procesadas.FechaHoraDesde"
                    cursor.execute(sql, [sector,tipo])
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for i in consulta:
                            tipo = str(i[0])
                            legajo = str(i[1])
                            nombres = str(i[2])
                            centro = str(i[3])
                            desde = str(i[4]) + " - " + str(i[5])
                            hasta = str(i[6]) + " - " + str(i[7])
                            motivo = str(i[8])
                            descripcion = str(i[9])
                            horas = str(i[10])
                            idHoras = str(i[12])
                            solicita = str(i[13])
                            importe = str(i[14])
                            datos = {'ID':idHoras,'tipo':tipo, 'legajo':legajo, 'nombres':nombres, 'centro': centro, 'desde':desde, 'hasta':hasta, 'motivo':motivo, 'descripcion':descripcion, 'horas':horas, 'importe': importe, 'solicita': solicita}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Datos': data})
                    else:
                        data = "No se encontrarón horas extras procesadas."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("RRHH","mostrarHorasCargadas",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@login_required
@csrf_exempt
def traeTodo(request): ### MUESTRA HORAS PROCESADAS POR SECTOR Y TIPO DE HORA
    if request.method == 'GET':
        user_has_permission = request.user.has_perm('RRHH.puede_ver')
        if user_has_permission:
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = "SELECT        RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), " \
                                                    "TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, TresAses_ISISPayroll.dbo.CentrosCostos.DescrCtroCosto AS CENTRO_COSTOS, " \
                                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, CONVERT(VARCHAR(10), " \
                                                    "HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, " \
                                                    "RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5), HorasExtras_Procesadas.CantidadHoras) AS HORAS, RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, " \
                                                    "HorasExtras_Procesadas.ID_HEP AS idHoras, (SELECT CONVERT(VARCHAR(21),ApellidoEmple + ' ' + NombresEmple) FROM TresAses_ISISPayroll.dbo.Empleados WHERE CodEmpleado = HorasExtras_Procesadas.UsuarioEncargado) AS SOLICITA, ISNULL(ImpArreglo, '0') AS ImpArreglo " \
                            "FROM            TresAses_ISISPayroll.dbo.CentrosCostos INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                    "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                    "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON " \
                                                    "S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado ON TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo = TresAses_ISISPayroll.dbo.Empleados.Regis_CCo " \
                            "WHERE        (HorasExtras_Procesadas.Sector = 'C' ) AND (HorasExtras_Procesadas.EstadoEnvia = '1') " \
                            "ORDER BY LEGAJO, HorasExtras_Procesadas.FechaHoraDesde"
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for i in consulta:
                            tipo = str(i[0])
                            legajo = str(i[1])
                            nombres = str(i[2])
                            centro = str(i[3])
                            desde = str(i[4]) + " - " + str(i[5])
                            hasta = str(i[6]) + " - " + str(i[7])
                            motivo = str(i[8])
                            descripcion = str(i[9])
                            horas = str(i[10])
                            idHoras = str(i[12])
                            solicita = str(i[13])
                            importe = str(i[14])
                            datos = {'ID':idHoras,'tipo':tipo, 'legajo':legajo, 'nombres':nombres, 'centro': centro, 'desde':desde, 'hasta':hasta, 'motivo':motivo, 'descripcion':descripcion, 'horas':horas, 'importe': importe, 'solicita': solicita}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Datos': data})
                    else:
                        data = "No se encontrarón horas extras procesadas."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("RRHH","mostrarHorasCargadas",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required  
@csrf_exempt
def mostrarHorasCargadasPorLegajo(request): ### MUESTRA HORAS CARGADAS Y PROCESADAS POR LEGAJO 
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('RRHH.puede_ver')
        if user_has_permission:
            legajo = request.POST.get('ComboxTipoLegajoTransf')
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = "SELECT        RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), " \
                                                    "TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, TresAses_ISISPayroll.dbo.CentrosCostos.DescrCtroCosto AS CENTRO_COSTOS, " \
                                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, CONVERT(VARCHAR(10), " \
                                                    "HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, " \
                                                    "RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5), HorasExtras_Procesadas.CantidadHoras) AS HORAS, RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, " \
                                                    "HorasExtras_Procesadas.ID_HEP AS idHoras, (SELECT CONVERT(VARCHAR(21),ApellidoEmple + ' ' + NombresEmple) FROM TresAses_ISISPayroll.dbo.Empleados WHERE CodEmpleado = HorasExtras_Procesadas.UsuarioEncargado) AS SOLICITA, ISNULL(ImpArreglo, '0') AS ImpArreglo " \
                            "FROM            TresAses_ISISPayroll.dbo.CentrosCostos INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                                    "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                    "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                    "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON " \
                                                    "S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado ON TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo = TresAses_ISISPayroll.dbo.Empleados.Regis_CCo " \
                            "WHERE        (HorasExtras_Procesadas.Legajo = %s ) AND (HorasExtras_Procesadas.EstadoEnvia = '1') " \
                            "ORDER BY LEGAJO, HorasExtras_Procesadas.FechaHoraDesde"
                    cursor.execute(sql, [legajo])
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for i in consulta:
                            tipo = str(i[0])
                            legajo = str(i[1])
                            nombres = str(i[2])
                            centro = str(i[3])
                            desde = str(i[4]) + " - " + str(i[5])
                            hasta = str(i[6]) + " - " + str(i[7])
                            motivo = str(i[8])
                            descripcion = str(i[9])
                            horas = str(i[10])
                            idHoras = str(i[12])
                            solicita = str(i[13])
                            importe = str(i[14])
                            datos = {'ID':idHoras,'tipo':tipo, 'legajo':legajo, 'nombres':nombres, 'centro': centro, 'desde':desde, 'hasta':hasta, 'motivo':motivo, 'descripcion':descripcion, 'horas':horas, 'importe': importe, 'solicita': solicita}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Datos': data})
                    else:
                        data = "No se encontrarón horas extras procesadas."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("RRHH","mostrarHorasCargadasPorLegajo",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required
@csrf_exempt
def enviarHorasCargadas(request): ### INSERTA LAS HORAS SELECCIONADAS EN S3A 
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('RRHH.puede_insertar')
        if user_has_permission:
            importe = request.POST.get('valor', None)
            pagada = request.POST.get('HePagada', 'N')
            checkboxes_tildados = request.POST.getlist('idCheck')
            resultados = []
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
                data = "Las horas se guardaron correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': data})
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required
@csrf_exempt
def cargaLegajos(request): ### MUESTRA LOS LEGAJOS DE LAS HORAS EXTRAS EN LA TABLA POR SECTOR 
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('RRHH.puede_ver')
        if user_has_permission:
            sector = request.POST.get('ComboxSectorHELegajos')  
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = "SELECT DISTINCT " \
                                                    "HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), CONVERT(VARCHAR(5), HorasExtras_Procesadas.Legajo) + ' - ' + TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple) AS DATOS " \
                            "FROM            TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                    "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo " \
                            "WHERE (HorasExtras_Procesadas.EstadoEnvia = '1') AND (HorasExtras_Procesadas.Sector = %s)"
                    cursor.execute(sql, [sector])
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
                        data = "No se encontrarón horas extras procesadas."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("RRHH","cargaLegajos",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

def buscaDatosParaInsertarHE(idHEP): ### SOLO FUNCIÓN, BUSCA DATOS PARA INSERTAR (NO REQUIERE PERMISOS)
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Legajo, CONVERT(VARCHAR(10), FechaHoraDesde, 126) AS FECHA_DESDE,CONVERT(VARCHAR(5), FechaHoraDesde, 108) AS HORA_DESDE, " \
                            "CONVERT(VARCHAR(10), FechaHoraHasta, 126) AS FECHA_HASTA, CONVERT(VARCHAR(5), FechaHoraHasta, 108) AS HORA_HASTA, CantidadHoras AS HORAS, " \
                            "IdMotivo AS MOTIVO, Autorizado AS AUTORIZADO, CONVERT(VARCHAR(99), RTRIM(DescripcionMotivo)) AS DESCRIPCION, TipoHoraExtra AS TIPO " \
                    "FROM HorasExtras_Procesadas " \
                    "WHERE ID_HEP = %s" 
            cursor.execute(sql, [idHEP])
            consulta = cursor.fetchone()
            if consulta:
                Legajo = str(consulta[0])
                Fdesde = str(consulta[1])
                Hdesde = str(consulta[2])
                Fhasta = str(consulta[3])
                Hhasta = str(consulta[4])
                Choras = str(consulta[5])
                IdMotivo = str(consulta[6])
                IdAutoriza = str(consulta[7])
                Descripcion = str(consulta[8])
                Thora = str(consulta[9])
                return Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora  
    except Exception as e:
        insertar_registro_error_sql("RRHH","buscaDatosParaInsertarHE","request.user",str(e))
        data = str(e)
        return data
    finally:
        connections['TRESASES_APLICATIVO'].close()

def insertaHorasExtras(ID_HEP,Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora, importe, pagada, fecha_y_hora): ### FUNCION QUE INSERTA LAS HORAS EN EL S3A SOLO FUNCION (NO REQUIERE PERMISOS)
    try:
        with connections['S3A'].cursor() as cursor:
            sql = "INSERT INTO RH_HE_Horas_Extras (IdRepl,IdHoraExtra,IdLegajo,FechaDesde,HoraDesde,FechaHasta,HoraHasta,CantHoras,IdMotivo,IdAutoriza,Descripcion,TipoHoraExtra,Valor,Pagada,FechaAlta,UserID) " \
                    "VALUES ('100',(SELECT MAX (IdHoraExtra) + 1 FROM RH_HE_Horas_Extras),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, 'APLICATIVO')"
            values = (Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora, importe, pagada, fecha_y_hora)
            cursor.execute(sql, values)
            cursor.close()
            actualizarEstadoHEP(ID_HEP)
            return 1
    except Exception as e:
        insertar_registro_error_sql("RRHH","insertaHorasExtras","request.user",str(e))
        return 0
    finally:
        connections['S3A'].close()

def actualizarEstadoHEP(ID_HEP): ### FUNCIÓN QUE ACTUALIZA EL ESTADO SI SE ENVÍO LA HS EXTRA SÓLO FUNCIÓN (NO REQUIERE PERMISOS)
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE HorasExtras_Procesadas SET EstadoEnvia = '0' WHERE ID_HEP = %s"
            cursor.execute(sql, [ID_HEP])
    except Exception as e:
        insertar_registro_error_sql("RRHH","actualizarEstadoHEP","request.user",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

def eliminaHEP(ID_HEP): ### FUNCIÓN QUE ELIMNA LAS HORAS SELECCIONADS SEGUN EL ID SÓLO FUNCIÓN(NO REQUIERE PERMISOS)
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE HorasExtras_Procesadas SET EstadoEnvia = '8' WHERE ID_HEP = %s"
            cursor.execute(sql, [ID_HEP])

            slq2 = "UPDATE HorasExtras_Sin_Procesar SET Estado='8' WHERE ID_HESP = (SELECT ID_HESP FROM HorasExtras_Procesadas WHERE ID_HEP = %s)"
            cursor.execute(slq2, [ID_HEP])

    except Exception as e:
        insertar_registro_error_sql("RRHH","eliminaHEP","request.user",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

@login_required
@csrf_exempt
def eliminaHorasCargadas(request): ### PETICIÓN QUE ELIMINA LAS HORAS SELECCIONADAS (REQUIERE PERMISOS delete)
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('RRHH.puede_borrar')
        if user_has_permission:
            importe = request.POST.get('valor', None)
            pagada = request.POST.get('HePagada', 'N')
            checkboxes_tildados = request.POST.getlist('idCheck')
            resultados = []
            for i in checkboxes_tildados:
                ID_HEP = str(i)  
                resultado = eliminaHEP(ID_HEP)
                resultados.append(resultado)

            if 0 in resultados:
                data = "Se produjo un Error en alguna de las horas a eliminar."
                return JsonResponse({'Message': 'Error', 'Nota': data})
            else:
                data = "Las horas se eliminaron correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': data})
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})










