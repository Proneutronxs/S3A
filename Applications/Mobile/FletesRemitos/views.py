from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.http import HttpResponse, Http404
from django.views.static import serve
from django.http import JsonResponse
from S3A.funcionesGenerales import *
from Applications.ModelosPDF.remitoChacra import Remito_Movimiento_Chacras
import barcode
import json
import os

# Create your views here.


def datos_Iniciales_Flete(request):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:

                listado_planta_destino = []
                listado_productor = []
                listado_especie = []

                ## PLANTA DESTINO 
                sql = "SELECT IdUbicacion, RTRIM(Descripcion) FROM Ubicacion ORDER BY Descripcion"
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    listado_planta_destino = []
                    for row in consulta:
                        idUbicacion = str(row[0])
                        descripcion = str(row[1])
                        datos = {'IdUbicacion': idUbicacion, 'Descripcion': descripcion}
                        listado_planta_destino.append(datos)

                ## PRODUCTOR
                sql2 = "SELECT IdProductor, RTRIM(RazonSocial) FROM Productor WHERE Activo = 'S' ORDER BY RazonSocial"
                cursor.execute(sql2)
                consulta2 = cursor.fetchall()
                if consulta2:
                    listado_productor = []
                    for row2 in consulta2:
                        idProductor = str(row2[0])
                        razonSocial = str(row2[1])
                        datos2 = {'IdProductor': idProductor, 'RazonSocial': razonSocial}
                        listado_productor.append(datos2)

                ## ESPECIE
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

                if listado_planta_destino and listado_productor and listado_especie:
                    return JsonResponse({'Message': 'Success', 'DataPlanta': listado_planta_destino, 'DataProductor': listado_productor, 'DataEspecie': listado_especie})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se pudieron obtener los datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","DatosInicialesFletes","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    

def idProductor_Chacra(request,idProductor):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                listado_Chacra = []
                ## CHACRA
                sql = "SELECT IdChacra, RTRIM(Nombre) FROM Chacra WHERE IdProductor = %s ORDER BY Nombre"
                cursor.execute(sql, [idProductor])
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idChacra = str(row[0])
                        nombreChacra = str(row[1])
                        datos = {'idChacra': idChacra, 'NombreChacra': nombreChacra}
                        listado_Chacra.append(datos)

                    return JsonResponse({'Message': 'Success', 'DataChacra': listado_Chacra})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se pudieron obtener los datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","DatosInicialesFletes","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def idProductor_Zona(request,idProductor,idChacra):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:                
                listado_Zona = []
                ## ZONA
                sql2 = "SELECT Z.IdZona, RTRIM(Z.Nombre) FROM Zona as Z Left Join Chacra as C on (Z.IdZona = C.Zona) WHERE C.IdProductor = %s AND C.IdChacra = %s "
                cursor.execute(sql2, [idProductor, idChacra])
                consulta2 = cursor.fetchall()
                if consulta2:
                    for row2 in consulta2:
                        idZona = str(row2[0])
                        nombreZona = str(row2[1])
                        datos2 = {'IdZona': idZona, 'NombreZona': nombreZona}
                        listado_Zona.append(datos2)                
                    return JsonResponse({'Message': 'Success', 'DataZona': listado_Zona})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se pudieron obtener los datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","DatosInicialesFletes","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


def idEspecie_Varierad(request,idEspecie):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                ## VARIEDAD
                sql = "SELECT  IdVariedad, (CONVERT(VARCHAR(3),IdVariedad) + ' - ' + RTRIM(Nombre)) AS Especie FROM Variedad WHERE IdEspecie = %s and IdVariedad < 1000 ORDER BY Nombre"
                cursor.execute(sql, [idEspecie])
                consulta = cursor.fetchall()
                if consulta:
                    listado_variedad = []
                    for row in consulta:
                        idVariedad = str(row[0])
                        nombreVariedad = str(row[1])
                        datos = {'idVariedad': idVariedad, 'NombreVariedad': nombreVariedad}
                        listado_variedad.append(datos)
                        
                    return JsonResponse({'Message': 'Success', 'DataVariedad': listado_variedad})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se pudieron obtener los datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","DatosInicialesFletes","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def traeIdEspecies():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Texto FROM Parametros_Aplicativo WHERE Codigo = 'APP-ESP-FLETES'"
            cursor.execute(sql)
            consulta = cursor.fetchone()
            if consulta:
                datos = str(consulta[0])
                listado_id = datos.split(',')
                return listado_id
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","traeIdEspecies","Aplicacion",error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

