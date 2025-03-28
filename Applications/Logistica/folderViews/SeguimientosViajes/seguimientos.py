from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from Applications.NotificacionesPush.notificaciones_push import enviar_notificacion_chofer_solicita
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.http import JsonResponse
import datetime 
import json



@login_required
@csrf_exempt
def listadoChofer(request):
    if request.method == 'GET':
        user_has_permission = request.user.has_perm('Logistica.puede_ver')
        if user_has_permission:  
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ SELECT        CONVERT(VARCHAR(26), RTRIM(S3A.dbo.Transportista.RazonSocial)) AS TRANSPORTE, Logistica_Estado_Camiones.NombreChofer AS NOMBRE, 
                                        (CONVERT(VARCHAR(10), Logistica_Estado_Camiones.Actualizado, 103) + ' - ' + CONVERT(VARCHAR(8), Logistica_Estado_Camiones.Actualizado, 108) + ' Hs.') AS ACTUALIZADO,
                                        CASE Logistica_Estado_Camiones.Disponible WHEN 'S' THEN 'DISPONIBLE' ELSE 'NO DISPONIBLE' END AS DISPONIBILIDAD,
                                        CASE Logistica_Estado_Camiones.Disponible WHEN 'S' THEN '#008f39e7' ELSE '#d5393ce8' END AS COLOR_HEXA_DISPONIBLE,
                                        CASE Logistica_Estado_Camiones.Libre WHEN 'S' THEN 'LIBRE' ELSE 'OCUPADO' END AS DISPONIBILIDAD,
                                        CASE Logistica_Estado_Camiones.Libre WHEN 'S' THEN '#008f39e7' ELSE '#d5393ce8' END AS COLOR_HEXA_DISPONIBLE
                            FROM            Logistica_Estado_Camiones INNER JOIN
                                                    S3A.dbo.Chofer ON Logistica_Estado_Camiones.IdChofer = S3A.dbo.Chofer.IdChofer INNER JOIN
                                                    S3A.dbo.Transportista ON S3A.dbo.Chofer.IdTransportista = S3A.dbo.Transportista.IdTransportista
                            WHERE Estado = 'A' AND Logistica_Estado_Camiones.Disponible = 'S' AND Logistica_Estado_Camiones.Libre = 'S'
                            ORDER BY Logistica_Estado_Camiones.Disponible DESC, Logistica_Estado_Camiones.Actualizado DESC """
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for row in consulta:
                            transporte = str(row[0])
                            nombre = str(row[1])
                            actualiza = str(row[2])
                            disponible = str(row[3])
                            hexa_disponible = str(row[4])
                            libre = str(row[5])
                            hexa_libre = str(row[6])
                            datos = {'Transporte':transporte, 'Nombre':nombre, 'Actualiza':actualiza, 'Disponible':disponible, 'HexaDisponible':hexa_disponible, 'Libre':libre, 'HexaLibre':hexa_libre}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Data': data})
                    else:
                        data = "No se encontraron Choferes Cargados."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("Logistica","Disponibles",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@login_required
@csrf_exempt
def listadoViajes(request):
    if request.method == 'GET':
        user_has_permission = request.user.has_perm('Logistica.puede_ver')
        if user_has_permission:  
            try:
                with connections['S3A'].cursor() as cursor:
                    sql = """ SELECT        'PEDIDO: ' + CONVERT(VARCHAR, PedidoFlete.IdPedidoFlete) AS ID_PEDIDO, CONVERT(VARCHAR(26), RTRIM(Transportista.RazonSocial)) AS TRANSPORTE, 
                                            RTRIM(PedidoFlete.Chofer) AS NOMBRE, RTRIM(Chacra.Nombre) AS CHACRA,
                                            CASE TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Acepta 
                                                WHEN 'S' THEN 'ACEPTADO - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.FechaHora, 108) + ' Hs.' 
                                            END AS ACEPTA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraRetiraBins IS NULL THEN 'Retiró Bins - -' 
                                                ELSE 'Retiró Bins - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraRetiraBins, 108) + ' Hs.' 
                                            END AS RETIRA_BINS,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraRetiraBins IS NULL THEN '#d5393ce8' 
                                                ELSE '#008f39e7' 
                                            END AS HEXA_RETIRA_BINS,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.LlegaChacra IS NULL THEN 'Llegada Chacra - -' 
                                                ELSE 'Llega Chacra - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraLlegaChacra, 108) + ' Hs.' 
                                            END AS LLEGA_CHACRA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.LlegaChacra IS NULL THEN '#d5393ce8' 
                                                ELSE '#008f39e7' 
                                            END AS HEXA_LLEGA_CHACRA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.SaleChacra IS NULL THEN 'Salida Chacra - -' 
                                                ELSE 'Salida Chacra - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraSaleChacra, 108) + ' Hs.' 
                                            END AS SALE_CHACRA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.SaleChacra IS NULL THEN '#d5393ce8' 
                                                ELSE '#008f39e7' 
                                            END AS HEXA_SALE_CHACRA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Bascula IS NULL THEN 'Llegada Báscula - -' 
                                                ELSE 'Llegada Báscula - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraBascula, 108) + ' Hs.' 
                                            END AS LLEGA_BASCULA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Bascula IS NULL THEN '#d5393ce8' 
                                                ELSE '#008f39e7' 
                                            END AS HEXA_LLEGA_BASCULA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraFinal IS NULL THEN ' - ' 
                                                ELSE 'FINALIZADO - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraFinal, 108) + ' Hs.' 
                                            END AS FINALIZA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraFinal IS NULL THEN '#d5393ce8' 
                                                ELSE '#008f39e7' 
                                            END AS HEXA_FINALIZA,
                                            PedidoFlete.IdPedidoFlete, CONVERT(VARCHAR(10), PedidoFlete.FechaAlta, 103) AS FECHA
                            FROM            PedidoFlete INNER JOIN
                                                    Transportista ON PedidoFlete.IdTransportista = Transportista.IdTransportista INNER JOIN
                                                    Chacra ON PedidoFlete.IdChacra = Chacra.IdChacra INNER JOIN
                                                    TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento ON PedidoFlete.IdPedidoFlete = TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.IdAsignacion
                            WHERE        (PedidoFlete.Estado = 'A')
                                        AND (CONVERT(DATE, TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.FechaHora) >= DATEADD(DAY, - 2, CONVERT(DATE, GETDATE())))
                                        AND TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Estado IN ('S') 
                            ORDER BY TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Actualizacion DESC """
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for row in consulta:
                            pedido = str(row[0]) + " - F: " + str(row[16])
                            transporte = str(row[1])
                            nombre = str(row[2])
                            chacra = str(row[3])
                            acepta = str(row[4])
                            retira_bins = str(row[5])
                            hexa_retira = str(row[6])
                            llega = str(row[7])
                            hexa_llega = str(row[8])
                            sale = str(row[9])
                            hexa_sale = str(row[10])
                            bascula = str(row[11])
                            hexa_bascula = str(row[12])
                            finaliza = str(row[13])
                            hexa_finaliza = str(row[14])
                            id_pedido = str(row[15])
                            datos = {'Pedido':pedido,'Transporte':transporte, 'Nombre':nombre, 'Chacra':chacra, 
                                     'Acepta':acepta,'Retira':retira_bins, 'HexaRetira':hexa_retira, 'Llega':llega, 
                                     'HexaLlega':hexa_llega,'Sale':sale, 'HexaSale':hexa_sale, 'Bascula':bascula,
                                     'HexaBascula':hexa_bascula,'Finaliza':finaliza,'HexaFinaliza':hexa_finaliza,
                                     'ID':id_pedido}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Data': data})
                    else:
                        data = "No se encontraron Viajes."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("Logistica","Disponibles",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['S3A'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required
@csrf_exempt
def listadoAsignados(request):
    if request.method == 'GET':
        user_has_permission = request.user.has_perm('Logistica.puede_ver')
        if user_has_permission:  
            try:
                with connections['S3A'].cursor() as cursor:
                    sql = """ SELECT        PedidoFlete.IdPedidoFlete AS ID, RTRIM(Transportista.RazonSocial) AS TRANSPORTE, RTRIM(PedidoFlete.Chofer) AS CHOFER, RTRIM(Camion.Nombre) AS CAMION, 
                                                COALESCE(RTRIM(Productor.RazonSocial),'-') AS PRODUCTOR, COALESCE(RTRIM(Chacra.Nombre),'-') AS CHACRA, COALESCE(RTRIM(Zona.Nombre),'-') AS ZONA, 
                                                        CASE WHEN PedidoFlete.CantVacios IS NULL THEN '' ELSE 'NOTIFICADO' END, CONVERT(VARCHAR(10), PedidoFlete.FechaAlta, 103) AS ALTA
                                FROM            Transportista LEFT JOIN
                                                        PedidoFlete ON Transportista.IdTransportista = PedidoFlete.IdTransportista LEFT JOIN
                                                        Camion ON Transportista.IdTransportista = Camion.IdTransportista AND PedidoFlete.IdCamion = Camion.IdCamion LEFT JOIN
                                                        Productor ON PedidoFlete.IdProductor = Productor.IdProductor LEFT JOIN
                                                        Chacra ON Productor.IdProductor = Chacra.IdProductor AND PedidoFlete.IdChacra = Chacra.IdChacra LEFT JOIN
                                                        Zona ON PedidoFlete.IdZona = Zona.IdZona
                                WHERE        (CONVERT(DATE, PedidoFlete.FechaAlta) >= DATEADD(DAY, - 8, CONVERT(DATE, GETDATE()))) 
                                            AND (PedidoFlete.Estado = 'A')
                                            AND PedidoFlete.IdPedidoFlete LIKE '10%'
                                            AND NOT EXISTS ( 
                                                        SELECT 1 FROM TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento 
                                                        WHERE IdAsignacion = PedidoFlete.IdPedidoFlete 
                                                        AND Estado IN ('S','F','C','R'))
                                ORDER BY PedidoFlete.FechaAlta """
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for row in consulta:
                            flete = "PEDIDO: " + str(row[0]) + " - " + str(row[8])
                            transporte = str(row[1])
                            nombre = str(row[2])
                            camion = str(row[3])
                            productor = str(row[4])
                            chacra = str(row[5])
                            zona = str(row[6])
                            noti = str(row[7])
                            datos = {'Flete':flete, 'Transporte':transporte, 'Nombre':nombre, 'Camion':camion, 
                                     'Productor':productor, 'Chacra':chacra, 'Zona':zona, 'ID':str(row[0]), 'Alta':noti}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Data': data})
                    else:
                        data = "No se encontraron Viajes Asignados."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("Logistica","Disponibles",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['S3A'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required
@csrf_exempt
def listadoRechazados(request):
    if request.method == 'GET':
        user_has_permission = request.user.has_perm('Logistica.puede_ver')
        if user_has_permission:  
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ SELECT        Logistica_Camiones_Seguimiento.IdAsignacion AS ID, Logistica_Camiones_Seguimiento.Chofer AS CHOFER, RTRIM(S3A.dbo.Productor.RazonSocial) AS PRODUCTOR, 
                                                RTRIM(S3A.dbo.Chacra.Nombre) AS  CHACRA
                                FROM            Logistica_Camiones_Seguimiento INNER JOIN
                                                        S3A.dbo.PedidoFlete ON Logistica_Camiones_Seguimiento.IdAsignacion = S3A.dbo.PedidoFlete.IdPedidoFlete INNER JOIN
                                                        S3A.dbo.Productor ON S3A.dbo.PedidoFlete.IdProductor = S3A.dbo.Productor.IdProductor INNER JOIN
                                                        S3A.dbo.Chacra ON S3A.dbo.PedidoFlete.IdChacra = S3A.dbo.Chacra.IdChacra
                                WHERE        (Logistica_Camiones_Seguimiento.Estado IN ('C', 'R'))
                                                AND Logistica_Camiones_Seguimiento.FechaHora >= DATEADD(DAY, -2, GETDATE()) 
                                ORDER BY Logistica_Camiones_Seguimiento.FechaHora """
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for row in consulta:
                            flete = str("Pedido Flete: " + str(row[0]))
                            nombre = str(row[1])
                            productor = str(row[2])
                            chacra = str(row[3])
                            id_pedido_flete = str(row[0])
                            datos = {'Flete':flete, 'Nombre':nombre, 'Productor':productor, 'Chacra':chacra,'ID':id_pedido_flete}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Data': data})
                    else:
                        data = "No se encontraron Viajes Rechazados."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("Logistica","listarRechazados",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required
@csrf_exempt
def asignaViajeActualizaVacios(request):
    if request.method == 'POST':
        try:            
            cantidad = request.POST.get('integerInput') or '0'
            ubicacion = request.POST.get('selectBox')
            idPedidoFlete = request.POST.get('idasignacion')

            values = [cantidad, ubicacion, idPedidoFlete]
            with connections['S3A'].cursor() as cursor:
                sql = "UPDATE PedidoFlete SET CantVacios = %s, UbicacionVacios = %s WHERE IdPedidoFlete = %s "
                cursor.execute(sql, values) 

                cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                affected_rows = cursor.fetchone()[0]

            if affected_rows > 0:
                ### ENVÍAR NOTIFICACIONES
                ### CHOFER
                ch = enviar_notificacion_chofer_solicita(obtener_id_firebase("CH",idPedidoFlete),"Nuevo viaje asignado: N°: " + str(idPedidoFlete),"VJ")
                ### SOLICITANTE
                sl = enviar_notificacion_chofer_solicita(obtener_id_firebase("EC",idPedidoFlete),"Su pedido N°: " + str(idPedidoFlete) + " fué asignado. Vea el estado de los Pedidos.","PF")
                ### ACA SE VA A ENVIAR EL VIAJE
                chofer = traeChofer(idPedidoFlete)
                if chofer != '0':
                    ejecutar_url(str(idPedidoFlete),str(chofer),'S')
                
                return JsonResponse({'Message': 'Success', 'Nota': 'Actualizado ' + str(ch) + ' - ' + str(sl)})
            else:
                return JsonResponse({'Message': 'Error', 'Nota': 'No se Actualizó'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","asignaViajesVacios","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def traeChofer(idAsignacion):
    try:  
        with connections['S3A'].cursor() as cursor:
            sql = """ SELECT RTRIM(Chofer) FROM PedidoFlete WHERE IdPedidoFlete = %s """
            cursor.execute(sql, [idAsignacion]) 
            results = cursor.fetchone()
            if results:
                chofer = str(results[0])
                return chofer
            else:
                return '0'

    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("SEGUIMIENTO","TRAE CHOFER","Aplicacion",error)
        return '0'

def ejecutar_url(Asignacion, Chofer, valor):
    import urllib.request
    import urllib.parse
    import urllib.request
    Asignacion_encoded = urllib.parse.quote(Asignacion)
    Chofer_encoded = urllib.parse.quote(Chofer)
    valor_encoded = urllib.parse.quote(valor)
    try:  
        url = f"http://192.168.1.110/api/fletes-remitos/data-acepta-rechaza/isAsignacion={Asignacion_encoded}&chofer={Chofer_encoded}&acepta={valor_encoded}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        if 'Message' in data:
            return True
        else:
            return False
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("SEGUIMIENTO","EJECUTA URL","Aplicacion",error)
        return False

def eliminaRechazado(request, idAsignacion):
    if request.method == 'GET':            
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ UPDATE Logistica_Camiones_Seguimiento SET Estado='E' WHERE IdAsignacion = %s """
                cursor.execute(sql, [idAsignacion]) 

                cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                affected_rows = cursor.fetchone()[0]

                sqlDelete = "DELETE Logistica_Campos_Temporales WHERE IdAsignacion = %s"
                cursor.execute(sqlDelete, [idAsignacion])   


            if affected_rows > 0:
                return JsonResponse({'Message': 'Success', 'Nota': 'Eliminado'})
            else:
                return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Eliminar'})
                
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","EliminaRechazados","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def obtener_id_firebase(Tipo,nAsignacion):
    try:
        with connections['S3A'].cursor() as cursor:
            if Tipo == 'EC':
                sql = """ SELECT ISNULL(US.IdAndroid,0) AS ID_FIREBASE
                            FROM PedidoFlete AS PF LEFT JOIN 
                                TRESASES_APLICATIVO.dbo.Usuarios AS US ON US.Usuario = PF.UserID COLLATE database_default
                            WHERE PF.IdPedidoFlete = %s """
            else:
                sql = """ SELECT TOP 1 US.IdAndroid AS ID_FIREBASE
                            FROM TRESASES_APLICATIVO.dbo.USUARIOS AS US
                            WHERE CodEmpleado IN (SELECT IdChofer
                                                    FROM Chofer
                                                    WHERE LTRIM(RTRIM(Apellidos)) + ' ' + LTRIM(RTRIM(Nombres)) = (SELECT PF.Chofer
                                                                                            FROM PedidoFlete AS PF
                                                                                            WHERE PF.IdPedidoFlete = %s)) """
            cursor.execute(sql, [nAsignacion]) 
            results = cursor.fetchone()
            if results:
                id_firebase = str(results[0])
                return id_firebase
            return '0'
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","OBTENER_ID_FIREBASE","Aplicacion",error)
        return '0'
    finally:
        cursor.close()
        connections['S3A'].close()












































































