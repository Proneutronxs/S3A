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
        try:
            idFireBase = str(json.loads(body)['actual'])
        except KeyError:
            idFireBase = "IdAndroid"
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """
                        DECLARE @ParametroUser VARCHAR(255); 
                        DECLARE @ParametroPass VARCHAR(6); 
                        SET @ParametroUser = %s; 
                        SET @ParametroPass = %s;
                        DECLARE @MD_Chofer INT; 
                            SELECT @MD_Chofer = USR_PERMISOS_APP.MD_Chofer 
                            FROM USUARIOS 
                            INNER JOIN USR_PERMISOS_APP ON USUARIOS.CodEmpleado = USR_PERMISOS_APP.CodEmpleado 
                            WHERE (USUARIOS.Usuario = @ParametroUser) AND (USUARIOS.Clave = @ParametroPass); 
                        IF @MD_Chofer = 1 
                        BEGIN 
                            SELECT        USUARIOS.CodEmpleado, (RTRIM(S3A.dbo.Chofer.Apellidos) + ' ' + RTRIM(S3A.dbo.Chofer.Nombres)) AS Nombre, 
                                                USR_PERMISOS_APP.MD_AutoriHorasExt, USR_PERMISOS_APP.MD_Presentismo, USR_PERMISOS_APP.MD_Anticipos, USR_PERMISOS_APP.MD_PedidoFlete,  
                                                USR_PERMISOS_APP.MD_CrearRemito, USR_PERMISOS_APP.MD_ReporteBins, USR_PERMISOS_APP.MD_Chofer, USUARIOS.Usuario, USUARIOS.Tipo,USUARIOS.Chacras,USUARIOS.Centros
                            FROM            S3A.dbo.Chofer INNER JOIN 
                                                    USUARIOS INNER JOIN 
                                                    USR_PERMISOS_APP ON USUARIOS.CodEmpleado = USR_PERMISOS_APP.CodEmpleado ON S3A.dbo.Chofer.IdChofer = USUARIOS.CodEmpleado 
                            WHERE        (USUARIOS.Usuario = @ParametroUser) AND (USUARIOS.Clave = @ParametroPass) 
                        END
                        ELSE 
                        BEGIN 
                            SELECT        USR_PERMISOS_APP.CodEmpleado,CASE WHEN(SELECT TresAses_ISISPayroll.dbo.Empleados.CodEmpleado  
                                FROM TresAses_ISISPayroll.dbo.Empleados  
                                WHERE TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = USR_PERMISOS_APP.CodEmpleado) IS NOT NULL  
                                THEN (SELECT CONVERT(VARCHAR(22), (TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple))  
                                FROM TresAses_ISISPayroll.dbo.Empleados  
                                WHERE TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = USR_PERMISOS_APP.CodEmpleado) ELSE @ParametroUser END AS Nombres, 
                                USR_PERMISOS_APP.MD_AutoriHorasExt, USR_PERMISOS_APP.MD_Presentismo, USR_PERMISOS_APP.MD_Anticipos, USR_PERMISOS_APP.MD_PedidoFlete,   
                                USR_PERMISOS_APP.MD_CrearRemito, USR_PERMISOS_APP.MD_ReporteBins, USR_PERMISOS_APP.MD_Chofer, USUARIOS.Usuario,USUARIOS.Tipo,USUARIOS.Chacras,USUARIOS.Centros  
                            FROM            USUARIOS INNER JOIN  
                                            USR_PERMISOS_APP ON USUARIOS.CodEmpleado = USR_PERMISOS_APP.CodEmpleado  
                            WHERE        (USUARIOS.Usuario = @ParametroUser) AND (USUARIOS.Clave = @ParametroPass) 
                        END
                    """

                cursor.execute(sql, [usuario, clave])
                consulta = cursor.fetchone()
                
                if consulta:
                    legajo, nombre, hExtras, asistencia, anticipos, pedidoFlete, crearRemito, reporteBins, chofer, user, tipo, chacras, centros = map(str, consulta)
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
                        'Tipo': tipo,
                        'Chacras': chacras,
                        'Centros': centros,
                        'Delete': borraBaseDatosApp()

                    }
                    datos = {'Message': 'Success', 'Data': response_data}
                    estado = "E"
                    if idFireBase != '0':
                        if len(idFireBase) > 20:
                            actualizaIDFirebase(usuario,idFireBase)
                    return JsonResponse(datos)
                else:
                    response_data = {
                        'Message': 'Not Found',
                        'Nota': 'Usuario o Contraseña inválidos.'
                    }
                    estado = "F"
                    #insertaRegistro(usuario,fechaHora,registro,estado)
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