### INSERTA POST DE UNA ASIGNACIÓN
@csrf_exempt
def insertaPedidoFlete(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            solicita = str(json.loads(body)['solicita'])
            idPlanta = "100"
            usuario = str(json.loads(body)['usuario'])
            fechaPedido = obtenerFechaActualUSA()
            horaPedido = obtenerHoraActual()
            tipoDestino  = "P"
            tipoCarga = str(json.loads(body)['tipoCarga'])
            idProductor = str(json.loads(body)['idProductor'])
            idChacra = str(json.loads(body)['idChacra'])
            idZona = str(json.loads(body)['idZona'])
            idPlantaDestino = None
            idEspecie = str(json.loads(body)['idEspecie'])
            idVariedad = str(json.loads(body)['idVariedad'])
            binsTotal = str(json.loads(body)['binsTotal'])
            traeVacios = str(json.loads(body)['traeVacios'])
            traeCuellos = str(json.loads(body)['traeCuellos'])
            horaRequerida = str(json.loads(body)['horaRequerida'])
            observaciones = str(json.loads(body)['observaciones'])
            estado = "P"
            fechaRequerida = str(json.loads(body)['fechaRequerida'])
            binsRojos = str(json.loads(body)['binsRojos'])


            insertar_registro_error_sql("FletesRemitos","HORA REQUERIA","Aplicacion",horaRequerida)

            if tipoCarga == 'RAU':
                values = [idPlanta, solicita, horaPedido, tipoDestino, tipoCarga, idProductor, idChacra, idZona, 
                        idEspecie, idVariedad, binsTotal, traeVacios, traeCuellos, horaRequerida, observaciones, estado, 
                        usuario, binsRojos]
                with connections['S3A'].cursor() as cursor:
                    sql = """
                            INSERT INTO PedidoFlete (
                                IdPedidoFlete, IdPlanta, Solicitante, FechaPedido, HoraPedido, TipoDestino, TipoCarga,
                                IdProductor, IdChacra, IdZona, IdEspecie, IdVariedad, Bins, Vacios, Cuellos,
                                HoraRequerida, Obs, Estado, FechaRequerida, UserID, FechaAlta, CantBinsRojos
                            )
                            VALUES (
                                (SELECT MAX(IdPedidoFlete) + 1 FROM PedidoFlete WHERE IdPedidoFlete LIKE '10%%'),
                                %s, %s, GETDATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, GETDATE(), %s, GETDATE(), %s
                            )
                            """
                    cursor.execute(sql, values)

                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'El pedido se realizó correctamente.'})
                else:
                    return JsonResponse({'Message': 'Success', 'Nota': 'El pedido no se pudo realizar.'})                       
            else:
                values = [idPlanta, solicita, horaPedido, tipoDestino, tipoCarga, idProductor, idChacra, idZona, 
                         binsTotal, traeVacios, traeCuellos, horaRequerida, observaciones, estado, usuario]
                with connections['S3A'].cursor() as cursor:
                    sql = """
                            INSERT INTO PedidoFlete (
                                IdPedidoFlete, IdPlanta, Solicitante, FechaPedido, HoraPedido, TipoDestino, TipoCarga,
                                IdProductor, IdChacra, IdZona, Bins, Vacios, Cuellos,
                                HoraRequerida, Obs, Estado, FechaRequerida, UserID, FechaAlta
                            )
                            VALUES (
                                (SELECT MAX(IdPedidoFlete) + 1 FROM PedidoFlete WHERE IdPedidoFlete LIKE '10%%'),
                                %s, %s, GETDATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, GETDATE(), %s, GETDATE()
                            )
                            """
                    cursor.execute(sql, values)

                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'El pedido se realizó correctamente.'})
                else:
                    return JsonResponse({'Message': 'Success', 'Nota': 'El pedido no se pudo realizar.'})
            
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","insertaPedidoFlete","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})    




#### CREACION DE REMITOS DATOS A MOSTRAR ASIGNACIONES Y BINS 

def llamaAsignacionesPendientes(request, usuario):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """ SELECT         IdPedidoFlete AS ID, CONVERT(VARCHAR, PedidoFlete.IdPedidoFlete) + ' - ' +  RTRIM(Productor.RazonSocial) AS ASIGNACION 
                            FROM            PedidoFlete INNER JOIN 
                                            Productor ON PedidoFlete.IdProductor = Productor.IdProductor
                            WHERE        (PedidoFlete.UserID = %s) 
                                            AND (PedidoFlete.Estado = 'A')
                                            AND ((SELECT LlegaChacra FROM TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento WHERE IdAsignacion = IdPedidoFlete AND Estado = 'S' ) IS NOT NULL)
                                            AND ((SELECT DISTINCT AsigCerrada FROM TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins WHERE IdAsignacion = IdPedidoFlete) IS NULL)
                            ORDER BY IdPedidoFlete """
                cursor.execute(sql, [usuario])
                consulta = cursor.fetchall()
                if consulta:
                    listado_Asignaciones = []
                    for row in consulta:
                        idFlete = str(row[0])
                        descripcionFlete = str(row[1])
                        datos = {'idFlete': idFlete, 'DescripcionFlete': descripcionFlete}
                        listado_Asignaciones.append(datos)

                    return JsonResponse({'Message': 'Success', 'Asignaciones': listado_Asignaciones})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron Asignaciones pendientes.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","llamaAsisgnacionesPendientes","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'}) 

