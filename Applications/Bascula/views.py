from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import *
from Applications.Mobile.FletesRemitos.views import traeIdEspecies, traeIdMarcas
from django.views.static import serve
from Applications.ModelosPDF.remitoChacra import *
from Applications.Mobile.FletesRemitos.views import actualizaNombrePDF
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import os

# Create your views here.


@login_required
@permission_required('Bascula.puede_ingresar', raise_exception=True)
def Bascula(request):
    return render (request, 'Bascula/bascula.html')

@login_required
def remitos(request):
    return render (request, 'Bascula/Remitos/remitos.html')

@login_required
@csrf_exempt
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

                            SELECT        Datos_Remito_MovBins.NumeroRemito AS NUM_REMITO, CONVERT(VARCHAR(20),RTRIM(S3A.dbo.PedidoFlete.IdPedidoFlete)) AS CHACRA, 
                                        RTRIM(S3A.dbo.Camion.Patente) AS PATENTE, Datos_Remito_MovBins.IdProductor AS ID_PRODUCTOR,
                                        CASE Datos_Remito_MovBins.IdProductor WHEN '5200' THEN 'R-' WHEN '5000' THEN 'A-' ELSE 'T-' END
                            FROM            Datos_Remito_MovBins INNER JOIN
                                                    S3A.dbo.PedidoFlete ON Datos_Remito_MovBins.IdAsignacion = S3A.dbo.PedidoFlete.IdPedidoFlete INNER JOIN
                                                    S3A.dbo.Chacra ON S3A.dbo.PedidoFlete.IdChacra = S3A.dbo.Chacra.IdChacra INNER JOIN
                                                    S3A.dbo.Camion ON S3A.dbo.PedidoFlete.IdCamion = S3A.dbo.Camion.IdCamion
                            WHERE        (TRY_CONVERT(DATE, Datos_Remito_MovBins.FechaAlta, 103) >= TRY_CONVERT(DATE, @P_Desde, 103)) 
                                    AND (TRY_CONVERT(DATE, Datos_Remito_MovBins.FechaAlta, 103) <= TRY_CONVERT(DATE, @P_Hasta, 103))
                                    AND Datos_Remito_MovBins.Modificado IS NULL
                            ORDER BY S3A.dbo.PedidoFlete.IdPedidoFlete """
                    cursor.execute(sql, [desde,hasta])
                    consulta = cursor.fetchall()
                    if consulta:
                        data = []
                        for i in consulta:
                            numero_remito = str(i[0]) + "-" + str(i[3])
                            id_productor = str(i[3])
                            detalle = str(i[4]) + str(i[1]) + " - " + str(i[0]) + " - " + str(i[2])
                            datos = {'ID':numero_remito,'Detalle':detalle, 'Productor':id_productor}
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
            values = str(request.POST.get('ComboxTraeRemitosChacras')).split('-')
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ SELECT        FORMAT(Datos_Remito_MovBins.NumeroRemito, '00000000') AS NRO_REMITO, RTRIM(S3A.dbo.Productor.RazonSocial) AS RAZON_SOCIAL, RTRIM(S3A.dbo.Productor.Nombre) AS NOMBRE, 
                                                        RTRIM(S3A.dbo.Productor.Direccion) AS DIRECCION, Datos_Remito_MovBins.Renspa AS RENSPA, Datos_Remito_MovBins.UP, Datos_Remito_MovBins.Cantidad AS CANT_TOTAL, Datos_Remito_MovBins.IdAsignacion AS ID, 
                                                        RTRIM(S3A.dbo.PedidoFlete.Solicitante) AS CAPATAZ, RTRIM(S3A.dbo.Especie.Nombre) AS ESPECIE, RTRIM(S3A.dbo.Variedad.Nombre) AS VARIEDAD, RTRIM(S3A.dbo.Chacra.Nombre) AS CHACRA, RTRIM(S3A.dbo.PedidoFlete.Chofer) AS CHOFER, RTRIM(S3A.dbo.Camion.Nombre) AS CAMION, 
                                                        RTRIM(S3A.dbo.Camion.Patente) AS PATENTE, CONVERT(VARCHAR(10), Datos_Remito_MovBins.FechaAlta, 103) AS FECHA, CONVERT(VARCHAR(5), Datos_Remito_MovBins.FechaAlta, 108), Datos_Remito_MovBins.NumeroRemito, 
                                                        CASE WHEN Datos_Remito_MovBins.Observaciones IS NULL THEN '' ELSE Datos_Remito_MovBins.Observaciones END, S3A.dbo.Productor.IdProductor, Datos_Remito_MovBins.NombrePdf, Datos_Remito_MovBins.IdEspecie
                                FROM            S3A.dbo.Camion INNER JOIN
                                                        S3A.dbo.Chacra INNER JOIN
                                                        S3A.dbo.Variedad INNER JOIN
                                                        S3A.dbo.Especie INNER JOIN
                                                        S3A.dbo.Productor INNER JOIN
                                                        Datos_Remito_MovBins INNER JOIN
                                                        S3A.dbo.PedidoFlete ON Datos_Remito_MovBins.IdAsignacion = S3A.dbo.PedidoFlete.IdPedidoFlete ON S3A.dbo.Productor.IdProductor = S3A.dbo.PedidoFlete.IdProductor ON 
                                                        S3A.dbo.Especie.IdEspecie = Datos_Remito_MovBins.IdEspecie ON S3A.dbo.Variedad.IdVariedad = Datos_Remito_MovBins.IdVariedad ON S3A.dbo.Chacra.IdChacra = S3A.dbo.PedidoFlete.IdChacra ON 
                                                        S3A.dbo.Camion.IdCamion = S3A.dbo.PedidoFlete.IdCamion
                                WHERE        (Datos_Remito_MovBins.NumeroRemito = %s) AND (Datos_Remito_MovBins.IdProductor = %s) """
                    cursor.execute(sql, values)
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
                            observaciones = str(i[18])
                            IdProductor = str(i[19])
                            pdf = str(i[20])
                            idEspecie = str(i[21])
                            datos = {'Remito':numero_remito,'Productor':productor, 'Señor':señor, 'Direccion':direccion, 'Renspa':renspa, 'UP':up, 'Total':total, 
                                     'Capataz':capataz, 'Especie':especie, 'Variedad':variedad, 'Chacra':chacra, 'Chofer':chofer, 'Camion':camion, 'Patente':patente,
                                     'Fecha':fecha, 'Hora':hora, 'IdRemito':idRemito, 'Obs':observaciones, 'IdProductor':IdProductor, 'PDF':pdf, 'IdEspecie': idEspecie}
                            data.append(datos)

                        sqldetalle = """ SELECT        Contenido_Remito_MovBins.Cantidad AS CANTIDAD, RTRIM(S3A.dbo.Bins.Nombre) AS BIN, RTRIM(S3A.dbo.Marca.Nombre) AS MARCA				
                                FROM            S3A.dbo.Bins INNER JOIN
                                                        S3A.dbo.Marca INNER JOIN
                                                        Contenido_Remito_MovBins ON S3A.dbo.Marca.IdMarca = Contenido_Remito_MovBins.IdMarca ON S3A.dbo.Bins.IdBins = Contenido_Remito_MovBins.IdBins
                                WHERE        (Contenido_Remito_MovBins.NumeroRemito = %s) AND (Contenido_Remito_MovBins.IdProductor = %s) AND (Contenido_Remito_MovBins.Modificado IS NULL) """
                        cursor.execute(sqldetalle, values)
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
def verificaCreaNuevoRemito(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_crear_remito')
        if user_has_permission:
            return JsonResponse({'Message': 'Success'})
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@login_required
@csrf_exempt   
def donwloadPdf(request):
    if request.method == 'POST':
        remito = request.POST.get('numRemito')
        productor = request.POST.get('idProductor')
        nombre = creaDescarga(remito,productor)
        filename = 'Applications/ReportesPDF/RemitosChacra/' + nombre
        if os.path.exists(filename):
            response = serve(request, os.path.basename(filename), os.path.dirname(filename))
            response['Content-Disposition'] = f'attachment; filename="{nombre}"'
            return response
        else:
            raise Http404
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

def creaDescarga(remito,productor):
    values = [remito, productor]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            numero_remito,Nomproductor,señor,direccion,renspa,up,total,capataz,especie,variedad,chacra,chofer,camion,patente,fecha,hora = traeEncabezado(remito,productor)
            if productor == '5000':
                numero_chacra= "00018"
                pdf = Remito_Abadon_Movimiento_Chacras(fecha, hora, numero_chacra, 
                            numero_remito, Nomproductor, señor, direccion, 
                            chacra, especie, variedad, renspa, up, chofer, camion, patente, 
                            total, capataz)
                pdf.alias_nb_pages()
                pdf.add_page()
                index = 0
                sqldetalle = """ SELECT        Contenido_Remito_MovBins.Cantidad AS CANTIDAD, RTRIM(S3A.dbo.Bins.Nombre) AS BIN, RTRIM(S3A.dbo.Marca.Nombre) AS MARCA				
                        FROM            S3A.dbo.Bins INNER JOIN
                                                S3A.dbo.Marca INNER JOIN
                                                Contenido_Remito_MovBins ON S3A.dbo.Marca.IdMarca = Contenido_Remito_MovBins.IdMarca ON S3A.dbo.Bins.IdBins = Contenido_Remito_MovBins.IdBins
                        WHERE        (Contenido_Remito_MovBins.NumeroRemito = %s) AND (Contenido_Remito_MovBins.IdProductor = %s) AND (Contenido_Remito_MovBins.Modificado IS NULL) """
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
                    fecha = str(fecha).replace('/', '')
                    name = 'R_00018_' + str(numero_remito) + '_' + fecha + '.pdf'
                    nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name
                    #actualizaNombrePDF(name,numero_remito)
                    pdf.output(nameDireccion, 'F')
                    return name
            elif productor == '5200':
                numero_chacra= "00001"
                pdf = Remito_Romik_Movimiento_Chacras(fecha, hora, numero_chacra, 
                            numero_remito, Nomproductor, señor, direccion, 
                            chacra, especie, variedad, renspa, up, chofer, camion, patente, 
                            total, capataz)
                pdf.alias_nb_pages()
                pdf.add_page()
                index = 0
                sqldetalle = """ SELECT        Contenido_Remito_MovBins.Cantidad AS CANTIDAD, RTRIM(S3A.dbo.Bins.Nombre) AS BIN, RTRIM(S3A.dbo.Marca.Nombre) AS MARCA				
                        FROM            S3A.dbo.Bins INNER JOIN
                                                S3A.dbo.Marca INNER JOIN
                                                Contenido_Remito_MovBins ON S3A.dbo.Marca.IdMarca = Contenido_Remito_MovBins.IdMarca ON S3A.dbo.Bins.IdBins = Contenido_Remito_MovBins.IdBins
                        WHERE        (Contenido_Remito_MovBins.NumeroRemito = %s) AND (Contenido_Remito_MovBins.IdProductor = %s) AND (Contenido_Remito_MovBins.Modificado IS NULL) """
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
                    fecha = str(fecha).replace('/', '')
                    name = 'R_00001_' + str(numero_remito) + '_' + fecha + '.pdf'
                    nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name
                    #actualizaNombrePDF(name,numero_remito)
                    pdf.output(nameDireccion, 'F')
                    return name
            else:
                numero_chacra= "00017"
                pdf = Remito_Movimiento_Chacras(fecha, hora, numero_chacra, 
                            numero_remito, Nomproductor, señor, direccion, 
                            chacra, especie, variedad, renspa, up, chofer, camion, patente, 
                            total, capataz)
                pdf.alias_nb_pages()
                pdf.add_page()
                index = 0
                sqldetalle = """ SELECT        Contenido_Remito_MovBins.Cantidad AS CANTIDAD, RTRIM(S3A.dbo.Bins.Nombre) AS BIN, RTRIM(S3A.dbo.Marca.Nombre) AS MARCA				
                        FROM            S3A.dbo.Bins INNER JOIN
                                                S3A.dbo.Marca INNER JOIN
                                                Contenido_Remito_MovBins ON S3A.dbo.Marca.IdMarca = Contenido_Remito_MovBins.IdMarca ON S3A.dbo.Bins.IdBins = Contenido_Remito_MovBins.IdBins
                        WHERE        (Contenido_Remito_MovBins.NumeroRemito = %s) AND (Contenido_Remito_MovBins.IdProductor = %s) AND (Contenido_Remito_MovBins.Modificado IS NULL) """
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
                    fecha = str(fecha).replace('/', '')
                    name = 'R_00017_' + str(numero_remito) + '_' + fecha + '.pdf'
                    nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name
                    #actualizaNombrePDF(name,numero_remito)
                    pdf.output(nameDireccion, 'F')
                    return name
    except Exception as e:
        insertar_registro_error_sql("BÁSCULA","CREA DESCARGA","FUNCION",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

def traeEncabezado(remito,productor):
    values = [remito, productor]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                        SELECT        FORMAT(Datos_Remito_MovBins.NumeroRemito, '00000000') AS NRO_REMITO, RTRIM(S3A.dbo.Productor.RazonSocial) AS RAZON_SOCIAL, RTRIM(S3A.dbo.Productor.Nombre) AS NOMBRE, 
                                                RTRIM(S3A.dbo.Productor.Direccion) AS DIRECCION, Datos_Remito_MovBins.Renspa AS RENSPA, Datos_Remito_MovBins.UP, Datos_Remito_MovBins.Cantidad AS CANT_TOTAL, Datos_Remito_MovBins.IdAsignacion AS ID, 
                                                RTRIM(S3A.dbo.PedidoFlete.Solicitante) AS CAPATAZ, RTRIM(S3A.dbo.Especie.Nombre) AS ESPECIE, RTRIM(S3A.dbo.Variedad.Nombre) AS VARIEDAD, RTRIM(S3A.dbo.Chacra.Nombre) AS CHACRA, RTRIM(S3A.dbo.PedidoFlete.Chofer) AS CHOFER, RTRIM(S3A.dbo.Camion.Nombre) AS CAMION, 
                                                RTRIM(S3A.dbo.Camion.Patente) AS PATENTE, CONVERT(VARCHAR(10), Datos_Remito_MovBins.FechaAlta, 103) AS FECHA, CONVERT(VARCHAR(5), Datos_Remito_MovBins.FechaAlta, 108) + ' Hs.' AS HORA, Datos_Remito_MovBins.NumeroRemito, 
                                                CASE WHEN Datos_Remito_MovBins.Observaciones IS NULL THEN '' ELSE Datos_Remito_MovBins.Observaciones END AS OBS, S3A.dbo.Productor.IdProductor, Datos_Remito_MovBins.NombrePdf
                        FROM            S3A.dbo.Camion INNER JOIN
                                                S3A.dbo.Chacra INNER JOIN
                                                S3A.dbo.Variedad INNER JOIN
                                                S3A.dbo.Especie INNER JOIN
                                                S3A.dbo.Productor INNER JOIN
                                                Datos_Remito_MovBins INNER JOIN
                                                S3A.dbo.PedidoFlete ON Datos_Remito_MovBins.IdAsignacion = S3A.dbo.PedidoFlete.IdPedidoFlete ON S3A.dbo.Productor.IdProductor = S3A.dbo.PedidoFlete.IdProductor ON 
                                                S3A.dbo.Especie.IdEspecie = Datos_Remito_MovBins.IdEspecie ON S3A.dbo.Variedad.IdVariedad = Datos_Remito_MovBins.IdVariedad ON S3A.dbo.Chacra.IdChacra = S3A.dbo.PedidoFlete.IdChacra ON 
                                                S3A.dbo.Camion.IdCamion = S3A.dbo.PedidoFlete.IdCamion
                        WHERE        (Datos_Remito_MovBins.NumeroRemito = %s) AND (Datos_Remito_MovBins.IdProductor = %s)
                    """
            cursor.execute(sql, values)
            result = cursor.fetchall()
            if result:
                for i in result:
                    numero_remito = str(i[0])
                    Nomproductor = str(i[1])
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
                    hora = str(i[16])
                    idRemito = str(i[17])
                    observaciones = str(i[18])
                    IdProductor = str(i[19])
            return numero_remito,Nomproductor,señor,direccion,renspa,up,total,capataz,especie,variedad,chacra,chofer,camion,patente,fecha,hora
            
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("BASCULA","TRAE ENCABEZADO","Consulta",error)

@login_required
@csrf_exempt
def actualizaObsRemito(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_ver')
        if user_has_permission:
            num_remito = request.POST.get('numRemito')
            observacion = request.POST.get('observacionesRemito')
            idProductor = request.POST.get('idProductor')
            values =  [observacion,num_remito,idProductor]
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ UPDATE Datos_Remito_MovBins SET Observaciones = %s WHERE NumeroRemito = %s AND IdProductor = %s """
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
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    

##################### CARGA SPINNERS ##############################
    
def llamaEspecieMarca(request):
    if request.method == 'GET':
        user_has_permission = request.user.has_perm('Bascula.puede_ver')
        if user_has_permission:
            try:
                with connections['S3A'].cursor() as cursor:
                    listado = traeIdEspecies()
                    cantValues = ','.join(['%s'] * len(listado))
                    sql3 = f"SELECT IdEspecie, RTRIM(Nombre) FROM Especie WHERE IdEspecie IN ({cantValues}) ORDER BY IdEspecie"
                    cursor.execute(sql3, listado)
                    consulta3 = cursor.fetchall()
                    if consulta3:
                        listado_especie = []
                        for row3 in consulta3:
                            idEspecie = str(row3[0])
                            nombre = str(row3[1])
                            datos = {'IdEspecie': idEspecie, 'NombreEspecie': nombre}
                            listado_especie.append(datos)

                    listado = traeIdMarcas()
                    cantValues = ','.join(['%s'] * len(listado))
                    listado_marca = []
                    sql = f"SELECT IdMarca, RTRIM(Nombre) FROM Marca WHERE IdMarca IN ({cantValues})"
                    cursor.execute(sql,listado)
                    consulta = cursor.fetchall()
                    if consulta:
                        for row in consulta:
                            idMarca = str(row[0])
                            nombreMarca = str(row[1])
                            datos = {'idMarca': idMarca, 'NombreMarca': nombreMarca}
                            listado_marca.append(datos)
                    
                    if listado_especie and listado_marca:
                        return JsonResponse({'Message': 'Success', 'DataEspecie':listado_especie, 'DataMarca':listado_marca})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se Encontraron Datos.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("BASCULA","DatosInicialesFletes","Aplicacion",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                cursor.close()
                connections['S3A'].close()
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def traeTipoEnvase(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_ver')
        if user_has_permission:
            values = str(request.POST.get('ComboxMarcaBinsModifica'))
            try:
                with connections['S3A'].cursor() as cursor:
                    sql = " SELECT IdBins, RTRIM(Nombre) FROM Bins WHERE IdMarca = %s "
                    cursor.execute(sql,[values])
                    consulta = cursor.fetchall()
                    if consulta:
                        listado_envase = []
                        for row in consulta:
                            idBins = str(row[0])
                            nombreBins = str(row[1])
                            datos = {'idBins': idBins, 'NombreBins': nombreBins}
                            listado_envase.append(datos)
                            
                    if listado_envase:
                        return JsonResponse({'Message': 'Success', 'DataEnvase':listado_envase})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se Encontraron Datos.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("FletesRemitos","traeTipoBins","Aplicacion",error)
            finally:
                cursor.close()
                connections['S3A'].close()
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def actualizaDatos(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_modificar')
        if user_has_permission:
            num_remito = request.POST.get('numRemitoModifica').strip("'")
            num_productor = request.POST.get('idProductorModifica').strip("'")

            cantidades = request.POST.getlist('cantidades[]')
            envases = request.POST.getlist('envases[]')
            marcas = request.POST.getlist('marcas[]')

            Cantidad_Total = sum(int(numero) for numero in cantidades)
            items = len(cantidades)
            index = 0
            if eliminaBins(str(request.user),num_productor,num_remito):
                for cant, envase, marca in zip(cantidades, envases, marcas):
                    if insertaBins(num_productor,num_remito,cant.strip("'"),marca.strip("'"),envase.strip("'")):
                        index = index + 1

                if items == index:
                    if actualizaCantidad(str(request.user),Cantidad_Total,num_productor,num_remito):
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Remito se actualizó correctamente.'})
                else:
                    return JsonResponse ({'Message': 'Error', 'Nota': 'No se pudo guardar los cambios.'})
            else:
                return JsonResponse ({'Message': 'Error', 'Nota': 'No se pudo guardar los cambios.'})

            
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


def eliminaBins(user,num_productor,num_remito):
    values = [user,num_productor,num_remito]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                UPDATE Contenido_Remito_MovBins SET Modificado = 'S',FechaModificado = GETDATE(), UserModificado = %s WHERE IdProductor = %s AND NumeroRemito = %s """
            cursor.execute(sql, values)
            
            cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
            affected_rows = cursor.fetchone()[0]

        if affected_rows > 0:
            return True
        else:
            return False
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("BASCULA","ELIMINA BINS","Consulta",error)
        return False

def insertaBins(num_productor,num_remito,cantidad,marca,bins):
    values = [num_productor,num_remito,cantidad,marca,bins]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ INSERT INTO Contenido_Remito_MovBins (IdProductor,NumeroRemito,Cantidad,IdMarca,IdBins) VALUES (%s,%s,%s,%s,%s) """
            cursor.execute(sql, values)
            return True
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("BASCULA","INSERTA BINS","Consulta",error)

        return False

def actualizaCantidad(user,cantidad,num_productor,num_remito):
    values = [user,cantidad,num_productor,num_remito]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    UPDATE Datos_Remito_MovBins SET FechaModificado = GETDATE(), UserModificado = %s, Cantidad= %s WHERE IdProductor = %s AND NumeroRemito = %s
                    """
            cursor.execute(sql, values)
            
            cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
            affected_rows = cursor.fetchone()[0]

        if affected_rows > 0:
            return True
        else:
            return True
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("BASCULA","ELIMINA BINS","Consulta",error)
        return False
    

@login_required
@csrf_exempt
def actualizaUP(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_modificar')
        if user_has_permission:
            nueva_up = str(request.POST.get('nueva_up'))
            usuario = str(request.user)
            id_productor = request.POST.get('idProductor')
            id_remito = request.POST.get('numRemito')
            values = [nueva_up.upper(),usuario.upper(),id_productor,id_remito]
            try:    
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                        UPDATE Datos_Remito_MovBins SET UP = %s ,FechaModificado = GETDATE(), UserModificado = %s WHERE IdProductor = %s AND NumeroRemito = %s """
                    cursor.execute(sql, values)
                    
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'La UP se actualizó correctamente.'})
                else:
                    return JsonResponse ({'Message': 'Error', 'Nota': 'La UP no se pudo actualizar.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("BASCULA","ACTUALIZA UP","Consulta",error)
                print(e)
                return JsonResponse ({'Message': 'Error', 'Nota': 'Se produjo un error al intentar procesar la solicitud.'})   
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})       
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@login_required
@csrf_exempt
def eliminaRemito(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_borrar')
        if user_has_permission:
            usuario = str(request.user)
            id_productor = request.POST.get('idProductor')
            id_remito = request.POST.get('numRemito')
            values = [usuario.upper(),id_productor,id_remito]
            try:    
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                        UPDATE Datos_Remito_MovBins SET Modificado = 'E' ,FechaModificado = GETDATE(), UserModificado = %s WHERE IdProductor = %s AND NumeroRemito = %s """
                    cursor.execute(sql, values)
                    
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'El Remito se eliminó correctamente.'})
                else:
                    return JsonResponse ({'Message': 'Error', 'Nota': 'El Remito no se pudo eliminar.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("BASCULA","ELIMINA EL REMITO","Consulta",error)
                print(e)
                return JsonResponse ({'Message': 'Error', 'Nota': 'Se produjo un error al intentar procesar la solicitud.'})   
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})       
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    
@login_required
@csrf_exempt
def llama_variedades(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_ver')
        if user_has_permission:
            idEspecie = request.POST.get('idEspecie')
            try:
                with connections['S3A'].cursor() as cursor:
                    ## VARIEDAD
                    sql = """
                            SELECT  IdVariedad, (CONVERT(VARCHAR(3),IdVariedad) + ' - ' + RTRIM(Nombre)) AS Especie 
                            FROM Variedad 
                            WHERE IdEspecie = %s
                                    AND IdVariedad < 1000 
                                    AND IdVariedad NOT IN (940,957,927,951,906,948,934,937,950,908,122,73,84,97,931,935,83,963,86,933,85,936,932)
                            ORDER BY Nombre
                            """
                    cursor.execute(sql, [idEspecie])
                    consulta = cursor.fetchall()
                    if consulta:
                        listado_variedad = []
                        for row in consulta:
                            idVariedad = str(row[0])
                            nombreVariedad = str(row[1])
                            datos = {'idVariedad': idVariedad, 'NombreVariedad': nombreVariedad}
                            listado_variedad.append(datos)
                            
                        return JsonResponse({'Message': 'Success', 'Datos': listado_variedad})
                    else:
                        return JsonResponse({'Message': 'Not Found', 'Nota': 'No se pudieron obtener los datos.'})
            except Exception as e:
                error = str(e)
                print(error)
                insertar_registro_error_sql("FletesRemitos","DatosInicialesFletes","Aplicacion",error)
                return JsonResponse({'Message': 'Error', 'Nota': error})   
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})       
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@login_required
@csrf_exempt
def actualizaVariedad(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Bascula.puede_modificar')
        if user_has_permission:
            usuario = str(request.user)
            idVariedad = str(request.POST.get('ComboxVariedadModifica'))
            id_productor = request.POST.get('idProductor')
            id_remito = request.POST.get('numRemito')
            values = [idVariedad,usuario.upper(),id_productor,id_remito]
            try:    
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                        UPDATE Datos_Remito_MovBins SET IdVariedad = %s ,FechaModificado = GETDATE(), UserModificado = %s WHERE IdProductor = %s AND NumeroRemito = %s """
                    cursor.execute(sql, values)
                    
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'La Variedad se actualizó correctamente.'})
                else:
                    return JsonResponse ({'Message': 'Error', 'Nota': 'La Variedad no se pudo actualizar.'})
            except Exception as e:
                error = str(e)
                insertar_registro_error_sql("BASCULA","ACTUALIZA UP","Consulta",error)
                return JsonResponse ({'Message': 'Error', 'Nota': 'Se produjo un error al intentar procesar la solicitud.'})   
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})       
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})


























