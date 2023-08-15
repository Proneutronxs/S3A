from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from S3A.conexionessql import *
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
                Estado = item['Regis_TEA'] ### ESTADO ADELANTO
                Tipo = item['Regis_TLE'] ### TIPO DE LIQUIDACIÓN ADELANTO               
                auditaAnticipos(usuario, fechaHora,Regis_Epl, Importe)

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
        with connections['default'].cursor() as cursor:
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
        return listadoCorreos
    finally:
        connections['default'].close()

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
        return nombre
    finally:
        connections['ISISPayroll'].close()


def auditaAnticipos(usuario, Fechahora, Destino, Monto):
    estado = '1'
    try:
        with connections['default'].cursor() as cursor:
            sql = "INSERT INTO Auditoria_Anticipos (Usuario, FechaHora, Destino, Monto, EstadoCorreo) VALUES (%s, %s, %s, %s, %s)"
            values = (usuario,Fechahora,Destino,Monto,estado)
            cursor.execute(sql, values)
    except Exception as e:
        print(e)
    finally:
        connections['default'].close()


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

@csrf_exempt
def verAnticipos(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            ### VARIABLES
            usuario = str(json.loads(body)['usuario'])
            fecha = str(json.loads(body)['fecha'])
            mes = str(json.loads(body)['mes'])
            año = str(json.loads(body)['año'])
            tipo = str(json.loads(body)['tipo'])
            
            with connections['default'].cursor() as cursor:
                sql = "SELECT        CONVERT(VARCHAR(20), TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRES, '$ ' + CONVERT(VARCHAR(10), Auditoria_Anticipos.Monto, 2) AS IMPORTE, " \
                                                "'Tipo: ' + SUBSTRING(TresAses_ISISPayroll.dbo.EmpleadoAdelantos.MotivoAde, LEN('CH - ADELANTO ') + 1, LEN(TresAses_ISISPayroll.dbo.EmpleadoAdelantos.MotivoAde)) AS MOTIVO " \
                        "FROM            TresAses_ISISPayroll.dbo.EmpleadoAdelantos INNER JOIN " \
                                                "TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                "Auditoria_Anticipos ON TresAses_ISISPayroll.dbo.Empleados.Regis_Epl = Auditoria_Anticipos.Destino ON TresAses_ISISPayroll.dbo.EmpleadoAdelantos.Regis_Epl = Auditoria_Anticipos.Destino " \
                        "WHERE        (Auditoria_Anticipos.Usuario = %s) AND (CONVERT(VARCHAR(10), Auditoria_Anticipos.FechaHora, 103) = %s) AND (RIGHT('0' + CAST(MONTH(CONVERT(DATE, TresAses_ISISPayroll.dbo.EmpleadoAdelantos.FechaAde, 103)) " \
                                                "AS VARCHAR(2)), 2) = %s) AND (YEAR(CONVERT(DATE, TresAses_ISISPayroll.dbo.EmpleadoAdelantos.FechaAde, 103)) = %s) AND (TresAses_ISISPayroll.dbo.EmpleadoAdelantos.MotivoAde = %s) " \
                        "ORDER BY TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple"
                cursor.execute(sql, [usuario,fecha,mes,año,tipo])
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        nombre = str(row[0])
                        monto = str(row[1])
                        tipoA = str(row[2])
                        datos = {'Nombre': nombre, 'Monto': monto, 'TipoA': tipoA}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron Adelantos para la fecha: '})
        except Exception as e:
            error = str(e)
        finally:
            cursor.close()
            connections['default'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})












