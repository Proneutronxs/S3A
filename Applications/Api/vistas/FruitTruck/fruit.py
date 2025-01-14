
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from Applications.ModelosPDF.remitoChacra import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.http import FileResponse
from django.shortcuts import render
import json
import io


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
                            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'D',GETDATE(),'A')
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
    finally:
        connections['TRESASES_APLICATIVO'].close()

def data_chofer(idChofer):
    values = [idChofer]
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
    finally:
        connections['TRESASES_APLICATIVO'].close()

###OBTENER EL VIAJE CON LOS DESTINOS ASIGNADOS
def Obtener_Viaje_Chacras(request,ID_CA):
    if request.method == 'GET':
        ID_CA = str(ID_CA)
        values = [ID_CA]
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        DECLARE @@ID_CA INT;
                        SET @@ID_CA = %s;

                        IF (SELECT TipoDestino FROM S3A.dbo.PedidoFlete WHERE IdPedidoFlete = 
                            (SELECT TOP 1 CDCV.IdPedidoFlete
                            FROM Chofer_Alta AS CA 
                            LEFT JOIN Chofer_Viajes_Notificacion AS CVN ON CVN.ID_CA = CA.ID_CA 
                            LEFT JOIN Chofer_Detalle_Chacras_Viajes AS CDCV ON CDCV.ID_CVN = CVN.ID_CVN
                            WHERE CA.ID_CA = @@ID_CA
                            AND NOT EXISTS (SELECT 1 FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA)
                            AND CVN.ID_CVN = (SELECT MIN(ID_CVN) FROM Chofer_Viajes_Notificacion WHERE Estado = 'A' AND ID_CA = CA.ID_CA) 
                            AND CDCV.Estado = 'A')) = 'U'
                        BEGIN
                        -- CONSULTA PARA CAMBIOS DE DOMICILIO
                        (SELECT        VN.ID_CVN AS ID_VIAJE_NOTI, CA.ID_CA AS ID_CHOFER_ALTA, CA.NombreChofer AS NOM_CHOFER, CA.IdChofer AS ID_CHOFER, 
                                            DCV.ID_CDCV AS ID_DETALLES_CHACRAS, DCV.IdPedidoFlete AS ID_PEDIDO_FLETE, 
                                            DCV.IdChacra AS ID_CHACRA, ISNULL(UBID.Latitud,0) AS LATITUD, ISNULL(UBID.Longitud,0) AS LONGITUD, RTRIM(UBID.Descripcion) AS NOM_CHACRA, 
                                            COALESCE(ZN.IdZona,'0') AS ID_ZONA, COALESCE(RTRIM(ZN.Nombre),'-') AS NOM_ZONA, CASE PD.Vacios WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE '-' END AS VACIOS, 
                                            ISNULL(VN.CantidadVac, 0) AS CANT_VACIOS, ISNULL(VN.ID_CUV,0) AS ID_UBI_VAC, CASE WHEN UV.Nombre IS NULL THEN '0' ELSE UV.Nombre END AS NOM_UBI_VAC,
                                            ISNULL(UV.Latitud,0) AS LAT_VAC, ISNULL(UV.Longitud,0) AS LONG_VAC, CASE PD.Cuellos WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE '-' END AS CUELLOS,
                                            RTRIM(PD.Solicitante) AS SOLICITA, ISNULL(US.Telefono,0) AS TELEFONO, RTRIM(UBIO.Descripcion) AS ORIGEN, RTRIM(PD.Obs) AS OBSERVACIONES,
                                            CASE WHEN RTRIM(PD.TipoCarga) = 'RAU' THEN 'BINS FRUTA CHACRA' WHEN RTRIM(PD.TipoCarga) = 'VAC' THEN 'BIN VACÍOS' WHEN RTRIM(PD.TipoCarga) = 'EMB' THEN 'EMBALADO'
                                            WHEN RTRIM(PD.TipoCarga) = 'VAR' THEN 'VARIOS' WHEN RTRIM(PD.TipoCarga) = 'MAT' THEN 'MATERIALES' WHEN RTRIM(PD.TipoCarga) = 'FBI' THEN 'FRUTA EN BINS' ELSE RTRIM(PD.TipoCarga) END AS TIPO_CARGA,
                                            PD.TipoDestino AS TIPO_DESTINO
                                FROM            Chofer_Alta AS CA LEFT JOIN
                                                        Chofer_Viajes_Notificacion AS VN ON CA.ID_CA = VN.ID_CA LEFT JOIN
                                                        Chofer_Detalle_Chacras_Viajes AS DCV ON VN.ID_CVN = DCV.ID_CVN LEFT JOIN
                                                        S3A.dbo.Chacra AS CH ON CH.IdChacra = DCV.IdChacra LEFT JOIN
                                                        S3A.dbo.Zona AS ZN ON ZN.IdZona = CH.Zona LEFT JOIN
                                                        S3A.dbo.PedidoFlete AS PD ON PD.IdPedidoFlete = DCV.IdPedidoFlete LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBID ON UBID.IdUbicacion = PD.IdPlantaDestino LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBIO ON UBIO.IdUbicacion = PD.IdPlanta LEFT JOIN
                                                        Chofer_Ubicacion_Vacios AS UV ON UV.ID_CUV = VN.ID_CUV LEFT JOIN
                                                        USUARIOS AS US ON US.Usuario = PD.UserID COLLATE Modern_Spanish_CI_AS
                                WHERE CA.ID_CA = @@ID_CA 
                                    AND NOT EXISTS (SELECT 1 FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA)
                                    AND VN.ID_CVN = (SELECT MIN(ID_CVN) FROM Chofer_Viajes_Notificacion WHERE Estado = 'A' AND ID_CA = CA.ID_CA) 
                                    AND DCV.Estado = 'A')
                        END
                        ELSE 
                        BEGIN
                        -- CONSULTA PARA SOLICITUD DE FLETE CHACRA
                        (SELECT        VN.ID_CVN AS ID_VIAJE_NOTI, CA.ID_CA AS ID_CHOFER_ALTA, CA.NombreChofer AS NOM_CHOFER, CA.IdChofer AS ID_CHOFER, 
                                            DCV.ID_CDCV AS ID_DETALLES_CHACRAS, DCV.IdPedidoFlete AS ID_PEDIDO_FLETE, 
                                            DCV.IdChacra AS ID_CHACRA, ISNULL(CH.Latitud,0) AS LATITUD, ISNULL(CH.Longitud,0) AS LONGITUD, CONVERT(VARCHAR(19),RTRIM(PR.RazonSocial)) +'-'+ RTRIM(CH.Nombre) AS NOM_CHACRA, 
                                            ZN.IdZona AS ID_ZONA, RTRIM(ZN.Nombre) AS NOM_ZONA, CASE PD.Vacios WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Vacios END AS VACIOS, 
                                            ISNULL(VN.CantidadVac, 0) AS CANT_VACIOS, ISNULL(VN.ID_CUV,0) AS ID_UBI_VAC, CASE WHEN UV.Nombre IS NULL THEN '0' ELSE UV.Nombre END AS NOM_UBI_VAC,
                                            ISNULL(UV.Latitud,0) AS LAT_VAC, ISNULL(UV.Longitud,0) AS LONG_VAC, CASE PD.Cuellos WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Cuellos END AS CUELLOS,
                                            RTRIM(PD.Solicitante) AS SOLICITA, ISNULL(US.Telefono,0) AS TELEFONO, RTRIM(UBIO.Descripcion) AS ORIGEN, RTRIM(PD.Obs) AS OBSERVACIONES,
                                            CASE WHEN RTRIM(PD.TipoCarga) = 'RAU' THEN 'BINS FRUTA CHACRA' WHEN RTRIM(PD.TipoCarga) = 'VAC' THEN 'BIN VACÍOS' WHEN RTRIM(PD.TipoCarga) = 'EMB' THEN 'EMBALADO'
                                            WHEN RTRIM(PD.TipoCarga) = 'VAR' THEN 'VARIOS' WHEN RTRIM(PD.TipoCarga) = 'MAT' THEN 'MATERIALES' WHEN RTRIM(PD.TipoCarga) = 'FBI' THEN 'FRUTA EN BINS' ELSE RTRIM(PD.TipoCarga) END AS TIPO_CARGA,
                                            PD.TipoDestino AS TIPO_DESTINO
                                FROM            Chofer_Alta AS CA LEFT JOIN
                                                        Chofer_Viajes_Notificacion AS VN ON CA.ID_CA = VN.ID_CA LEFT JOIN
                                                        Chofer_Detalle_Chacras_Viajes AS DCV ON VN.ID_CVN = DCV.ID_CVN LEFT JOIN
                                                        S3A.dbo.Chacra AS CH ON CH.IdChacra = DCV.IdChacra LEFT JOIN
                                                        S3A.dbo.Zona AS ZN ON ZN.IdZona = CH.Zona LEFT JOIN
                                                        S3A.dbo.PedidoFlete AS PD ON PD.IdPedidoFlete = DCV.IdPedidoFlete LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBID ON UBID.IdUbicacion = PD.IdPlantaDestino LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBIO ON UBIO.IdUbicacion = PD.IdPlanta LEFT JOIN
								                        S3A.dbo.Productor AS PR ON PR.IdProductor = PD.IdProductor LEFT JOIN
                                                        Chofer_Ubicacion_Vacios AS UV ON UV.ID_CUV = VN.ID_CUV LEFT JOIN
                                                        USUARIOS AS US ON US.Usuario = PD.UserID COLLATE Modern_Spanish_CI_AS
                                WHERE CA.ID_CA = @@ID_CA 
                                    AND NOT EXISTS (SELECT 1 FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA)
                                    AND VN.ID_CVN = (SELECT MIN(ID_CVN) FROM Chofer_Viajes_Notificacion WHERE Estado = 'A' AND ID_CA = CA.ID_CA) 
                                    AND DCV.Estado = 'A')
                        END
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
                                "TipoDestino": str(row[24]),
                                "DetalleChacras": []
                            }
                        
                        detalle_chacra = {
                            "IdDetalleChacras": str(row[4]),
                            "IdPedidoFlete": str(row[5]),
                            "IdChacra": str(row[6]),
                            "LatChacra": str(row[7]),
                            "LonChacra": str(row[8]),
                            "MombreChacra": str(row[9]).replace("-","\n"),
                            "IdZona": str(row[10]),
                            "NombreZona": str(row[11]),
                            "Vacios": str(row[12]),
                            "Cuellos": str(row[18]),
                            "Solicita": str(row[19]),
                            "Telefono": str(row[20]),
                            "Origen": str(row[21]),
                            "Observaciones": str(row[22]),
                            "TipoCarga": str(row[23])
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
        values = [ID_CVN]
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
                    sql3 = """ 
                            DECLARE @ID_CVN INT;
                            SET @ID_CVN = %s; 

                            UPDATE S3A.dbo.PedidoFlete
                            SET Estado = 'R'
                            WHERE IdPedidoFlete IN (
                                SELECT CDCV.IdPedidoFlete
                                FROM Chofer_Detalle_Chacras_Viajes AS CDCV
                                WHERE CDCV.ID_CVN = @ID_CVN
                            );
                        """
                    cursor.execute(sql3,values)
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
        if Tipo == "C":
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql3 = """ 
                            DECLARE @ID_CVN INT;
                            SET @ID_CVN = %s; 

                            UPDATE S3A.dbo.PedidoFlete
                            SET Estado = 'R'
                            WHERE IdPedidoFlete IN (
                                SELECT CDCV.IdPedidoFlete
                                FROM Chofer_Detalle_Chacras_Viajes AS CDCV
                                WHERE CDCV.ID_CVN = @ID_CVN
                            );
                        """
                    cursor.execute(sql3,values)
                    sql = """ 
                            UPDATE VN SET VN.Estado = 'R', VN.FechaCancela = GETDATE()
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
                    return JsonResponse({'Message': 'Success', 'Nota': 'El Viaje se CANCELÓ correctamente.'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo cancelar el viaje, intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","CANCELA VIAJE","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        if Tipo == "S3A":
            return JsonResponse({'Message': 'Success', 'Nota': 'Se recibió.'})
            # try:
            #     with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            #         return JsonResponse({'Message': 'Success', 'Nota': 'Se recibió.'})
            # except Exception as e:
            #     error = str(e)
            #     insertar_registro_error_sql("API","CANCELA VIAJE","POST",error)
            #     return JsonResponse({'Message': 'Error', 'Nota': error})
            # finally:
            #     connections['TRESASES_APLICATIVO'].close()
        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def Obtener_Viaje_Aceptado(request,ID_CA):
    if request.method == 'GET':
        ID_CA = str(ID_CA)
        values = [ID_CA]
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        DECLARE @@ID_CA INT;
                        SET @@ID_CA = %s;

                        IF (SELECT TipoDestino FROM S3A.dbo.PedidoFlete WHERE IdPedidoFlete = 
                            (SELECT TOP 1 CDCV.IdPedidoFlete
                            FROM Chofer_Alta AS CA 
                            LEFT JOIN Chofer_Viajes_Notificacion AS CVN ON CVN.ID_CA = CA.ID_CA 
                            LEFT JOIN Chofer_Detalle_Chacras_Viajes AS CDCV ON CDCV.ID_CVN = CVN.ID_CVN
                            WHERE CA.ID_CA = @@ID_CA
                            --AND NOT EXISTS (SELECT 1 FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA)
                            AND CVN.ID_CVN = (SELECT MIN(ID_CVN) FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA) 
                            AND CDCV.Estado = 'V')) = 'U'
                        BEGIN
                        -- CONSULTA PARA CAMBIOS DE DOMICILIO
                        (SELECT        VN.ID_CVN AS ID_VIAJE_NOTI, CA.ID_CA AS ID_CHOFER_ALTA, CA.NombreChofer AS NOM_CHOFER, CA.IdChofer AS ID_CHOFER, 
                                            DCV.ID_CDCV AS ID_DETALLES_CHACRAS, DCV.IdPedidoFlete AS ID_PEDIDO_FLETE, 
                                            DCV.IdChacra AS ID_CHACRA, ISNULL(UBID.Latitud,0) AS LATITUD, ISNULL(UBID.Longitud,0) AS LONGITUD, RTRIM(UBID.Descripcion) AS NOM_CHACRA, 
                                            COALESCE(ZN.IdZona,'0') AS ID_ZONA, COALESCE(RTRIM(ZN.Nombre),'-') AS NOM_ZONA, CASE PD.Vacios WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE '-' END AS VACIOS, 
                                            ISNULL(VN.CantidadVac, 0) AS CANT_VACIOS, ISNULL(VN.ID_CUV,0) AS ID_UBI_VAC, CASE WHEN UV.Nombre IS NULL THEN '0' ELSE UV.Nombre END AS NOM_UBI_VAC,
                                            ISNULL(UV.Latitud,0) AS LAT_VAC, ISNULL(UV.Longitud,0) AS LONG_VAC, CASE PD.Cuellos WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE '-' END AS CUELLOS,
                                            RTRIM(PD.Solicitante) AS SOLICITA, ISNULL(US.Telefono,0) AS TELEFONO, RTRIM(UBIO.Descripcion) AS ORIGEN, RTRIM(PD.Obs) AS OBSERVACIONES,
                                            CASE WHEN RTRIM(PD.TipoCarga) = 'RAU' THEN 'BINS FRUTA CHACRA' WHEN RTRIM(PD.TipoCarga) = 'VAC' THEN 'BIN VACÍOS' WHEN RTRIM(PD.TipoCarga) = 'EMB' THEN 'EMBALADO'
                                            WHEN RTRIM(PD.TipoCarga) = 'VAR' THEN 'VARIOS' WHEN RTRIM(PD.TipoCarga) = 'MAT' THEN 'MATERIALES' WHEN RTRIM(PD.TipoCarga) = 'FBI' THEN 'FRUTA EN BINS' ELSE RTRIM(PD.TipoCarga) END AS TIPO_CARGA,
                                            PD.TipoDestino AS TIPO_DESTINO
                                FROM            Chofer_Alta AS CA LEFT JOIN
                                                        Chofer_Viajes_Notificacion AS VN ON CA.ID_CA = VN.ID_CA LEFT JOIN
                                                        Chofer_Detalle_Chacras_Viajes AS DCV ON VN.ID_CVN = DCV.ID_CVN LEFT JOIN
                                                        S3A.dbo.Chacra AS CH ON CH.IdChacra = DCV.IdChacra LEFT JOIN
                                                        S3A.dbo.Zona AS ZN ON ZN.IdZona = CH.Zona LEFT JOIN
                                                        S3A.dbo.PedidoFlete AS PD ON PD.IdPedidoFlete = DCV.IdPedidoFlete LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBID ON UBID.IdUbicacion = PD.IdPlantaDestino LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBIO ON UBIO.IdUbicacion = PD.IdPlanta LEFT JOIN
                                                        Chofer_Ubicacion_Vacios AS UV ON UV.ID_CUV = VN.ID_CUV LEFT JOIN
                                                        USUARIOS AS US ON US.Usuario = PD.UserID COLLATE Modern_Spanish_CI_AS
                                WHERE CA.ID_CA = @@ID_CA 
                                    --AND NOT EXISTS (SELECT 1 FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA)
                                    AND VN.ID_CVN = (SELECT MIN(ID_CVN) FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA) 
                                    AND DCV.Estado = 'V')
                        END
                        ELSE 
                        BEGIN
                        -- CONSULTA PARA SOLICITUD DE FLETE CHACRA
                        (SELECT        VN.ID_CVN AS ID_VIAJE_NOTI, CA.ID_CA AS ID_CHOFER_ALTA, CA.NombreChofer AS NOM_CHOFER, CA.IdChofer AS ID_CHOFER, 
                                            DCV.ID_CDCV AS ID_DETALLES_CHACRAS, DCV.IdPedidoFlete AS ID_PEDIDO_FLETE, 
                                            DCV.IdChacra AS ID_CHACRA, ISNULL(CH.Latitud,0) AS LATITUD, ISNULL(CH.Longitud,0) AS LONGITUD, RTRIM(CH.Nombre) AS NOM_CHACRA, 
                                            ZN.IdZona AS ID_ZONA, RTRIM(ZN.Nombre) AS NOM_ZONA, CASE PD.Vacios WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Vacios END AS VACIOS, 
                                            ISNULL(VN.CantidadVac, 0) AS CANT_VACIOS, ISNULL(VN.ID_CUV,0) AS ID_UBI_VAC, CASE WHEN UV.Nombre IS NULL THEN '0' ELSE UV.Nombre END AS NOM_UBI_VAC,
                                            ISNULL(UV.Latitud,0) AS LAT_VAC, ISNULL(UV.Longitud,0) AS LONG_VAC, CASE PD.Cuellos WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Cuellos END AS CUELLOS,
                                            RTRIM(PD.Solicitante) AS SOLICITA, ISNULL(US.Telefono,0) AS TELEFONO, RTRIM(UBIO.Descripcion) AS ORIGEN, RTRIM(PD.Obs) AS OBSERVACIONES,
                                            CASE WHEN RTRIM(PD.TipoCarga) = 'RAU' THEN 'BINS FRUTA CHACRA' WHEN RTRIM(PD.TipoCarga) = 'VAC' THEN 'BIN VACÍOS' WHEN RTRIM(PD.TipoCarga) = 'EMB' THEN 'EMBALADO'
                                            WHEN RTRIM(PD.TipoCarga) = 'VAR' THEN 'VARIOS' WHEN RTRIM(PD.TipoCarga) = 'MAT' THEN 'MATERIALES' WHEN RTRIM(PD.TipoCarga) = 'FBI' THEN 'FRUTA EN BINS' ELSE RTRIM(PD.TipoCarga) END AS TIPO_CARGA,
                                            PD.TipoDestino AS TIPO_DESTINO
                                FROM            Chofer_Alta AS CA LEFT JOIN
                                                        Chofer_Viajes_Notificacion AS VN ON CA.ID_CA = VN.ID_CA LEFT JOIN
                                                        Chofer_Detalle_Chacras_Viajes AS DCV ON VN.ID_CVN = DCV.ID_CVN LEFT JOIN
                                                        S3A.dbo.Chacra AS CH ON CH.IdChacra = DCV.IdChacra LEFT JOIN
                                                        S3A.dbo.Zona AS ZN ON ZN.IdZona = CH.Zona LEFT JOIN
                                                        S3A.dbo.PedidoFlete AS PD ON PD.IdPedidoFlete = DCV.IdPedidoFlete LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBID ON UBID.IdUbicacion = PD.IdPlantaDestino LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBIO ON UBIO.IdUbicacion = PD.IdPlanta LEFT JOIN
                                                        Chofer_Ubicacion_Vacios AS UV ON UV.ID_CUV = VN.ID_CUV LEFT JOIN
                                                        USUARIOS AS US ON US.Usuario = PD.UserID COLLATE Modern_Spanish_CI_AS
                                WHERE CA.ID_CA = @@ID_CA 
                                    --AND NOT EXISTS (SELECT 1 FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA)
                                    AND VN.ID_CVN = (SELECT MIN(ID_CVN) FROM Chofer_Viajes_Notificacion WHERE Estado = 'V' AND ID_CA = CA.ID_CA) 
                                    AND DCV.Estado = 'V')
                        END
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
                                "TipoDestino": str(row[24]),
                                "DetalleChacras": []
                            }
                        
                        detalle_chacra = {
                            "IdDetalleChacras": str(row[4]),
                            "IdPedidoFlete": str(row[5]),
                            "IdChacra": str(row[6]),
                            "LatChacra": str(row[7]),
                            "LonChacra": str(row[8]),
                            "MombreChacra": str(row[9]).replace("-","\n"),
                            "IdZona": str(row[10]),
                            "NombreZona": str(row[11]),
                            "Vacios": str(row[12]),
                            "Cuellos": str(row[18]),
                            "Solicita": str(row[19]),
                            "Telefono": str(row[20]),
                            "Origen": str(row[21]),
                            "Observaciones": str(row[22]),
                            "TipoCarga": str(row[23])
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
def mostrar_remitos_fecha_chofer(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        ID_CHOFER = str(json.loads(body)['ID_CHOFER'])
        FECHA = str(json.loads(body)['FECHA'])
        values = [FECHA,ID_CHOFER]
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        SELECT DRM.ID AS ID_REMITO, RTRIM(CH.Nombre) AS CHACRA, RTRIM(EP.Nombre) AS ESPECIE, 
                                RTRIM(VR.Nombre) AS VARIEDAD, DRm.UP AS UP, DRM.Cantidad AS CANTIDAD
                        FROM Datos_Remito_MovBins AS DRM INNER JOIN
                            S3A.dbo.PedidoFlete AS PF ON PF.IdPedidoFlete = DRM.IdAsignacion INNER JOIN
                            S3A.dbo.Chacra AS CH ON CH.IdChacra = PF.IdChacra INNER JOIN
                            S3A.dbo.Especie AS EP ON EP.IdEspecie = PF.IdEspecie INNER JOIN
                            S3A.dbo.Variedad AS VR ON VR.IdVariedad = PF.IdVariedad 
                        WHERE TRY_CONVERT(DATE, DRM.FechaAlta) = TRY_CONVERT(DATE, %s)
                            AND PF.IdChofer = %s
                        ORDER BY DRM.FechaAlta
                    """
                cursor.execute(sql,values)
                consulta = cursor.fetchall()
                if consulta:
                    listado_data = []
                    for row in consulta:
                        idRemito = str(row[0])
                        chacra = str(row[1])
                        especie = str(row[2])
                        variedad = str(row[3])
                        up = str(row[4])
                        cantidad = str(row[5])
                        listado_data.append({'ID': idRemito,'Chacra':chacra,'Especie':especie,'Variedad':variedad,'UP':up,'Cantidad':cantidad})
                    return JsonResponse({'Message': 'Success', 'Nota': 'Mostrando Remitos...', 'Remitos':listado_data})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron Remitos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("API","ACEPTA VIAJE","POST",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def crear_remito_ID(request,ID_REMITO):
    if request.method == 'GET':
        ID_REMITO = str(ID_REMITO)
        values = [ID_REMITO]
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        SELECT DRM.ID AS ID, FORMAT(DRM.NumeroRemito, '00000000') AS NRO_REMITO, CONVERT(VARCHAR(10),DRM.FechaAlta,103) AS FECHA,
                            CONVERT(VARCHAR(5),DRM.FechaAlta,108) + ' Hs.' AS HORA, PF.IdPedidoFlete AS ID_PEDIDO_FLETE, RTRIM(PR.RazonSocial) AS PRODUCTOR,
                            RTRIM(PR.Nombre) AS SEÑOR, RTRIM(PR.Direccion) AS DOMICILIO, RTRIM(CH.Nombre) AS CHACRA, RTRIM(ES.Nombre) AS ESPECIE,
                            RTRIM(VR.Nombre) AS VARIEDAD, DRM.Renspa AS RENSPA, DRM.UP AS UP, RTRIM(CF.Apellidos) + ' ' + RTRIM(CF.Nombres) AS CHOFER,
                            RTRIM(CM.Nombre) AS CAMION, RTRIM(CM.Patente) AS PATENTE, DRM.Cantidad AS CANTIDAD, PF.Solicitante AS CAPATAZ, PR.IdProductor AS ID_PRODUCTOR,
	                        CASE WHEN PR.IdProductor = '5200' THEN '00001' WHEN PR.IdProductor = '5000' THEN '00018' ELSE '00017' END AS ITEM_PRODUCTOR
                        FROM Datos_Remito_MovBins AS DRM INNER JOIN
                            S3A.dbo.PedidoFlete AS PF ON PF.IdPedidoFlete = DRM.IdAsignacion INNER JOIN
                            S3A.dbo.Productor AS PR ON PR.IdProductor = PF.IdProductor INNER JOIN
                            S3A.dbo.Chacra AS CH ON CH.IdChacra = PF.IdChacra INNER JOIN
                            S3A.dbo.Especie AS ES ON ES.IdEspecie = DRM.IdEspecie INNER JOIN
                            S3A.dbo.Variedad AS VR ON VR.IdVariedad = DRM.IdVariedad INNER JOIN
                            S3A.dbo.Chofer AS CF on CF.IdChofer = PF.IdChofer INNER JOIN
                            S3A.dbo.Camion AS CM ON CM.IdCamion = PF.IdCamion 
                        WHERE DRM.ID = %s
                    """
                cursor.execute(sql,values)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        ID = str(row[0])
                        NRO_REMITO = str(row[1])
                        FECHA = str(row[2])
                        HORA = str(row[3])
                        ID_PEDIDO_FLETE = str(row[4])
                        PRODUCTOR = str(row[5])
                        SEÑOR = str(row[6])
                        DOMICILIO = str(row[7])
                        CHACRA = str(row[8])
                        ESPECIE = str(row[9])
                        VARIEDAD = str(row[10])
                        RENSPA = str(row[11])
                        UP = str(row[12])
                        CHOFER = str(row[13])
                        CAMION = str(row[14])
                        PATENTE = str(row[15])
                        CANTIDAD = str(row[16])
                        CAPATAZ = str(row[17])
                        ID_PRODUCTOR = str(row[18])
                        ITEM_PRODUCTOR = str(row[19])
                        values = [ID_PRODUCTOR,NRO_REMITO]
                        if ID_PRODUCTOR == "5000":
                            pdf = Remito_Abadon_Movimiento_Chacras(FECHA,HORA,ITEM_PRODUCTOR,NRO_REMITO,PRODUCTOR,SEÑOR,DOMICILIO,CHACRA,ESPECIE,VARIEDAD,RENSPA,UP,
                                                                   CHOFER,CAMION,PATENTE,CANTIDAD,CAPATAZ)
                            pdf.alias_nb_pages()
                            pdf.add_page()
                            index = 0
                            sqldetalle = """ 
                                SELECT CRM.Cantidad AS CANTIDAD, RTRIM(B.Nombre) AS BIN, RTRIM(M.Nombre) AS MARCA
                                FROM Contenido_Remito_MovBins AS CRM INNER JOIN
                                        S3A.dbo.Bins AS B ON B.IdBins = CRM.IdBins INNER JOIN
                                        S3A.dbo.Marca AS M ON M.IdMarca = CRM.IdMarca
                                WHERE (CRM.IdProductor = %s) AND (CRM.NumeroRemito = %s) AND (CRM.Modificado IS NULL) 
                                """
                            cursor.execute(sqldetalle, values)
                            consultaDetalle = cursor.fetchall()
                            if consultaDetalle:
                                for row in consultaDetalle:
                                    cantidad = str(row[0])
                                    tamaño = str(row[1])
                                    marca = str(row[2])
                                    if index == 9:
                                        pdf.alias_nb_pages()
                                        pdf.add_page()
                                        index = 0
                                    pdf.set_font('Arial', '', 8)
                                    pdf.cell(w=24, h=5, txt= str(cantidad), border='LBR', align='C', fill=0)
                                    pdf.cell(w=86, h=5, txt= str(tamaño), border='BR', align='C', fill=0)
                                    pdf.multi_cell(w=0, h=5, txt= str(marca), border='BR', align='C', fill=0)
                                    index = index + 1
                            fecha = str(FECHA).replace('/', '')
                            name = 'R_00018_' + str(NRO_REMITO) + '_' + fecha + '.pdf'
                            nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name
                            pdf.output(nameDireccion, 'F')
                            return JsonResponse({'Message': 'Success', 'Nota': 'El Remito se creó correctamente.', 'Nombre':name})
                        elif ID_PRODUCTOR == "5200":
                            pdf = Remito_Romik_Movimiento_Chacras(FECHA,HORA,ITEM_PRODUCTOR,NRO_REMITO,PRODUCTOR,SEÑOR,DOMICILIO,CHACRA,ESPECIE,VARIEDAD,RENSPA,UP,
                                                                   CHOFER,CAMION,PATENTE,CANTIDAD,CAPATAZ)
                            pdf.alias_nb_pages()
                            pdf.add_page()
                            index = 0
                            sqldetalle = """ 
                                SELECT CRM.Cantidad AS CANTIDAD, RTRIM(B.Nombre) AS BIN, RTRIM(M.Nombre) AS MARCA
                                FROM Contenido_Remito_MovBins AS CRM INNER JOIN
                                        S3A.dbo.Bins AS B ON B.IdBins = CRM.IdBins INNER JOIN
                                        S3A.dbo.Marca AS M ON M.IdMarca = CRM.IdMarca
                                WHERE (CRM.IdProductor = %s) AND (CRM.NumeroRemito = %s) AND (CRM.Modificado IS NULL) 
                                """
                            cursor.execute(sqldetalle, values)
                            consultaDetalle = cursor.fetchall()
                            if consultaDetalle:
                                for row in consultaDetalle:
                                    cantidad = str(row[0])
                                    tamaño = str(row[1])
                                    marca = str(row[2])
                                    if index == 9:
                                        pdf.alias_nb_pages()
                                        pdf.add_page()
                                        index = 0
                                    pdf.set_font('Arial', '', 8)
                                    pdf.cell(w=24, h=5, txt= str(cantidad), border='LBR', align='C', fill=0)
                                    pdf.cell(w=86, h=5, txt= str(tamaño), border='BR', align='C', fill=0)
                                    pdf.multi_cell(w=0, h=5, txt= str(marca), border='BR', align='C', fill=0)
                                    index = index + 1
                            fecha = str(FECHA).replace('/', '')
                            name = 'R_00001_' + str(NRO_REMITO) + '_' + fecha + '.pdf'
                            nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name
                            pdf.output(nameDireccion, 'F')
                            return JsonResponse({'Message': 'Success', 'Nota': 'El Remito se creó correctamente.', 'Nombre':name})
                        else:
                            pdf = Remito_Movimiento_Chacras(FECHA,HORA,ITEM_PRODUCTOR,NRO_REMITO,PRODUCTOR,SEÑOR,DOMICILIO,CHACRA,ESPECIE,VARIEDAD,RENSPA,UP,
                                                                   CHOFER,CAMION,PATENTE,CANTIDAD,CAPATAZ)
                            pdf.alias_nb_pages()
                            pdf.add_page()
                            index = 0
                            sqldetalle = """ 
                                SELECT CRM.Cantidad AS CANTIDAD, RTRIM(B.Nombre) AS BIN, RTRIM(M.Nombre) AS MARCA
                                FROM Contenido_Remito_MovBins AS CRM INNER JOIN
                                        S3A.dbo.Bins AS B ON B.IdBins = CRM.IdBins INNER JOIN
                                        S3A.dbo.Marca AS M ON M.IdMarca = CRM.IdMarca
                                WHERE (CRM.IdProductor = %s) AND (CRM.NumeroRemito = %s) AND (CRM.Modificado IS NULL) 
                                """
                            cursor.execute(sqldetalle, values)
                            consultaDetalle = cursor.fetchall()
                            if consultaDetalle:
                                for row in consultaDetalle:
                                    cantidad = str(row[0])
                                    tamaño = str(row[1])
                                    marca = str(row[2])
                                    if index == 9:
                                        pdf.alias_nb_pages()
                                        pdf.add_page()
                                        index = 0
                                    pdf.set_font('Arial', '', 8)
                                    pdf.cell(w=24, h=5, txt= str(cantidad), border='LBR', align='C', fill=0)
                                    pdf.cell(w=86, h=5, txt= str(tamaño), border='BR', align='C', fill=0)
                                    pdf.multi_cell(w=0, h=5, txt= str(marca), border='BR', align='C', fill=0)
                                    index = index + 1
                            fecha = str(FECHA).replace('/', '')
                            name = 'R_00017_' + str(NRO_REMITO) + '_' + fecha + '.pdf'
                            nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name
                            pdf.output(nameDireccion, 'F')
                            return JsonResponse({'Message': 'Success', 'Nota': 'El Remito se creó correctamente.', 'Nombre':name})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontró el Remito.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("API","ACEPTA VIAJE","POST",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def descargar_pdf(request, nombreRemito):
    filename = 'Applications/ReportesPDF/RemitosChacra/' + nombreRemito
    return FileResponse(open(filename, 'rb'), content_type='application/pdf')

# buffer = io.BytesIO()
# pdf_output = pdf.output(dest='S').encode('latin1')  # Cambia 'F' por 'S'
# buffer.write(pdf_output)
# buffer.seek(0)

# respuesta = HttpResponse(buffer.getvalue(), content_type='application/pdf')
# respuesta['Content-Disposition'] = f'attachment; filename="R_{NRO_REMITO}.pdf"'
# return respuesta


@csrf_exempt
def cambia_estado_chofer(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        ID_CHOFER = str(json.loads(body)['ID_CHOFER'])
        ESTADO = str(json.loads(body)['ESTADO'])
        values = [ESTADO,ID_CHOFER]
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        UPDATE Chofer_Alta SET EstadoCamion = %s, FechaActualiza = GETDATE() WHERE IdChofer = %s
                    """
                cursor.execute(sql,values)
                cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                affected_rows = cursor.fetchone()[0]
                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'El Estado se actualizó correctamente.'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo actualizar el Estado, intente más tarde.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("API","ACEPTA VIAJE","POST",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def servicio_finalizacion(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        ID_CVN = str(json.loads(body)['ID_CVN'])
        ID_CA = str(json.loads(body)['ID_CA'])
        Finaliza = str(json.loads(body)['Finaliza'])
        LlegaVacios = str(json.loads(body)['LlegaVacios'])
        LlegaPlanta = str(json.loads(body)['LlegaPlanta'])
        Listado_Chacras = json.loads(body)['Chacras']
        Listado_Coordenadas = json.loads(body)['Coordenadas']
        values = [ID_CVN]
        values2 = [ID_CA]
        if Finaliza != '0':
            if LlegaVacios != '0':
                update_vacios(ID_CVN,LlegaVacios)
            if LlegaPlanta != '0':
                update_planta(ID_CVN,LlegaPlanta)
            for chacra in Listado_Chacras:
                ID_CDCV = str(chacra['ID_CDCV'])
                LlegaChacra = str(chacra['LlegaChacra'])
                if LlegaChacra != '0':
                    update_chacra(ID_CDCV,LlegaChacra)
            for coor in Listado_Coordenadas:
                Latitud = str(coor['Latitud'])
                Longitud = str(coor['Longitud'])
                Fecha = str(coor['Fecha'])
                inserta_coordenadas(ID_CVN,Latitud,Longitud,Fecha,ID_CA)
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            UPDATE Chofer_Viajes_Notificacion SET Finaliza = GETDATE(), Estado = 'F' WHERE ID_CVN = %s
                        """
                    cursor.execute(sql,values)
                    sql2 = """ 
                            UPDATE Chofer_Detalle_Chacras_Viajes SET Estado = 'F' WHERE ID_CVN = %s
                        """
                    cursor.execute(sql2,values)
                    sql3 = """ 
                            UPDATE Chofer_Alta SET EstadoCamion = 'D', FechaActualiza = GETDATE() WHERE ID_CA = %s
                        """
                    cursor.execute(sql3,values2)
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Viaje finalizó correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo finalizar el Viaje, intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","FINALIZA VIAJE VIAJE","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        else:
            if LlegaVacios != '0':
                update_vacios(ID_CVN,LlegaVacios)
            if LlegaPlanta != '0':
                update_planta(ID_CVN,LlegaPlanta)
            for chacra in Listado_Chacras:
                ID_CDCV = str(chacra['ID_CDCV'])
                LlegaChacra = str(chacra['LlegaChacra'])
                if LlegaChacra != '0':
                    update_chacra(ID_CDCV,LlegaChacra)
            for coor in Listado_Coordenadas:
                Latitud = str(coor['Latitud'])
                Longitud = str(coor['Longitud'])
                Fecha = str(coor['Fecha'])
                inserta_coordenadas(ID_CVN,Latitud,Longitud,Fecha,ID_CA)
            return JsonResponse({'Message': 'Success', 'Nota': 'Se guardaron todos los Registros.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
def update_vacios(ID_CVN, LlegaVacios):
    values = [LlegaVacios,ID_CVN]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    UPDATE Chofer_Viajes_Notificacion SET LlegaVacios = %s WHERE ID_CVN = %s
                """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","UPDATE VACIOS","FUNCION",error)
    finally:
        connections['TRESASES_APLICATIVO'].close()

def update_chacra(ID_CDCV, LlegaChacra):
    values = [LlegaChacra,ID_CDCV]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    UPDATE Chofer_Detalle_Chacras_Viajes SET LlegaChacra = %s WHERE ID_CDCV = %s
                """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","UPDATE CHACRA","FUNCION",error)
    finally:
        connections['TRESASES_APLICATIVO'].close()

def update_planta(ID_CVN, LlegaPlanta):
    values = [LlegaPlanta,ID_CVN]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    UPDATE Chofer_Viajes_Notificacion SET LlegaPlanta = %s WHERE ID_CVN = %s
                """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","UPDATE PLANTA","FUNCION",error)
    finally:
        connections['TRESASES_APLICATIVO'].close()

def inserta_coordenadas(ID_CVN, Latitud, Longitud, FechaAlta, ID_CA):
    values = [ID_CVN, Latitud, Longitud, FechaAlta,ID_CA]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    DECLARE @@ID_CVN INT;
                    DECLARE @@Latitud VARCHAR(255);
                    DECLARE @@Longitud VARCHAR(255);
                    DECLARE @@FechaAlta DATETIME;
                    DECLARE @@ID_CA INT;

                    SET @@ID_CVN = %s;
                    SET @@Latitud = %s;
                    SET @@Longitud = %s;
                    SET @@FechaAlta = %s;
                    SET @@ID_CA = %s;

                    IF NOT EXISTS (SELECT 1 FROM Chofer_Detalle_Viajes_Coordenadas 
                                    WHERE ID_CVN = @@ID_CVN AND FechaAlta = @@FechaAlta)
                    BEGIN
                    INSERT INTO Chofer_Detalle_Viajes_Coordenadas (ID_CVN, Latitud, Longitud, FechaAlta, ID_CA) 
                    VALUES (@@ID_CVN,@@Latitud,@@Longitud,@@FechaAlta,@@ID_CA)
END
                """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","INSERTA COORDENADAS","FUNCION",error)
    finally:
        connections['TRESASES_APLICATIVO'].close()

@csrf_exempt
def actualiza_notificacion_recibida(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        Tipo = str(json.loads(body)['Tipo'])
        ID_CVN = str(json.loads(body)['ID_CVN'])
        values = [ID_CVN]
        if Tipo == 'N':
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            UPDATE Chofer_Notificacion_Destinos_Actualizados SET EstadoNotificacion = 'R', FechaNotificacion = GETDATE() WHERE ID_CVN = %s
                        """
                    cursor.execute(sql,values)
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Estado de la notificación se actualizó correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo actualizar el Estado de la notificación, intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","RECIBE NOTIFICACION DESTINOS","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        elif Tipo == 'S3A':
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            UPDATE Canal_Notificaciones_Generales SET Estado = 'R', FechaRecibo = GETDATE() WHERE ID_CNG = %s
                        """
                    cursor.execute(sql,values)
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Estado de la notificación (S3A) se actualizó correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo actualizar el Estado de la notificación (S3A), intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","RECIBE NOTIFICACION DESTINOS","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
        else:
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                            UPDATE Chofer_Viajes_Notificacion SET EstadoNotificacion = 'R' WHERE ID_CVN =  %s
                        """
                    cursor.execute(sql,values)
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Estado de la notificación se actualizó correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo actualizar el Estado de la notificación, intente más tarde.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","RECIBE NOTIFICACION","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def Obtener_Nuevos_destinos(request,ID_CA):
    if request.method == 'GET':
        ID_CA = str(ID_CA)
        values = [ID_CA]
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        DECLARE @@ID_CA INT;
                        SET @@ID_CA = %s;

                        IF (SELECT TipoDestino FROM S3A.dbo.PedidoFlete WHERE IdPedidoFlete = 
                            (SELECT TOP 1 CDCV.IdPedidoFlete
                            FROM Chofer_Alta AS CA 
                            LEFT JOIN Chofer_Viajes_Notificacion AS CVN ON CVN.ID_CA = CA.ID_CA 
                            LEFT JOIN Chofer_Detalle_Chacras_Viajes AS CDCV ON CDCV.ID_CVN = CVN.ID_CVN
                            WHERE CA.ID_CA = @@ID_CA
                                AND CVN.Estado = 'V'
                                AND CDCV.Estado <> 'E')) = 'U'
                        BEGIN
                        -- CONSULTA PARA CAMBIOS DE DOMICILIO
                            (SELECT        VN.ID_CVN AS ID_VIAJE_NOTI, CA.ID_CA AS ID_CHOFER_ALTA, CA.NombreChofer AS NOM_CHOFER, CA.IdChofer AS ID_CHOFER, 
                                        DCV.ID_CDCV AS ID_DETALLES_CHACRAS, DCV.IdPedidoFlete AS ID_PEDIDO_FLETE, 
                                        DCV.IdChacra AS ID_CHACRA, ISNULL(CH.Latitud,0) AS LATITUD, ISNULL(CH.Longitud,0) AS LONGITUD, RTRIM(CH.Nombre) AS NOM_CHACRA, 
                                        ZN.IdZona AS ID_ZONA, RTRIM(ZN.Nombre) AS NOM_ZONA, CASE PD.Vacios WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Vacios END AS VACIOS, 
                                        ISNULL(VN.CantidadVac, 0) AS CANT_VACIOS, ISNULL(VN.ID_CUV,0) AS ID_UBI_VAC, CASE WHEN UV.Nombre IS NULL THEN '0' ELSE UV.Nombre END AS NOM_UBI_VAC,
                                        ISNULL(UV.Latitud,0) AS LAT_VAC, ISNULL(UV.Longitud,0) AS LONG_VAC, CASE PD.Cuellos WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Cuellos END AS CUELLOS,
                                        RTRIM(PD.Solicitante) AS SOLICITA, ISNULL(US.Telefono,0) AS TELEFONO, RTRIM(UBIO.Descripcion) AS ORIGEN, RTRIM(PD.Obs) AS OBSERVACIONES,
                                        CASE WHEN PD.TipoCarga = 'RAU' THEN 'BINS FRUTA CHACRA' WHEN PD.TipoCarga = 'VAC' THEN 'BIN VACÍOS' WHEN PD.TipoCarga = 'EMB' THEN 'EMBALADO'
                                        WHEN PD.TipoCarga = 'VAR' THEN 'VARIOS' WHEN PD.TipoCarga = 'MAT' THEN 'MATERIALES' WHEN PD.TipoCarga = 'FBI' THEN 'FRUTA EN BINS' ELSE PD.TipoCarga END AS TIPO_CARGA,
                                        PD.TipoDestino AS TIPO_DESTINO
                            FROM            Chofer_Alta AS CA LEFT JOIN
                                                    Chofer_Viajes_Notificacion AS VN ON CA.ID_CA = VN.ID_CA LEFT JOIN
                                                    Chofer_Detalle_Chacras_Viajes AS DCV ON VN.ID_CVN = DCV.ID_CVN LEFT JOIN
                                                    S3A.dbo.Chacra AS CH ON CH.IdChacra = DCV.IdChacra LEFT JOIN
                                                    S3A.dbo.Zona AS ZN ON ZN.IdZona = CH.Zona LEFT JOIN
                                                    S3A.dbo.PedidoFlete AS PD ON PD.IdPedidoFlete = DCV.IdPedidoFlete LEFT JOIN
                                                    S3A.dbo.Ubicacion AS UBID ON UBID.IdUbicacion = PD.IdPlantaDestino LEFT JOIN
                                                    S3A.dbo.Ubicacion AS UBIO ON UBIO.IdUbicacion = PD.IdPlanta LEFT JOIN
                                                    Chofer_Ubicacion_Vacios AS UV ON UV.ID_CUV = VN.ID_CUV LEFT JOIN
                                                    USUARIOS AS US ON US.Usuario = PD.UserID COLLATE Modern_Spanish_CI_AS
                            WHERE CA.ID_CA = @@ID_CA
                                    AND VN.Estado = 'V'
                                    AND DCV.Estado <> 'E')
                        END
                        ELSE 
                        BEGIN
                        -- CONSULTA PARA SOLICITUD DE FLETE CHACRA
                        (SELECT        VN.ID_CVN AS ID_VIAJE_NOTI, CA.ID_CA AS ID_CHOFER_ALTA, CA.NombreChofer AS NOM_CHOFER, CA.IdChofer AS ID_CHOFER, 
                                            DCV.ID_CDCV AS ID_DETALLES_CHACRAS, DCV.IdPedidoFlete AS ID_PEDIDO_FLETE, 
                                            DCV.IdChacra AS ID_CHACRA, ISNULL(CH.Latitud,0) AS LATITUD, ISNULL(CH.Longitud,0) AS LONGITUD, RTRIM(CH.Nombre) AS NOM_CHACRA, 
                                            ZN.IdZona AS ID_ZONA, RTRIM(ZN.Nombre) AS NOM_ZONA, CASE PD.Vacios WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Vacios END AS VACIOS, 
                                            ISNULL(VN.CantidadVac, 0) AS CANT_VACIOS, ISNULL(VN.ID_CUV,0) AS ID_UBI_VAC, CASE WHEN UV.Nombre IS NULL THEN '0' ELSE UV.Nombre END AS NOM_UBI_VAC,
                                            ISNULL(UV.Latitud,0) AS LAT_VAC, ISNULL(UV.Longitud,0) AS LONG_VAC, CASE PD.Cuellos WHEN 'N' THEN 'NO' WHEN 'S' THEN 'SI' ELSE PD.Cuellos END AS CUELLOS,
                                            RTRIM(PD.Solicitante) AS SOLICITA, ISNULL(US.Telefono,0) AS TELEFONO, RTRIM(UBIO.Descripcion) AS ORIGEN, RTRIM(PD.Obs) AS OBSERVACIONES,
                                            CASE WHEN PD.TipoCarga = 'RAU' THEN 'BINS FRUTA CHACRA' WHEN PD.TipoCarga = 'VAC' THEN 'BIN VACÍOS' WHEN PD.TipoCarga = 'EMB' THEN 'EMBALADO'
                                            WHEN PD.TipoCarga = 'VAR' THEN 'VARIOS' WHEN PD.TipoCarga = 'MAT' THEN 'MATERIALES' WHEN PD.TipoCarga = 'FBI' THEN 'FRUTA EN BINS' ELSE PD.TipoCarga END AS TIPO_CARGA,
                                            PD.TipoDestino AS TIPO_DESTINO
                                FROM            Chofer_Alta AS CA LEFT JOIN
                                                        Chofer_Viajes_Notificacion AS VN ON CA.ID_CA = VN.ID_CA LEFT JOIN
                                                        Chofer_Detalle_Chacras_Viajes AS DCV ON VN.ID_CVN = DCV.ID_CVN LEFT JOIN
                                                        S3A.dbo.Chacra AS CH ON CH.IdChacra = DCV.IdChacra LEFT JOIN
                                                        S3A.dbo.Zona AS ZN ON ZN.IdZona = CH.Zona LEFT JOIN
                                                        S3A.dbo.PedidoFlete AS PD ON PD.IdPedidoFlete = DCV.IdPedidoFlete LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBID ON UBID.IdUbicacion = PD.IdPlantaDestino LEFT JOIN
                                                        S3A.dbo.Ubicacion AS UBIO ON UBIO.IdUbicacion = PD.IdPlanta LEFT JOIN
                                                        Chofer_Ubicacion_Vacios AS UV ON UV.ID_CUV = VN.ID_CUV LEFT JOIN
                                                        USUARIOS AS US ON US.Usuario = PD.UserID COLLATE Modern_Spanish_CI_AS
                                WHERE CA.ID_CA = @@ID_CA
                                    AND VN.Estado = 'V'
                                    AND DCV.Estado <> 'E')
                        END
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
                                "TipoDestino": str(row[24]),
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
                            "Telefono": str(row[20]),
                            "Origen": str(row[21]),
                            "Observaciones": str(row[22]),
                            "TipoCarga": str(row[23])
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
def listado_asignados(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        ID_CA = str(json.loads(body)['ID_CA'])
        values = [ID_CA]
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        SELECT CVN.ID_CVN AS ID_VIAJE, 'DESTINO N°: ' + CONVERT(VARCHAR, ROW_NUMBER() OVER (PARTITION BY CVN.ID_CVN ORDER BY CVN.ID_CVN)) AS NUM_DESTINO,
                            PF.IdPedidoFlete AS NUM_PEDIDO, CONVERT(VARCHAR(20), RTRIM(PF.Solicitante)) AS SOLICITA, RTRIM(PF.Obs) AS OBSERVACIONES,
                            CONVERT(VARCHAR(10), PF.FechaRequerida, 103) AS FECHA_REQUERIDA, 
                            CASE 
                                WHEN PF.HoraRequerida IS NULL THEN CONVERT(VARCHAR(10), PF.HoraPedido, 108) 
                                ELSE CONVERT(VARCHAR(10), PF.HoraRequerida, 108) 		
                            END AS HORA_REQUERIDA,
                            CASE
                                WHEN PF.TipoDestino = 'P' THEN CONVERT(VARCHAR(19),RTRIM(PR.RazonSocial)) +'\n'+ RTRIM(CH.Nombre)
                                WHEN PF.TipoDestino = 'U' THEN RTRIM(UB.Descripcion)
                            END AS DESTINO,
                            US.Telefono AS TELEFONO, RTRIM(OUB.Descripcion) AS ORIGEN
                        FROM Chofer_Alta AS CA LEFT JOIN 
                            Chofer_Viajes_Notificacion AS CVN ON CVN.ID_CA = CA.ID_CA LEFT JOIN 
                            Chofer_Detalle_Chacras_Viajes AS CDCV ON CDCV.ID_CVN = CVN.ID_CVN LEFT JOIN
                            S3A.dbo.PedidoFlete AS PF ON PF.IdPedidoFlete = CDCV.IdPedidoFlete LEFT JOIN
                            S3A.dbo.Chacra AS CH ON CH.IdChacra = CDCV.IdChacra LEFT JOIN
                            S3A.dbo.Ubicacion AS UB ON UB.IdUbicacion = CDCV.IdChacra LEFT JOIN 
                            S3A.dbo.Ubicacion AS OUB ON OUB.IdUbicacion = PF.IdPlanta LEFT JOIN 
                            S3A.dbo.Productor AS PR ON PR.IdProductor = PF.IdProductor LEFT JOIN
                            USUARIOS AS US ON US.Usuario = PF.UserID COLLATE Modern_Spanish_CI_AS
                        WHERE CVN.ID_CA = %s AND CVN.Estado = 'A' AND CDCV.Estado = 'A'
                        ORDER BY CVN.ID_CVN
                    """
                cursor.execute(sql,values)
                results = cursor.fetchall()
                if results:
                    viajes = {}
                    for row in results:
                        num_viaje = str(row[0])
                        if num_viaje not in viajes:
                            viajes[num_viaje] = {
                                "NumViaje":num_viaje,
                                "DetalleDestinos": []
                            }
                        
                        DetalleDestinos = {
                            "NumDestino":str(row[1]),
                            "IdPedidoFlete":str(row[2]),
                            "Solicita":str(row[3]),
                            "Obs":str(row[4]),
                            "Fecha":str(row[5]),
                            "Hora":str(row[6]),
                            "Destinos":str(row[7]),
                            "Telefono":str(row[8]),
                            "Origen":str(row[9])
                        }
                        viajes[num_viaje]["DetalleDestinos"].append(DetalleDestinos)

                    viajes_list = list(viajes.values())
                    return JsonResponse({'Message': 'Success', 'Viajes': viajes_list})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron más viajes.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("API","ACEPTA VIAJE","POST",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def servicio_fcs_online(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        ID_CA = str(json.loads(body)['ID_CA'])
        Tipo = str(json.loads(body)['Tipo'])
        Listado_Coordenadas = json.loads(body)['Coordenadas']

        values = [ID_CA]

        if Tipo == 'F':
            for coor in Listado_Coordenadas:
                Latitud = str(coor['Latitud'])
                Longitud = str(coor['Longitud'])
                Fecha = str(coor['Fecha'])
                inserta_coordenadas_online(Latitud,Longitud,Fecha,ID_CA)

            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql2 = """ 
                            DECLARE @@ID_CA INT;
                            SET @@ID_CA = %s;
                            UPDATE Chofer_Detalle_Chacras_Viajes SET Estado = 'F' 
                            WHERE ID_CVN = (SELECT TOP 1 CVN.ID_CVN 
                                    FROM Chofer_Viajes_Notificacion AS CVN
                                    WHERE ID_CA = @@ID_CA AND CVN.Estado = 'V')
                        """
                    cursor.execute(sql2,values)
                    sql = """ 
                            DECLARE @@ID_CA INT;
                            SET @@ID_CA = %s;

                            UPDATE Chofer_Viajes_Notificacion SET Finaliza = GETDATE(), Estado = 'F' 
                            WHERE ID_CVN = (SELECT TOP 1 CVN.ID_CVN 
                                    FROM Chofer_Viajes_Notificacion AS CVN
                                    WHERE ID_CA = @@ID_CA AND CVN.Estado = 'V')
                        """
                    cursor.execute(sql,values)
                    sql3 = """ 
                            UPDATE Chofer_Alta SET EstadoCamion = 'D', FechaActualiza = GETDATE() WHERE ID_CA = %s
                        """
                    cursor.execute(sql3,values)
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Viaje finalizó correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo finalizar el Viaje, intente más tarde.'})
                    
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("API","FINALIZA VIAJE ONLINE","POST",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['TRESASES_APLICATIVO'].close()

        if Tipo == 'S':
            for coor in Listado_Coordenadas:
                Latitud = str(coor['Latitud'])
                Longitud = str(coor['Longitud'])
                Fecha = str(coor['Fecha'])
                inserta_coordenadas_online(Latitud,Longitud,Fecha,ID_CA)

            return JsonResponse({'Message': 'Success', 'Nota': 'Se guardaron todos los Registros.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


def update_vacios_online(ID_CA, LlegaVacios):
    values = [ID_CA,LlegaVacios]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    DECLARE @@ID_CA INT;
                    SET @@ID_CA = %s;

                    UPDATE Chofer_Viajes_Notificacion 
                    SET LlegaVacios = %s 
                    WHERE ID_CVN = (SELECT TOP 1 CVN.ID_CVN 
                                    FROM Chofer_Viajes_Notificacion AS CVN
                                    WHERE ID_CA = @@ID_CA AND CVN.Estado = 'V')
                """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","UPDATE VACIOS ONLINE","FUNCION",error)
    finally:
        connections['TRESASES_APLICATIVO'].close()

def update_planta_online(ID_CA, LlegaPlanta):
    values = [ID_CA,LlegaPlanta]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    DECLARE @@ID_CA INT;
                    SET @@ID_CA = %s;

                    UPDATE Chofer_Viajes_Notificacion 
                    SET LlegaPlanta = %s 
                    WHERE ID_CVN = (SELECT TOP 1 CVN.ID_CVN 
                                    FROM Chofer_Viajes_Notificacion AS CVN
                                    WHERE ID_CA = @@ID_CA AND CVN.Estado = 'V')
                """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","UPDATE PLANTA ONLINE","FUNCION",error)
    finally:
        connections['TRESASES_APLICATIVO'].close()

def inserta_coordenadas_online(Latitud, Longitud, FechaAlta, ID_CA):
    values = [ID_CA,Latitud, Longitud, FechaAlta]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    DECLARE @@ID_CA INT;
                    DECLARE @@Latitud VARCHAR(255);
                    DECLARE @@Longitud VARCHAR(255);
                    DECLARE @@FechaAlta DATETIME;
                    SET @@ID_CA = %s;
                    SET @@Latitud = %s;
                    SET @@Longitud = %s;
                    SET @@FechaAlta = %s;

                    IF NOT EXISTS (
                    SELECT 1
                    FROM Chofer_Detalle_Viajes_Coordenadas
                    WHERE ID_CVN = (SELECT TOP 1 CVN.ID_CVN 
                                        FROM Chofer_Viajes_Notificacion AS CVN
                                        WHERE ID_CA = @@ID_CA AND CVN.Estado = 'V')
                    AND FechaAlta = @@FechaAlta
                    )
                    BEGIN
                    INSERT INTO Chofer_Detalle_Viajes_Coordenadas (ID_CVN, Latitud, Longitud, FechaAlta, ID_CA) 
                    VALUES ((SELECT TOP 1 CVN.ID_CVN 
                            FROM Chofer_Viajes_Notificacion AS CVN
                            WHERE ID_CA = @@ID_CA AND CVN.Estado = 'V'),@@Latitud,@@Longitud,@@FechaAlta,@@ID_CA)
                    END
                """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","INSERTA COORDENADAS ONLINE","FUNCION",error + " - " + str(values))
    finally:
        connections['TRESASES_APLICATIVO'].close()

def update_chacra_online(ID_CDCV, LlegaChacra):
    values = [LlegaChacra,ID_CDCV]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    UPDATE Chofer_Detalle_Chacras_Viajes SET LlegaChacra = %s WHERE ID_CDCV = %s
                """
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("API","UPDATE CHACRA ONLINE","FUNCION",error)
    finally:
        connections['TRESASES_APLICATIVO'].close()
























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