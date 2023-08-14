from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from S3A.conexionessql import *
import json
from Applications.Mobile.GeneralApp.archivosGenerales import insertaRegistro, enviarCorreo
from django.db import connections
from django.http import JsonResponse

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
            
            enviaCorreo(listado)
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
    try:
        with connections['default'].cursor() as cursor:
            sql = "INSERT INTO Auditoria_Anticipos (Usuario, FechaHora, Destino, Monto) VALUES (%s, %s, %s, %s)"
            values = (usuario,Fechahora,Destino,Monto)
            cursor.execute(sql, values)
    except Exception as e:
        print(e)
    finally:
        connections['default'].close()


def enviaCorreo(listado):
    contenido = 'Se cargaron anticipos de las siguientes personas: \n \n' + ', \n'.join(listado) + '.'
    asunto = 'Carga de Anticipos.'
    listadoCorreos = correosChacras()
    #for correo in listadoCorreos:
    correo = 'aplicativo@tresases.com.ar'
    enviarCorreo(asunto,contenido,correo)