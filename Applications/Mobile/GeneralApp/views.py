from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from S3A.conexionessql import *
import json
from Applications.Mobile.GeneralApp.archivosGenerales import insertaRegistro
from django.db import connections
from django.http import JsonResponse


### LOGIN DE LA APLICACIÓN

@csrf_exempt
def login_app(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        usuario = str(json.loads(body)['usuario'])
        clave = str(json.loads(body)['contraseña'])
        fechaHora = str(json.loads(body)['actual']) + ".000"
        registro = str(json.loads(body)['registro'])
        print(fechaHora,registro)
        try:
            with connections['default'].cursor() as cursor:
                sql = "SELECT USUARIOS.CodEmpleado AS LEGAJO, USR_PERMISOS_APP.MD_AutoriHorasExt AS H_EXTRAS, USR_PERMISOS_APP.MD_Presentismo AS ASISTENCIA, USR_PERMISOS_APP.MD_Anticipos AS ANTICIPOS " \
                      "FROM USUARIOS CROSS JOIN USR_PERMISOS_APP " \
                      "WHERE USUARIOS.Usuario = %s AND USUARIOS.Clave = %s"
                cursor.execute(sql, [usuario, clave])
                consulta = cursor.fetchone()
                
                if consulta:
                    legajo, hExtras, asistencia, anticipos = map(str, consulta)
                    response_data = {                        
                        'Legajo': legajo,
                        'Usuario': usuario,
                        'HExtras': hExtras,
                        'Asistencia': asistencia,
                        'Anticipos': anticipos
                    }
                    #print("INICIA SESION")
                    datos = {'Message': 'Success', 'Data': response_data}
                    estado = "E"
                    insertaRegistro(usuario,fechaHora,registro,estado)
                    return JsonResponse(datos)
                else:
                    response_data = {
                        'Message': 'Not Found',
                        'Nota': 'Usuario o Contraseña inválidos.'
                    }
                    estado = "F"
                    insertaRegistro(usuario,fechaHora,registro,estado)
                    return JsonResponse(response_data)
        except Exception as e:
            error = str(e)
            response_data = {
                'Message': 'Error',
                'Nota': error
            }
            return JsonResponse(response_data)
        finally:
            connections['default'].close()
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)

###  METODO GET PARA TRAER CHACRAS Y ID

@csrf_exempt
def id_Nombre_Ccostos(request, legajo):
    if request.method == 'GET':
        id = str(legajo)
        try:
            with connections['default'].cursor() as cursor:
                sql = "SELECT        USR_CCOSTOS.CodCtroCosto AS CODIGO, TresAses_ISISPayroll.dbo.CentrosCostos.DescrCtroCosto AS DESCRIPCION, TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo AS REGISCCo " \
                      "FROM            USR_CCOSTOS INNER JOIN " \
                      "TresAses_ISISPayroll.dbo.CentrosCostos ON USR_CCOSTOS.CodCtroCosto = TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo " \
                      "WHERE (USR_CCOSTOS.CodEmpleado = %s) "
                cursor.execute(sql, [id])
                consulta = cursor.fetchall()

                if consulta:
                    lista_data = []
                    for row in consulta:
                        codigo = str(row[0])
                        descripcion = str(row[1])
                        regis_epl = str(row[2])
                        datos = {'Codigo': codigo, 'Descripcion': descripcion, 'Regis_Epl': regis_epl}
                        lista_data.append(datos)
                    lista_data_motivos = traeMotivos()
                    montoMax = traeMontoMax()
                    #print("LLAMA A LAS CHACRAS ASIGNADAS")
                    return JsonResponse({'Message': 'Success', 'Data': lista_data, 'DataMotivos': lista_data_motivos, 'Monto': montoMax})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['default'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

### TRAE PERSONAL DE ASISTENCIA

@csrf_exempt
def personal_por_Ccostos_asistencia(request, codigo):
    if request.method == 'GET':
        idCC = str(codigo)
        try:
            with connections['ISISPayroll'].cursor() as cursor:
                sql = "SELECT        Empleados.CodEmpleado AS LEGAJO, principal.dbo.T_Legajos.legCodigo AS LEGCODIGO, Empleados.ApellidoEmple + ' ' + Empleados.NombresEmple AS NOMBREyAPELLIDO " \
                      "FROM            Empleados INNER JOIN " \
                      "principal.dbo.T_Legajos ON CONVERT(VARCHAR, Empleados.CodEmpleado) = principal.dbo.T_Legajos.legLegajo " \
                      "WHERE        (Empleados.Regis_CCo = %s AND Empleados.BajaDefinitivaEmple='2') " \
                      "ORDER BY Empleados.ApellidoEmple"
                cursor.execute(sql, [idCC])
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        legajo = str(row[0])
                        legCodigo = str(row[1])
                        nombre = str(row[2])
                        datos = {'Legajo': legajo, 'legCodigo': legCodigo, 'Nombre': nombre}
                        lista_data.append(datos)
                    #print("LLAMA PERSONAL DE ASISTENCIA")
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['ISISPayroll'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    

@csrf_exempt
def personal_por_Ccostos_anticipos(request, codigo):
    if request.method == 'GET':
        id = str(codigo)
        lista_data_personal = traePersonal(id)
        #print("LLAMA PERSONAL DE ANTICIPOS / HORAS EXTRAS")
        return JsonResponse({'Message': 'Success','DataPersonal': lista_data_personal})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    


def traePersonal(id):
    try:
        with connections['ISISPayroll'].cursor() as cursor:
            sql = "SELECT Regis_Epl AS REGIS, CodEmpleado AS LEGAJO, (ApellidoEmple + ' ' + NombresEmple) AS NOMBREyAPELLIDO " \
                    "FROM Empleados " \
                    "WHERE Regis_CCo = %s AND BajaDefinitivaEmple='2' "\
                    "ORDER BY ApellidoEmple "
            cursor.execute(sql, [id])
            consulta = cursor.fetchall()
            lista_data = []
            if consulta:
                for row in consulta:
                    legajo = str(row[1])
                    Regis_Epl = str(row[0])
                    nombre = str(row[2])
                    datos = {'Legajo': legajo, 'Regis_Epl': Regis_Epl, 'Nombre': nombre}
                    lista_data.append(datos)
                return lista_data
            else:
                return lista_data
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['ISISPayroll'].close()
    
def traeMotivos():
    try:
        with connections['S3A'].cursor() as cursor:
            sql = "SELECT IdMotivo AS ID, RTRIM(Descripcion) AS MOTIVO " \
                    "FROM RH_HE_Motivo " \
                    "ORDER BY Descripcion "
            cursor.execute(sql)
            consulta = cursor.fetchall()
            lista_data = []
            if consulta:
                for row in consulta:
                    idMotivo = str(row[0])
                    Motivo = str(row[1])
                    datos = {'idMotivo': idMotivo, 'Motivo': Motivo}
                    lista_data.append(datos)
                return lista_data
            else:
                return lista_data
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['S3A'].close()
    
def traeMontoMax():
    try:
        with connections['default'].cursor() as cursor:
            sql = "SELECT Monto AS MONTO " \
                    "FROM MAX_ADELANTO "
            cursor.execute(sql)
            consulta = cursor.fetchone()
            monto = "0"
            if consulta:
                monto = str(consulta[0])
                return monto
            else:
                return monto
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['default'].close()