
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
                            INSERT INTO Chofer_Alta (IdTransporte, NombreTransporte, IdChofer, NombreChofer, IdCamion, NombreCamion, IdAcoplado, NombreAcoplado, NumTelefono, IdFirebase, EstadoCamion, FechaAlta, Estado) VALUES 
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
        else:
            values2 = (idTransporte,nombreTransporte,idCamion,nombreCamion,idAcoplado,nombreAcoplado,telefono,idFirebase,idChofer)
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            UPDATE Chofer_Alta SET IdTransporte = %s, NombreTransporte = %s, IdCamion = %s, NombreCamion = %s, IdAcoplado = %s, NombreAcoplado = %s, NumTelefono = %s, IdFirebase = %s, EstadoCamion = 'D', FechaActualiza = GETDATE()
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
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def existe_chofer_alta(idChofer):
    values = [idChofer]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT 1
                    FROM Chofer_Alta
                    WHERE (IdChofer = %s)
                """
            cursor.execute(sql,values)
            consulta = cursor.fetchone()
            if consulta:
                return False
            else:
                return True
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","EXISTE CHOFER CHOFER","GET",error)
        return True

def data_chofer(idChofer):
    values = (idChofer)
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT   ID_CA, IdTransporte, NombreTransporte, IdChofer, NombreChofer, IdCamion, NombreCamion, IdAcoplado, NombreAcoplado, NumTelefono, IdFirebase, EstadoCamion, FechaAlta, Estado
                    FROM Chofer_Alta
                    WHERE (IdChofer = %s)
                """
            cursor.execute(sql, values)
            consulta = cursor.fetchone()
            if consulta:
                info_Alta_chofer = [{'ID_CA': str(consulta[0]), 'IdTransporte': str(consulta[1]), 'NombreTransporte':str(consulta[2]), 'IdChofer':str(consulta[3]), 'NombreChofer':str(consulta[4]),
                                    'IdCamion':str(consulta[5]), 'NombreCamion':str(consulta[6]), 'IdAcoplado':str(consulta[7]), 'NombreAcoplado':str(consulta[8]), 'NumTelefono':str(consulta[9]),
                                    'IdFirebase':str(consulta[10]), 'EstadoCamion':str(consulta[11]), 'FechaAlta':str(consulta[12]), 'Estado':str(consulta[13])}]
                return info_Alta_chofer
            else:
                return []
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","DATA CHOFER","GET",error)
        return []