### LLAMA A LOS DATOS DE LA ASIGNACION SELECCIONADA CON EL ID
def llamaDataAsignacionPendiente(request, idAsignacion):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                sql = "SELECT        RTRIM(P.RazonSocial) AS Productor, RTRIM(C.Nombre) AS Chacra, RTRIM(Z.Nombre) AS Zona, CONVERT(VARCHAR(30), T.RazonSocial) AS Transporte, " \
                                        "RTRIM(PF.Chofer), RTRIM(CA.Nombre) AS Camion, RTRIM(CA.Patente), RTRIM(C.RENSPA) AS Renspa " \
                        "FROM            PedidoFlete AS PF LEFT OUTER JOIN " \
                                                "Productor AS P ON PF.IdProductor = P.IdProductor LEFT OUTER JOIN " \
                                                "Chacra AS C ON PF.IdChacra = C.IdChacra LEFT OUTER JOIN " \
                                                "Zona AS Z ON PF.IdZona = Z.IdZona LEFT OUTER JOIN " \
                                                "Ubicacion AS U ON PF.IdPlantaDestino = U.IdUbicacion LEFT OUTER JOIN " \
                                                "Especie AS E ON PF.IdEspecie = E.IdEspecie LEFT OUTER JOIN " \
                                                "Variedad AS V ON PF.IdVariedad = V.IdVariedad LEFT OUTER JOIN " \
                                                "Transportista AS T ON PF.IdTransportista = T.IdTransportista LEFT OUTER JOIN " \
                                                "Camion AS CA ON PF.IdCamion = CA.IdCamion LEFT OUTER JOIN " \
                                                "Acoplado AS A ON PF.IdAcoplado = A.IdAcoplado " \
                        "WHERE        (PF.IdPedidoFlete = %s)"
                cursor.execute(sql, [idAsignacion])
                consulta = cursor.fetchall()
                if consulta:
                    listadoData_Asignaciones = []
                    for row in consulta:
                        productor = str(row[0])
                        chacra = str(row[1])
                        zona = str(row[2])
                        transporte = str(row[3])
                        chofer = str(row[4])
                        camion = str(row[5])
                        patente = str(row[6])
                        renspa = str(row[7])
                        datos = {'Productor': productor, 'Chacra': chacra, 'Zona': zona, 'Transporte': transporte, 'Chofer': chofer, 'Camion':camion, 'Patente': patente, 'Renspa': renspa}
                        listadoData_Asignaciones.append(datos)
                
                listadoData_UP = traeUPS(renspa)
                listadoData_Marca = traeMarcaBins()

                listado_idMarcas = traeIdMarcas()

                listados = {item: [] for item in listado_idMarcas}

                for item in listados.items():
                    dato = traeTipoBins(item[0])
                    listados[item[0]] = dato

                listadoData_TipoBins = []

                for item, dato in listados.items():
                    listadoData_TipoBins.append({item: dato})
                    

                if listadoData_Asignaciones and listadoData_UP and listadoData_Marca and listadoData_TipoBins:
                    return JsonResponse({'Message': 'Success', 'DataAsignaciones': listadoData_Asignaciones, 'DataUp': listadoData_UP, 'DataMarcas': listadoData_Marca, 'DataTipo': listadoData_TipoBins})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron Datos para la Asignacion seleccionada.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","llamaDataAsignacionPendiente","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

### LLAMA A LAS UP DE LA RENSPA  DE LA ASIGNACION SELECCIONADA
def traeUPS(renspa):
    listadoUP_Renspa = []
    try:
        with connections['S3A'].cursor() as cursor:
            sql = "SELECT DISTINCT RTRIM(UP) FROM ReporteDanio WHERE RENSPA = %s AND (YEAR(Fecha) = YEAR(GETDATE()))"
            cursor.execute(sql, [renspa])
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    up = str(row[0])
                    datos = {'up': up}
                    listadoUP_Renspa.append(datos)
                return listadoUP_Renspa
            else:
                return listadoUP_Renspa
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("traeFletesRemitos","traeUPS","Aplicacion",error)
        return listadoUP_Renspa
    finally:
        cursor.close()
        connections['S3A'].close()

def traeMarcaBins():
    try:
        with connections['S3A'].cursor() as cursor:
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
                    
                return listado_marca
            else: 
                return listado_marca
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","TraeMarcaBins","Aplicacion",error)
    finally:
        cursor.close()
        connections['S3A'].close()

def traeTipoBins(idMarca):
    try:
        with connections['S3A'].cursor() as cursor:
            listado_tipo = []
            sql = "SELECT IdBins, RTRIM(Nombre) FROM Bins WHERE IdMarca = %s"
            cursor.execute(sql,[idMarca])
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    idBins = str(row[0])
                    nombreBins = str(row[1])
                    datos = {'idBins': idBins, 'NombreBins': nombreBins}
                    listado_tipo.append(datos)
                    
                return listado_tipo
            else: 
                return listado_tipo
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","traeTipoBins","Aplicacion",error)
    finally:
        cursor.close()
        connections['S3A'].close()
    
def traeIdMarcas():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Texto FROM Parametros_Aplicativo WHERE Codigo = 'APP-BINS-REMITO'"
            cursor.execute(sql)
            consulta = cursor.fetchone()
            if consulta:
                datos = str(consulta[0])
                listado_id = datos.split(',')
                return listado_id
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","traeIdMarca","Aplicacion",error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

