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
import os

# Create your views here.


@login_required
def Md_Chacras(request):
    user_has_permission = request.user.has_perm('Md_Chacras.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Chacras/index.html')
    return render (request, 'Md_Chacras/404.html')

@login_required
def Presupuesto(request):
    user_has_permission = request.user.has_perm('Md_Chacras.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Chacras/Sipreta/presupuesto.html')
    return render (request, 'Md_Chacras/404.html')

@login_required
def Horas_Extras(request):
    user_has_permission = request.user.has_perm('Md_Chacras.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Chacras/Mobile/horas_extras.html')
    return render (request, 'Md_Chacras/404.html')


def descarga_archivo_excel(request, filename):
    nombre = filename
    filename = 'Applications/Md_Chacras/Archivos/Excel/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    else:
        raise Http404

@csrf_exempt    
def data_listado_horas_extras(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            inicio = str(request.POST.get('Incio'))
            final = str(request.POST.get('Final'))
            estado = str(request.POST.get('Estado'))
            tipo = str(request.POST.get('Tipo'))
            archivo = str(request.POST.get('Archivo'))
            values = [inicio,final,estado,tipo]
            lista_data = jsonHorasExtras(values)
            if lista_data:
                if archivo == "N":
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})  
                else:
                    excel_response = general_excel_horas_extras(lista_data)            
                    return excel_response 
            else:
                data = 'No se encontraron datos.'
                return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def jsonHorasExtras(values):
    lista_data = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            cursor.execute('EXEC MDC_HORAS_EXTRAS %s,%s,%s,%s', values)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    lista_data.append({
                        'IDhep':str(row[0]), 
                        'Tipo':str(row[1]), 
                        'Legajo':str(row[2]), 
                        'Nombre':str(row[3]), 
                        'Centro':str(row[4]), 
                        'Desde':str(row[5]), 
                        'Hasta':str(row[6]), 
                        'Motivo':str(row[7]), 
                        'Descripcion':str(row[8]), 
                        'Cantidad':str(row[9]), 
                        'Solicita':str(row[10]), 
                        'Importe':str(row[11]), 
                        'Estado':str(row[12])
                    })
                return lista_data 
            else:
                return lista_data
    except Exception as e:
        return lista_data

def general_excel_horas_extras(lista_data):
    try:
        df = pd.DataFrame(lista_data)
        df.fillna('', inplace=True)
        output = BytesIO()
        columns1 = ['ID HORA', 'TIPO HORA', 'LEGAJO', 'APELLIDO Y NOMBRE', 'CENTRO DE COSTO', 'DESDE', 'HASTA', 'MOTIVO', 'DESCRIPCIÓN', 'CANTIDAD', 'SOLICITA', 'IMPORTE A', 'ESTADO']
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, startrow=5, sheet_name='LISTADO HORAS EXTRAS',header=columns1)
            worksheet = writer.sheets['LISTADO HORAS EXTRAS']
            logo = Image('static/3A/images/TA.png')
            logo.width = 100
            logo.height = 60
            worksheet.add_image(logo, 'G2')
            worksheet['C4'] = 'LISTADO HORAS EXTRAS'
            worksheet['C4'].font = Font(size=14, bold=True)
            worksheet['C4'].alignment = Alignment(horizontal='center', vertical='center')
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            worksheet['E2'] = fecha_actual
            worksheet['E2'].alignment = Alignment(horizontal='right', vertical='center')
            header_fill = PatternFill(start_color="44546a", end_color="44546a", fill_type="solid")
            header_font = Font(color="FFFFFF")
            header_alignment = Alignment(horizontal='center', vertical='center')

            for cell in worksheet[6]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_alignment
                
            border_style = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            for row in worksheet.iter_rows(min_row=7, min_col=1, max_row=worksheet.max_row, max_col=worksheet.max_column):
                for cell in row:
                    cell.border = border_style

            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column].width = adjusted_width
                
        output.seek(0)
        nombre_excel = f'Listado_horas_extras_{obtenerHorasArchivo()}.xlsx'
        with open('Applications/Md_Chacras/Archivos/Excel/'+ nombre_excel, 'wb') as f:
            f.write(output.getvalue())

        return JsonResponse({'Message': 'Success', 'Archivo': nombre_excel}) 
    except Exception as e:
        data = str(e)
        return JsonResponse({'Message': 'Error', 'Nota': data})

