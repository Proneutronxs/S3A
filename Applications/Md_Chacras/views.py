
from S3A.funcionesGenerales import obtenerHorasArchivo, registroRealizado
from openpyxl.styles import PatternFill, Font, Border, Side
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from openpyxl.styles import Protection
from django.views.static import serve
from openpyxl.styles import Alignment
from django.shortcuts import render
from django.db import connections
from openpyxl import load_workbook
from openpyxl import Workbook
from datetime import datetime
from io import BytesIO
import pandas as pd
import xlrd
import json
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
def listado_labores(request):
    user_has_permission = request.user.has_perm('Md_Chacras.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Chacras/Sipreta/listadoLabores.html')
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
                    lista_data = [] #{'IdChacra': '', 'Descripcion':'TODOS'}
                    for row in consulta:
                        lista_data.append({
                            "IdChacra":str(row[0]),
                            "Descripcion":str(row[1])
                        })
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data, 'Chacras':lista_data})
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
            else:
                nombre_excel = crear_excel_presupuesto(listado_data,idChacra,idProductor)
                return JsonResponse({'Message': 'Success', 'Excel': nombre_excel})
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
                        "Presupuesto":str(row[15]),
                        "QRFila":str(row[16]),
                        "IdCuadro":str(row[17])
                    })
                return lista_data 
            else:
                return lista_data
    except Exception as e:
        return lista_data
    
def crear_excel_presupuesto(lista_data, chacra, productor):
    try:
        wb = Workbook()
        ws = wb.active

        columnas = [
            "PRODUCTOR", "ID CHACRA", "CHACRA", "ID CUADRO", "CUADRO", "FILA",
            "CANT. PLANTAS", "ID VARIEDAD", "VARIEDAD", "AÑO", "P. PODA", "P. RALEO"
        ]
        ws.append(columnas)
        
        for row in lista_data:
            fila = [
                row["Productor"],
                row["IdChacra"],
                row["Chacra"],
                row["IdCuadro"],
                row["Cuadro"],
                row["Fila"],
                row["NroPlantas"],
                row["IdVariedad"],
                row["Variedad"],
                "",  # AÑO
                "",  # P. PODA
                ""   # P. RALEO
            ]
            ws.append(fila)

        for col in ws.columns:
            max_length = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = (max_length + 5)
            ws.column_dimensions[col_letter].width = adjusted_width

        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=12):
            for cell in row:
                if cell.col_idx in [10, 11, 12]:
                    cell.protection = Protection(locked=False)
                else:
                    cell.protection = Protection(locked=True)
        
        ws.protection.sheet = True
        nombre = f'Listado_Chacra_{chacra}_{productor}.xlsx'
        wb.save('Applications/Md_Chacras/Archivos/Excel/' + nombre)
        return nombre
    except Exception as e:
        return str(e)