@csrf_exempt
def insertCreaciónRemitos(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            fechaActual = obtenerFechaActual()
            horaActual = obtenerHoraActual()
            numero_chacra= "00017"
            Usuario = str(json.loads(body)['usuario'])
            capataz = str(json.loads(body)['nombre'])
            IdAsignación = str(json.loads(body)['idAsignacion'])
            Renspa = str(json.loads(body)['renspa'])
            UP = str(json.loads(body)['up'])
            IdEspecie = str(json.loads(body)['idEspecie'])
            IdVariedad = str(json.loads(body)['idVariedad'])
            total_bins = str(json.loads(body)['totalBins'])
            listadoBins = json.loads(body)['DataBins']

            #### primero inserta el remito para generar el número

            numero_remito = insertaDatosRemito(IdAsignación, Renspa, UP, IdEspecie, IdVariedad, total_bins, Usuario)

            ### busca datos de la Asignacion

            productor, lote, zona, transporte, chofer, camion, patente, domicilio = datosRemito(IdAsignación)
            
            especie, variedad = traeEspecieVariedad(IdEspecie,IdVariedad)

            pdf = Remito_Movimiento_Chacras(fechaActual, horaActual, numero_chacra, 
                                    numero_remito, productor, productor, domicilio, 
                                    lote, especie, variedad, Renspa, UP, chofer, camion, patente, 
                                    total_bins, capataz, Usuario,)
            pdf.alias_nb_pages()
            pdf.add_page()

            index = 0
            for item in listadoBins:
                if index == 9:
                    pdf.alias_nb_pages()
                    pdf.add_page()
                    index = 0
                IdMarca = item['idMarca']
                IdTamaño = item['idTamaño']
                Cantidad = item['cantidad']   
                marca, bins = traeMarcaBinsConID(IdMarca, IdTamaño)
                ##INSERTA DATA BINS
                insertaBinsRemito(numero_remito,Cantidad, IdMarca, IdTamaño)
                pdf.set_font('Arial', '', 8)
                pdf.cell(w=24, h=5, txt= str(Cantidad), border='LBR', align='C', fill=0)
                pdf.cell(w=86, h=5, txt= str(bins), border='BR', align='C', fill=0)
                pdf.multi_cell(w=0, h=5, txt= str(marca), border='BR', align='C', fill=0)
                index = index + 1
                
            fecha = str(fechaActual).replace('/', '')

            name = 'R_' + str(numero_remito) + '_' + fecha + '.pdf'
            nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name

            actualizaNombrePDF(name,numero_remito)

            pdf.output(nameDireccion, 'F')

            nota = "El Remito se creó correctamente."
            return JsonResponse({'Message': 'Success', 'Nota': nota})                  
        except Exception as e:
            error = f"ERROR: {type(e).__name__} - {str(e)}"
            insertar_registro_error_sql("FletesRemitos","insertCreacionRemitos","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})      
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})  

def datosRemito(idAsignacion):
    try:    
        with connections['S3A'].cursor() as cursor:
            sql = "SELECT        RTRIM(P.RazonSocial) AS Productor, RTRIM(C.Nombre) AS Chacra, RTRIM(Z.Nombre) AS Zona, CONVERT(VARCHAR(30), T.RazonSocial) AS Transporte, " \
                                    "RTRIM(PF.Chofer), RTRIM(CA.Nombre) AS Camion, RTRIM(CA.Patente), RTRIM(C.RENSPA) AS Renspa, P.Direccion " \
                    "FROM            PedidoFlete AS PF LEFT OUTER JOIN " \
                                            "Productor AS P ON PF.IdProductor = P.IdProductor LEFT OUTER JOIN " \
                                            "Chacra AS C ON PF.IdChacra = C.IdChacra LEFT OUTER JOIN " \
                                            "Zona AS Z ON PF.IdZona = Z.IdZona LEFT OUTER JOIN " \
                                            "Ubicacion AS U ON PF.IdPlantaDestino = U.IdUbicacion LEFT OUTER JOIN " \
                                            "Especie AS E ON PF.IdEspecie = E.IdEspecie LEFT OUTER JOIN " \
                                            "Variedad AS V ON PF.IdVariedad = V.IdVariedad LEFT OUTER JOIN " \
                                            "Transportista AS T ON PF.IdTransportista = T.IdTransportista LEFT OUTER JOIN " \
                                            "Camion AS CA ON PF.IdCamion = CA.IdCamion LEFT OUTER JOIN " \
                                            "Acoplado AS A ON PF.IdAcoplado = A.IdAcoplado " \
                    "WHERE        (PF.IdPedidoFlete = %s)"
            cursor.execute(sql, [idAsignacion])
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    productor = str(row[0])
                    chacra = str(row[1])
                    zona = str(row[2])
                    transporte = str(row[3])
                    chofer = str(row[4])
                    camion = str(row[5])
                    patente = str(row[6])
                    domicilio = str(row[8])
            return productor, chacra, zona, transporte, chofer, camion, patente, domicilio
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","DatosRemito","Consulta",error)
    finally:
        cursor.close()
        connections['S3A'].close()

def traeEspecieVariedad(IdEspecie,IdVariedad):
    try:    
        with connections['S3A'].cursor() as cursor:
            sql = "SELECT RTRIM(Nombre) AS Especie, (SELECT RTRIM(Nombre) FROM Variedad WHERE IdVariedad = %s) AS VAriedad " \
                    "FROM Especie " \
                    "WHERE IdEspecie = %s"
            cursor.execute(sql, [IdVariedad, IdEspecie])
            consulta = cursor.fetchone()
            if consulta:
                especie = str(consulta[0])
                variedad = str(consulta[1])
            return especie, variedad
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","traeEspecieVariedad","Consulta",error)
    finally:
        cursor.close()
        connections['S3A'].close()

def traeMarcaBinsConID(IdMarca,IdBins):
    try:    
        with connections['S3A'].cursor() as cursor:
            sql = "SELECT RTRIM(Nombre) AS Marca, (SELECT RTRIM(Nombre) FROM Bins WHERE IdBins = %s) AS Bins " \
                    "FROM Marca " \
                    "WHERE IdMarca = %s"
            cursor.execute(sql, [IdBins, IdMarca])
            consulta = cursor.fetchone()
            if consulta:
                marca = str(consulta[0])
                bins = str(consulta[1])
            return marca, bins
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","traeEspecieVariedad","Consulta",error)
    finally:
        cursor.close()
        connections['S3A'].close()

