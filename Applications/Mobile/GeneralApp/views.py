from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from S3A.funcionesGenerales import *
import json
from django.http import FileResponse
import os
from Applications.Mobile.GeneralApp.archivosGenerales import insertaRegistro
from django.db import connections


def subirApp(request):
    return render (request, 'generalapp/subirApp.html')

### LOGIN DE LA APLICACIÓN
@csrf_exempt
def login_app(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        usuario = str(json.loads(body)['usuario'])
        clave = str(json.loads(body)['contraseña'])
        fechaHora = str(json.loads(body)['actual'])
        registro = str(json.loads(body)['registro'])
        #print(fechaHora,registro) " \
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "DECLARE @ParametroUser VARCHAR(255) " \
                        "DECLARE @ParametroPass VARCHAR(6) " \
                        "SET @ParametroUser = %s " \
                        "SET @ParametroPass = %s " \
                        "DECLARE @MD_Chofer INT; " \
                        "SELECT @MD_Chofer = USR_PERMISOS_APP.MD_Chofer " \
                        "FROM USUARIOS " \
                        "INNER JOIN USR_PERMISOS_APP ON USUARIOS.CodEmpleado = USR_PERMISOS_APP.CodEmpleado " \
                        "WHERE (USUARIOS.Usuario = @ParametroUser) AND (USUARIOS.Clave = @ParametroPass); " \
                        "IF @MD_Chofer = 1 " \
                            "BEGIN " \
                                "SELECT        USUARIOS.CodEmpleado, (RTRIM(S3A.dbo.Chofer.Apellidos) + ' ' + RTRIM(S3A.dbo.Chofer.Nombres)) AS Nombre, " \
                                                    "USR_PERMISOS_APP.MD_AutoriHorasExt, USR_PERMISOS_APP.MD_Presentismo, USR_PERMISOS_APP.MD_Anticipos, USR_PERMISOS_APP.MD_PedidoFlete,  " \
                                                    "USR_PERMISOS_APP.MD_CrearRemito, USR_PERMISOS_APP.MD_ReporteBins, USR_PERMISOS_APP.MD_Chofer, USUARIOS.Usuario " \
                                "FROM            S3A.dbo.Chofer INNER JOIN " \
                                                        "USUARIOS INNER JOIN " \
                                                        "USR_PERMISOS_APP ON USUARIOS.CodEmpleado = USR_PERMISOS_APP.CodEmpleado ON S3A.dbo.Chofer.IdChofer = USUARIOS.CodEmpleado " \
                                "WHERE        (USUARIOS.Usuario = @ParametroUser) AND (USUARIOS.Clave = @ParametroPass) " \
                            "END " \
                        "ELSE " \
                            "BEGIN " \
                                "SELECT        USR_PERMISOS_APP.CodEmpleado,CASE WHEN(SELECT TresAses_ISISPayroll.dbo.Empleados.CodEmpleado  " \
                                    "FROM TresAses_ISISPayroll.dbo.Empleados  " \
                                    "WHERE TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = USR_PERMISOS_APP.CodEmpleado) IS NOT NULL  " \
                                    "THEN (SELECT CONVERT(VARCHAR(22), (TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple))  " \
                                    "FROM TresAses_ISISPayroll.dbo.Empleados  " \
                                    "WHERE TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = USR_PERMISOS_APP.CodEmpleado) ELSE '-' END AS Nombres,  " \
                                    "USR_PERMISOS_APP.MD_AutoriHorasExt, USR_PERMISOS_APP.MD_Presentismo, USR_PERMISOS_APP.MD_Anticipos, USR_PERMISOS_APP.MD_PedidoFlete,   " \
                                    "USR_PERMISOS_APP.MD_CrearRemito, USR_PERMISOS_APP.MD_ReporteBins, USR_PERMISOS_APP.MD_Chofer, USUARIOS.Usuario  " \
                                "FROM            USUARIOS INNER JOIN  " \
                                                "USR_PERMISOS_APP ON USUARIOS.CodEmpleado = USR_PERMISOS_APP.CodEmpleado  " \
                                "WHERE        (USUARIOS.Usuario = @ParametroUser) AND (USUARIOS.Clave = @ParametroPass) " \
                            "END"

                cursor.execute(sql, [usuario, clave])
                consulta = cursor.fetchone()
                
                if consulta:
                    legajo, nombre, hExtras, asistencia, anticipos, pedidoFlete, crearRemito, reporteBins, chofer, user = map(str, consulta)
                    response_data = {                        
                        'Legajo': legajo,
                        'Nombre': nombre,
                        'Usuario': user,
                        'HExtras': hExtras,
                        'Asistencia': asistencia,
                        'Anticipos': anticipos,
                        'PedidoFlete': pedidoFlete,
                        'CrearRemito': crearRemito,
                        'ReporteBins': reporteBins,
                        'Chofer': chofer,
                        'Delete': borraBaseDatosApp()

                    }
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
            insertar_registro_error_sql("GeneralApp","login_app",usuario,error)
            response_data = {
                'Message': 'Error',
                'Nota': error
            }
            return JsonResponse(response_data)
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)