def actualizaIDFirebase(usuario,token):
    values = (token, token, usuario)
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ UPDATE USUARIOS 
                        SET IdAndroid = %s 
                        WHERE IdAndroid != %s AND Usuario = %s; """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp","ACTUALIZA ID FIREBASE","usuario",error)

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

@csrf_exempt
def id_Nombre_Ccostos(request, legajo):
    if request.method == 'GET':
        id = str(legajo)
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ EXEC APP_SELECT_CENTROS_X_LEGAJO %s """
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

                    sql2 = """ SELECT Texto FROM Parametros_Aplicativo WHERE Codigo = 'APP-MONTO-MAX' """
                    cursor.execute(sql2)
                    consulta2 = cursor.fetchone()
                    monto = "0"
                    if consulta2:
                        monto = str(consulta2[0])
                    return JsonResponse({'Message': 'Success', 'Data': lista_data, 'DataMotivos': lista_data_motivos, 'Monto': monto})
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
                sql = """ SELECT        Empleados.CodEmpleado AS LEGAJO, principal.dbo.T_Legajos.legCodigo AS LEGCODIGO, Empleados.ApellidoEmple + ' ' + Empleados.NombresEmple AS NOMBREyAPELLIDO 
                      FROM          Empleados INNER JOIN 
                                    principal.dbo.T_Legajos ON CONVERT(VARCHAR, Empleados.CodEmpleado) = principal.dbo.T_Legajos.legLegajo 
                      WHERE        (Empleados.Regis_CCo = %s AND Empleados.BajaDefinitivaEmple='2')
                      ORDER BY Empleados.ApellidoEmple """
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
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """EXEC APP_SELECT_EMPLEADOS_X_REGIS_CCO %s"""
                cursor.execute(sql, [id])
                consulta = cursor.fetchall()
                lista_data = []
                if consulta:
                    for row in consulta:
                        legajo = str(row[0]) if row[0] is not None else ''
                        Regis_Epl = str(row[1]) if row[1] is not None else ''
                        nombre = str(row[2]) if row[2] is not None else ''
                        datos = {'Legajo': legajo, 'Regis_Epl': Regis_Epl, 'Nombre': nombre}
                        lista_data.append(datos)
            return JsonResponse({'Message': 'Success','Datos': lista_data,'DataPersonal':lista_data})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("GeneralApp","traePersonal","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    

def traePersonal(id):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """EXEC APP_SELECT_EMPLEADOS_X_REGIS_CCO %s"""
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
    
def traeMotivos():
    try:
        with connections['S3A'].cursor() as cursor:
            sql = """SELECT IdMotivo AS ID, RTRIM(Descripcion) AS MOTIVO 
                    FROM RH_HE_Motivo 
                    ORDER BY Descripcion """
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
    
def traeMontoMax():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql2 = """ SELECT Texto FROM Parametros_Aplicativo WHERE Codigo = 'APP-MONTO-MAX' """
            cursor.execute(sql2)
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



### ACTUALIZACIÓN DE BASE DE DATOS

def Actualiza_Datos():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT Numerico
                    FROM Parametros_Aplicativo
                    WHERE Codigo = 'APP-ACT-DATOS'

                """
            cursor.execute(sql)
            consulta = cursor.fetchone() 
            if consulta:
                if str(consulta[0]) == '1':
                    return True
                else:
                    return False
            else: 
                return False
    except Exception as e:
        error = str(e)
        return False
    finally:
        connections['TRESASES_APLICATIVO'].close()

def Datos_usuario_aplicacion():
    listado_usuarios = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT        ID_USR, CodEmpleado, Usuario, Clave, Tipo, Telefono, Productor, Chacras, Centros, IdAndroid
                    FROM            USUARIOS
                    --WHERE Tipo = 'EC' AND Tipo = 'G'
                """
            cursor.execute(sql)
            consulta = cursor.fetchall() 
            if consulta:
                for row in consulta:
                    ID = str(row[0])
                    CodEmpleado = str(row[1])
                    Usuario = str(row[2])
                    Clave = str(row[3])
                    Tipo = str(row[4])
                    Telefono = str(row[5])
                    Productor = str(row[6])
                    Chacras = str(row[7])
                    Centros = str(row[8])
                    IdAndroid = str(row[9])
                    datos = {'ID': ID, 'CodEmpleado': CodEmpleado, 'Usuario': Usuario, 'Clave': Clave, 'Tipo': Tipo,
                             'Telefono': Telefono, 'Productor':Productor, 'Chacras': Chacras, 'Centros': Centros, 'IdAndroid':IdAndroid}
                    listado_usuarios.append(datos)
                    
                return listado_usuarios
            else: 
                return listado_usuarios
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp","Datos_usuario_aplicacion","usuario",error)
        return listado_usuarios
    finally:
        connections['TRESASES_APLICATIVO'].close()

def Datos_centros_aplicacion():
    listado_centros = []
    try:
        with connections['ISISPayroll'].cursor() as cursor:
            sql = """ 
                    SELECT Regis_CCo AS ID, DescrCtroCosto AS ALIAS
                    FROM CentrosCostos 
                    WHERE DescrCtroCosto LIKE 'C%'
                    ORDER BY DescrCtroCosto

                """
            cursor.execute(sql)
            consulta = cursor.fetchall() 
            if consulta:
                for row in consulta:
                    ID = str(row[0])
                    centro = str(row[1])
                    datos = {'ID': ID, 'Centro': centro}
                    listado_centros.append(datos)
                    
                return listado_centros
            else: 
                return listado_centros
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp","Datos_usuario_aplicacion","usuario",error)
        return listado_centros
    finally:
        connections['ISISPayroll'].close()

def Datos_usuario_permisos():
    listado_permisos = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT         CodEmpleado, MD_Anticipos, MD_Presentismo, MD_AutoriHorasExt, MD_PedidoFlete, MD_CrearRemito, MD_ReporteBins, MD_Chofer
                    FROM            USR_PERMISOS_APP
                """
            cursor.execute(sql)
            consulta = cursor.fetchall() 
            if consulta:
                for row in consulta:
                    CodEmpleado = str(row[0])
                    Anticipos = str(row[1])
                    Presentismo = str(row[2])
                    HorasExtras = str(row[3])
                    PedidoFlete = str(row[4])
                    Remito = str(row[5])
                    ReporteBins = str(row[6])
                    Chofer = str(row[7])
                    datos = {'CodEmpleado': CodEmpleado, 'Anticipos': Anticipos, 'Presentismo': Presentismo, 'HorasExtras': HorasExtras,
                             'PedidoFlete': PedidoFlete, 'Remmito':Remito, 'ReporteBins': ReporteBins, 'Chofer':Chofer}
                    listado_permisos.append(datos)
                    
                return listado_permisos
            else: 
                return listado_permisos
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp","Datos_usuario_permisos","usuario",error)
        return listado_permisos
    finally:
        connections['TRESASES_APLICATIVO'].close()

def Datos_legajos():
    listado_legajos = []
    try:
        with connections['ISISPayroll'].cursor() as cursor:
            sql = """ 
                    SELECT        Empleados.CodEmpleado AS LEGAJO, Empleados.Regis_CCo AS CENTRO, Empleados.ApellidoEmple + ' ' + Empleados.NombresEmple AS NOMBRE
                    FROM            Empleados INNER JOIN
                                            CentrosCostos ON Empleados.Regis_CCo = CentrosCostos.Regis_CCo
                    WHERE        (Empleados.BajaDefinitivaEmple = '2') AND CentrosCostos.DescrCtroCosto LIKE 'C%'
                """
            cursor.execute(sql)
            consulta = cursor.fetchall() 
            if consulta:
                for row in consulta:
                    CodEmpleado = str(row[0])
                    Centro = str(row[1])
                    Nombres = str(row[2])
                    datos = {'CodEmpleado': CodEmpleado, 'Centro': Centro, 'Nombres': Nombres}
                    listado_legajos.append(datos)
                    
                return listado_legajos
            else: 
                return listado_legajos
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp","Datos_legajos","usuario",error)
        return listado_legajos
    finally:
        connections['ISISPayroll'].close()

def Datos_Chacras_Aplicacion():
    listado = listado_Chacras()
    resultado = ','.join(f"'{chacra}'" for chacra in listado)
    listado_chacras_dev = []
    try:
        with connections['S3A'].cursor() as cursor:
            sql = f""" 
                    SELECT        IdChacra, RTRIM(Nombre)
                    FROM            Chacra
                    WHERE IdChacra IN ({resultado})
                    ORDER BY Nombre
                """
            cursor.execute(sql)
            consulta = cursor.fetchall() 
            if consulta:
                for row in consulta:
                    IdChacra = str(row[0])
                    NombreChacra = str(row[1])
                    datos = {'IdChacra': IdChacra, 'Nombre': NombreChacra}
                    listado_chacras_dev.append(datos)
                    
                return listado_chacras_dev
            else: 
                return listado_chacras_dev
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp","Datos_Chacras_Aplicacion","usuario",error)
        return listado_chacras_dev
    finally:
        connections['S3A'].close()

def listado_Chacras():
    listado_chacras = set()  # Usar un conjunto para evitar duplicados
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT Chacras
                    FROM USUARIOS
                    --WHERE Tipo = 'EC'
                """
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    if row[0] is not None:
                        listado = str(row[0]).split(',')
                        for i in listado:
                            listado_chacras.add(str(i))  # Agregar al conjunto
            return list(listado_chacras)  # Convertir el conjunto a lista antes de devolver
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp", "listado_Chacras", "usuario", error)
        return list(listado_chacras) 

@csrf_exempt
def sincronizaDatos(request):
    if request.method == 'GET':
        
        try:
            datos = {'Message': 'Success', 'Centros': Datos_centros_aplicacion(), 'Chacras': Datos_Chacras_Aplicacion(), 'Legajos': Datos_legajos(), 'Usuarios':Datos_usuario_aplicacion(), 'Permisos': Datos_usuario_permisos()}
            return JsonResponse(datos)
        except Exception as e:
            response_data = {
            'Message': 'No se pudo resolver la petición. ' + str(e)
            }
            return JsonResponse(response_data)

    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
    
@csrf_exempt
def sincronizaLegajosChacras(request):
    if request.method == 'GET':
        
        try:
            datos = {'Message': 'Success', 'Chacras': Datos_Chacras_Aplicacion(), 'Legajos': Datos_legajos()}
            return JsonResponse(datos)
        except Exception as e:
            response_data = {
            'Message': 'No se pudo resolver la petición. ' + str(e)
            }
            return JsonResponse(response_data)

    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
    
@csrf_exempt
def sincronizaUsuariosPermisos(request):
    if request.method == 'GET':
        
        try:
            datos = {'Message': 'Success', 'Usuarios':Datos_usuario_aplicacion(), 'Permisos': Datos_usuario_permisos()}
            return JsonResponse(datos)
        except Exception as e:
            response_data = {
            'Message': 'No se pudo resolver la petición. ' + str(e)
            }
            return JsonResponse(response_data)

    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)