def insertaDatosRemito(IdAsignación, Renspa, UP, IdEspecie, IdVariedad, total_bins, Usuario):
    values = [IdAsignación, Renspa, UP, IdEspecie, IdVariedad, total_bins, Usuario]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Datos_Remito_MovBins (NumeroRemito, IdAsignacion, Renspa, UP, IdEspecie, IdVariedad, Cantidad, FechaAlta, Usuario) " \
			        "VALUES ((SELECT (MAX(NumeroRemito) + 1) AS NumeroSiguiente FROM Datos_Remito_MovBins), %s, %s, %s, %s, %s, %s, getdate(), %s)"
            cursor.execute(sql, values)
            
            sql2 = "SELECT FORMAT(NumeroRemito, '00000000') FROM Datos_Remito_MovBins WHERE IdAsignacion = %s AND NombrePdf IS NULL"
            cursor.execute(sql2, [IdAsignación])
            consulta = cursor.fetchone()
            if consulta:
                numero_remito = str(consulta[0])
            return numero_remito
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","InsertaDatosRemito","Consulta",error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

def insertaBinsRemito(numeroRemito, cantidad, idMarca, idBins):
    values = [numeroRemito, cantidad, idMarca, idBins]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Contenido_Remito_MovBins (NumeroRemito, Cantidad, IdMarca, IdBins) " \
			        "VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, values)
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","InsertaBinsRemito","Consulta",error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

def actualizaNombrePDF(nombrePdf, numero_remito):
    values = [nombrePdf, numero_remito]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE Datos_Remito_MovBins SET NombrePdf = %s WHERE FORMAT(NumeroRemito, '00000000') = %s"
            cursor.execute(sql, values)
            
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","actualizaNombrePDF","Consulta",error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

def descarga_pdf_remito_chacra(request, filename):
    nombre = filename
    filename = 'Applications/ReportesPDF/RemitosChacra/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    else:
        raise Http404