# @csrf_exempt
# def login_app(request):
#     if request.method == 'POST':
#         body = request.body.decode('utf-8')
#         usuario = str(json.loads(body)['usuario'])
#         clave = str(json.loads(body)['contraseña'])
#         fechaHora = str(json.loads(body)['actual'])
#         registro = str(json.loads(body)['registro'])
#         #print(fechaHora,registro) " \
#         try:
#             with connections['TRESASES_APLICATIVO'].cursor() as cursor:
#                 sql = "SELECT        USR_PERMISOS_APP.CodEmpleado,CASE WHEN(SELECT TresAses_ISISPayroll.dbo.Empleados.CodEmpleado " \
#                                                                                 "FROM TresAses_ISISPayroll.dbo.Empleados " \
#                                                                                 "WHERE TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = USR_PERMISOS_APP.CodEmpleado) IS NOT NULL " \
#                                                                         "THEN (SELECT CONVERT(VARCHAR(22), (TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple)) " \
#                                                                                 "FROM TresAses_ISISPayroll.dbo.Empleados " \
#                                                                                 "WHERE TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = USR_PERMISOS_APP.CodEmpleado) ELSE '-' END AS Nombres, " \
#                                     "USR_PERMISOS_APP.MD_AutoriHorasExt, USR_PERMISOS_APP.MD_Presentismo, USR_PERMISOS_APP.MD_Anticipos, USR_PERMISOS_APP.MD_PedidoFlete,  " \
#                                     "USR_PERMISOS_APP.MD_CrearRemito, USR_PERMISOS_APP.MD_ReporteBins, USR_PERMISOS_APP.MD_Chofer " \
#                     "FROM            USUARIOS INNER JOIN " \
#                                     "USR_PERMISOS_APP ON USUARIOS.CodEmpleado = USR_PERMISOS_APP.CodEmpleado " \
#                     "WHERE        (USUARIOS.Usuario = %s) AND (USUARIOS.Clave = %s)"
#                 cursor.execute(sql, [usuario, clave])
#                 consulta = cursor.fetchone()
                
#                 if consulta:
#                     legajo, nombre, hExtras, asistencia, anticipos, pedidoFlete, crearRemito, reporteBins, chofer = map(str, consulta)
#                     response_data = {                        
#                         'Legajo': legajo,
#                         'Nombre': nombre,
#                         'Usuario': usuario,
#                         'HExtras': hExtras,
#                         'Asistencia': asistencia,
#                         'Anticipos': anticipos,
#                         'PedidoFlete': pedidoFlete,
#                         'CrearRemito': crearRemito,
#                         'ReporteBins': reporteBins,
#                         'Chofer': chofer

