from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.http import JsonResponse
from S3A.funcionesGenerales import *

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
                cantValues = ','.join(['?'] * len(listado))
                sql3 = (f"SELECT IdEspecie, RTRIM(Nombre) FROM Especie WHERE IdEspecie IN ({cantValues}) ORDER BY IdEspecie")
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
                datos = consulta[0]
                listado_id = datos.split(',')
                return listado_id
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("FletesRemitos","traeIdEspecies","Aplicacion",error)
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()


#### CREACION DE REMITOS DATOS A MOSTRAR ASIGNACIONES

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
                if listadoData_Asignaciones and listadoData_UP:
                    return JsonResponse({'Message': 'Success', 'DataAsignaciones': listadoData_Asignaciones, 'DataUp': listadoData_UP})
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
                listadoUP_Renspa
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("traeFletesRemitos","traeUPS","Aplicacion",error)
        return listadoUP_Renspa
    finally:
        cursor.close()
        connections['S3A'].close()