@csrf_exempt
def buscaLegajosNuevos(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        usuario = str(json.loads(body)['usuario'])
        try:
            with connections['ISISPayroll'].cursor() as cursor:
                sql = """
                    SELECT 
                        CodEmpleado AS LEGAJO, 
                        Regis_CCo AS CENTRO, 
                        CONVERT(VARCHAR(25), ApellidoEmple + ' ' + NombresEmple) AS NOMBRE
                    FROM 
                        Empleados
                    WHERE 
                    BajaDefinitivaEmple = 2 AND
                        Regis_CCo IN (
                            SELECT 
                                valor 
                            FROM 
                                dbo.fn_Split((SELECT Centros FROM TRESASES_APLICATIVO.dbo.USUARIOS WHERE Usuario = %s), ',')
                        )
                    ORDER BY 
                        ApellidoEmple + ' ' + NombresEmple
                    """

                cursor.execute(sql, [usuario])
                consulta = cursor.fetchall()
                
                if consulta:
                    response_data = []
                    for row in consulta:
                        legajo, centros, nombre = map(str, row)
                        response_data.append({
                            'Legajos': legajo,
                            'Centros': centros,
                            'Nombres': nombre
                        })
                    datos = {'Message': 'Success', 'Data': response_data}
                    estado = "E"
                    return JsonResponse(datos)
                else:
                    response_data = {
                        'Message': 'Not Found',
                        'Nota': 'No se encontraron datos.'
                    }
                    return JsonResponse(response_data)
        except Exception as e:
            error = str(e)
            response_data = {
                'Message': 'Error',
                'Nota': error
            }
            return JsonResponse(response_data)
        finally:
            connections['ISISPayroll'].close()
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)