#                     }
#                     #print("INICIA SESION")
#                     datos = {'Message': 'Success', 'Data': response_data}
#                     estado = "E"
#                     insertaRegistro(usuario,fechaHora,registro,estado)
#                     return JsonResponse(datos)
#                 else:
#                     response_data = {
#                         'Message': 'Not Found',
#                         'Nota': 'Usuario o Contraseña inválidos.'
#                     }
#                     estado = "F"
#                     insertaRegistro(usuario,fechaHora,registro,estado)
#                     return JsonResponse(response_data)
#         except Exception as e:
#             error = str(e)
#             insertar_registro_error_sql("GeneralApp","login_app",usuario,error)
#             response_data = {
#                 'Message': 'Error',
#                 'Nota': error
#             }
#             return JsonResponse(response_data)
#         finally:
#             connections['TRESASES_APLICATIVO'].close()
#     else:
#         response_data = {
#             'Message': 'No se pudo resolver la petición.'
#         }
#         return JsonResponse(response_data)

###  METODO GET PARA TRAER CHACRAS Y ID

def borraBaseDatosApp():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Numerico FROM Parametros_Aplicativo WHERE Codigo = 'APP-DEL-TABLE' " 
            cursor.execute(sql)
            consulta = cursor.fetchone()
            dato = "0"
            if consulta:
                dato = str(consulta[0])
                return dato
            else:
                return dato
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp","borraBaseDatosApp","usuario",error)
        return dato
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

@csrf_exempt
def id_Nombre_Ccostos(request, legajo):
    if request.method == 'GET':
        id = str(legajo)
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
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
            insertar_registro_error_sql("GeneralApp","id_Nombre_Ccostos","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['TRESASES_APLICATIVO'].close()
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
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("GeneralApp","personal_por_Ccostos_asistencia","usuario",error)
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
        insertar_registro_error_sql("GeneralApp","traePersonal","usuario",error)
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
        insertar_registro_error_sql("GeneralApp","traeMotivos","usuario",error)
        return error
    finally:
        connections['S3A'].close()
    
def traeMontoMax():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
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
        insertar_registro_error_sql("GeneralApp","traerMontoMAx","usuario",error)
        return error
    finally:
        connections['TRESASES_APLICATIVO'].close()






#### SUBIR APLICACION


@csrf_exempt
def recibir_apk(request):
    if request.method == 'POST' and request.FILES.get('archivo_apk'):
        archivo_apk = request.FILES['archivo_apk']
        nombre_archivo = archivo_apk.name
        ruta_destino = os.path.join('Applications/Mobile/GeneralApp/archivosAPK/', nombre_archivo)
        try:
            with open(ruta_destino, 'wb+') as destino:
                for chunk in archivo_apk.chunks():
                    destino.write(chunk)
            return JsonResponse({'Message': 'Success','Nota': 'Archivo .apk almacenado correctamente.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("GeneralApp","recibir_apk","usuario",error)
            return JsonResponse({'Message': 'Error','Nota': 'Error al almacenar el archivo .apk: {}'.format(e)}, status=500)
    else:
        return JsonResponse({'mensaje': 'No se encontró el archivo .apk en la solicitud POST.'}, status=400)

@csrf_exempt
def descargar_apk(request, nombre_apk):
    ruta_apk = os.path.join('Applications/Mobile/GeneralApp/archivosAPK/', nombre_apk)
    if os.path.exists(ruta_apk):
        try:
            with open(ruta_apk, 'rb') as archivo:
                contenido = archivo.read()
                response = HttpResponse(contenido, content_type='application/vnd.android.package-archive')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(ruta_apk)}"'
                return response
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("GeneralApp","descargar_apk","usuario",error)
            return JsonResponse({'Message': error})  
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición (El Archivo no Existe).'})

@csrf_exempt
def buscaParametro(request, codigo):
    if request.method == 'GET':
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "SELECT Texto " \
                      "FROM Parametros_Aplicativo " \
                      "WHERE Codigo = %s "
                cursor.execute(sql, [codigo])
                consulta = cursor.fetchone()
                
                if consulta:
                    parametro = str(consulta[0])
                    datos = {'Message': 'Success', 'Parametro': parametro}                    
                    return JsonResponse(datos)
                else:
                    error = 'No se encontraron Parámetros.'
                    response_data = {
                        'Message': 'Error',
                        'Nota': error
                    }
                return JsonResponse(response_data)
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("GeneralApp","buscaParametro","usuario",error)
            response_data = {
                'Message': 'Error',
                'Nota': error
            }
            return JsonResponse(response_data)
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
















