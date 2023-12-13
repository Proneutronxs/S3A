from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime 

from django.db import connections
from django.http import JsonResponse


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
                    sql = """ SELECT        'PEDIDO FLETE: ' + CONVERT(VARCHAR, PedidoFlete.IdPedidoFlete) AS ID_PEDIDO, CONVERT(VARCHAR(26), RTRIM(Transportista.RazonSocial)) AS TRANSPORTE, 
                                            RTRIM(Chofer.Apellidos) + ' ' + RTRIM(Chofer.Nombres) AS NOMBRE, RTRIM(Chacra.Nombre) AS CHACRA,
                                            CASE TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Acepta 
                                                WHEN 'S' THEN 'ACEPTADO - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.FechaHora, 108) + ' Hs.' 
                                            END AS ACEPTA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.RetiraBins IS NULL THEN 'Retiró Bins - -' 
                                                ELSE 'Retiró Bins - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraLlegaChacra, 108) + ' Hs.' 
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
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Final IS NULL THEN ' - ' 
                                                ELSE 'FINALIZADO - ' + CONVERT(VARCHAR(5), TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.HoraFinal, 108) + ' Hs.' 
                                            END AS FINALIZA,
                                            CASE 
                                                WHEN TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Final IS NULL THEN '#d5393ce8' 
                                                ELSE '#008f39e7' 
                                            END AS HEXA_FINALIZA,
                                            PedidoFlete.IdPedidoFlete
                            FROM            PedidoFlete INNER JOIN
                                                    Transportista ON PedidoFlete.IdTransportista = Transportista.IdTransportista INNER JOIN
                                                    Chofer ON PedidoFlete.IdTransportista = Chofer.IdTransportista INNER JOIN
                                                    Chacra ON PedidoFlete.IdChacra = Chacra.IdChacra INNER JOIN
                                                    TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento ON PedidoFlete.IdPedidoFlete = TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.IdAsignacion
                            WHERE        (PedidoFlete.Estado = 'A') 
                                        --AND (TRY_CONVERT(DATE, PedidoFlete.FechaAlta) = '10/12/2023')--
                                        AND TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento.Estado = 'S' """
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for row in consulta:
                            pedido = str(row[0])
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
                    sql = """ SELECT        'PEDIDO FLETE: ' + CONVERT(VARCHAR, PedidoFlete.IdPedidoFlete) AS ID_PEDIDO, CONVERT(VARCHAR(26), RTRIM(Transportista.RazonSocial)) AS TRANSPORTE, RTRIM(Chofer.Apellidos) + ' ' + RTRIM(Chofer.Nombres) 
                                                    AS NOMBRE, RTRIM(Camion.Nombre) AS CAMION, RTRIM(Productor.RazonSocial) AS PRODUCTOR, RTRIM(Chacra.Nombre) AS CHACRA, RTRIM(Zona.Nombre) AS ZONA,PedidoFlete.IdPedidoFlete AS ID,PedidoFlete.FechaAlta
                            FROM            PedidoFlete INNER JOIN
                                                    Transportista ON PedidoFlete.IdTransportista = Transportista.IdTransportista INNER JOIN
                                                    Chofer ON PedidoFlete.IdTransportista = Chofer.IdTransportista INNER JOIN
                                                    Chacra ON PedidoFlete.IdChacra = Chacra.IdChacra INNER JOIN
                                                    Camion ON PedidoFlete.IdCamion = Camion.IdCamion INNER JOIN
                                                    Productor ON PedidoFlete.IdProductor = Productor.IdProductor INNER JOIN
                                                    Zona ON PedidoFlete.IdZona = Zona.IdZona
                            WHERE        (PedidoFlete.Estado = 'A') 
                                            AND (TRY_CONVERT(DATE, PedidoFlete.FechaAlta) >= DATEADD(DAY, -8, GETDATE()))
                                            AND (PedidoFlete.Estado = 'A')
                                            AND NOT EXISTS ( 
                                                    SELECT 1 FROM TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento 
                                                    WHERE IdAsignacion = PedidoFlete.IdPedidoFlete 
                                                    AND Estado IN ('S','F','C')) """
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for row in consulta:
                            flete = str(row[0])
                            transporte = str(row[1])
                            nombre = str(row[2])
                            camion = str(row[3])
                            productor = str(row[4])
                            chacra = str(row[5])
                            zona = str(row[6])
                            id_pedido_flete = str(row[7])
                            datos = {'Flete':flete, 'Transporte':transporte, 'Nombre':nombre, 'Camion':camion, 
                                     'Productor':productor, 'Chacra':chacra, 'Zona':zona, 'ID':id_pedido_flete}
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
                                                AND Logistica_Camiones_Seguimiento.FechaHora >= DATEADD(DAY, -8, GETDATE()) """
                    cursor.execute(sql)
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for row in consulta:
                            flete = str("Pedido Flete: " + row[0])
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



























