@csrf_exempt 
def recibir_archivo_excel(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            archivo_excel = request.FILES['archivoExcel']
            nombre_archivo = archivo_excel.name
            extension = os.path.splitext(nombre_archivo)[1].lower()
            lista_data = []

            if extension == '.xlsx':
                wb = load_workbook(archivo_excel)
                ws = wb.worksheets[0]  
                for row in ws.iter_rows(min_row=2, values_only=True):
                    validar_fila_chacras(row)
                    lista_data.append(row)

            elif extension == '.xls':
                libro = xlrd.open_workbook(file_contents=archivo_excel.read())
                hoja = libro.sheet_by_index(0)
                for i in range(1, hoja.nrows): 
                    row = [None if cell == '' else cell for cell in hoja.row_values(i)]
                    row = tuple(row)
                    validar_fila_chacras(row)
                    lista_data.append(row)
            else:
                raise ValueError("Formato de archivo no soportado. Solo se aceptan .xls o .xlsx")
        
            if lista_data:
                json_resultado = json_chacras(lista_data)
                return JsonResponse({'Message': 'Success', 'Datos': json_resultado})
            else:
                raise ValueError("No se pudieron cargar los datos.")
        except Exception as e:
            return JsonResponse({'Message': 'Error', 'Nota': str(e)})

    return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt 
def recibir_archivo_excel_presupuesto(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            archivo_excel = request.FILES['archivoExcel']
            nombre_archivo = archivo_excel.name
            extension = os.path.splitext(nombre_archivo)[1].lower()
            lista_data = []
            if extension == '.xlsx':
                wb = load_workbook(archivo_excel)
                ws = wb.worksheets[0]  
                for row in ws.iter_rows(min_row=2, values_only=True):
                    validar_fila_presupuesto(row)
                    lista_data.append({
                        "Productor":row[0],
                        "IdChacra":row[1],
                        "Chacra":row[2],
                        "IdCuadro":row[3],
                        "Cuadro":row[4],
                        "Fila":row[5],
                        "CantPlantas":row[6],
                        "IdVariedad":row[7],
                        "Variedad":row[8],
                        "Año":row[9],
                        "Poda":row[10],
                        "Raleo":row[11]
                    })
            else:
                raise ValueError("Formato de archivo no soportado. Solo se aceptan .xlsx")
            if lista_data:
                return JsonResponse({'Message': 'Success', 'Datos': lista_data})
            else:
                raise ValueError("No se pudieron cargar los datos.")
        except Exception as e:
            return JsonResponse({'Message': 'Error', 'Nota': str(e)})
    return JsonResponse({'Message': 'No se pudo resolver la petición.'})

class ValidacionError(Exception):
    pass

def validar_fila_chacras(row):  
    try:
        legajo = int(row[1]) 
    except ValueError:
        raise ValidacionError("La columna 'ID CHACRA' debe contener sólo números enteros.")  
    
    if not str(row[7]).strip():
        raise ValidacionError("La columna 'ID CUADRO' no puede estar vacía.")
    
    if row[8] is None:
        raise ValidacionError("La columna 'FILA' debe contener un valor.")
    
    try:
        variedad = int(row[11]) 
    except ValueError:
        raise ValidacionError("La columna 'ID VARIEDAD' debe contener sólo números enteros.")
    
    try:
        anio = int(row[13]) 
    except ValueError:
        raise ValidacionError("La columna 'AÑO' debe contener sólo números enteros.")
    
    try:
        anio = int(row[14]) 
    except ValueError:
        raise ValidacionError("La columna 'N° PLANTAS' debe contener sólo números enteros.")
    
    for i in [15, 16, 17, 18]:
        if not isinstance(row[i], (int, float, type(None))):
            raise ValidacionError(f"La columna {i+1} debe contener sólo números o estar vacía.")
        
def validar_fila_presupuesto(row):  
    try:
        legajo = int(row[9]) 
    except ValueError:
        raise ValidacionError("La columna AÑO' debe contener sólo números enteros.")  
        
    for i in [10, 11]:
        if not isinstance(row[i], (int, float, type(None))):
            raise ValidacionError(f"La columna {i+1} debe contener sólo números o estar vacía.")
        
def json_chacras(filas):
    resultado = {
        "Chacras": []
    }

    chacras_dict = {}

    for row in filas:
        IdFila = row[0]
        IdChacra = int(row[1])
        Chacra = (row[2] or "")
        RazonSocial = (row[5] or "")
        Productor = (row[6] or "")
        Cuadro = str(row[7]).replace('.0','')
        FilaNum = str(row[8]).replace('.0','')
        IdEspecie = str(row[9])
        Especie = (row[10] or "")
        IdVariedad = int(row[11])
        Variedad = (row[12] or "")
        Año = str(row[13]).replace('.0','')
        NroPlantas = str(row[14]).replace('.0','')
        DistFilas = str(row[15]).replace('.0','')
        DistPlantas = str(row[16]).replace('.0','')
        Superficie = f"{row[17]:.3f}" if row[17] else None
        Presupuesto = str(row[18]) if row[18] else None
        Tarea = str(row[19]) if row[19] else None

        # Agrupar por IdChacra
        if IdChacra not in chacras_dict:
            chacras_dict[IdChacra] = {
                "IdCracra": str(IdChacra),
                "Chacra": Chacra,
                "Productor": Productor,
                "Cuadros": []
            }

        chacra = chacras_dict[IdChacra]

        # Buscar cuadro existente
        cuadro_existente = next((c for c in chacra["Cuadros"] if Cuadro in c), None)

        if not cuadro_existente:
            cuadro_existente = {Cuadro: []}
            chacra["Cuadros"].append(cuadro_existente)

        # Crear fila
        nueva_fila = {
            "IdFila": IdFila,
            "Fila": FilaNum,
            "IdEspecie": IdEspecie,
            "Especie": Especie,
            "IdVariedad": IdVariedad,
            "Variedad": Variedad,
            "Año": Año,
            "NroPlantas": NroPlantas,
            "DistFilas": DistFilas,
            "DistPlantas": DistPlantas,
            "Superficie": Superficie,
            "Presupuesto": Presupuesto,
            "Tarea": Tarea
        }

        cuadro_existente[Cuadro].append(nueva_fila)

    resultado["Chacras"] = list(chacras_dict.values())
    return resultado

@csrf_exempt 
def insertar_chacras(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            Usuario = str(request.user).upper()
            chacras_json = request.POST.get('Chacras')
            datos_chacras = json.loads(chacras_json)
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:           
                for chacra in datos_chacras['Chacras']:
                    id_chacra = chacra['IdCracra']
                    for cuadro in chacra['Cuadros']:
                        for cuadro_id, filas in cuadro.items():
                            values = [id_chacra, cuadro_id]
                            cursor.execute("EXEC SP_INSERTA_CHACRA_CUADRO %s,%s", values)
                            cursor.execute("SELECT ID_CUADRO FROM SPA_CUADRO WHERE ID_CHACRA = %s AND NOMBRE_CUADRO = %s ", values)
                            result = cursor.fetchone()
                            id_cuadro = result[0]
                            for fila in filas:
                                values_filas = [id_cuadro, fila['Fila'], fila['IdVariedad'], fila['Año'], fila['NroPlantas'], fila['DistFilas'], fila['DistPlantas'], fila['Superficie'], 'A']
                                cursor.execute("EXEC SPA_INSERTA_CHACRAS_CUADROS_FILAS %s,%s,%s,%s,%s,%s,%s,%s,%s", values_filas)
            return JsonResponse({'Message': 'Success', 'Nota': 'El archivo se subió correctamente.'})
        except Exception as e:
            return JsonResponse({'Message': 'Error', 'Nota': str(e)})
    return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt 
def insertar_presupuesto(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            presupuesto_json = request.POST.get('Presupuesto')
            datos_presupuesto = json.loads(presupuesto_json)
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:  
                for row in datos_presupuesto:
                    IdCuadro = row['IdCuadro']
                    IdFila = row['Fila']
                    IdVariedad = row['IdVariedad']
                    Año = row['Año']
                    Poda = row['Poda']
                    Raleo = row['Raleo']
                    values_poda = [IdFila, IdCuadro, IdVariedad, 'P', Año, Poda]
                    values_raleo = [IdFila, IdCuadro, IdVariedad, 'R', Año, Poda] 

                    if Poda != None:
                        cursor.execute("EXEC SP_INSERTA_PRESUPUESTO %s,%s,%s,%s,%s,%s", values_poda)
                    if Raleo != None:
                        cursor.execute("EXEC SP_INSERTA_PRESUPUESTO %s,%s,%s,%s,%s,%s", values_raleo)

            return JsonResponse({'Message': 'Success', 'Nota': 'Los datos se guardaron correctamente.'})
        except Exception as e:
            return JsonResponse({'Message': 'Error', 'Nota': str(e)})
    return JsonResponse({'Message': 'No se pudo resolver la petición.'})



############# LISTADO LABORES

def carga_inicial_listado_labores(request):
    if request.method == 'GET':
        try:
            listado_productores = []
            listado_personal = []
            listado_labores = [{'Codigo': 'P', 'Descripcion':'PODA'},{'Codigo': 'R', 'Descripcion':'RALEO'}]
            listado_encargados = []
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                #### listado productores
                sql = """ EXEC LISTADO_PRODUCTORES_HABILITADOS """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        listado_productores.append({
                            'Codigo':str(row[0]),
                            'Descripcion':str(row[1])
                        })

                #### listado personal
                sql = """
                        SELECT EM.CodEmpleado AS LEGAJO, ((CONVERT(VARCHAR, EM.CodEmpleado)) + ' - ' + EM.ApellidoEmple + ' ' + EM.NombresEmple) AS NOMBRES
                        FROM TresAses_ISISPayroll.dbo.Empleados AS EM INNER JOIN
                            TresAses_ISISPayroll.dbo.CentrosCostos AS CC ON CC.Regis_CCo = EM.Regis_CCo
                        WHERE CC.AbrevCtroCosto LIKE ('C%%')
                                AND EM.BajaDefinitivaEmple = '2'
                        ORDER BY EM.ApellidoEmple + ' ' + EM.NombresEmple
                    """

                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        listado_personal.append({
                            'Codigo':str(row[0]),
                            'Descripcion':str(row[1])
                        })

                #### listado encargados
                sql = """
                        SELECT RTRIM(US.Usuario) AS ENCARGADO, CASE WHEN ( EM.ApellidoEmple + ' ' + EM.NombresEmple) IS NULL THEN US.Usuario 
                            ELSE ( EM.ApellidoEmple + ' ' + EM.NombresEmple) END AS NOMBRES
                        FROM USUARIOS AS US LEFT JOIN 
                            TresAses_ISISPayroll.dbo.Empleados AS EM ON EM.CodEmpleado = US.CodEmpleado
                        WHERE US.Estado = 'A'
                            AND US.CodEmpleado NOT IN('99999')
                            AND US.Tipo = 'EC' 
                        ORDER BY EM.ApellidoEmple + ' ' + EM.NombresEmple

                    """

                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        listado_encargados.append({
                            'Codigo':str(row[0]),
                            'Descripcion':str(row[1])
                        })
            return JsonResponse({'Message': 'Success', 'Productores':listado_productores, 'Personal':listado_personal, 'Labores':listado_labores, 'Encargados':listado_encargados})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})



















































