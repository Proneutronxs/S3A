from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import *
from S3A.conexionessql import *
from django.db import connections
from django.http import JsonResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, PatternFill, Border, Side, Font
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
import datetime
import calendar
import json


# Create your views here.

@login_required
def Estadisticas(request):
    return render (request, 'Estadisticas/estadisticas.html')

@login_required
def Cosecha(request):
    return render (request, 'Estadisticas/Cosecha/eCosecha.html')






@login_required
@csrf_exempt
def estadisticaCosecha(request):
    if request.method == 'POST': 
        user_has_permission = request.user.has_perm('Estadisticas.puede_ver') 
        if user_has_permission: 
            usuario = str(request.user)
            desde = str(request.POST.get('fechaBusquedaDesde'))
            hasta = str(request.POST.get('fechaBusquedaHasta'))
            especie = str(request.POST.get('ComboxEspecie'))
            variedad = str(request.POST.get('ComboxVariedad'))
            chacra = str(request.POST.get('ComboxChacra'))
            results = busqueda(desde,hasta,especie,variedad,chacra)
            if results:
                result_dict = {}
                for cantidad, fecha, fruta in results:
                    if fruta not in result_dict:
                        result_dict[fruta] = []
                    result_dict[fruta].append({"Cantidad": str(cantidad), "Fecha": fecha})
                json_data = json.dumps(result_dict)
                return JsonResponse({'Message': 'Success', 'Datos': json_data})
            else:
                return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'}) 
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

def busqueda(desde,hasta,especie,variedad,chacra):
    data = []
    lista_fechas = obtener_fechas_entre(desde,hasta)
    nombreEspecie = NombreEspecie(especie)
    for fecha in lista_fechas:
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """
                        SET DATEFORMAT ymd;
                        DECLARE @P_Fecha DATE;
                        DECLARE @P_Especie INT;
                        DECLARE @P_Variedad INT;
                        DECLARE @P_Chacra INT;
                        SET @P_Fecha = %s;
                        SET @P_Especie = %s;
                        SET @P_Variedad = %s;
                        SET @P_Chacra = %s;

                        SELECT  SUM(CONVERT(INT, Lote.CantBins)) AS CANTIDAD_BINS, CONVERT(VARCHAR(5), CONVERT(DATE, Fecha, 103), 103) AS FECHA,
                                RTRIM(Especie.Nombre) AS ESPECIE
                        FROM Lote INNER JOIN
                                Especie ON Lote.IdEspecie = Especie.IdEspecie INNER JOIN
                                Variedad ON Lote.IdVariedad = Variedad.IdVariedad INNER JOIN
                                Chacra ON Lote.IdChacra = Chacra.IdChacra
                        WHERE (FORMAT(TRY_CONVERT(DATE, Lote.FechaAlta), 'yyyy-MM-dd') = @P_Fecha OR @P_Fecha IS NULL OR @P_Fecha = '')
                                AND ((Lote.IdEspecie IN (@P_Especie)) OR @P_Especie IS NULL OR @P_Especie = '')
                                AND ((Lote.IdVariedad IN (@P_Variedad)) OR @P_Variedad IS NULL OR @P_Variedad = '')
                                AND ((Lote.IdChacra IN (@P_Chacra)) OR @P_Chacra IS NULL OR @P_Chacra = '')
                        GROUP BY
                                Lote.Fecha, Especie.Nombre;

                    """
                cursor.execute(sql,[fecha,especie,variedad,chacra])
                results = cursor.fetchone()
                if results:
                    data.append(results)
                else:
                    fecha = formatear_fecha_a_dia_mes(fecha)
                    dato = (0,fecha,nombreEspecie)
                    data.append(dato)
        except Exception as e:
            insertar_registro_error_sql("ESTADISTICAS","BUSQUEDA","request.user",str(e))
    return data 




