###OBTENER EL VIAJE CON LOS DESTINOS ASIGNADOS
def Obtener_Viaje_Chacras(request,ID_CA):
    if request.method == 'GET':
        ID_CA = str(ID_CA)
        values = [ID_CA]
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        SELECT        VN.ID_CVN AS ID_VIAJE_NOTI, CA.ID_CA AS ID_CHOFER_ALTA, CA.NombreChofer AS NOM_CHOFER, CA.IdChofer AS ID_CHOFER, 
                                    DCV.ID_CDCV AS ID_DETALLES_CHACRAS, DCV.IdPedidoFlete AS ID_PEDIDO_FLETE, 
                                    DCV.IdChacra AS ID_CHACRA, ISNULL(CH.Latitud,0) AS LATITUD, ISNULL(CH.Longitud,0) AS LONGITUD, RTRIM(CH.Nombre) AS NOM_CHACRA, 
                                    ZN.IdZona AS ID_ZONA, RTRIM(ZN.Nombre) AS NOM_ZONA, CASE PD.Vacios WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Vacios END AS VACIOS, 
                                    ISNULL(VN.CantidadVac, 0) AS CANT_VACIOS, ISNULL(VN.ID_CUV,0) AS ID_UBI_VAC, CASE WHEN UV.Nombre IS NULL THEN '0' ELSE UV.Nombre END AS NOM_UBI_VAC,
                                    ISNULL(UV.Latitud,0) AS LAT_VAC, ISNULL(UV.Longitud,0) AS LONG_VAC, CASE PD.Cuellos WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Cuellos END AS CUELLOS,
			                        RTRIM(PD.Solicitante) AS SOLICITA, ISNULL(US.Telefono,0) AS TELEFONO
                        FROM            Chofer_Alta AS CA INNER JOIN
                                                Chofer_Viajes_Notificacion AS VN ON CA.ID_CA = VN.ID_CA INNER JOIN
                                                Chofer_Detalle_Chacras_Viajes AS DCV ON VN.ID_CVN = DCV.ID_CVN INNER JOIN
                                                S3A.dbo.Chacra AS CH ON CH.IdChacra = DCV.IdChacra INNER JOIN
                                                S3A.dbo.Zona AS ZN ON ZN.IdZona = CH.Zona INNER JOIN
                                                S3A.dbo.PedidoFlete AS PD ON PD.IdPedidoFlete = DCV.IdPedidoFlete LEFT JOIN
                                                Chofer_Ubicacion_Vacios AS UV ON UV.ID_CUV = VN.ID_CUV LEFT JOIN
						                        USUARIOS AS US ON US.Usuario = PD.UserID COLLATE Modern_Spanish_CI_AS
                        WHERE CA.ID_CA = %s 
	                        AND NOT EXISTS (SELECT 1 FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA)
                            AND VN.ID_CVN = (SELECT MIN(ID_CVN) FROM Chofer_Viajes_Notificacion WHERE Estado = 'A' AND ID_CA = CA.ID_CA) 
                            AND DCV.Estado = 'A'
                        ORDER BY DCV.ID_CDCV
                    """
                cursor.execute(sql,values)
                consulta = cursor.fetchall()
                if consulta:
                    viajes = {}
                    for row in consulta:
                        id_viaje = str(row[0])
                        if id_viaje not in viajes:
                            viajes[id_viaje] = {
                                "IdViaje": id_viaje,
                                "IdChoferAlta": str(row[1]),
                                "NombreChofer": str(row[2]),
                                "IdChofer": str(row[3]),
                                "CantVacios": str(row[13]),
                                "IdUbiVac": str(row[14]),
                                "NombreUbiVacios": str(row[15]),
                                "LatVacios": str(row[16]),
                                "LonVacios": str(row[17]),
                                "DetalleChacras": []
                            }
                        
                        detalle_chacra = {
                            "IdDetalleChacras": str(row[4]),
                            "IdPedidoFlete": str(row[5]),
                            "IdChacra": str(row[6]),
                            "LatChacra": str(row[7]),
                            "LonChacra": str(row[8]),
                            "MombreChacra": str(row[9]),
                            "IdZona": str(row[10]),
                            "NombreZona": str(row[11]),
                            "Vacios": str(row[12]),
                            "Cuellos": str(row[18]),
                            "Solicita": str(row[19]),
                            "Telefono": str(row[20])
                        }
                        viajes[id_viaje]["DetalleChacras"].append(detalle_chacra)

                    viajes_list = list(viajes.values())
                    return JsonResponse({'Message': 'Success', 'Viaje': viajes_list})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': "No existen viajes disponibles."})

        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("API","OBTIENE VIAJE","GET",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


@csrf_exempt
def acepta_rechaza_viaje(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        ID_CVN = str(json.loads(body)['ID_CVN'])
        Tipo = str(json.loads(body)['Tipo'])
        values = (ID_CVN)
        if Tipo == "A":
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            UPDATE VN SET VN.Estado = 'V', VN.FechaAltaEstado = GETDATE()
                            FROM Chofer_Viajes_Notificacion AS VN 
                            WHERE VN.ID_CVN = %s;
                        """
                    cursor.execute(sql,values)
                    sql2 = """ 
                            UPDATE DCV SET DCV.Estado = 'V'
                            FROM Chofer_Detalle_Chacras_Viajes AS DCV 
                            WHERE DCV.ID_CVN = %s;
                        """
                    cursor.execute(sql2,values)

                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'El Viaje se Aceptó correctamente.'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Aceptar el viaje, intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","ACEPTA VIAJE","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        if Tipo == "R":
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            UPDATE VN SET VN.Estado = 'R', VN.FechaAltaEstado = GETDATE()
                            FROM Chofer_Viajes_Notificacion AS VN 
                            WHERE VN.ID_CVN = %s;
                        """
                    cursor.execute(sql,values)
                    sql2 = """ 
                            UPDATE DCV SET DCV.Estado = 'R'
                            FROM Chofer_Detalle_Chacras_Viajes AS DCV 
                            WHERE DCV.ID_CVN = %s;
                        """
                    cursor.execute(sql2,values)
                    
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'El Viaje se Rechazó correctamente.'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Rechazar el viaje, intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","RECHAZA VIAJE","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})



















































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