from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import *
from django.db import connections
from django.http import JsonResponse

# Create your views here.


@login_required
@permission_required('Bascula.puede_ingresar', raise_exception=True)
def Bascula(request):
    return render (request, 'Bascula/bascula.html')


def remitos(request):
    return render (request, 'Bascula/Remitos/remitos.html')

def verRemitosChacras(request):
    return render (request, 'Bascula/Remitos/verRemitosChacras.html')

@login_required
@csrf_exempt
def listadoRemitos(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_ver')
        if user_has_permission:
            desde = request.POST.get('desde') or ''
            hasta = request.POST.get('hasta') or ''
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ DECLARE @P_Desde DATE;
                            DECLARE @P_Hasta DATE;
                            SET @P_Desde = %s;
                            SET @P_Hasta = %s;
                            SET @P_Desde = CASE WHEN @P_Desde = '' THEN GETDATE() ELSE TRY_CONVERT(DATE, @P_Desde, 103) END;
                            SET @P_Hasta = CASE WHEN @P_Hasta = '' THEN GETDATE() ELSE TRY_CONVERT(DATE, @P_Hasta, 103) END;

                            SELECT        Datos_Remito_MovBins.NumeroRemito AS NUM_REMITO, CONVERT(VARCHAR(20),RTRIM(S3A.dbo.Chacra.Nombre)) AS CHACRA, 
                                        RTRIM(S3A.dbo.Camion.Patente) AS PATENTE
                            FROM            Datos_Remito_MovBins INNER JOIN
                                                    S3A.dbo.PedidoFlete ON Datos_Remito_MovBins.IdAsignacion = S3A.dbo.PedidoFlete.IdPedidoFlete INNER JOIN
                                                    S3A.dbo.Chacra ON S3A.dbo.PedidoFlete.IdChacra = S3A.dbo.Chacra.IdChacra INNER JOIN
                                                    S3A.dbo.Camion ON S3A.dbo.PedidoFlete.IdCamion = S3A.dbo.Camion.IdCamion
                            WHERE        (TRY_CONVERT(DATE, Datos_Remito_MovBins.FechaAlta, 103) >= TRY_CONVERT(DATE, @P_Desde, 103)) 
                                    AND (TRY_CONVERT(DATE, Datos_Remito_MovBins.FechaAlta, 103) <= TRY_CONVERT(DATE, @P_Hasta, 103)) """
                    cursor.execute(sql, [desde,hasta])
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for i in consulta:
                            numero_remito = str(i[0])
                            detalle = str(i[1]) + " - " +str(i[2])
                            datos = {'ID':numero_remito,'Detalle':detalle}
                            data.append(datos)
                        return JsonResponse({'Message': 'Success', 'Datos': data})
                    else:
                        data = "No se encontraron datos."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                insertar_registro_error_sql("Bascula","listadoRemitos",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@login_required
@csrf_exempt
def buscaRemito(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_ver')
        if user_has_permission:
            num_remito = request.POST.get('ComboxTraeRemitosChacras')
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ SELECT        FORMAT(Datos_Remito_MovBins.NumeroRemito, '00000000') AS NRO_REMITO, RTRIM(S3A.dbo.Productor.RazonSocial) AS RAZON_SOCIAL, RTRIM(S3A.dbo.Productor.Nombre) AS NOMBRE, 
                                                        RTRIM(S3A.dbo.Productor.Direccion) AS DIRECCION, Datos_Remito_MovBins.Renspa AS RENSPA, Datos_Remito_MovBins.UP, Datos_Remito_MovBins.Cantidad AS CANT_TOTAL, Datos_Remito_MovBins.IdAsignacion AS ID, 
                                                        RTRIM(S3A.dbo.PedidoFlete.Solicitante) AS CAPATAZ, RTRIM(S3A.dbo.Especie.Nombre) AS ESPECIE, RTRIM(S3A.dbo.Variedad.Nombre) AS VARIEDAD, RTRIM(S3A.dbo.Chacra.Nombre) AS CHACRA, RTRIM(S3A.dbo.PedidoFlete.Chofer) AS CHOFER, RTRIM(S3A.dbo.Camion.Nombre) AS CAMION, 
                                                        RTRIM(S3A.dbo.Camion.Patente) AS PATENTE, CONVERT(VARCHAR(10), Datos_Remito_MovBins.FechaAlta, 103) AS FECHA, CONVERT(VARCHAR(5), Datos_Remito_MovBins.FechaAlta, 108), Datos_Remito_MovBins.NumeroRemito, 
                                                        CASE WHEN Datos_Remito_MovBins.Observaciones IS NULL THEN '' ELSE Datos_Remito_MovBins.Observaciones END
                                FROM            S3A.dbo.Camion INNER JOIN
                                                        S3A.dbo.Chacra INNER JOIN
                                                        S3A.dbo.Variedad INNER JOIN
                                                        S3A.dbo.Especie INNER JOIN
                                                        S3A.dbo.Productor INNER JOIN
                                                        Datos_Remito_MovBins INNER JOIN
                                                        S3A.dbo.PedidoFlete ON Datos_Remito_MovBins.IdAsignacion = S3A.dbo.PedidoFlete.IdPedidoFlete ON S3A.dbo.Productor.IdProductor = S3A.dbo.PedidoFlete.IdProductor ON 
                                                        S3A.dbo.Especie.IdEspecie = Datos_Remito_MovBins.IdEspecie ON S3A.dbo.Variedad.IdVariedad = Datos_Remito_MovBins.IdVariedad ON S3A.dbo.Chacra.IdChacra = S3A.dbo.PedidoFlete.IdChacra ON 
                                                        S3A.dbo.Camion.IdCamion = S3A.dbo.PedidoFlete.IdCamion
                                WHERE        (Datos_Remito_MovBins.NumeroRemito = %s) """
                    cursor.execute(sql, [num_remito])
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        dataDetalle = []
                        for i in consulta:
                            numero_remito = str(i[0])
                            productor = str(i[1])
                            señor = str(i[2])
                            direccion = str(i[3])
                            renspa = str(i[4])
                            up = str(i[5])
                            total = str(i[6])
                            capataz = str(i[8])
                            especie = str(i[9])
                            variedad =str(i[10])
                            chacra = str(i[11])
                            chofer = str(i[12])
                            camion = str(i[13])
                            patente = str(i[14])
                            fecha = str(i[15])
                            hora = str(i[16]) + " Hs."
                            idRemito = str(i[17])
                            observaciones= str(i[18])
                            datos = {'Remito':numero_remito,'Productor':productor, 'Señor':señor, 'Direccion':direccion, 'Renspa':renspa, 'UP':up, 'Total':total, 
                                     'Capataz':capataz, 'Especie':especie, 'Variedad':variedad, 'Chacra':chacra, 'Chofer':chofer, 'Camion':camion, 'Patente':patente,
                                     'Fecha':fecha, 'Hora':hora, 'IdRemito':idRemito, 'Obs':observaciones}
                            data.append(datos)

                        sqldetalle = """ SELECT        Contenido_Remito_MovBins.Cantidad AS CANTIDAD, RTRIM(S3A.dbo.Bins.Nombre) AS BIN, RTRIM(S3A.dbo.Marca.Nombre) AS MARCA				
                                FROM            S3A.dbo.Bins INNER JOIN
                                                        S3A.dbo.Marca INNER JOIN
                                                        Contenido_Remito_MovBins ON S3A.dbo.Marca.IdMarca = Contenido_Remito_MovBins.IdMarca ON S3A.dbo.Bins.IdBins = Contenido_Remito_MovBins.IdBins
                                WHERE        (Contenido_Remito_MovBins.NumeroRemito = %s) """
                        cursor.execute(sqldetalle, [num_remito])
                        consultaDetalle = cursor.fetchall()
                        if consultaDetalle:
                            for row in consultaDetalle:
                                cantidad = str(row[0])
                                tamaño = str(row[1])
                                marca = str(row[2])
                                datos = {'Cantidad':cantidad, 'Tamaño':tamaño, 'Marca':marca}
                                dataDetalle.append(datos)
                    else:
                        data = "No se encontraron datos."
                        return JsonResponse({'Message': 'Error', 'Nota': data})
                        
                    return JsonResponse({'Message': 'Success', 'Datos': data, 'Detalle':dataDetalle})
                
            except Exception as e:
                insertar_registro_error_sql("Bascula","buscaRemito",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@login_required
@csrf_exempt   
def verificaModificaRemito(request):
    if request.method == 'GET':
        user_has_permission = request.user.has_perm('Bascula.puede_modificar')
        if user_has_permission:
            return JsonResponse({'Message': 'Success'})
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@login_required
@csrf_exempt
def actualizaObsRemito(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_ver')
        if user_has_permission:
            num_remito = request.POST.get('numRemito')
            observacion = request.POST.get('observacionesRemito')
            values =  [observacion,num_remito]
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ UPDATE Datos_Remito_MovBins SET Observaciones = %s, Modificado = 'P' WHERE NumeroRemito = %s """
                    cursor.execute(sql, values)
                   
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'Actualizado.'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Actualizar.'})
            except Exception as e:
                insertar_registro_error_sql("BASCULA","ACTUALIZA OBSERVACIONES",request.user,str(e))
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
            finally:
                cursor.close()
                connections['TRESASES_APLICATIVO'].close()
        return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})