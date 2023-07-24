from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import datetime 

from django.db import connections
from django.http import JsonResponse


# Create your views here.
### RENDERIZADO DE RRHH 
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

@csrf_exempt
def mostrarHorasCargadas(request):
    if request.method == 'POST':
        tipo = request.POST.get('ComboxTipoHoraTransf')
        if tipo == "A":
            data = "Llamo a las horas arregladas."
            return JsonResponse({'Message': 'Error', 'Nota': data})
        try:
            with connections['default'].cursor() as cursor:
                sql = "SELECT        RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, " \
                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, " \
                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, " \
                                                "RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5), HorasExtras_Procesadas.CantidadHoras) AS HORAS, RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, HorasExtras_Procesadas.ID_HEP AS idHoras " \
                        "FROM            S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                                "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON  " \
                                                "S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado " \
                        "WHERE        (HorasExtras_Procesadas.TipoHoraExtra = %s) AND (HorasExtras_Procesadas.EstadoEnvia = '1') " \
                        "ORDER BY HorasExtras_Procesadas.Legajo, HorasExtras_Procesadas.FechaHoraDesde"
                cursor.execute(sql, [tipo])
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
            connections['default'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@csrf_exempt
def mostrarHorasCargadasPorLegajo(request):
    if request.method == 'POST':
        legajo = request.POST.get('ComboxTipoLegajoTransf')
        try:
            with connections['default'].cursor() as cursor:
                sql = "SELECT        RTRIM(HorasExtras_Procesadas.TipoHoraExtra) AS TIPO, HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, " \
                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraDesde, 103) AS FECHA_DESDE, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraDesde, 108) AS HORA_DESDE, " \
                                    "CONVERT(VARCHAR(10), HorasExtras_Procesadas.FechaHoraHasta, 103) AS FECHA_HASTA, CONVERT(VARCHAR(5), HorasExtras_Procesadas.FechaHoraHasta, 108) AS HORA_HASTA, " \
                                                "RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, RTRIM(HorasExtras_Procesadas.DescripcionMotivo) AS DESCRIPCION, CONVERT(VARCHAR(5), HorasExtras_Procesadas.CantidadHoras) AS HORAS, RTRIM(S3A.dbo.RH_HE_Autoriza.Apellidos) AS AUTORIZADO, HorasExtras_Procesadas.ID_HEP AS idHoras " \
                        "FROM            S3A.dbo.RH_HE_Autoriza INNER JOIN " \
                                                "S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo ON  " \
                                                "S3A.dbo.RH_HE_Motivo.IdMotivo = HorasExtras_Procesadas.IdMotivo ON S3A.dbo.RH_HE_Autoriza.IdAutoriza = HorasExtras_Procesadas.Autorizado " \
                        "WHERE        (HorasExtras_Procesadas.Legajo = %s) AND (HorasExtras_Procesadas.EstadoEnvia = '1') " \
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
            connections['default'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
   
@csrf_exempt
def enviarHorasCargadas(request):
    if request.method == 'POST':
        importe = request.POST.get('valor', None)
        pagada = request.POST.get('HePagada', 'N')
        checkboxes_tildados = request.POST.getlist('idCheck')
        resultados = []
        for i in checkboxes_tildados:
            ID_HEP = str(i) 
            print(ID_HEP)
            fecha_y_hora = str(obtener_fecha_hora_actual_con_milisegundos())
            Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora = buscaDatosParaInsertarHE(ID_HEP) 
            resultado = insertaHorasExtras(ID_HEP,Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora, importe, pagada, fecha_y_hora)
            resultados.append(resultado)

            print('100', 'IdHoraExtra', Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora, importe, pagada, fecha_y_hora, 'APLICATIVO' )       

        if 0 in resultados:
            data = "Se produjo un Error en alguna de las inserciones."
            return JsonResponse({'Message': 'Error', 'Nota': data})
        else:
            data = "Las horas se guardaron correctamente."
            return JsonResponse({'Message': 'Success', 'Nota': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@csrf_exempt
def cargaLegajos(request):
    if request.method == 'GET':
        try:
            with connections['default'].cursor() as cursor:
                sql = "SELECT DISTINCT " \
                                                "HorasExtras_Procesadas.Legajo AS LEGAJO, CONVERT(VARCHAR(25), CONVERT(VARCHAR(5), HorasExtras_Procesadas.Legajo) + ' - ' + TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple) AS DATOS " \
                        "FROM            TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                "HorasExtras_Procesadas ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Procesadas.Legajo " \
                        "WHERE (HorasExtras_Procesadas.EstadoEnvia = '1')"
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
                    data = "No se encontrarón horas extras procesadas."
                    return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
        finally:
            connections['default'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


def buscaDatosParaInsertarHE(idHEP):
    try:
        with connections['default'].cursor() as cursor:
            sql = "SELECT Legajo, CONVERT(VARCHAR(10), FechaHoraDesde, 126) AS FECHA_DESDE,CONVERT(VARCHAR(5), FechaHoraDesde, 108) AS HORA_DESDE, " \
                            "CONVERT(VARCHAR(10), FechaHoraHasta, 126) AS FECHA_HASTA, CONVERT(VARCHAR(5), FechaHoraHasta, 108) AS HORA_HASTA, CantidadHoras AS HORAS, " \
                            "IdMotivo AS MOTIVO, Autorizado AS AUTORIZADO, RTRIM(DescripcionMotivo) AS DESCRIPCION, TipoHoraExtra AS TIPO " \
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
        data = str(e)
        return data
    finally:
        connections['default'].close()


def insertaHorasExtras(ID_HEP,Legajo, Fdesde, Hdesde, Fhasta, Hhasta, Choras, IdMotivo, IdAutoriza, Descripcion, Thora, importe, pagada, fecha_y_hora):
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
        error = str(e)
        print(error)
        return 0
    finally:
        connections['S3A'].close()

def actualizarEstadoHEP(ID_HEP):
    try:
        with connections['default'].cursor() as cursor:
            sql = "UPDATE HorasExtras_Procesadas SET EstadoEnvia = '0' WHERE ID_HEP = %s"
            cursor.execute(sql, [ID_HEP])
            cursor.close()
    except Exception as e:
        error = str(e)
        print(error)
    finally:
        connections['default'].close()




