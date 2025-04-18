from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.http import HttpResponse, Http404
from django.views.static import serve
from django.http import JsonResponse
from S3A.funcionesGenerales import *
from Applications.ModelosPDF.remitoChacra import *
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
                sql2 = "SELECT IdProductor, RTRIM(RazonSocial) FROM Productor WHERE IdProductor IN(5000,5405,5200,5212,5116,5163,5213,5024) ORDER BY RazonSocial"
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

                if listado_productor and listado_especie:
                    return JsonResponse({'Message': 'Success', 'DataPlanta': listado_planta_destino, 'DataProductor': listado_productor, 'DataEspecie': listado_especie})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se pudieron obtener los datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","DatosInicialesFletesPRODUCTORES","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def datos_Iniciales_Flete_Productores(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        productor = str(json.loads(body)['usuario'])
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

                listadoProductores = traeIdProductor(productor)
                cantValuesP = ','.join(['%s'] * len(listadoProductores))
                ## PRODUCTOR
                sql2 = f"SELECT IdProductor, RTRIM(RazonSocial) FROM Productor WHERE IdProductor IN({cantValuesP}) ORDER BY RazonSocial"
                cursor.execute(sql2, listadoProductores)
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

                if listado_productor and listado_especie:
                    return JsonResponse({'Message': 'Success', 'DataPlanta': listado_planta_destino, 'DataProductor': listado_productor, 'DataEspecie': listado_especie})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se pudieron obtener los datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","DatosInicialesFletesPRODUCTORES","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
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

def traeZona(idChacra):
    try:
        with connections['S3A'].cursor() as cursor:          
            ## ZONA
            sql2 = """ SELECT LTRIM(RTRIM(Zona)) FROM Chacra WHERE IdChacra = %s """
            cursor.execute(sql2, [idChacra])
            consulta2 = cursor.fetchone()
            if consulta2:
                return str(consulta2[0])
            else:
                return "0"
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","BUSCA ID ZONA","Aplicacion",error)
        return "0"

def idEspecie_Varierad(request,idEspecie):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                ## VARIEDAD
                sql = """
                        SELECT  IdVariedad, (CONVERT(VARCHAR(3),IdVariedad) + ' - ' + RTRIM(Nombre)) AS Especie 
                        FROM Variedad 
                        WHERE IdEspecie = %s
                                AND IdVariedad IN (SELECT valor FROM dbo.fn_Split((SELECT Texto FROM TRESASES_APLICATIVO.dbo.Parametros_Aplicativo WHERE Codigo = 'APP-VAR-FLETES'), ','))
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

def traeIdProductor(productor):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Productor FROM USUARIOS WHERE Usuario = %s"
            cursor.execute(sql, [productor])
            consulta = cursor.fetchone()
            if consulta:
                datos = str(consulta[0])
                listado_id = datos.split(',')
                return listado_id
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","TRAE PRODUCTORES","Aplicacion",error)

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
            horaPedido = obtenerHoraActual() + ":00"
            tipoDestino  = "P"
            tipoCarga = str(json.loads(body)['tipoCarga'])
            idProductor = str(json.loads(body)['idProductor'])
            idChacra = str(json.loads(body)['idChacra'])
            idZona = traeZona(str(json.loads(body)['idChacra']))
            idPlantaDestino = None
            idEspecie = str(json.loads(body)['idEspecie'])
            idVariedad = str(json.loads(body)['idVariedad'])
            binsTotal = str(json.loads(body)['binsTotal'])
            traeVacios = str(json.loads(body)['traeVacios'])
            traeCuellos = str(json.loads(body)['traeCuellos'])
            horaRequerida = str(json.loads(body)['horaRequerida']) + ":00"
            observaciones = str(json.loads(body)['observaciones'])
            estado = "P"
            fechaRequerida = str(json.loads(body)['fechaRequerida'])
            binsRojos = str(json.loads(body)['binsRojos'])

            registroRealizado(usuario,"PEDIDO FLETE",str(body))

            #insertar_registro_error_sql("FletesRemitos","HORA REQUERIA","Aplicacion",horaRequerida)

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
                sql = """ 
                     SELECT        PedidoFlete.IdPedidoFlete AS ID, 
                                CONVERT(VARCHAR,PedidoFlete.IdPedidoFlete) + ' - ' + RTRIM(Chacra.Nombre) AS ASIGNACION, PedidoFlete.Estado
                    FROM            PedidoFlete 
                                INNER JOIN      Chacra ON PedidoFlete.IdChacra = Chacra.IdChacra
                    WHERE        (PedidoFlete.UserID = %s) 
                                AND (PedidoFlete.TipoCarga = 'RAU')
                                AND (PedidoFlete.Estado = 'A') 
                                AND (EXISTS (
                                    SELECT 1 
                                    FROM TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins 
                                    WHERE IdAsignacion = PedidoFlete.IdPedidoFlete 
                                        AND AsigCerrada IS NULL
                                ) OR NOT EXISTS (
                                    SELECT 1 
                                    FROM TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins 
                                    WHERE IdAsignacion = PedidoFlete.IdPedidoFlete ))
                 """
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
                sql =   """
                        SELECT        RTRIM(P.RazonSocial) AS Productor, RTRIM(C.Nombre) AS Chacra, RTRIM(Z.Nombre) AS Zona, RTRIM(CONVERT(VARCHAR(30), T.RazonSocial)) AS Transporte,
                                    RTRIM(PF.Chofer), RTRIM(CA.Nombre) AS Camion, RTRIM(CA.Patente), RTRIM(C.RENSPA) AS Renspa, PF.IdProductor, 
									CASE WHEN (SELECT DISTINCT Telefono
													FROM Chofer
													WHERE (RTRIM(Apellidos) + ' ' + RTRIM(Nombres)) = RTRIM(PF.Chofer)) IS NULL THEN '0' ELSE (SELECT DISTINCT Telefono
													FROM Chofer
													WHERE (RTRIM(Apellidos) + ' ' + RTRIM(Nombres)) = RTRIM(PF.Chofer)) END AS TELEFONO
                        FROM            PedidoFlete AS PF LEFT OUTER JOIN 
                                    Productor AS P ON PF.IdProductor = P.IdProductor LEFT OUTER JOIN 
                                    Chacra AS C ON PF.IdChacra = C.IdChacra LEFT OUTER JOIN 
                                    Zona AS Z ON PF.IdZona = Z.IdZona LEFT OUTER JOIN 
                                    Ubicacion AS U ON PF.IdPlantaDestino = U.IdUbicacion LEFT OUTER JOIN 
                                    Especie AS E ON PF.IdEspecie = E.IdEspecie LEFT OUTER JOIN 
                                    Variedad AS V ON PF.IdVariedad = V.IdVariedad LEFT OUTER JOIN 
                                    Transportista AS T ON PF.IdTransportista = T.IdTransportista LEFT OUTER JOIN 
                                    Camion AS CA ON PF.IdCamion = CA.IdCamion LEFT OUTER JOIN 
                                    Acoplado AS A ON PF.IdAcoplado = A.IdAcoplado 
                        WHERE        (PF.IdPedidoFlete = %s)
                        """
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
                        idProductor = str(row[8])
                        tel = str(row[9])
                        datos = {'Productor': productor, 'Chacra': chacra, 'Zona': zona, 'Transporte': transporte,
                                  'Chofer': chofer, 'Camion':camion, 'Patente': patente, 'Renspa': renspa, 'IdProductor': idProductor, 'Tel': tel}
                        listadoData_Asignaciones.append(datos)
                
                listadoData_UP = traeUPS(renspa)
                listadoData_Marca = traeMarcaBins()

                
                listadoData_especie = []
                listado_idEspecies = traeIdEspecies()
                cantValuesEspecie = ','.join(['%s'] * len(listado_idEspecies))
                sql3 = f"SELECT IdEspecie, RTRIM(Nombre) FROM Especie WHERE IdEspecie IN ({cantValuesEspecie}) ORDER BY IdEspecie"
                cursor.execute(sql3, listado_idEspecies)
                consulta3 = cursor.fetchall()
                if consulta3:
                    for row3 in consulta3:
                        idEspecie = str(row3[0])
                        nombre = str(row3[1])
                        datos = {'IdEspecie': idEspecie, 'NombreEspecie': nombre}
                        listadoData_especie.append(datos)

                ## VARIEDADES
                listados = {item: [] for item in listado_idEspecies}

                for item in listados.items():
                    dato = traeTipoVariedad(item[0])
                    listados[item[0]] = dato

                listadoData_variedades = []

                for item, dato in listados.items():
                    listadoData_variedades.append({item: dato})   
            
                #### BINS
                listado_idMarcas = traeIdMarcas()
                listados = {item: [] for item in listado_idMarcas}

                for item in listados.items():
                    dato = traeTipoBins(item[0])
                    listados[item[0]] = dato

                listadoData_TipoBins = []

                for item, dato in listados.items():
                    listadoData_TipoBins.append({item: dato})
                    
                registroRealizado(str(idAsignacion),"LISTAS CARGADAS",str(listadoData_Asignaciones) + "-" + str(listadoData_UP) + "-" + str(listadoData_Marca) + "-" + str(listadoData_TipoBins)) 
                if listadoData_Asignaciones and listadoData_UP and listadoData_Marca and listadoData_TipoBins:
                    return JsonResponse({'Message': 'Success', 'DataAsignaciones': listadoData_Asignaciones, 'DataUp': listadoData_UP, 'DataMarcas': listadoData_Marca, 'DataTipo': listadoData_TipoBins, 
                                         'DataEspecie': listadoData_especie, 'DataVariedades':listadoData_variedades})
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
            sql = "SELECT DISTINCT RTRIM(UP) FROM ReporteDanio WHERE RENSPA = %s "
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
            Usuario = str(json.loads(body)['usuario'])
            capataz = str(json.loads(body)['nombre'])
            IdAsignación = str(json.loads(body)['idAsignacion'])
            Renspa = str(json.loads(body)['renspa'])
            UP = str(json.loads(body)['up'])
            IdEspecie = str(json.loads(body)['idEspecie'])
            IdVariedad = str(json.loads(body)['idVariedad'])
            total_bins = str(json.loads(body)['totalBins'])
            idPrductor = str(json.loads(body)['idProductor'])
            listadoBins = json.loads(body)['DataBins']

            

            registroRealizado(Usuario,"CREACION DE REMITO",str(body))
            #### primero inserta el remito para generar el número
            numero_remito = insertaDatosRemito(IdAsignación, Renspa, UP, IdEspecie, IdVariedad, total_bins, Usuario,idPrductor)
            ### busca datos de la Asignacion
            productor, lote, zona, transporte, chofer, camion, patente, domicilio = datosRemito(IdAsignación)
            especie, variedad = traeEspecieVariedad(IdEspecie,IdVariedad)

            if idPrductor == '5000':
                numero_chacra= "00018"
                pdf = Remito_Abadon_Movimiento_Chacras(fechaActual, horaActual, numero_chacra, 
                                    numero_remito, productor, productor, domicilio, 
                                    lote, especie, variedad, Renspa, UP, chofer, camion, patente, 
                                    total_bins, capataz)
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
                    insertaBinsRemito(numero_remito,Cantidad, IdMarca, IdTamaño,idPrductor)
                    pdf.set_font('Arial', '', 8)
                    pdf.cell(w=24, h=5, txt= str(Cantidad), border='LBR', align='C', fill=0)
                    pdf.cell(w=86, h=5, txt= str(bins), border='BR', align='C', fill=0)
                    pdf.multi_cell(w=0, h=5, txt= str(marca), border='BR', align='C', fill=0)
                    index = index + 1   
                fecha = str(fechaActual).replace('/', '')
                name = 'R_00018_' + str(numero_remito) + '_' + fecha + '.pdf'
                nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name
                actualizaNombrePDF(name,numero_remito)
                pdf.output(nameDireccion, 'F')
                nota = "El Remito se creó correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': nota})
            
            elif idPrductor == '5200':
                numero_chacra= "00001"
                pdf = Remito_Romik_Movimiento_Chacras(fechaActual, horaActual, numero_chacra, 
                    numero_remito, productor, productor, domicilio, 
                    lote, especie, variedad, Renspa, UP, chofer, camion, patente, 
                    total_bins, capataz)
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
                    insertaBinsRemito(numero_remito,Cantidad, IdMarca, IdTamaño,idPrductor)
                    pdf.set_font('Arial', '', 8)
                    pdf.cell(w=24, h=5, txt= str(Cantidad), border='LBR', align='C', fill=0)
                    pdf.cell(w=86, h=5, txt= str(bins), border='BR', align='C', fill=0)
                    pdf.multi_cell(w=0, h=5, txt= str(marca), border='BR', align='C', fill=0)
                    index = index + 1   
                fecha = str(fechaActual).replace('/', '')
                name = 'R_00001_' + str(numero_remito) + '_' + fecha + '.pdf'
                nameDireccion = 'Applications/ReportesPDF/RemitosChacra/' + name
                actualizaNombrePDF(name,numero_remito)
                pdf.output(nameDireccion, 'F')
                nota = "El Remito se creó correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': nota})
            
            else:
                numero_chacra = "00017"
                pdf = Remito_Movimiento_Chacras(fechaActual, horaActual, numero_chacra, 
                    numero_remito, productor, productor, domicilio, 
                    lote, especie, variedad, Renspa, UP, chofer, camion, patente, 
                    total_bins, capataz)
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
                    insertaBinsRemito(numero_remito,Cantidad, IdMarca, IdTamaño,idPrductor)
                    pdf.set_font('Arial', '', 8)
                    pdf.cell(w=24, h=5, txt= str(Cantidad), border='LBR', align='C', fill=0)
                    pdf.cell(w=86, h=5, txt= str(bins), border='BR', align='C', fill=0)
                    pdf.multi_cell(w=0, h=5, txt= str(marca), border='BR', align='C', fill=0)
                    index = index + 1   
                fecha = str(fechaActual).replace('/', '')
                name = 'R_00017_' + str(numero_remito) + '_' + fecha + '.pdf'
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

def insertaDatosRemito(IdAsignación, Renspa, UP, IdEspecie, IdVariedad, total_bins, Usuario, idProductor):
    if str(idProductor) == "5000" or str(idProductor) == "5200":
        values = [idProductor, IdAsignación, Renspa, UP, IdEspecie, IdVariedad, total_bins, Usuario,idProductor]
        try:    
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "INSERT INTO Datos_Remito_MovBins (NumeroRemito, IdAsignacion, Renspa, UP, IdEspecie, IdVariedad, Cantidad, FechaAlta, Usuario, IdProductor) " \
                        "VALUES ((SELECT (MAX(NumeroRemito) + 1) AS NumeroSiguiente FROM Datos_Remito_MovBins WHERE IdProductor = %s), %s, %s, %s, %s, %s, %s, getdate(), %s,%s)"
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
    else:
        values = [IdAsignación, Renspa, UP, IdEspecie, IdVariedad, total_bins, Usuario,idProductor]
        try:    
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "INSERT INTO Datos_Remito_MovBins (NumeroRemito, IdAsignacion, Renspa, UP, IdEspecie, IdVariedad, Cantidad, FechaAlta, Usuario, IdProductor) " \
                        "VALUES ((SELECT (MAX(NumeroRemito) + 1) AS NumeroSiguiente FROM Datos_Remito_MovBins), %s, %s, %s, %s, %s, %s, getdate(), %s,%s)"
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

def insertaBinsRemito(numeroRemito, cantidad, idMarca, idBins, idProductor):
    values = [numeroRemito, cantidad, idMarca, idBins, idProductor]
    try:    
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Contenido_Remito_MovBins (NumeroRemito, Cantidad, IdMarca, IdBins, IdProductor) " \
			        "VALUES (%s, %s, %s, %s, %s)"
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
                                --AND PedidoFlete.Estado IN ('A', 'C')
                                --AND (SELECT Final FROM TRESASES_APLICATIVO.dbo.Logistica_Camiones_Seguimiento WHERE IdAsignacion = PedidoFlete.IdPedidoFlete) IS NULL 
                            ORDER BY TRESASES_APLICATIVO.dbo.Datos_Remito_MovBins.FechaAlta """
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
                                    "WHERE Chofer = %s " \
                                ") " \
                                "THEN (SELECT MAX(Orden) + 1 FROM Logistica_Camiones_Seguimiento WHERE Chofer = %s) " \
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
                                    "WHERE Chofer = %s " \
                                ") " \
                                "THEN (SELECT MAX(Orden) + 1 FROM Logistica_Camiones_Seguimiento WHERE Chofer = %s) " \
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
                    return JsonResponse({'Message': 'Success', 'Nota': 'Retiró Bins', 'Estado':textUbicacion(Chofer)})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'Ya se confirmó el retiro.', 'Estado':textUbicacion(Chofer)})
                
            if Columna == 'Final':
                if verificaBinLleno(IdAsignacion) == 'RAU':
                    if verificaLote(IdAsignacion):
                        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                            sql = f"UPDATE Logistica_Camiones_Seguimiento SET {Columna} = %s, HoraFinal = GETDATE(), Estado = 'F', Actualizacion = GETDATE() WHERE IdAsignacion = %s AND Estado = 'S' "
                            cursor.execute(sql, [Valor, IdAsignacion])           

                            sqlUpdate = """UPDATE Logistica_Estado_Camiones 
                                        SET Libre = 'S', Actualizado = GETDATE() 
                                        WHERE NombreChofer = %s 
                                        AND NOT EXISTS (
                                            SELECT 1 
                                            FROM Logistica_Camiones_Seguimiento 
                                            WHERE Chofer = %s AND Estado = 'S'
                                        )""" 
                            cursor.execute(sqlUpdate, [Chofer,Chofer])     

                            sqlDelete = "DELETE Logistica_Campos_Temporales WHERE IdAsignacion = %s"
                            cursor.execute(sqlDelete, [IdAsignacion])

                            cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                            affected_rows = cursor.fetchone()[0]

                        if affected_rows > 0:
                            return JsonResponse({'Message': 'Success', 'Nota': 'F', 'Estado':textUbicacion(Chofer)})
                        else:
                            return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Finalizar', 'Estado':textUbicacion(Chofer)})
                    #return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Finalizar', 'Estado':textUbicacion(Chofer)})
                    else:
                        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                            sql = f"UPDATE Logistica_Camiones_Seguimiento SET {Columna} = %s, HoraFinal = GETDATE(), Estado = 'F', Actualizacion = GETDATE() WHERE IdAsignacion = %s AND Estado = 'S' "
                            cursor.execute(sql, [Valor, IdAsignacion])           

                            sqlUpdate = """UPDATE Logistica_Estado_Camiones 
                                        SET Libre = 'S', Actualizado = GETDATE() 
                                        WHERE NombreChofer = %s 
                                        AND NOT EXISTS (
                                            SELECT 1 
                                            FROM Logistica_Camiones_Seguimiento 
                                            WHERE Chofer = %s AND Estado = 'S'
                                        )""" 
                            cursor.execute(sqlUpdate, [Chofer,Chofer])     

                            sqlDelete = "DELETE Logistica_Campos_Temporales WHERE IdAsignacion = %s"
                            cursor.execute(sqlDelete, [IdAsignacion])

                            cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                            affected_rows = cursor.fetchone()[0]

                        if affected_rows > 0:
                            return JsonResponse({'Message': 'Success', 'Nota': 'F', 'Estado':textUbicacion(Chofer)})
                        else:
                            return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Finalizar', 'Estado':textUbicacion(Chofer)})
                    #return JsonResponse({'Message': 'Error', 'Nota': 'EL VIAJE NO SE PUEDE FINALIZAR SI NO INGRESÓ EN BÁSCULA.', 'Estado':textUbicacion(Chofer)})                        
                else:
                    with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                        sql = f"UPDATE Logistica_Camiones_Seguimiento SET {Columna} = %s, HoraFinal = GETDATE(), Estado = 'F', Actualizacion = GETDATE() WHERE IdAsignacion = %s AND Estado = 'S' "
                        cursor.execute(sql, [Valor, IdAsignacion])           

                        sqlUpdate = """UPDATE Logistica_Estado_Camiones 
                                    SET Libre = 'S', Actualizado = GETDATE() 
                                    WHERE NombreChofer = %s 
                                    AND NOT EXISTS (
                                        SELECT 1 
                                        FROM Logistica_Camiones_Seguimiento 
                                        WHERE Chofer = %s AND Estado = 'S'
                                    )""" 
                        cursor.execute(sqlUpdate, [Chofer,Chofer])     

                        sqlDelete = "DELETE Logistica_Campos_Temporales WHERE IdAsignacion = %s"
                        cursor.execute(sqlDelete, [IdAsignacion])

                        cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                        affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'F', 'Estado':textUbicacion(Chofer)})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Finalizar', 'Estado':textUbicacion(Chofer)})
                
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
                        return JsonResponse({'Message': 'Success', 'Nota': 'Punto Actualizado', 'Estado':textUbicacion(Chofer)})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Actualizar', 'Estado':textUbicacion(Chofer)})
                else:
                    with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                        cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                        affected_rows = cursor.fetchone()[0]
                        
                    return JsonResponse({'Message': 'Error', 'Nota': 'Se Actualizaron todos los Puntos', 'Estado':textUbicacion(Chofer)})
            return JsonResponse({'Message': 'Error', 'Nota': 'EL VIAJE NO SE PUEDE FINALIZAR SI NO INGRESÓ EN BÁSCULA.', 'Estado':textUbicacion(Chofer)})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FletesRemitos","actualizaEstadoPosicion","Aplicacion",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
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