def convertir_a_numerico_stock_ventas(df):
    try:
        df['Valor1'] = pd.to_numeric(df['Valor1'], errors='coerce')
        df['Valor2'] = pd.to_numeric(df['Valor2'], errors='coerce')
        df['Valor3'] = pd.to_numeric(df['Valor3'], errors='coerce')
        df['Valor4'] = pd.to_numeric(df['Valor4'], errors='coerce')
        df['Valor5'] = pd.to_numeric(df['Valor5'], errors='coerce')
        df['Valor6'] = pd.to_numeric(df['Valor6'], errors='coerce')
        df['Valor7'] = pd.to_numeric(df['Valor7'], errors='coerce')
        df['Valor8'] = pd.to_numeric(df['Valor8'], errors='coerce')
        df['Valor9'] = pd.to_numeric(df['Valor9'], errors='coerce')
        df['Valor10'] = pd.to_numeric(df['Valor10'], errors='coerce')
        df['Valor11'] = pd.to_numeric(df['Valor11'], errors='coerce')
        df['Valor12'] = pd.to_numeric(df['Valor12'], errors='coerce')
        df['Valor13'] = pd.to_numeric(df['Valor13'], errors='coerce')
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
        return df
    except Exception as e:
        return None 

@csrf_exempt    
def inserta_elimina_horas_extras(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            with connections['S3A'].cursor() as cursor:
                metodo = request.POST.get('Metodo', '')
                importe = request.POST.get('Importe', '')
                cantidad = int(request.POST.get('IDHEP', 0))
                usuario = str(request.user).upper()
                index = 0
                for i in range(cantidad):
                    id_key = f'IDhep{i}'
                    id_value = request.POST.get(id_key)
                    values = [metodo, importe, id_value, usuario]
                    cursor.execute('EXEC MDC_HORAS_EXTRAS_INSERTA_ELIMINA %s, %s, %s, %s', values)
                    index = index + 1
            if index == cantidad:
                return JsonResponse({'Message': 'Success', 'Nota': 'La petición se realizó correctamente.'}) 
            else: 
                return JsonResponse({'Message': 'Error', 'Nota': 'Uno o más items no se pudieron guardad o eliminar.'})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


#SIPRETA → Sistema de Información para Poda y Raleo en Establecimientos de Tres Ases

def listado_combox_productor(request):
    if request.method == 'GET':
        try:
            lista_data = []
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        EXEC LISTADO_PRODUCTORES_HABILITADOS
                    """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        lista_data.append({
                            "IdProductor":str(row[0]),
                            "Descripcion":str(row[1])
                        })
            if lista_data:
                return JsonResponse({'Message': 'Success', 'Datos': lista_data})
            else:
                data = "No se encontraron Datos."
                return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def listado_combox_chacras_x_productor(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            idProductor = str(request.POST.get('IdProductor'))
            values = [idProductor]
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        EXEC LISTADO_CHACRAS_X_PRODUCTOR %s
                    """
                cursor.execute(sql, values)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = [{'IdChacra': '', 'Descripcion':'TODOS'}]
                    for row in consulta:
                        lista_data.append({
                            "IdChacra":str(row[0]),
                            "Descripcion":str(row[1])
                        })
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    data = "No se encontraron Datos."
                    return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
@csrf_exempt
def listado_chacras_x_filas(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            idProductor = str(request.POST.get('IdProductor'))
            idChacra = str(request.POST.get('IdChacra'))
            tipo = str(request.POST.get('Tipo'))
            values = [idProductor,idChacra]
            listado_data = jsonListadoChacrasFilas(values)
            if tipo == 'TT':
                return JsonResponse({'Message': 'Success', 'Datos': listado_data})

        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


def jsonListadoChacrasFilas(values):
    lista_data = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            cursor.execute('EXEC LISTADO_FILAS_POR_CHACRA %s,%s', values)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    lista_data.append({
                        "IdProductor":str(row[0]),
                        "Productor":str(row[1]),
                        "IdChacra":str(row[2]),
                        "Chacra":str(row[3]),
                        "Cuadro":str(row[4]),
                        "Fila":str(row[5]),
                        "IdEspecie":str(row[6]),
                        "Especie":str(row[7]),
                        "IdVariedad":str(row[8]),
                        "Variedad":str(row[9]),
                        "AñoPlantacion":str(row[10]),
                        "NroPlantas":str(row[11]),
                        "DFilas":str(row[12]),
                        "DPlantas":str(row[13]),
                        "SupPlanta":str(row[14]),
                        "Presupuesto":str(row[15])
                    })
                return lista_data 
            else:
                return lista_data
    except Exception as e:
        return lista_data






















































