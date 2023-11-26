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
            idPlanta = '100'
            usuario = str(json.loads(body)['usuario'])
            fechaPedido = obtenerFechaActual()
            horaPedido = obtenerHoraActual()
            tipoDestino  = 'P'
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
            estado = 'P'
            fechaRequerida = str(json.loads(body)['fechaRequerida'])
            binsBlancos = str(json.loads(body)['binsBlancos'])
            binsRojos = str(json.loads(body)['binsRojos'])

            values = [idPlanta, solicita, fechaPedido, horaPedido, tipoDestino, tipoCarga, idProductor, idChacra, idZona, idPlantaDestino, 
                      idEspecie, idVariedad, binsTotal, traeVacios, traeCuellos, horaRequerida, observaciones, estado, fechaRequerida, 
                      usuario, binsBlancos, binsRojos]
            
            valores = ["INSERTA FLETES", obtenerFechaActual(), str(values)]
            #Insert PedidoFlete(IdPedidoFlete,IdPlanta,Solicitante,FechaPedido,HoraPedido,TipoDestino,TipoCarga,IdProductor,IdChacra,IdZona,IdPlantaDestino,
            # IdEspecie,IdVariedad,Bins,Vacios,Cuellos,HoraRequerida,Obs,Estado,FechaRequerida,FechaAlta,UserID)values(1004651,100,''PRUEBA - SISTEMAS'',''14/11/2023'',
            # ''12:17:25'',''P'',''RAU'',5405,1000732,12,NULL,1,34,40,''S'',''S'',''11:53'',''PRUEBA - OBSERVACIÓN'',''P'',''14/11/2023'',getdate(),''JCHAMBI'')

            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                # sql = "INSERT PedidoFlete (IdPedidoFlete,IdPlanta,Solicitante,FechaPedido,HoraPedido,TipoDestino,TipoCarga, " \
                #     "IdProductor,IdChacra,IdZona,IdPlantaDestino,IdEspecie,IdVariedad,Bins,Vacios,Cuellos,HoraRequerida,Obs, " \
                #     "Estado,FechaRequerida,FechaAlta,UserID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,getdate(),%s,) "
                # cursor.execute(sql, values)      
                
                sql = "INSERT Data_Funciones (Funcion, Fecha, Textos) VALUES (%s, %s, %s)"
                cursor.execute(sql, valores)                         

                return JsonResponse({'Message': 'Success', 'Nota': 'El pedido se realizó correctamente.'})

        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","insertaPedidoFlete","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})    




#### CREACION DE REMITOS DATOS A MOSTRAR ASIGNACIONES Y BINS 

def llamaAsignacionesPendientes(request, usuario):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                sql = "SELECT         IdPedidoFlete, CONVERT(VARCHAR, PedidoFlete.IdPedidoFlete) + ' - ' +  Productor.RazonSocial AS Asignacion " \
                        "FROM            PedidoFlete INNER JOIN " \
                                                "Productor ON PedidoFlete.IdProductor = Productor.IdProductor " \
                        "WHERE        (PedidoFlete.UserID = %s) AND (PedidoFlete.Estado = 'A') " \
                        "ORDER BY IdPedidoFlete"
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
            Nombre = str(json.loads(body)['nombre'])
            IdAsignación = str(json.loads(body)['idAsignacion'])
            Renspa = str(json.loads(body)['renspa'])
            UP = str(json.loads(body)['up'])
            IdEspecie = str(json.loads(body)['idEspecie'])
            IdVariedad = str(json.loads(body)['idVariedad'])
            TotalBins = str(json.loads(body)['totalBins'])
            listadoBins = json.loads(body)['DataBins']

            #### primero inserta el remito para generar el número

            numero_remito = insertaDatosRemito(IdAsignación, Renspa, UP, IdEspecie, IdVariedad, Usuario)

            ### busca datos de la Asignacion

            productor, chacra, zona, transporte, chofer, camion, patente, domicilio = datosRemito(IdAsignación)

            especie, variedad = traeEspecieVariedad(IdEspecie,IdVariedad)

            # pdf = Remito_Movimiento_Chacras(fechaActual, horaActual, numero_chacra, 
            #                         numero_remito, productor, productor, domicilio, 
            #                         chacra, especie, variedad, Renspa, UP, chofer, camion, patente, 
            #                         TotalBins, Nombre, Usuario,)
            # pdf.alias_nb_pages()
            # pdf.add_page()

            index = 0
            for item in listadoBins:
                # if index > 9:
                #     pdf.add_page()
                IdMarca = item['idMarca']
                IdTamaño = item['idTamaño']
                Cantidad = item['cantidad']   
                marca, bins = traeMarcaBinsConID(IdMarca, IdTamaño)
                # pdf.set_font('Arial', '', 8)
                # pdf.cell(w=24, h=5, txt= str(Cantidad), border='LBR', align='C', fill=0)
                # pdf.cell(w=86, h=5, txt= str(bins), border='BR', align='C', fill=0)
                # pdf.multi_cell(w=0, h=5, txt= str(marca), border='BR', align='C', fill=0)
                index = index + 1
                
            #code128 = barcode.get('code128', codigo_barra, writer=barcode.writer.ImageWriter())
            #barcode_filename = code128.save('barcode')
            # barcode_filename = 'Applications/ReportesPDF/RemitosChacra/barcode.png'
            # pdf.image(barcode_filename, x=22, y=129, w=65, h=12)

            #fecha = str(fechaActual).replace('/', '')

            name = 'R_' + str(numero_remito) + '.pdf'
            nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name

            actualizaNombrePDF(name,numero_remito)

            # pdf.output(nameDireccion, 'F')

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
            sql = "SELECT RTRIM(Nombre) AS Especie, (SELECT Nombre FROM Variedad WHERE IdVariedad = %s) AS VAriedad " \
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
            sql = "SELECT RTRIM(Nombre) AS Marca, (SELECT Nombre FROM Bins WHERE IdBins = %s) AS Bins " \
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

def insertaDatosRemito(IdAsignación, Renspa, UP, IdEspecie, IdVariedad, Usuario):
    values = [IdAsignación, Renspa, UP, IdEspecie, IdVariedad, Usuario]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Datos_Remito (NumeroRemito, IdAsignacion, Renspa, UP, IdEspecie, IdVariedad, FechaAlta, Usuario) " \
			        "VALUES ((SELECT (MAX(NumeroRemito) + 1) AS NumeroSiguiente FROM Datos_Remito), %s, %s, %s, %s, %s, getdate(), %s)"
            cursor.execute(sql, values)
            
            sql2 = "SELECT FORMAT(NumeroRemito, '00000000') FROM Datos_Remito WHERE IdAsignacion = %s"
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


def actualizaNombrePDF(nombrePdf, numero_remito):
    values = [nombrePdf, numero_remito]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE Datos_Remito SET NombrePdf = %s WHERE FORMAT(NumeroRemito, '00000000') = %s"
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


















































