def verificaLote(idAsignacion):
    try:
        with connections['S3A'].cursor() as cursor:
            sql = """ SELECT 1
                        FROM Lote
                        WHERE IdPedidoFlete = %s """
            cursor.execute(sql, [idAsignacion])
            results = cursor.fetchone()
            if results:
                return True
            else:
                return False
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","verifica Lote","consulta",error)
        return False
    
def verificaBinLleno(idAsignacion):
    try:
        with connections['S3A'].cursor() as cursor:
            sql = """ SELECT RTRIM(TipoCarga)
                        FROM PedidoFlete
                        WHERE IdPedidoFlete = %s """
            cursor.execute(sql, [idAsignacion])
            results = cursor.fetchone()
            if results:
                tipo = str(results[0])
                return tipo
            else:
                return 'VAC'
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","VERIFICA BIN LLENO","consulta",error)
        return 'VAC'
    
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
                sql = """   DECLARE @@Chofer VARCHAR(255);
                            SET @@Chofer = %s;
                            SELECT        LCS.Orden AS ORDEN, LCS.IdAsignacion AS ID_ASIGNACION, CASE LCS.Acepta WHEN 'S' THEN 'ACEPTADO' ELSE '-' END AS ACEPTADO,
                                        CASE PF.UbicacionVacios WHEN '0' THEN '-' ELSE CONVERT(VARCHAR, PF.CantVacios) + ' B. VACIOS - ' + LUCB.Nombre END AS UBICACION_BINS, RTRIM(PF.Solicitante) AS SOLICITA, 
                                        COALESCE(RTRIM(CH.Nombre),'-') AS CHACRA, COALESCE(RTRIM(ZN.Nombre),'-') AS ZONA, CONVERT(VARCHAR(10), PF.FechaPedido, 103) + ' - ' + CONVERT(VARCHAR(5), PF.HoraPedido, 108) +' Hs.' AS FECHA,  
                                        CASE WHEN LUCB.Coordenadas IS NULL THEN '-' ELSE LUCB.Coordenadas END AS COORDENADAS_RETIRA_BINS, 
                                        CASE WHEN LUCB1.Coordenadas IS NULL THEN '-' ELSE LUCB1.Coordenadas END AS COORDENADAS_CHACRA, COALESCE(US.Telefono,'0') AS TELEFONO,
                                        CASE WHEN PF.IdChacra IS NULL THEN 'CD' ELSE 'PC' END AS TIPO, COALESCE(RTRIM(UB.Descripcion),'-') AS ORIGEN, COALESCE(RTRIM(UBS.Descripcion),'-') AS DESTINO, COALESCE(RTRIM(PF.Obs),'-') AS OBS
                            FROM            Logistica_Camiones_Seguimiento AS LCS INNER JOIN
                                        S3A.dbo.PedidoFlete AS PF ON LCS.IdAsignacion = PF.IdPedidoFlete LEFT JOIN
                                        S3A.dbo.Chacra AS CH ON PF.IdChacra = CH.IdChacra LEFT JOIN
                                        S3A.dbo.Zona AS ZN ON PF.IdZona = ZN.IdZona LEFT JOIN
                                        Logistica_Ubicacion_Chacras_Bins AS LUCB ON PF.UbicacionVacios = LUCB.IdUbicacion LEFT OUTER JOIN
                                        Logistica_Ubicacion_Chacras_Bins AS LUCB1 ON CH.IdChacra = LUCB1.IdUbicacion LEFT JOIN
                                        USUARIOS AS US ON US.Usuario = PF.UserID COLLATE database_default LEFT JOIN
                                        S3A.dbo.Ubicacion AS UB ON UB.IdUbicacion = PF.IdPlanta LEFT JOIN
                                        S3A.dbo.Ubicacion AS UBS ON UBS.IdUbicacion = PF.IdPlantaDestino
                            WHERE        (LCS.Chofer = @@Chofer ) AND (LCS.Estado = 'S') AND (LCS.Orden =
                                            (SELECT        MIN(Orden) AS Expr1
                                            FROM            Logistica_Camiones_Seguimiento
                                            WHERE        (Chofer = @@Chofer ) AND (Estado = 'S'))) """
                cursor.execute(sql, [chofer]) 
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
                        tel = str(row[10])
                        tipo = str(row[11])
                        origen = str(row[12])
                        destino = str(row[13])
                        obs = str(row[14])
                        datos = {'IdAsignacion': idAsignacion, 'Aceptado': aceptado, 'Fecha': fecha, 'Chacra': chacra, 'Zona': zona, 
                                 'UbicacionBins': ubicacionBins, 'Solicita': solicita, 'Orden': orden, 'CoordenadasBins': coorBins, 
                                 'CoordenadasChacra': coorChacra, 'Tel': tel, 'Tipo': tipo, 'Origen': origen, 'Destino': destino, 'Obs': obs}
                        listado_Viajes_Aceptados.append(datos)    
                    
                    if  textUbicacion(chofer) == '-':
                        return JsonResponse({'Message': 'Success', 'DataViajesAceptado': listado_Viajes_Aceptados, 'DataEstadoChofer' : traeEstadoChofer(chofer)})
                    else:
                        return JsonResponse({'Message': 'Success', 'DataViajesAceptado': listado_Viajes_Aceptados, 'DataEstadoChofer' : traeEstadoChofer(chofer), 'Estado':textUbicacion(chofer)})
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

