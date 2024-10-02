
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import json


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