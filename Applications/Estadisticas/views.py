from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import *
from django.db import connections
from django.http import JsonResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, PatternFill, Border, Side, Font
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
import datetime
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
            values = ['2023-02-01', '2023-02-28', '1']
            try:
                data = []
                with connections['S3A'].cursor() as cursor:
                    sql = """
                            SET DATEFORMAT ymd;
                            DECLARE @P_Desde DATE;
                            DECLARE @P_Hasta DATE;
                            DECLARE @P_Especie INT;
                            SET @P_Desde = %s;
                            SET @P_Hasta = %s;
                            SET @P_Especie = %s;

                            SELECT  SUM(CONVERT(INT, Lote.CantBins)) AS CANTIDAD_BINS, CONVERT(VARCHAR(5), CONVERT(DATE, Fecha, 103), 103) AS FECHA,
                                    RTRIM(Especie.Nombre) AS ESPECIE
                            FROM Lote INNER JOIN
                                Especie ON Lote.IdEspecie = Especie.IdEspecie
                            WHERE (FORMAT(TRY_CONVERT(DATE, Lote.FechaAlta), 'yyyy-MM-dd') >= @P_Desde OR @P_Desde IS NULL OR @P_Desde = '')
                                AND (FORMAT(TRY_CONVERT(DATE, Lote.FechaAlta), 'yyyy-MM-dd') <= @P_Hasta OR @P_Hasta IS NULL OR @P_Hasta = '')
                                AND (Lote.IdEspecie IN (1,2))-- @P_Especie OR @P_Especie IS NULL OR @P_Especie = '')
                            GROUP BY
                                Lote.Fecha, Especie.Nombre;
                        """
                    cursor.execute(sql, values)
                    results = cursor.fetchall()
                    if results:
                        result_dict = {}
                        for cantidad, fecha, fruta in results:
                            if fruta not in result_dict:
                                result_dict[fruta] = []
                            result_dict[fruta].append({"Cantidad": str(cantidad), "Fecha": fecha})
                        json_data = json.dumps(result_dict)
                        #print(json_data)
                        return JsonResponse({'Message': 'Success', 'Datos': json_data})
                    else:
                        return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
            except Exception as e:
                print(e)
                insertar_registro_error_sql("ESTADISTICAS","BUSAQUEDA","request.user",str(e))
                    
            data = "TODO OK."
            return JsonResponse({'Message': 'Success', 'Nota': data})
        return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'}) 
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

def busqueda(id): ### FUNCION QUE INSERTA LAS HORAS EN EL S3A SOLO FUNCION (NO REQUIERE PERMISOS)
    values = [id]
    data = []
    try:
        with connections['S3A'].cursor() as cursor:
            sql = """
                    DECLARE @P_Desde DATE;
                    DECLARE @P_Hasta DATE;
                    DECLARE @P_Especie INT;
                    SET @P_Desde = '2023-02-01';
                    SET @P_Hasta = '2023-02-28';
                    SET @P_Especie = '1';

                    SELECT  SUM(CONVERT(INT, Lote.CantBins)) AS CANTIDAD_BINS, CONVERT(VARCHAR(5), Lote.Fecha, 108) AS FECHA,
                            RTRIM(Especie.Nombre) AS ESPECIE
                    FROM Lote INNER JOIN
                        Especie ON Lote.IdEspecie = Especie.IdEspecie
                    WHERE (TRY_CONVERT(DATE, Lote.Fecha) >= @P_Desde OR @P_Desde IS NULL OR @P_Desde = '')
                        AND (TRY_CONVERT(DATE, Lote.Fecha) <= @P_Hasta OR @P_Hasta IS NULL OR @P_Hasta = '')
                        AND (Lote.IdEspecie = @P_Especie OR @P_Especie IS NULL OR @P_Especie = '')
                    GROUP BY
                        Lote.Fecha, Especie.Nombre;

                """
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                print(results)
                for row in results:
                    cant = str(row[0])
                    fecha = str(row[1])
                    datos = {'Cantidad':cant, 'Fecha':fecha}
                    data.append(datos)
                print(data)
                return data
            else:
                return data
    except Exception as e:
        print(e)
        insertar_registro_error_sql("ESTADISTICAS","BUSAQUEDA","request.user",str(e))
        return data 




































