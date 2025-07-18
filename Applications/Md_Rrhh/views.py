from openpyxl.styles import PatternFill, Font, Border, Side
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import obtenerHorasArchivo, registroRealizado
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from openpyxl.drawing.image import Image
from django.views.static import serve
from openpyxl.styles import Alignment
from django.shortcuts import render
from django.db import connections
from datetime import datetime
from io import BytesIO
import pandas as pd
import json
import os


# Create your views here.

@login_required
def Md_Rrhh(request):
    user_has_permission = request.user.has_perm('Md_Rrhh.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Rrhh/index.html')
    return render (request, 'Md_Rrhh/404.html')


@login_required
def Listado_Sipreta(request):
    user_has_permission = request.user.has_perm('Md_Rrhh.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Rrhh/Chacras/listadoSipreta.html')
    return render (request, 'Md_Rrhh/404.html')

@login_required
def Archivo_Isis(request):
    user_has_permission = request.user.has_perm('Md_Rrhh.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Rrhh/HorasExtras/archivo_isis.html')
    return render (request, 'Md_Rrhh/404.html')







def listaCentrosChacras(request):
    if request.method == 'GET':
        try:
            with connections['ISISPayroll'].cursor() as cursor:
                sql = """
                        SELECT Regis_Cco AS ID, UPPER(CONVERT(VARCHAR(45),(AbrevCtroCosto + ' - ' + DescrCtroCosto))) AS CENTRO
                        FROM CentrosCostos
                        WHERE AbrevCtroCosto LIKE ('C%')
                        ORDER BY CENTRO
                    """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    lista_tarea = [{'Codigo': '', 'Descripcion': 'TODO'},{'Codigo': 'P', 'Descripcion': 'PODA'},{'Codigo': 'R', 'Descripcion': 'RALEO'}]
                    lista_data = [{'Codigo': '', 'Descripcion': 'TODOS - (NO ROMMIK)'},{'Codigo': '18', 'Descripcion': 'RMK - ROMMIK'}]
                    for row in consulta:
                        codigo = str(row[0])
                        descripcion = str(row[1])
                        datos = {'Codigo': codigo, 'Descripcion': descripcion}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data, 'Tareas':lista_tarea })
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def descarga_archivo_excel(request, filename):
    nombre = filename
    filename = 'Applications/Md_Rrhh/Archivos/Excel/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    else:
        raise 
    
