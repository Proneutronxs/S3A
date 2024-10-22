
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import json


def listarTransporte(request):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """ 
                        SELECT IdTransportista, RTRIM(CONVERT(VARCHAR(23), RazonSocial)) AS RAZON_SOCIAL
                        FROM Transportista 
                        WHERE Activo ='S' 
                        ORDER BY RazonSocial
                    """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        idTransporte = str(row[0])
                        razonSocial = str(row[1])
                        datos = {'IdTransporte': idTransporte, 'RazonSocial': razonSocial}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("API","LISTAR TRANSPORTES","GET",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def listarDataTransporte(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        idTransporte = str(json.loads(body)['IdTransporte'])
        try:
            with connections['S3A'].cursor() as cursor:

                lista_chofer = []
                lista_camion = []
                lista_acoplado = []


                sql = """ 
                    SELECT IdChofer, ISNULL(RTRIM(Apellidos),'') + ' ' + ISNULL(RTRIM(Nombres),'') 
                    FROM Chofer 
                    WHERE IdTransportista = %s 
                    ORDER BY Apellidos, Nombres
                    """
                cursor.execute(sql, [idTransporte])
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idChofer = str(row[0])
                        nombre = str(row[1])
                        datos = {'IdChofer': idChofer, 'Chofer': nombre}
                        lista_chofer.append(datos)

                sql2 = """ 
                    SELECT IdCamion, Descripcion = RTRIM(Nombre) + ' - ' + RTRIM(CONVERT(CHAR(6),Tara)) + ' - ' + RTRIM(Patente)
                    FROM Camion 
                    WHERE IdTransportista = %s 
                    ORDER BY Nombre
                    """
                cursor.execute(sql2, [idTransporte])
                consulta2 = cursor.fetchall()
                if consulta2:
                    for row2 in consulta2:
                        idCamion = str(row2[0])
                        camion = str(row2[1])
                        datos = {'IdCamion': idCamion, 'Camion': camion}
                        lista_camion.append(datos)

                sql3 = """ 
                    SELECT IdAcoplado, Descripcion = RTRIM(Nombre) + ' - ' + RTRIM(CONVERT(CHAR(6),Tara)) + ' - ' + RTRIM(Patente) 
                    FROM Acoplado 
                    WHERE IdTransportista = %s 
                    ORDER BY Nombre
                    """
                cursor.execute(sql3, [idTransporte])
                consulta3 = cursor.fetchall()
                if consulta3:
                    for row3 in consulta3:
                        idAcoplado = str(row3[0])
                        acoplado = str(row3[1])
                        datos = {'IdAcoplado': idAcoplado, 'Acoplado': acoplado}
                        lista_acoplado.append(datos)


                if lista_chofer and lista_camion and lista_acoplado:
                    return JsonResponse({'Message': 'Success', 'DataChofer': lista_chofer, 'DataCamion':lista_camion, 'DataAcoplado':lista_acoplado})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("GeneralApp","personal_por_Ccostos_asistencia","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def guardar_transporte_chofer(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        idTransporte = str(json.loads(body)['IdTransporte'])
        nombreTransporte = str(json.loads(body)['NombreTransporte'])
        idChofer = str(json.loads(body)['IdChofer'])
        nombreChofer = str(json.loads(body)['NombreChofer'])
        idCamion = str(json.loads(body)['IdCamion'])
        nombreCamion = str(json.loads(body)['NombreCamion'])
        idAcoplado = str(json.loads(body)['IdAcoplado'])
        nombreAcoplado = str(json.loads(body)['NombreAcoplado'])
        telefono = str(json.loads(body)['Telefono'])
        idFirebase = str(json.loads(body)['IdFirebase'])
        values = (idTransporte,nombreTransporte,idChofer,nombreChofer,idCamion,nombreCamion,idAcoplado,nombreAcoplado,telefono,idFirebase)
        if existe_chofer_alta(idChofer):
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            INSERT INTO Transporte_Chofer_Alta (IdTransporte, NombreTransporte, IdChofer, NombreChofer, IdCamion, NombreCamion, IdAcoplado, NombreAcoplado, NumTelefono, IdFirebase, EstadoCamion, FechaAlta, Estado) VALUES 
                            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'D',GETDATE(),'S')
                        """
                    cursor.execute(sql,values)
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                if affected_rows > 0:
                    info_Alta_chofer = data_chofer(idChofer)
                    return JsonResponse({'Message': 'Success', 'Nota': 'El Chofer se dió de alta Correctamente.', 'Info': info_Alta_chofer})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo dar de alta el Chofer, intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","GUARDA CHOFER","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        else:
            values2 = (idTransporte,nombreTransporte,idCamion,nombreCamion,idAcoplado,nombreAcoplado,telefono,idFirebase,idChofer)
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            UPDATE Transporte_Chofer_Alta SET IdTransporte = %s, NombreTransporte = %s, IdCamion = %s, NombreCamion = %s, IdAcoplado = %s, NombreAcoplado = %s, NumTelefono = %s, IdFirebase = %s, EstadoCamion = 'D'
                            WHERE (IdChofer = %s)
                        """
                    cursor.execute(sql,values2)
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                if affected_rows > 0:
                    info_Alta_chofer = data_chofer(idChofer)
                    return JsonResponse({'Message': 'Success', 'Nota': 'El Chofer se actualizó Correctamente.', 'Info': info_Alta_chofer})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo actualizar el Chofer, intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","ACTUALIZA CHOFER","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def existe_chofer_alta(idChofer):
    values = [idChofer]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT 1
                    FROM Transporte_Chofer_Alta
                    WHERE (IdChofer = %s)
                """
            cursor.execute(sql,values)
            consulta = cursor.fetchone()
            if consulta:
                return False
            else:
                return True
    except Exception as e:
        return True
    finally:
        connections['TRESASES_APLICATIVO'].close()

def data_chofer(idChofer):
    values = (idChofer)
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT   ID_TC, IdTransporte, NombreTransporte, IdChofer, NombreChofer, IdCamion, NombreCamion, IdAcoplado, NombreAcoplado, NumTelefono, IdFirebase, EstadoCamion, FechaAlta, Estado
                    FROM Transporte_Chofer_Alta
                    WHERE (IdChofer = %s)
                """
            cursor.execute(sql,values)
            consulta = cursor.fetchone()
            if consulta:
                info_Alta_chofer = [{'ID_TC': str(consulta[0]), 'IdTransporte': str(consulta[1]), 'NombreTransporte':str(consulta[2]), 'IdChofer':str(consulta[3]), 'NombreChofer':str(consulta[4]),
                                    'IdCamion':str(consulta[5]), 'NombreCamion':str(consulta[6]), 'IdAcoplado':str(consulta[7]), 'NombreAcoplado':str(consulta[8]), 'NumTelefono':str(consulta[9]),
                                    'IdFirebase':str(consulta[10]), 'EstadoCamion':str(consulta[11]), 'FechaAlta':str(consulta[12]), 'Estado':str(consulta[13])}]
                return info_Alta_chofer
            else:
                return []
    except Exception as e:
        return []
    finally:
        connections['TRESASES_APLICATIVO'].close()





# CREATE TABLE Transporte_Chofer_Alta
#    (
#       ID_TC INT IDENTITY(1,1) PRIMARY KEY,
# 	  IdTransporte INT,
# 	  NombreTransporte VARCHAR(255),
# 	  IdChofer INT,
# 	  NombreChofer VARCHAR(255),
# 	  IdCamion INT,
# 	  NombreCamion VARCHAR(255),
# 	  IdAcoplado INT,
# 	  NombreAcoplado VARCHAR(255),
# 	  NumTelefono VARCHAR(255),
# 	  IdFirebase VARCHAR(MAX),
# 	  EstadoCamion VARCHAR(5),
# 	  FechaAlta DATETIME,
# 	  Estado VARCHAR(1)
#    )




















































# SELECT IdTransportista, RTRIM(CONVERT(VARCHAR(23), RazonSocial)) AS RAZON_SOCIAL
# FROM Transportista 
# WHERE Activo ='S' 
# ORDER BY RazonSocial

# SELECT IdChofer, ISNULL(RTRIM(Apellidos),'') + ' ' + ISNULL(RTRIM(Nombres),'') 
# FROM Chofer 
# WHERE IdTransportista = 1000325 
# ORDER BY Apellidos, Nombres

# SELECT IdCamion, Descripcion = RTRIM(Nombre) + ' - ' + RTRIM(CONVERT(CHAR(6),Tara)) + ' - ' + RTRIM(Patente)
# FROM Camion 
# WHERE IdTransportista = 1000325 
# ORDER BY Nombre

# SELECT IdAcoplado, Descripcion = RTRIM(Nombre) + ' - ' + RTRIM(CONVERT(CHAR(6),Tara)) + ' - ' + RTRIM(Patente) 
# FROM Acoplado 
# WHERE IdTransportista = 1000325 
# ORDER BY Nombre