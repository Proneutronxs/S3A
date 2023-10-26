from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from S3A.conexionessql import *
from S3A.funcionesGenerales import *
import json
from Applications.Mobile.GeneralApp.archivosGenerales import insertaRegistro, enviarCorreo
from django.db import connections
from django.http import JsonResponse
from django.core.mail import send_mail

# Create your views here.


###  METODO POST PARA PODER INSERTAR LOS ANTICIPOS EN SQL
@csrf_exempt
def insert_anticipos(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            usuario = str(json.loads(body)['usuario'])
            fechaHora = str(json.loads(body)['actual'])
            registro = str(json.loads(body)['registro'])
            datos = json.loads(body)['Data']
            listado = []

            for item in datos:
                Regis_Epl = item['Regis_Epl'] ### ID LEGAJO
                Fecha = item['Fecha']### FECHA DEL ADELANTO
                Importe = item['Importe'] ### IMPORTE ADELANTO
                Motivo = 'CH - ' + str(item['MotivoAd']) ### MOTIVO ADELANTO
                motivoAuditoria = str(item['MotivoAd'])
                Estado = item['Regis_TEA'] ### ESTADO ADELANTO
                Tipo = item['Regis_TLE'] ### TIPO DE LIQUIDACIÓN ADELANTO               
                auditaAnticipos(usuario, fechaHora,Regis_Epl, Importe, motivoAuditoria)

                with connections['ISISPayroll'].cursor() as cursor:
                    sql = "INSERT INTO EmpleadoAdelantos (Regis_Epl, FechaAde, ImporteAde, MotivoAde, SaldoAde, Regis_TEA, Regis_TLE, CantCuotasPrest, ImporteCuotaPrest, UltCuotaDesconPrest, SenDadoBajaPrest, LapsoReorganizado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (Regis_Epl, Fecha, Importe, Motivo, Importe, Estado, Tipo, '0', '0.00', '0', '0', '0')
                    cursor.execute(sql, values)
                
                LegajoNombre = obtieneNombres(Regis_Epl)
                datosLegajo = LegajoNombre + ' Monto: $' + Importe
                listado.append(datosLegajo)
            
            estado = "E"
            insertaRegistro(usuario, fechaHora, registro, estado)
            nota = "Los registros se guardaron exitosamente."
            return JsonResponse({'Message': 'Success', 'Nota': nota})      
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("Anticipos","insert_anticipos","usuario",error)
            estado = "F"
            insertaRegistro(usuario, fechaHora, registro, estado)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['ISISPayroll'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'}) 

def correosChacras():
    listadoCorreos = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Correo " \
                    "FROM Correos " \
                    "WHERE Sector = 'CHACRA' "
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                for i in consulta:
                    correo = str(i[0])
                    listadoCorreos.append(correo)
        return listadoCorreos
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("Anticipos","correosChacras","usuario",error)
        return listadoCorreos
    finally:
        connections['TRESASES_APLICATIVO'].close()

def obtieneNombres(Regis_Epl):
    nombre = ''
    try:
        with connections['ISISPayroll'].cursor() as cursor:
            sql = "SELECT (CONVERT(VARCHAR(6), CodEmpleado) + ' - ' + ApellidoEmple + ' ' + nombresEmple) " \
                    "FROM Empleados " \
                    "WHERE Regis_Epl = %s "
            cursor.execute(sql, [Regis_Epl])
            consulta = cursor.fetchone()
            if consulta:
                nombre = str(consulta[0])
        return nombre
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("Anticipos","obtiene_nobres","usuario",error)
        return nombre
    finally:
        connections['ISISPayroll'].close()

def auditaAnticipos(usuario, Fechahora, Destino, Monto,motivoAuditoria):
    estado = '1'
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Auditoria_Anticipos (Usuario, FechaHora, Destino, Monto, Tipo, EstadoCorreo) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (usuario,Fechahora,Destino,Monto,motivoAuditoria,estado)
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("Anticipos","AuditaAnticipos","usuario",error)
    finally:
        connections['TRESASES_APLICATIVO'].close()

def enviar_correo_sendMail(asunto, mensaje, destinatario):
    remitente = 'aplicativo@tresases.com.ar'
    asunto = 'No Responder - ' + asunto

    send_mail(
        asunto,
        mensaje,
        remitente,
        [destinatario],
        fail_silently=False,
    )

def enviaCorreo(listado):
    contenido = 'Se cargaron anticipos de las siguientes personas: \n \n' + ', \n'.join(listado) + '.'
    asunto = 'Carga de Anticipos.'
    listadoCorreos = correosChacras()
    for correo in listadoCorreos:
        enviar_correo_sendMail(asunto,contenido,correo)

def obtenerAñoActual():
    import datetime 
    now = datetime.datetime.now()
    año_actual = now.strftime("%Y")
    año = str(año_actual)
    return año

@csrf_exempt
def verAnticipos(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            ### VARIABLES
            usuario = str(json.loads(body)['usuario'])
            fecha = str(json.loads(body)['fecha'])
            mes = str(json.loads(body)['mes'])
            tipo = 'CH - %'
            año = obtenerAñoActual()
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "SELECT        CONVERT(VARCHAR(25), TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRE, '$ ' + CONVERT(VARCHAR(10), Auditoria_Anticipos.Monto, 2) " \
                                                "AS IMPORTE, 'Tipo: ' + SUBSTRING(TresAses_ISISPayroll.dbo.EmpleadoAdelantos.MotivoAde, LEN('CH - ADELANTO ') + 1, LEN(TresAses_ISISPayroll.dbo.EmpleadoAdelantos.MotivoAde)) AS MOTIVO " \
                        "FROM            TresAses_ISISPayroll.dbo.EmpleadoAdelantos INNER JOIN " \
                                                "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                "Auditoria_Anticipos ON TresAses_ISISPayroll.dbo.Empleados.Regis_Epl = Auditoria_Anticipos.Destino ON TresAses_ISISPayroll.dbo.EmpleadoAdelantos.Regis_Epl = TresAses_ISISPayroll.dbo.Empleados.Regis_Epl " \
                        "WHERE        (CONVERT(VARCHAR(10), Auditoria_Anticipos.FechaHora, 103) = %s) AND (Auditoria_Anticipos.Usuario = %s) AND (TresAses_ISISPayroll.dbo.EmpleadoAdelantos.MotivoAde LIKE %s) AND  " \
                                                "(RIGHT('0' + CAST(MONTH(CONVERT(DATE, TresAses_ISISPayroll.dbo.EmpleadoAdelantos.FechaAde, 103)) AS VARCHAR(2)), 2) = %s) AND (YEAR(CONVERT(DATE, TresAses_ISISPayroll.dbo.EmpleadoAdelantos.FechaAde, 103)) = %s)"
                cursor.execute(sql, [fecha,usuario,tipo,mes,año])
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        nombre = str(row[0])
                        monto = str(row[1])
                        tipoA = str(row[2])
                        datos = {'Nombre': nombre, 'Monto': monto, 'TipoA': tipoA, 'Estado': '00'}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron Adelantos para la fecha: '})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("Anticipos","verAnticipos","usuario",error)
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def cargaFechasDeAnticipos(request, mes, usuario):
    if request.method == 'GET':
        Mes = str(mes)
        User = str(usuario)
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "SELECT DISTINCT CONVERT(VARCHAR(10), FechaHora, 103) AS ID_FECHA, 'Fecha de Carga: ' + CONVERT(VARCHAR(5), FechaHora, 103) AS FECHAS " \
                        "FROM Auditoria_Anticipos " \
                        "WHERE (RIGHT('0' + CAST(MONTH(CONVERT(DATE, FechaHora, 103)) AS VARCHAR(2)), 2) = %s) AND (Usuario = %s) "
                cursor.execute(sql, [Mes,User])
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        idFecha = str(row[0])
                        Fecha = str(row[1])
                        datos = {'idFecha': idFecha, 'Fecha': Fecha}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("Anticipos","cargaFechasAnticipos","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def pruebaMetodo(request):
    if request.method == 'GET':
        print("")
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})