def textUbicacion(chofer):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT	CONVERT(VARCHAR(1), CASE Acepta WHEN 'S' THEN '*' ELSE '' END) + ' ' +
                            CONVERT(VARCHAR(1), CASE WHEN LlegaChacra IS NULL THEN '' ELSE '*' END) + ' ' +
                            CONVERT(VARCHAR(1), CASE WHEN SaleChacra IS NULL THEN '' ELSE '*' END) + ' ' +
                            CONVERT(VARCHAR(1), CASE WHEN Bascula IS NULL THEN '' ELSE '*' END)
                    FROM Logistica_Camiones_Seguimiento
                    WHERE Chofer = %s AND Estado = 'S'
                """
            cursor.execute(sql, [chofer])
            consulta = cursor.fetchone()
            if consulta:
                estado = str(consulta[0])
                return estado
            else:
                return "-"
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","textUbicacion","consulta",error)
        return "-"

def finalizaRemito(request, idAsignacion):
    if request.method == 'GET':
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ UPDATE Datos_Remito_MovBins SET AsigCerrada = 'P' WHERE IdAsignacion = %s """
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
            values = [usuario,productor,chacra,bins]
            if existeRegistro(usuario,chacra):
                return JsonResponse({'Message': 'Error', 'Nota': 'Ya se guardó el registro de hoy de esa chacra.'})
            else:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ INSERT INTO Registro_Cosecha_Diaria (Usuario, Productor, Chacra, CantBins, FechaAlta) VALUES (%s, %s, %s, %s, GETDATE()); """
                    cursor.execute(sql, values)
                    cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                if affected_rows > 0:
                    return JsonResponse({'Message': 'Success', 'Nota': 'Guardado.'})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo Guardar.'})
                
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FLETES REMITOS","GUARDA COSECHA","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def existeRegistro(usuario, idChacra):
    try:
        values = [usuario,idChacra]
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ SELECT 1
                    FROM Registro_Cosecha_Diaria
                    WHERE Usuario = %s
                    AND CONVERT(DATE, FechaAlta) = CONVERT(DATE, GETDATE()) AND Chacra = %s """
            cursor.execute(sql, values)
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
            
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("EXISTE REGISTRO","SELECT","usuario",error)
        return False
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