@csrf_exempt    
def data_listado_horas_extras_isis(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Md_Rrhh.puede_ver')
        if user_has_permission:
            try:
                inicio = str(request.POST.get('Incio'))
                final = str(request.POST.get('Final'))
                archivo = str(request.POST.get('Archivo'))
                values = [inicio,final]
                lista_data = jsonArchivoIsis(values)
                if lista_data:
                    if archivo == "N":
                        return JsonResponse({'Message': 'Success', 'Datos': lista_data})  
                    # else:
                    #     excel_response = general_excel_horas_extras(lista_data)            
                    #     return excel_response 
                else:
                    data = 'No se encontraron datos.'
                    return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def jsonArchivoIsis(values):
    lista_data = []
    try:
        with connections['S3A'].cursor() as cursor:
            cursor.execute('EXEC MDR_LISTADO_ARCHIVO_ISIS %s,%s', values)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    lista_data.append({
                        'Legajo':str(row[0]), 
                        'Horas50':str(row[1]), 
                        'Cod50':str(row[2]), 
                        'Horas100':str(row[3]), 
                        'Cod100':str(row[4]), 
                        'HorasS':str(row[5]), 
                        'CodS':str(row[6]), 
                        'Ac50':str(row[7]), 
                        'Ac100':str(row[8]), 
                        'Sindicato':str(row[9]), 
                        'Nombre':str(row[10]), 
                        'Centro':str(row[11])
                    })
                return lista_data 
            else:
                return lista_data
    except Exception as e:
        return lista_data


@csrf_exempt    
def data_listado_planilla_labores(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Md_Rrhh.puede_ver')
        if user_has_permission:
            try:
                inicio = str(request.POST.get('Inicio'))
                final = str(request.POST.get('Final'))
                centro = str(request.POST.get('IdCentro'))
                labor = str(request.POST.get('IdLabor'))
                archivo = str(request.POST.get('Tipo'))
                filtros = request.POST.get('Filtros')
                filtros_dict = json.loads(filtros)
                values = [inicio,final,centro,labor]
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """ 
                        DECLARE @Inicio DATE;
                        DECLARE @Final DATE;
                        DECLARE @IdCentro VARCHAR(10);
                        DECLARE @Labor VARCHAR(10);

                        SET @Inicio = %s;
                        SET @Final = %s;
                        SET @IdCentro = %s;
                        SET @Labor = %s;


                        WITH Datos AS (
                        SELECT        ST.FECHA,
                        CASE WHEN ST.USUARIO = 'JCASTILLO' THEN
                                                    (SELECT        CONVERT(VARCHAR(30), (ApellidoEmple + ' ' + NombresEmple))
                                                    FROM            Rommik_isispayroll.dbo.Empleados
                                                    WHERE        CodEmpleado = ST.ID_LEGAJO) ELSE
                                                    (SELECT        CONVERT(VARCHAR(30), (ApellidoEmple + ' ' + NombresEmple))
                                                    FROM            TresAses_ISISPayroll.dbo.Empleados
                                                    WHERE        CodEmpleado = ST.ID_LEGAJO) END AS NOMBRES, CASE WHEN ST.USUARIO = 'JCASTILLO' THEN
                                                    (SELECT        CC.AbrevCtroCosto
                                                    FROM            Rommik_isispayroll.dbo.Empleados AS EMP INNER JOIN
                                                                                Rommik_isispayroll.dbo.CentrosCostos AS CC ON CC.Regis_CCo = EMP.Regis_CCo
                                                    WHERE        EMP.CodEmpleado = ST.ID_LEGAJO) ELSE
                                                    (SELECT        CC.AbrevCtroCosto
                                                    FROM            TresAses_ISISPayroll.dbo.Empleados AS EMP INNER JOIN
                                                                                TresAses_ISISPayroll.dbo.CentrosCostos AS CC ON CC.Regis_CCo = EMP.Regis_CCo
                                                    WHERE        EMP.CodEmpleado = ST.ID_LEGAJO) END AS ABREV_CENTRO, ST.ID_LEGAJO AS LEGAJO, CASE WHEN ST.USUARIO = 'JCASTILLO' THEN
                                                    (SELECT        CC.Regis_CCo
                                                    FROM            Rommik_isispayroll.dbo.Empleados AS EMP INNER JOIN
                                                                                Rommik_isispayroll.dbo.CentrosCostos AS CC ON CC.Regis_CCo = EMP.Regis_CCo
                                                    WHERE        EMP.CodEmpleado = ST.ID_LEGAJO) ELSE
                                                    (SELECT        CC.Regis_CCo
                                                    FROM            TresAses_ISISPayroll.dbo.Empleados AS EMP INNER JOIN
                                                                                TresAses_ISISPayroll.dbo.CentrosCostos AS CC ON CC.Regis_CCo = EMP.Regis_CCo
                                                    WHERE        EMP.CodEmpleado = ST.ID_LEGAJO) END AS REGIS_CCO, SL.NOMBRE_LABOR AS LABOR, ST.VALOR AS IMPORTE, 
                                                    CASE WHEN P_1.DIAS_TRABAJADOS IS NULL 
                                                THEN 0 ELSE P_1.DIAS_TRABAJADOS END AS DIAS_TRABAJADOS, SPA_QR.ID_FILA,
                                                CASE
                                                    WHEN SL.ALIAS_LABOR = 'P' THEN '51'
                                                    WHEN SL.ALIAS_LABOR = 'R' THEN '52'
                                                    WHEN SL.ALIAS_LABOR = 'C' THEN '53'
                                                END  AS CODIGO_ASISTENCIA
                        FROM            SPA_QR INNER JOIN
                                                SPA_CUADRO ON SPA_QR.ID_CUADRO = SPA_CUADRO.ID_CUADRO RIGHT OUTER JOIN
                                                SPA_TAREA AS ST INNER JOIN
                                                SPA_LABOR AS SL ON SL.ID_LABOR = ST.ID_LABOR ON SPA_QR.ID_QR = ST.ID_QR_FILA LEFT OUTER JOIN
                                                    (SELECT        IdLegajo, SUM(CASE WHEN P.M = 'P' THEN 0.5 ELSE 0 END + CASE WHEN P. T = 'P' THEN 0.5 ELSE 0 END) AS DIAS_TRABAJADOS
                                                    FROM            S3A.dbo.RH_Presentismo AS P
                                                    WHERE        (CONVERT(DATE, Fecha) >= @Inicio) AND (CONVERT(DATE, Fecha) <= @Final)
                                                    GROUP BY IdLegajo) AS P_1 ON P_1.IdLegajo = ST.ID_LEGAJO
                        )
                        SELECT NOMBRES, ABREV_CENTRO, LEGAJO, REGIS_CCO, LABOR, IMPORTE, DIAS_TRABAJADOS, ID_FILA, CODIGO_ASISTENCIA
                        FROM Datos 
                        WHERE 
                            CONVERT(DATE, FECHA) >= @Inicio 
                            AND CONVERT(DATE, FECHA) <= @Final 
                            AND (REGIS_CCO = @IdCentro OR (@IdCentro = '' AND REGIS_CCO NOT IN ('18','20')))
                            AND (LABOR = @Labor OR @Labor = '')
                        ORDER BY NOMBRES
                     """
                    cursor.execute(sql,values)  ##INSERTAR VALUES
                    results = cursor.fetchall()
                    listado_json = {}

                    if results:
                        for row in results:
                            legajo = str(row[2])
                            tarea = str(row[4])

                            if legajo not in listado_json:
                                listado_json[legajo] = {
                                    "LEGAJO": legajo,
                                    "NOMBRES": str(row[0]),
                                    "CENTRO": str(row[1]),
                                    "REGIS": str(row[3]),
                                    "TAREA": tarea,
                                    "DETALLES": [
                                        {
                                            "ITEM": str(row[8]), 
                                            "CANTIDAD": str(row[6]),
                                            "IMPORTE": "",
                                            "SUMA_IMPORTE": ""
                                        }
                                    ]
                                }

                            importe = float(row[5])

                            # Definir rangos de ítems según la tarea
                            start_item = 200 if tarea == "PODA" else 300
                            max_item = 215 if tarea == "PODA" else 315

                            detalles = listado_json[legajo]["DETALLES"]

                            # Buscar si ya existe un detalle con el mismo importe (a partir del segundo elemento)
                            found = False
                            for detalle in detalles[1:]:
                                if detalle["IMPORTE"] == str(importe):
                                    detalle["CANTIDAD"] = str(int(detalle["CANTIDAD"]) + 1)
                                    detalle["SUMA_IMPORTE"] = str(float(detalle["SUMA_IMPORTE"]) + importe)
                                    found = True
                                    break

                            # Si no existe, agregar nuevo ítem si no se supera el límite
                            if not found:
                                current_count = len(detalles) - 1  # excluye el ítem de asistencia
                                if start_item + current_count <= max_item:
                                    new_item = str(start_item + current_count)
                                    detalles.append({
                                        "ITEM": new_item,
                                        "CANTIDAD": "1",
                                        "IMPORTE": str(importe),
                                        "SUMA_IMPORTE": str(importe)
                                    })
                                else:
                                    #print(f"¡Límite de ítems alcanzado para LEGAJO {legajo} y tarea {tarea}!")
                                    pass


                        listado_json = {k: [v] for k, v in listado_json.items()}

                        if archivo == 'TT':
                            #listado_json = dict(sorted(listado_json.items(), key=lambda x: x[1]['NOMBRES']))
                            return JsonResponse({'Message': 'Success', 'Datos': listado_json})
                        else:
                            nombre_excel = crear_excel_rrhh(archivo,listado_json,filtros_dict)
                            return JsonResponse({'Message': 'Success', 'Datos': listado_json, 'Archivo':nombre_excel})
                    else:
                        data = 'No se encontraron datos.'
                        return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


def crear_excel_rrhh(tipo, json_data, filtros):
    if tipo == 'RP':
        try:
            lista_filas = []
            for legajo, registros in json_data.items():
                for reg in registros:
                    for detalle in reg['DETALLES']:
                        fila = {
                            'LEGAJO': str(reg['LEGAJO']),
                            'APELLIDO Y NOMBRE': str(reg['NOMBRES']),
                            'CENTRO': str(reg['CENTRO']),
                            'TAREA': str(reg['TAREA']),
                            'CODIGO': str(detalle['ITEM']),
                            'CANTIDAD': formatear_numero(detalle['CANTIDAD']),
                            'IMPORTE': formatear_importe(str(detalle['IMPORTE'])),
                            'SUMA TOTAL': formatear_importe(str(detalle['SUMA_IMPORTE']))
                        }
                        lista_filas.append(fila)
            lista_filas = sorted(lista_filas, key=lambda x: x['APELLIDO Y NOMBRE'])
            df = pd.DataFrame(lista_filas)
            output = BytesIO()
            columnas = ['LEGAJO', 'APELLIDO Y NOMBRE', 'CENTRO', 'TAREA', 'CODIGO', 'CANTIDAD', 'IMPORTE', 'SUMA TOTAL']
            df = df[columnas]
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, startrow=9, sheet_name='DETALLE IMPORTES')
                ws = writer.sheets['DETALLE IMPORTES']

                logo = Image('static/3A/images/TA.png')  
                logo.width = 80
                logo.height = 50
                ws.add_image(logo, 'J2')
                ws['E5'] = 'DETALLE DE IMPORTES'
                ws['E5'].font = Font(size=14, bold=True)
                ws['E5'].alignment = Alignment(horizontal='center', vertical='center')

                fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                ws['E2'] = fecha_actual
                ws['E2'].alignment = Alignment(horizontal='right', vertical='center')

                ws['A2'] = 'DESDE:'
                ws['B2'] = filtros['DESDE']
                ws['A2'].font = Font(size=12, bold=True)

                ws['A3'] = 'HASTA:'
                ws['B3'] = filtros['HASTA']
                ws['A3'].font = Font(size=12, bold=True)

                ws['A4'] = 'CENTRO:'
                ws['B4'] = filtros['CENTRO']
                ws['A4'].font = Font(size=12, bold=True)

                ws['A5'] = 'TAREA:'
                ws['B5'] = filtros['LABOR']
                ws['A5'].font = Font(size=12, bold=True)
                
                header_fill = PatternFill(start_color="44546a", end_color="44546a", fill_type="solid")
                header_font = Font(color="FFFFFF")
                header_alignment = Alignment(horizontal='center', vertical='center')

                for cell in ws[10]:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = header_alignment
                border_style = Border(
                    left=Side(style='thin'),
                    right=Side(style='thin'),
                    top=Side(style='thin'),
                    bottom=Side(style='thin')
                )
                for row in ws.iter_rows(min_row=11, min_col=1, max_row=ws.max_row, max_col=ws.max_column):
                    for cell in row:
                        cell.border = border_style

                for col in ws.columns:
                    max_length = 0
                    column = col[0].column_letter
                    for cell in col[10:]:
                        try:
                            if cell.value and len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = max_length + 8
                    ws.column_dimensions[column].width = adjusted_width

                    columnas = ['E', 'F', 'G', 'H']
                    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
                        for cell in row:
                            if cell.column_letter in columnas:
                                cell.alignment = Alignment(horizontal='right')

                    columnas = ['A', 'C', 'D']
                    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
                        for cell in row:
                            if cell.column_letter in columnas:
                                cell.alignment = Alignment(horizontal='center')

            output.seek(0)
            nombre_excel = f'DETALLE_IMPORTES_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.xlsx'
            with open('Applications/Md_Rrhh/Archivos/Excel/'+nombre_excel, 'wb') as f:
                f.write(output.getvalue())
            return nombre_excel
        except Exception as e:
            #print(f"Error: {e}")
            return 'e'
    
    else:
        try:
            lista_filas = []
            for legajo, registros in json_data.items():
                for reg in registros:
                    for detalle in reg['DETALLES']:
                        fila = {
                            'LEGAJO': str(reg['LEGAJO']),
                            'CODIGO': str(detalle['ITEM']),
                            'CC': "1",
                            'CD': "0",
                            'CE': "1",
                            'CF': "1",
                            'CG': "1",
                            'CANTIDAD': f"{float(detalle['CANTIDAD']):.2f}".replace('.', ','),
                            'CI': "1",
                            'CJ': "1",
                            'CK': "1",
                            'IMPORTE': f"{float(detalle['IMPORTE'] or 0):.2f}".replace('.', ',')
                        }
                        lista_filas.append(fila)

            df = pd.DataFrame(lista_filas)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False, startrow=0, sheet_name='ARCHIVO ISIS')
                ws = writer.sheets['ARCHIVO ISIS']            
                columnas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'L', 'I', 'J', 'K']
                for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
                    for cell in row:
                        if cell.column_letter in columnas:
                            cell.alignment = Alignment(horizontal='right')

            output.seek(0)
            nombre_excel = f'ARCHIVO_ISIS_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.xlsx'
            with open('Applications/Md_Rrhh/Archivos/Excel/'+nombre_excel, 'wb') as f:
                f.write(output.getvalue())
            return nombre_excel
        except Exception as e:
            #print(f"Error: {e}")
            return 'e'

def formatear_numero(numero):
    if not numero:
        return ''
    return f"{float(numero):.2f}".replace('.', ',')

def formatear_importe(numero):
    if not numero:
        return ''
    return f"$ {float(numero):,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')

































