@csrf_exempt
def insertaAdicionales(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            usuario = str(json.loads(body)['usuario'])
            datos = json.loads(body)['Data']
            listadoFilas = []
            for item in datos:
                IdAdicional = str(item['IdAdicional'])
                IdEncargado = str(item['IdEncargado'])
                IdLegajo = str(item['IdLegajo'])
                Centro = str(item['Centro'])
                Categoria = str(item['Categoria'])
                Descripcion = str(item['Descripcion'])
                Tarea = str(item['Tarea'])
                Jornales = str(item['Jornales'])
                qr = item['qr']
                Tipo = str(item['Tipo'])
                Cantidad = str(item['Cantidad'])
                NroFila = str(item['NroFila'])
                Precio = str(item['Precio'])
                Lote = str(item['Lote'])
                Cuadro = str(item['Cuadro'])
                Pago = str(item['Pago'])
                Observaciones = str(item['Observaciones'])
                Semana = str(item.get('Semana', '0'))
                Usuario = str(item['Usuario'])
                FechaAlta = str(item['FechaAlta']).replace(' ','T')
                if qr is None or qr == '' or qr == 'null' or qr == 'NULL' or qr =='0':
                    #print(IdAdicional,IdEncargado,IdLegajo,Centro,Categoria,Descripcion,Tarea,Jornales, str(qr),Tipo,Cantidad,NroFila,Precio,Lote,Cuadro,Pago,Observaciones,usuario,FechaAlta,Usuario)
                    guardaAdicional(IdAdicional,IdEncargado,IdLegajo,Centro,Categoria,Descripcion,Tarea,Jornales,str(qr),Tipo,Cantidad,NroFila,Precio,Lote,Cuadro,Pago,Observaciones, Semana,usuario,FechaAlta,Usuario)
                else:
                    if  existeQR(str(qr),Tarea,IdLegajo):
                        existe = "Fila: " + NroFila + " " + nombreChacra(Lote)
                        listadoFilas.append(existe)
                    else:
                        #print(IdAdicional,IdEncargado,IdLegajo,Centro,Categoria,Descripcion,Tarea,Jornales,str(qr),Tipo,Cantidad,NroFila,Precio,Lote,Cuadro,Pago,Observaciones,usuario,FechaAlta,Usuario)
                        guardaAdicional(IdAdicional,IdEncargado,IdLegajo,Centro,Categoria,Descripcion,Tarea,Jornales,str(qr),Tipo,Cantidad,NroFila,Precio,Lote,Cuadro,Pago,Observaciones, Semana,usuario,FechaAlta,Usuario)
            if listadoFilas:
                nota = 'Las siguientes filas ya están cargadas: \n \n' + ', \n'.join(listadoFilas) + '.'
                return JsonResponse({'Message': 'Success', 'Nota': nota})  
            else:
                nota = "Los registros se guardaron exitosamente."
                return JsonResponse({'Message': 'Success', 'Nota': nota})                  
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("GENERAL","INSERTA ADICIONALES","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'}) 


def nombreChacra(idChacra):
    nombre = ""
    try:
        with connections['S3A'].cursor() as cursor:
            sql = """ 
                    SELECT RTRIM(Nombre)
                    FROM Chacra
                    WHERE IdChacra = %s
                """
            cursor.execute(sql, [idChacra])
            consulta = cursor.fetchone()
            if consulta:
                return str(consulta[0])
            return nombre  
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp", "NOMBRE CHACRA", "usuario", error)
        return nombre
    
def existeQR(qr,tarea,legajo):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT QR
                    FROM Planilla_Chacras
                    WHERE QR = %s AND Tarea = %s AND Legajo = %s AND YEAR(Fecha) = YEAR(GETDATE())
                """
            cursor.execute(sql,[qr,tarea,legajo])
            consulta = cursor.fetchall()
            if consulta:
                return True
            return False  
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp", "EXISTE QR", "usuario", error)
        return False
    
def guardaAdicional(IdLocal, IdEncargado, Legajo, Centro, Categoria, Descripcion, Tarea, Jornales, QR, Tipo, Cantidad, NroFila, PrecioUnitario, Lote, Cuadro, Pago, Observaciones, Semana, Usuario, Fecha, UserAlta):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Planilla_Chacras (IdLocal, IdEncargado, Legajo, Centro, Categoria, Descripcion, Tarea, Jornales, QR, Tipo, Cantidad, NroFila, PrecioUnitario, Lote, Cuadro, Pago, Observaciones, Semana, Usuario, Fecha, UserAlta, FechaAlta,E) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, GETDATE(),'P')"
            values = (IdLocal, IdEncargado, Legajo, Centro, Categoria, Descripcion, Tarea, Jornales, QR, Tipo, Cantidad, NroFila, PrecioUnitario, Lote, Cuadro, Pago, Observaciones, Semana, Usuario, Fecha, UserAlta)
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GeneralApp", "GUARDA ADICIONAL", "usuario", error)
    finally:
        connections['TRESASES_APLICATIVO'].close()




























