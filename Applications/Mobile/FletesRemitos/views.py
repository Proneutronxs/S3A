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
                sql3 = "SELECT IdEspecie, RTRIM(Nombre) FROM Especie ORDER BY nombre"
                cursor.execute(sql3)
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

                ## CHACRA
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