def ver_pdf_remito_chacra(request, filename):
    nombre = filename
    filename = 'Applications/ReportesPDF/RemitosChacra/' + filename
    if os.path.exists(filename):
        with open(filename, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{nombre}"'
            return response
    else:
        raise Http404

def mostrarListadoRemitos(request, chofer):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """ SELECT        RTRIM(Productor.RazonSocial) AS PRODUCTOR, RTRIM(Chacra.Nombre) AS CHACRA, RTRIM(Especie.Nombre) AS ESPECIE, RTRIM(Variedad.Nombre) AS VARIEDAD, TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins.Cantidad AS CANTIDAD, 
                                        TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins.NombrePdf AS PDF 
                            FROM            TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins INNER JOIN 
                                            PedidoFlete INNER JOIN 
                                            Productor ON PedidoFlete.IdProductor = Productor.IdProductor INNER JOIN 
                                            Chacra ON PedidoFlete.IdChacra = Chacra.IdChacra ON TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins.IdAsignacion = PedidoFlete.IdPedidoFlete INNER JOIN 
                                            Especie ON TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins.IdEspecie = Especie.IdEspecie INNER JOIN
                                            Variedad ON TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins.IdVariedad = Variedad.IdVariedad 
                            WHERE RTRIM(PedidoFlete.Chofer) = %s
                                AND TRY_CONVERT(DATE, TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins.FechaAlta) = TRY_CONVERT(DATE, GETDATE()) 
                                AND PedidoFlete.Estado = 'A'
                                AND (SELECT Final FROM TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento WHERE IdAsignacion = PedidoFlete.IdPedidoFlete) IS NULL """
                cursor.execute(sql, [chofer])
                consulta = cursor.fetchall()
                if consulta:
                    listado_Remitos = []
                    for row in consulta:
                        productor = str(row[0])
                        chacra = str(row[1])
                        especie = str(row[2])
                        variedad = str(row[3])
                        cantidad = str(row[4])
                        pdf = str(row[5])
                        datos = {'Productor': productor, 'Chacra': chacra, 'Especie': especie, 'Variedad': variedad, 'Cantidad': cantidad, 'PDF': pdf}
                        listado_Remitos.append(datos)

                    return JsonResponse({'Message': 'Success', 'Nota': '', 'Remitos': listado_Remitos})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron Remitos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","mostrarListadoRemitos","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def listadoViajesAsignados(request, chofer):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """ SELECT        PedidoFlete.IdPedidoFlete AS ID, RTRIM(PedidoFlete.Solicitante) AS SOLICITA, CONVERT(VARCHAR(10), PedidoFlete.FechaPedido, 103) AS FECHA, 
                                        RTRIM(Chacra.Nombre) AS CHACRA, RTRIM(Zona.Nombre) AS ZONA, CASE PedidoFlete.Vacios WHEN 'S' THEN 'SI' WHEN 'N' THEN 'NO' ELSE '-' END AS VACIOS, 
                                        CASE PedidoFlete.Cuellos WHEN 'S' THEN 'SI' WHEN 'N' THEN 'NO' ELSE '-' END AS CUELLOS  
                            FROM            PedidoFlete INNER JOIN 
                                            Chacra ON PedidoFlete.IdChacra = Chacra.IdChacra INNER JOIN 
                                            Zona ON PedidoFlete.IdZona = Zona.IdZona 
                            WHERE        (PedidoFlete.Chofer = %s) 
                                                    AND (PedidoFlete.Estado = 'A')
                                                    AND (PedidoFlete.UbicacionVacios IS NOT NULL)
                                                    AND NOT EXISTS ( 
                                                    SELECT 1 FROM TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento 
                                                    WHERE IdAsignacion = PedidoFlete.IdPedidoFlete 
                                                        AND Estado IN ('S','F','R')) """
                cursor.execute(sql, [chofer])
                consulta = cursor.fetchall()
                if consulta:
                    listado_Viajes = []
                    for row in consulta:
                        idAsignacion = str(row[0])
                        solicita = str(row[1])
                        fecha = str(row[2])
                        chacra = str(row[3])
                        zona = str(row[4])
                        vacios = str(row[5])
                        cuellos = str(row[6])
                        datos = {'IdAsignacion': idAsignacion, 'Solicita': solicita, 'Fecha': fecha, 'Chacra': chacra, 'Zona': zona, 'Vacios': vacios, 'Cuellos': cuellos}
                        listado_Viajes.append(datos)

                    return JsonResponse({'Message': 'Success', 'Viajes': listado_Viajes})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron Viajes Asignados.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","listadoViajesAsignados","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def viajesAceptaRechaza(request, idAsignacion, chofer, acepta):
    if request.method == 'GET':            
        try:
            if soloAceptaSiNoExiste(idAsignacion,chofer):
                if acepta == 'S':
                    with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                        sql = "INSERT INTO Logistica_Camiones_Seguimiento (Orden, IdAsignacion, Chofer, FechaHora, Acepta, Estado) VALUES ( CASE " \
                                "WHEN EXISTS ( " \
                                    "SELECT Orden " \
                                    "FROM Logistica_Camiones_Seguimiento " \
                                    "WHERE TRY_CONVERT(DATE, FechaHora) = TRY_CONVERT(DATE, GETDATE()) AND Chofer = %s " \
                                ") " \
                                "THEN (SELECT MAX(Orden) + 1 FROM Logistica_Camiones_Seguimiento WHERE TRY_CONVERT(DATE, FechaHora) = TRY_CONVERT(DATE, GETDATE()) AND Chofer = %s) " \
                                "ELSE 1 " \
                            "END , %s, %s, GETDATE(), %s, %s) "
                        cursor.execute(sql, [chofer,chofer, idAsignacion, chofer, acepta, acepta]) 

                        sqlUpdate = "UPDATE Logistica_Estado_Camiones SET Libre = 'N', Actualizado= GETDATE() WHERE NombreChofer = %s "                  
                        cursor.execute(sqlUpdate, [chofer])

                        sqlInsert = "INSERT INTO Logistica_Campos_Temporales (IdAsignacion, Punto) VALUES (%s, '0')"                  
                        cursor.execute(sqlInsert, [idAsignacion])

                        cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                        affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'Aceptado'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Rechazar'})

                else:
                    with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                        sql = "INSERT INTO Logistica_Camiones_Seguimiento (Orden, IdAsignacion, Chofer, FechaHora, Acepta, Estado) VALUES ( CASE " \
                                "WHEN EXISTS ( " \
                                    "SELECT Orden " \
                                    "FROM Logistica_Camiones_Seguimiento " \
                                    "WHERE TRY_CONVERT(DATE, FechaHora) = TRY_CONVERT(DATE, GETDATE()) AND Chofer = %s " \
                                ") " \
                                "THEN (SELECT MAX(Orden) + 1 FROM Logistica_Camiones_Seguimiento WHERE TRY_CONVERT(DATE, FechaHora) = TRY_CONVERT(DATE, GETDATE()) AND Chofer = %s) " \
                                "ELSE 1 " \
                            "END , %s, %s, GETDATE(), %s, %s) "
                        cursor.execute(sql, [chofer,chofer, idAsignacion, chofer, acepta, "R"])

                        cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                        affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'Rechazado'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Rechazar'})
                
            else:
                return JsonResponse({'Message': 'Success', 'Nota': 'Ya fue Aceptado o Rechazado'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","viajesAceptaRechaza","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def soloAceptaSiNoExiste(idAsignacion, chofer):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT IdAsignacion FROM Logistica_Camiones_Seguimiento WHERE IdAsignacion = %s AND Chofer = %s AND Estado = 'S'"
            cursor.execute(sql, [idAsignacion,chofer])
            consulta = cursor.fetchone()
            if consulta:
                return False
            else:
                return True
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","soloAceptaSiNoExiste","consulta",error)
        return False
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()
    
@csrf_exempt
def actualizaEstadoPosicion(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            IdAsignacion = str(json.loads(body)['idAsignacion'])
            Columna = str(json.loads(body)['columna'])
            Chofer = str(json.loads(body)['chofer'])
            Valor = str(json.loads(body)['valor'])
            
            if Columna == 'RetiraBins':
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = f"UPDATE Logistica_Camiones_Seguimiento SET {Columna} = %s, HoraRetiraBins = GETDATE(), Actualizacion = GETDATE() WHERE IdAsignacion = %s AND Estado = 'S' AND HoraRetiraBins IS NULL "
                    cursor.execute(sql, [Valor, IdAsignacion])               

                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'Retiró Bins'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'Ya se confirmó el retiro.'})
                
            if Columna == 'Final':
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = f"UPDATE Logistica_Camiones_Seguimiento SET {Columna} = %s, HoraFinal = GETDATE(), Estado = 'F', Actualizacion = GETDATE() WHERE IdAsignacion = %s AND Estado = 'S' "
                    cursor.execute(sql, [Valor, IdAsignacion])           

                    sqlUpdate = "UPDATE Logistica_Estado_Camiones SET Libre = 'S', Actualizado = GETDATE() WHERE NombreChofer = %s " 
                    cursor.execute(sqlUpdate, [Chofer])     

                    sqlDelete = "DELETE Logistica_Campos_Temporales WHERE IdAsignacion = %s"
                    cursor.execute(sqlDelete, [IdAsignacion])

                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'F'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Finalizar'})
                
            if Columna == 'Cancelar':
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = f"UPDATE Logistica_Camiones_Seguimiento SET Estado = 'C', Actualizacion = GETDATE() WHERE IdAsignacion = %s AND Estado = 'S' "
                    cursor.execute(sql, [IdAsignacion])     

                    sqlDelete = "DELETE Logistica_Campos_Temporales WHERE IdAsignacion = %s"
                    cursor.execute(sqlDelete, [IdAsignacion])           

                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'Cancelado'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Finalizar'})
                
            if Columna == 'Columna':
                if traeNumColumna(IdAsignacion) < 3:

                    Row = ["LlegaChacra", "SaleChacra", "Bascula"]
                    Hora = ["HoraLlegaChacra", "HoraSaleChacra", "HoraBascula"]

                    with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                        sql = f"UPDATE Logistica_Camiones_Seguimiento SET {Row[traeNumColumna(IdAsignacion)]} = %s, {Hora[traeNumColumna(IdAsignacion)]} = GETDATE(), Actualizacion = GETDATE() WHERE IdAsignacion = %s AND Estado = 'S' "
                        cursor.execute(sql, [Valor, IdAsignacion])                

                        cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                        affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        actualizaNumColumna(IdAsignacion)
                        return JsonResponse({'Message': 'Success', 'Nota': 'Punto Actualizado'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Actualizar'})
                else:
                    with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                        cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                        affected_rows = cursor.fetchone()[0]
                        
                    return JsonResponse({'Message': 'Error', 'Nota': 'Se Actualizaron todos los Puntos'})
            
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","actualizaEstadoPosicion","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def traeNumColumna(idAsignacion):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Punto FROM Logistica_Campos_Temporales WHERE IdAsignacion = %s "
            cursor.execute(sql, [idAsignacion])
            consulta = cursor.fetchone()
            if consulta:
                punto = int(consulta[0])
                return punto
            else:
                return 0
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","traeNumColumna","consulta",error)
        return 0

def actualizaNumColumna(idAsignacion):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE Logistica_Campos_Temporales SET Punto = (Punto + 1) WHERE IdAsignacion = %s "
            cursor.execute(sql, [idAsignacion])
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","actualizaNumColumna","consulta",error)
    
@csrf_exempt
def actualizaEstadoChofer(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            chofer = str(json.loads(body)['chofer'])
            Columna = str(json.loads(body)['columna'])
            Valor = str(json.loads(body)['valor'])
            
            if Columna == 'Disponible' and Valor == 'N':
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = "UPDATE Logistica_Estado_Camiones SET Disponible = 'N', Libre = 'N', Actualizado = GETDATE() WHERE NombreChofer = %s "
                    cursor.execute(sql, [chofer]) 

                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'Actualizado'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se Actualizó'})
            else:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = f"UPDATE Logistica_Estado_Camiones SET {Columna} = %s, Actualizado = GETDATE() WHERE NombreChofer = %s "
                    cursor.execute(sql, [Valor,chofer])   

                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'Actualizado'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se Actualizó'})
            
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","actualizaEstadoChofer","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def datosViajesAceptados(request, chofer):
    if request.method == 'GET':
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ SELECT        Logistica_Camiones_Seguimiento.Orden AS ORDEN, Logistica_Camiones_Seguimiento.IdAsignacion AS ID_ASIGNACION, CASE Logistica_Camiones_Seguimiento.Acepta WHEN 'S' THEN 'ACEPTADO' ELSE '-' END AS ACEPTADO,
                                                    CASE S3A.dbo.PedidoFlete.UbicacionVacios WHEN '0' THEN '-' ELSE CONVERT(VARCHAR, S3A.dbo.PedidoFlete.CantVacios) + ' B. VACIOS - ' + Logistica_Ubicacion_Chacras_Bins.Nombre END AS UBICACION_BINS, RTRIM(S3A.dbo.PedidoFlete.Solicitante) AS SOLICITA, 
                                                    RTRIM(S3A.dbo.Chacra.Nombre) AS CHACRA, RTRIM(S3A.dbo.Zona.Nombre) AS ZONA, CONVERT(VARCHAR(10), S3A.dbo.PedidoFlete.FechaPedido, 103) AS FECHA,  Logistica_Ubicacion_Chacras_Bins.Coordenadas AS COORDENADAS_RETIRA_BINS, 
                                                    CASE WHEN Logistica_Ubicacion_Chacras_Bins_1.Coordenadas IS NULL THEN '-' ELSE Logistica_Ubicacion_Chacras_Bins_1.Coordenadas END AS COORDENADAS_CHACRA 
                            FROM            Logistica_Camiones_Seguimiento INNER JOIN
                                                    S3A.dbo.PedidoFlete ON Logistica_Camiones_Seguimiento.IdAsignacion = S3A.dbo.PedidoFlete.IdPedidoFlete INNER JOIN
                                                    S3A.dbo.Chacra ON S3A.dbo.PedidoFlete.IdChacra = S3A.dbo.Chacra.IdChacra INNER JOIN
                                                    S3A.dbo.Zona ON S3A.dbo.PedidoFlete.IdZona = S3A.dbo.Zona.IdZona INNER JOIN
                                                    Logistica_Ubicacion_Chacras_Bins ON S3A.dbo.PedidoFlete.UbicacionVacios = Logistica_Ubicacion_Chacras_Bins.IdUbicacion LEFT OUTER JOIN
                                                    Logistica_Ubicacion_Chacras_Bins AS Logistica_Ubicacion_Chacras_Bins_1 ON S3A.dbo.Chacra.IdChacra = Logistica_Ubicacion_Chacras_Bins_1.IdUbicacion
                            WHERE        (Logistica_Camiones_Seguimiento.Chofer = %s ) AND (Logistica_Camiones_Seguimiento.Estado = 'S') AND (Logistica_Camiones_Seguimiento.Orden =
                                                        (SELECT        MIN(Orden) AS Expr1
                                                        FROM            Logistica_Camiones_Seguimiento AS Logistica_Camiones_Seguimiento_1
                                                        WHERE        (Chofer = %s ) AND (Estado = 'S'))) """
                cursor.execute(sql, [chofer, chofer]) 
                consulta = cursor.fetchall()
                if consulta:
                    listado_Viajes_Aceptados = []
                    for row in consulta:
                        orden = str(row[0])
                        idAsignacion = str(row[1])
                        aceptado = str(row[2])
                        ubicacionBins = str(row[3])
                        solicita = str(row[4])
                        chacra = str(row[5])
                        zona = str(row[6])
                        fecha = str(row[7])
                        coorBins = str(row[8])
                        coorChacra = str(row[9])
                        datos = {'IdAsignacion': idAsignacion, 'Aceptado': aceptado, 'Fecha': fecha, 'Chacra': chacra, 'Zona': zona, 'UbicacionBins': ubicacionBins, 'Solicita': solicita, 'Orden': orden, 'CoordenadasBins': coorBins, 'CoordenadasChacra': coorChacra}
                        listado_Viajes_Aceptados.append(datos)                    
                    return JsonResponse({'Message': 'Success', 'DataViajesAceptado': listado_Viajes_Aceptados, 'DataEstadoChofer' : traeEstadoChofer(chofer)})
                else:
                    return JsonResponse({'Message': 'No', 'DataEstadoChofer' : traeEstadoChofer(chofer)})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","datos viajes aceptados","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def traeEstadoChofer(chofer):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "DECLARE @P_Chofer VARCHAR(255) " \
                    "SET @P_Chofer = %s " \
                    "SELECT        Logistica_Estado_Camiones.Disponible, Logistica_Estado_Camiones.Libre, Logistica_Estado_Camiones.NombreChofer, " \
                                "(SELECT RTRIM(RazonSocial) FROM S3A.dbo.Transportista WHERE (IdTransportista = S3A.dbo.Chofer.IdTransportista)) AS TRANSPORTE,  " \
                                "CASE Disponible  " \
                                        "WHEN 'S' THEN 'DISPONIBLE' WHEN 'N' THEN 'NO DISPONIBLE'  " \
                                "END AS DISPONIBLE,  " \
                                "CASE Libre  " \
                                        "WHEN 'S' THEN 'LIBRE' WHEN 'N' THEN 'OCUPADO'  " \
                                "END AS LIBRE " \
                    "FROM            S3A.dbo.Chofer INNER JOIN " \
                                            "Logistica_Estado_Camiones ON S3A.dbo.Chofer.IdChofer = Logistica_Estado_Camiones.IdChofer " \
                    "WHERE        (Logistica_Estado_Camiones.NombreChofer = @P_Chofer)"
            cursor.execute(sql, [chofer])
            consulta = cursor.fetchone()
            listado_estado = []
            if consulta:
                disponible = str(consulta[0])
                libre = str(consulta[1])
                transporte = str(consulta[3])
                textoDisponible = str(consulta[4])
                textoLibre = str(consulta[5])
                datos = {'Disponible': disponible, 'Libre': libre, 'Transporte': transporte, 'TextoDisponible': textoDisponible, 'TextoLibre': textoLibre}
                listado_estado.append(datos)
                return listado_estado
            else:
                listado_estado = [{'Disponible': 'S', 'Libre': 'S', 'Transporte': 'Transporte', 'TextoDisponible': 'textoDisponible', 'TextoLibre': 'textoLibre'}]
                return listado_estado
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","traeEstadoChofer","consulta",error)
        return listado_estado
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()



def finalizaRemito(request, idAsignacion):
    if request.method == 'GET':
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ UPDATE Datos_Remito_MovBins SET AsigCerrada = 'C' WHERE IdAsignacion = %s """
                cursor.execute(sql, [idAsignacion]) 

                cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'Finalizado'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se Finalizar'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","finalizaRemito","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def guardaCosechaDiaria(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            usuario = str(json.loads(body)['usuario'])
            productor = str(json.loads(body)['idProductor'])
            chacra = str(json.loads(body)['idChacra'])
            bins = str(json.loads(body)['binsTotal'])
            values = [usuario,usuario,productor,chacra,bins]
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1
                            FROM Registro_Cosecha_Diaria
                            WHERE Usuario = %s
                            AND CONVERT(DATE, FechaAlta) = CONVERT(DATE, GETDATE())
                        )
                        BEGIN
                            INSERT INTO Registro_Cosecha_Diaria (Usuario, Productor, Chacra, CantBins, FechaAlta)
                            VALUES (%s, %s, %s, %s, GETDATE());
                            SELECT 0 AS AffectedRows;
                        END
                        ELSE
                        BEGIN
                            SELECT 1 AS AffectedRows;
                        END
                    END 
                """
                cursor.execute(sql, values)
                
                affected_rows = cursor.fetchone()[0]

            if affected_rows == 0:
                return JsonResponse({'Message': 'Success', 'Nota': 'Guardado.'})
            elif affected_rows == 1:
                return JsonResponse({'Message': 'Error', 'Nota': 'Ya se guardó el registro para hoy.'})
            else:
                return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Guardar.'})
                
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("Anticipos","verAnticipos","usuario",error)
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


































