@csrf_exempt
def verReporteBins(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            fecha = str(json.loads(body)['fecha'])
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """
                        DECLARE @@Fecha DATE;
                        SET @@Fecha = %s;
                        SELECT        TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple AS NOMBRE, RTRIM(S3A.dbo.Productor.RazonSocial) AS PRODUCTOR, 
                                                RTRIM(S3A.dbo.Chacra.Nombre) AS CHACRA, Registro_Cosecha_Diaria.CantBins AS BINS_COSECHADOS, CONVERT(VARCHAR(5), Registro_Cosecha_Diaria.FechaAlta, 108) + ' HS.' AS HORA_INFORME,
                                                (SELECT SUM(Registro_Cosecha_Diaria.CantBins)
                                                    FROM Registro_Cosecha_Diaria
                                                    WHERE        (TRY_CONVERT(DATE, Registro_Cosecha_Diaria.FechaAlta) = TRY_CONVERT(DATE, @@Fecha ))) AS TOTAL_COSECHADO
                        FROM            TresAses_ISISPayroll.dbo.Empleados INNER JOIN
                                                Registro_Cosecha_Diaria INNER JOIN
                                                USUARIOS ON Registro_Cosecha_Diaria.Usuario = USUARIOS.Usuario ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = USUARIOS.CodEmpleado INNER JOIN
                                                S3A.dbo.Productor ON Registro_Cosecha_Diaria.Productor = S3A.dbo.Productor.IdProductor INNER JOIN
                                                S3A.dbo.Chacra ON Registro_Cosecha_Diaria.Chacra = S3A.dbo.Chacra.IdChacra
                        WHERE        (TRY_CONVERT(DATE, Registro_Cosecha_Diaria.FechaAlta) = TRY_CONVERT(DATE, @@Fecha))
                        ORDER BY Registro_Cosecha_Diaria.FechaAlta
                    """
                cursor.execute(sql,[fecha])
                results = cursor.fetchall()
                if results:
                    listado = []
                    for result in results:
                        nombre = str(result[0])
                        productor = str(result[1])
                        chacra = str(result[2])
                        cantidad = str(result[3])
                        hora = str(result[4])
                        total = str(result[5])
                        datos = {'Nombre': nombre, 'Productor': productor, 'Chacra': chacra, 'Cantidad': cantidad, 'Hora': hora, 'Total': total}
                        listado.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': listado})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
                    error = str(e)
                    insertar_registro_error_sql("FLETES REMITOS","VER REPORTE DIARIO","usuario",error)
                    return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

### PARTE NUEVA 
@csrf_exempt
def Carga_Inicial_Flete(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        usuario = str(json.loads(body)['usuario'])
        print(usuario)
        try:
            with connections['S3A'].cursor() as cursor:

                listado_chacras = []
                listado_especie = []
                listado_variedades = []
                
                listado_idChacras = chacrasUsuario(usuario)
                cantValuesChacras = ','.join(['%s'] * len(listado_idChacras))
                ## CHACRAS ASIGNADAS
                sql = f"SELECT IdChacra, RTRIM(Nombre) AS NOMBRE FROM Chacra WHERE IdChacra IN ({cantValuesChacras})"
                cursor.execute(sql,listado_idChacras)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        IdChacra = str(row[0])
                        NombreChacra = str(row[1])
                        datos = {'IdChacra': IdChacra, 'NombreChacra': NombreChacra}
                        listado_chacras.append(datos)
                    
               
                ## ESPECIE
                listado_idEspecies = traeIdEspecies()
                cantValuesEspecie = ','.join(['%s'] * len(listado_idEspecies))
                sql3 = f"SELECT IdEspecie, RTRIM(Nombre) FROM Especie WHERE IdEspecie IN ({cantValuesEspecie}) ORDER BY IdEspecie"
                cursor.execute(sql3, listado_idEspecies)
                consulta3 = cursor.fetchall()
                if consulta3:
                    listado_especie = []
                    for row3 in consulta3:
                        idEspecie = str(row3[0])
                        nombre = str(row3[1])
                        datos = {'IdEspecie': idEspecie, 'NombreEspecie': nombre}
                        listado_especie.append(datos)

                ## VARIEDADES
                listados = {item: [] for item in listado_idEspecies}

                for item in listados.items():
                    dato = traeTipoVariedad(item[0])
                    listados[item[0]] = dato

                listadoData_variedades = []

                for item, dato in listados.items():
                    listadoData_variedades.append({item: dato})   



                if listado_chacras and listado_especie and listado_variedades:
                    return JsonResponse({'Message': 'Success', 'DataChacras': listado_chacras, 'DataEspecie': listado_especie, 'DataVariedades': listadoData_variedades})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se pudieron obtener los datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FLETES REMITO","CARGA INICIAL FLETE NUEVO",usuario,error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def chacrasUsuario(usuario):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT Chacras
                    FROM USUARIOS
                    WHERE Usuario = %s
                """
            cursor.execute(sql, [usuario])
            consulta = cursor.fetchone()
            if consulta:
                datos = str(consulta[0])
                listado_id = datos.split(',')
                return listado_id
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FLETES REMITO","CHACRAS USUARIO",usuario,error)
        return "-"

def traeTipoVariedad(idEspecie):
    try:
        with connections['S3A'].cursor() as cursor:
            listado_tipo = []
            sql = "SELECT IdVariedad, RTRIM(Nombre) FROM Variedad WHERE IdEspecie = %s"
            cursor.execute(sql,[idEspecie])
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    idVariedad = str(row[0])
                    nombreVariedad = str(row[1])
                    datos = {'IdVarierad': idVariedad, 'NombreVariedad': nombreVariedad}
                    listado_tipo.append(datos)
                    
                return listado_tipo
            else: 
                return listado_tipo
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","TRAE TIPO VARIEDAD","Aplicacion",error)
    finally:
        cursor.close()
        connections['S3A'].close()

#### CONSULTA DE CALIDAD SEGUN LAS CHACRAS ######
@csrf_exempt
def verReporteCalidad(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        usuario = str(json.loads(body)['usuario'])
        desde = str(json.loads(body)['desde'])
        hasta = str(json.loads(body)['hasta'])
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """
                        SET DATEFORMAT dmy;
                        DECLARE @@Usuario VARCHAR(12);
                        DECLARE @@Desde DATE;
                        DECLARE @@Hasta DATE;
                        SET @@Usuario = %s ;
                        SET @@Desde = %s ;
                        SET @@Hasta = %s ;
                        SELECT        Datos_Remito_MovBins.IdAsignacion AS ID_ASIGNACION, Datos_Remito_MovBins.IdProductor AS ID_PRODUCTOR, RTRIM(S3A.dbo.Productor.RazonSocial) AS PRODUCTOR, Datos_Remito_MovBins.NumeroRemito AS NUM_REMITO, 
                                        S3A.dbo.Lote.IdRemito AS ID_REMITO, S3A.dbo.Lote.IdLote AS NUM_LOTE, S3A.dbo.Lote.IdProductor AS ID_PRODUCTOR1, S3A.dbo.Lote.IdVariedad AS ID_VARIEDAD, RTRIM(S3A.dbo.Lote.Fecha) AS FECHA, RTRIM(S3A.dbo.Variedad.Nombre) AS VARIEDAD, S3A.dbo.Lote.CantBins AS CANT_BINS, 
                                        S3A.dbo.Lote.IdChacra AS ID_CHACRA, RTRIM(S3A.dbo.Chacra.Nombre) AS CHACRA, S3A.dbo.ControlCalidad.IdCC AS ID_CONTROL, RTRIM(S3A.dbo.ControlCalidad.CondLote) AS CONDICION, 
                                        CASE WHEN S3A.dbo.ControlCalidad.ObsAD IS NULL THEN '' ELSE RTRIM(S3A.dbo.ControlCalidad.ObsAD) END AS OBS_AD_EXTERNO,
                                        CASE WHEN S3A.dbo.ControlCalidad.ObsAV IS NULL THEN '' ELSE RTRIM(S3A.dbo.ControlCalidad.ObsAV) END AS OBS_AV_EXTERNO,
                                        CASE WHEN S3A.dbo.ControlCalidad.ObsControlCalidad IS NULL THEN '' ELSE RTRIM(S3A.dbo.ControlCalidad.ObsControlCalidad) END AS OBS_CONTROL_INTERNO,
                                        CASE WHEN RTRIM(S3A.dbo.ControlCalidad.CondLote) = 'ACEPTADO' THEN '#00913f' WHEN RTRIM(S3A.dbo.ControlCalidad.CondLote) = 'RECHAZADO' THEN '#FF0000' ELSE '#ff8000' END AS HEXADECIMAL,
                                        Datos_Remito_MovBins.Usuario AS USUARIO
                        FROM            Datos_Remito_MovBins INNER JOIN
                                                S3A.dbo.Lote ON Datos_Remito_MovBins.NumeroRemito = S3A.dbo.Lote.IdRemito AND Datos_Remito_MovBins.IdProductor = S3A.dbo.Lote.IdProductor INNER JOIN
                                                S3A.dbo.Variedad ON S3A.dbo.Lote.IdVariedad = S3A.dbo.Variedad.IdVariedad INNER JOIN
                                                S3A.dbo.Chacra ON S3A.dbo.Lote.IdChacra = S3A.dbo.Chacra.IdChacra INNER JOIN
                                                S3A.dbo.ControlCalidad ON S3A.dbo.Lote.IdLote = S3A.dbo.ControlCalidad.IdLote INNER JOIN
                                                S3A.dbo.Productor ON Datos_Remito_MovBins.IdProductor = S3A.dbo.Productor.IdProductor
                        WHERE        (Datos_Remito_MovBins.Usuario = @@Usuario OR @@Usuario IS NULL OR @@Usuario = '') 
                                    AND (Datos_Remito_MovBins.Modificado IS NULL) 
                                    AND (TRY_CONVERT(DATE, S3A.dbo.Lote.Fecha) >= @@Desde OR @@Desde IS NULL OR @@Desde = '') 
                                    AND (TRY_CONVERT(DATE, S3A.dbo.Lote.Fecha) <= @@Hasta OR @@Hasta IS NULL OR @@Hasta = '')
                        ORDER BY TRY_CONVERT(DATE, S3A.dbo.Lote.Fecha), Datos_Remito_MovBins.Usuario
                    """
                cursor.execute(sql,[usuario,desde,hasta])
                results = cursor.fetchall()
                if results:
                    listado = []
                    for result in results:
                        productor = str(result[2])
                        lote = str(result[5])
                        fecha = str(result[8])
                        variedad = str(result[9])
                        bins = str(result[10])
                        chacra = str(result[12])
                        condicion = str(result[14])
                        obsAD = "-"
                        obsAV = "-"
                        obsControl = "-"
                        hexa = str(result[18])
                        user = str(result[19])
                        datos = {'Productor': productor, 'Lote': lote, 'Fecha': fecha, 'Variedad': variedad, 'Bins': bins, 'Chacra': chacra,
                                 'Condicion': condicion, 'ObsAD': obsAD, 'ObsAV': obsAV, 'ObsControl': obsControl, 'Hexa': hexa, 'Usuario': user}
                        listado.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': listado})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
                    error = str(e)
                    insertar_registro_error_sql("FLETES REMITOS","VER REPORTE CHACRAS",usuario,error)
                    return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

####################### PEDIDOS DE FLETE NUEVO #########################

def Data_Destinos_Origenes(request):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """ 
                        SELECT IdUbicacion AS ID, RTRIM(Descripcion) AS UBICACION
                        FROM Ubicacion AS UB
                        WHERE IdUbicacion IN (59,100,102,103,110,120,130,140,200,231,600,866)
                        ORDER BY Descripcion
                    """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        idUbicacion = str(row[0])
                        ubicacion = str(row[1])
                        datos = {'IdUbicacion': idUbicacion, 'Ubicacion': ubicacion}
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
def Inserta_Cambio_Domicilio(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            Usuario = str(json.loads(body)['Usuario'])
            Solicita = str(json.loads(body)['Solicita'])
            Tipo = str(json.loads(body)['Tipo'])
            Origen = str(json.loads(body)['Origen'])
            Destino = str(json.loads(body)['Destino'])
            Hora = str(json.loads(body)['Hora'])
            Observaciones = str(json.loads(body)['Observaciones'])
            values = [Origen,Solicita,Destino,Tipo,Hora,Observaciones,Usuario]
            with connections['S3A'].cursor() as cursor:
                sql = """
                        INSERT INTO PedidoFlete (IdPedidoFlete, IdPlanta, Solicitante, FechaPedido, HoraPedido, TipoDestino, IdPlantaDestino, TipoCarga, HoraRequerida, Obs, Estado, FechaRequerida, UserID, FechaAlta)
                        VALUES ((SELECT MAX(IdPedidoFlete) + 1 FROM PedidoFlete WHERE IdPedidoFlete LIKE '10%%'), %s, %s, GETDATE(), CONVERT(VARCHAR(8), GETDATE(), 108), 
                                    'U', %s, %s, %s, %s, 'P', GETDATE(), %s, GETDATE())
                        """
                cursor.execute(sql, values)
                cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                affected_rows = cursor.fetchone()[0]
            if affected_rows > 0:
                return JsonResponse({'Message': 'Success', 'Nota': 'El Pedido se realizó correctamente.'})
            else:
                return JsonResponse({'Message': 'Success', 'Nota': 'El Pedido no se pudo realizar, intente nuevamente.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FLETES REMITOS","CAMBIO DOMICILIO","APLICACION",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})    

@csrf_exempt
def Buscar_Pedidos_Flete(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            Usuario = str(json.loads(body)['Usuario'])
            Fecha = str(json.loads(body)['Fecha'])
            values = [Fecha,Usuario]
            with connections['S3A'].cursor() as cursor:
                sql = """
                        DECLARE @@Fecha DATE;
                        DECLARE @@User VARCHAR(10);
                        SET @@Fecha = %s;
                        SET @@User = %s;
                        SELECT CASE WHEN PF.Estado = 'P' THEN 'PENDIENTE' WHEN PF.Estado = 'PP' THEN 'POSTERGADO' WHEN PF.Estado = 'A' THEN 'ASIGNADO' WHEN PF.Estado = 'B' THEN 'BAJA' WHEN PF.Estado = 'D' THEN 'DESPACHADO' ELSE PF.Estado END AS ESTADO,
                                CASE WHEN PF.Estado = 'P' THEN '#ff8000' WHEN PF.Estado = 'PP' THEN '#F7DC6F' WHEN PF.Estado = 'A' THEN '#008f39' WHEN PF.Estado = 'B' THEN '#8A0000' ELSE '#6E6E6E' END AS COLOR_ESTADO,
                                CASE WHEN RTRIM(PF.TipoCarga) = 'VAC' THEN 'BINS VACÍOS' WHEN RTRIM(PF.TipoCarga) = 'EMB' THEN 'EMBALADO' WHEN RTRIM(PF.TipoCarga) = 'FBI' THEN 'FRUTA EN BINS'
                                WHEN RTRIM(PF.TipoCarga) = 'MAT' THEN 'MATERIALES' WHEN RTRIM(PF.TipoCarga) = 'VAR' THEN 'VARIOS' WHEN RTRIM(PF.TipoCarga) = 'RAU' THEN 'BINS FRUTA - CHACRA' ELSE RTRIM(PF.TipoCarga) END AS TIPO_CARGA,
                                RTRIM(UB.Descripcion) AS ORIGEN, COALESCE(RTRIM(UBS.Descripcion), '-') AS DESTINO, COALESCE(RTRIM(CONVERT(VARCHAR(5), PF.HoraRequerida, 108) + ' Hs.'), RTRIM(CONVERT(VARCHAR(5), PF.HoraPedido, 108) + ' Hs.')) + ' - ' +
                                CONVERT(VARCHAR(10), PF.FechaPedido, 103) AS HORA_REQUERIDA,
                                COALESCE(RTRIM(CH.Nombre), '-') AS NOMBRE_CHACRA, COALESCE(RTRIM(VR.Nombre), '-') AS NOMBRE_VARIEDAD,
                                COALESCE(RTRIM(TR.RazonSocial), '-') AS TRANSPORTE, COALESCE(RTRIM(CM.Nombre), '-') AS CAMION, COALESCE(RTRIM(PF.Chofer), '-') AS CHOFER,
                                COALESCE(RTRIM(CF.Telefono), '0') AS TELEFONO, COALESCE(RTRIM(PF.Obs), '') AS OBSERVACIONES, PF.IdPedidoFlete
                        FROM PedidoFlete AS PF LEFT JOIN
                                Ubicacion AS UB ON UB.IdUbicacion = PF.IdPlanta LEFT JOIN
                                Ubicacion AS UBS ON UBS.IdUbicacion = PF.IdPlantaDestino LEFT JOIN
                                Chacra AS CH ON CH.IdChacra = PF.IdChacra LEFT JOIN
                                Variedad AS VR ON VR.IdVariedad = PF.IdVariedad LEFT JOIN
                                Transportista AS TR ON TR.IdTransportista = PF.IdTransportista LEFT JOIN
                                Camion AS CM ON CM.IdCamion = PF.IdCamion LEFT JOIN
                                Chofer AS CF ON CONCAT(RTRIM(CF.Apellidos), ' ', RTRIM(CF.Nombres)) = RTRIM(PF.Chofer) AND PF.IdTransportista = CF.IdTransportista
                        WHERE PF.UserID = @@User
                                AND ((CONVERT(DATE, PF.FechaPedido) = @@Fecha) OR (@@Fecha = '1900-01-01' AND CONVERT(DATE, PF.FechaPedido) >= DATEADD(DAY, -5, CONVERT(DATE, GETDATE()))))
                                AND PF.Estado NOT IN ('C','B')
                                AND PF.IdPedidoFlete > (1000000)
                                AND PF.IdPedidoFlete < (2000000)
                        GROUP BY PF.Estado, PF.TipoCarga, UB.Descripcion, UBS.Descripcion, PF.HoraRequerida, PF.HoraPedido, PF.FechaPedido, CH.Nombre, VR.Nombre, TR.RazonSocial,
                                CM.Nombre, PF.Chofer, CF.Telefono, PF.Obs, IdPedidoFlete
                        ORDER BY PF.FechaPedido DESC
                        """
                cursor.execute(sql, values)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        Estado = str(row[0])
                        Hexadecimal = str(row[1])
                        Tipo = str(row[2])
                        Origen = str(row[3])
                        Destino = str(row[4])
                        Hora = str(row[5])
                        Chaccra = str(row[6])
                        Variedad = str(row[7])
                        Transporte = str(row[8])
                        Camion = str(row[9])
                        Chofer = str(row[10])
                        Telefono = str(row[11])
                        Obs = str(row[12])
                        ID = str(row[13])
                        datos = {'Estado': Estado, 'Color': Hexadecimal, 'Tipo':Tipo, 'Origen':Origen, 'Destino':Destino, 'Hora':Hora,
                            'Chacra':Chaccra, 'Variedad':Variedad, 'Transporte':Transporte, 'Camion':Camion, 'Chofer':Chofer, 'Telefono':Telefono, 'Obs':Obs, 'ID':ID}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FLETES REMITOS","BUSCAR PEDIDOS FLETE","APLICACION",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})    

@csrf_exempt
def ver_remitos_por_usuario(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            inicio = str(json.loads(body)['Inicio'])
            final = str(json.loads(body)['Final'])
            usuario = str(json.loads(body)['Usuario'])
            values = [usuario,inicio,final]
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """
                        DECLARE @@Inicio DATE;
                        DECLARE @@Final DATE;
                        DECLARE @@Usuario VARCHAR(20);

                        SET @@Usuario = %s;
                        SET @@Inicio = %s;
                        SET @@Final = %s;

                        SELECT        FORMAT(Datos_Remito_MovBins.NumeroRemito, '00000000') AS NRO_REMITO, RTRIM(S3A.dbo.Productor.RazonSocial) AS RAZON_SOCIAL, RTRIM(S3A.dbo.Productor.Nombre) AS NOMBRE, 
                                                RTRIM(S3A.dbo.Productor.Direccion) AS DIRECCION, Datos_Remito_MovBins.Renspa AS RENSPA, Datos_Remito_MovBins.UP, Datos_Remito_MovBins.Cantidad AS CANT_TOTAL, Datos_Remito_MovBins.IdAsignacion AS ID, 
                                                RTRIM(S3A.dbo.PedidoFlete.Solicitante) AS CAPATAZ, RTRIM(S3A.dbo.Especie.Nombre) AS ESPECIE, RTRIM(S3A.dbo.Variedad.Nombre) AS VARIEDAD, RTRIM(S3A.dbo.Chacra.Nombre) AS CHACRA, RTRIM(S3A.dbo.PedidoFlete.Chofer) AS CHOFER, RTRIM(S3A.dbo.Camion.Nombre) AS CAMION, 
                                                RTRIM(S3A.dbo.Camion.Patente) AS PATENTE, CONVERT(VARCHAR(10), Datos_Remito_MovBins.FechaAlta, 103) AS FECHA, CONVERT(VARCHAR(5), Datos_Remito_MovBins.FechaAlta, 108) + ' Hs.' AS HORA, Datos_Remito_MovBins.NumeroRemito, 
                                                CASE WHEN Datos_Remito_MovBins.Observaciones IS NULL THEN '' ELSE Datos_Remito_MovBins.Observaciones END AS OBS, S3A.dbo.Productor.IdProductor, Datos_Remito_MovBins.NombrePdf,
                                                Datos_Remito_MovBins.NumeroRemito, Datos_Remito_MovBins.IdProductor AS IDPR
                        FROM            S3A.dbo.Camion INNER JOIN
                                                S3A.dbo.Chacra INNER JOIN
                                                S3A.dbo.Variedad INNER JOIN
                                                S3A.dbo.Especie INNER JOIN
                                                S3A.dbo.Productor INNER JOIN
                                                Datos_Remito_MovBins INNER JOIN
                                                S3A.dbo.PedidoFlete ON Datos_Remito_MovBins.IdAsignacion = S3A.dbo.PedidoFlete.IdPedidoFlete ON S3A.dbo.Productor.IdProductor = S3A.dbo.PedidoFlete.IdProductor ON 
                                                S3A.dbo.Especie.IdEspecie = Datos_Remito_MovBins.IdEspecie ON S3A.dbo.Variedad.IdVariedad = Datos_Remito_MovBins.IdVariedad ON S3A.dbo.Chacra.IdChacra = S3A.dbo.PedidoFlete.IdChacra ON 
                                                S3A.dbo.Camion.IdCamion = S3A.dbo.PedidoFlete.IdCamion
                        WHERE (Datos_Remito_MovBins.USUARIO = @@Usuario)
                                AND (CONVERT(DATE, Datos_Remito_MovBins.FechaAlta) >= @@Inicio)
                                AND (CONVERT(DATE, Datos_Remito_MovBins.FechaAlta) <= @@Final)
                    """
                cursor.execute(sql,values)
                results = cursor.fetchall()
                if results:
                    listado = []
                    for i in results:
                        numero_remito = str(i[0])
                        razon_social = str(i[1])
                        señor = str(i[2])
                        direccion = str(i[3])
                        renspa = str(i[4])
                        up = str(i[5])
                        cant_total = str(i[6])
                        idPedido = str(i[7])
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
                        nombre_pdf = str(i[20])
                        rmt = str(i[21])
                        pr = str(i[22])

                        datos = {'Remito':numero_remito, 'RSocial':razon_social, 'Señor':señor, 'Direccion':direccion, 'Respa':renspa, 'Up':up, 'Cantidad':cant_total,
                                 'Capataz':capataz, 'Especie':especie, 'Variedad':variedad, 'Chacra':chacra, 'Chofer':chofer, 'Camion':camion, 'Patente':patente,
                                 'Fecha':fecha, 'Hora':hora, 'Contenido':busca_cantidad_bins(pr,rmt)}
                        listado.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': listado})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
                    error = str(e)
                    insertar_registro_error_sql("FLETES REMITOS","VER REPORTE DIARIO","usuario",error)
                    return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


def busca_cantidad_bins(IdProductor,NroRemito):
    values = [NroRemito,IdProductor]
    listado = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT        Contenido_Remito_MovBins.Cantidad AS CANTIDAD, RTRIM(S3A.dbo.Bins.Nombre) AS BIN, RTRIM(S3A.dbo.Marca.Nombre) AS MARCA				
                    FROM            S3A.dbo.Bins INNER JOIN
                                            S3A.dbo.Marca INNER JOIN
                                            Contenido_Remito_MovBins ON S3A.dbo.Marca.IdMarca = Contenido_Remito_MovBins.IdMarca ON S3A.dbo.Bins.IdBins = Contenido_Remito_MovBins.IdBins
                    WHERE        (Contenido_Remito_MovBins.NumeroRemito = %s) AND (Contenido_Remito_MovBins.IdProductor = %s) AND (Contenido_Remito_MovBins.Modificado IS NULL)
                """
            cursor.execute(sql, values)
            consulta = cursor.fetchall()
            if consulta:
                for i in consulta:
                    cantidad = str(i[0])
                    bins = str(i[1])
                    marca = str(i[2])
                    data = {'Cantidad':cantidad, 'Bins':bins, 'Marca':marca}
                    listado.append(data)
                return listado
            else:
                data = {'Cantidad':'-', 'Bins':'-', 'Marca':'-'}
                listado.append(data)
                return listado
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FLETES REMITO","BUSCA CONTENIDO REMITOS","usuario",error)
        data = {'Cantidad':'-', 'Bins':'-', 'Marca':'-'}
        listado.append(data)
        return listado













































