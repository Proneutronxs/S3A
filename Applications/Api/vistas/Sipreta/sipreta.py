
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.views.static import serve
from django.http import JsonResponse
from S3A.funcionesGenerales import *
from django.db import connections
from fpdf import FPDF
import json
import math
import os






def chacras_filas_qr(request,usuario):
    if request.method == 'GET':
        values = [str(usuario)]
        try:
            lista_data = []
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                lista_chacras = listado_Chacras(values)
                sql = """ 
                        EXEC SP_SELECT_CHACRAS_FILAS_QR %s
                    """
                cursor.execute(sql,values)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        lista_data.append({
                            "ID_PRODUCTOR": row[0],
                            "PRODUCTOR": row[1],
                            "ID_CHACRA": row[2],
                            "CHACRA": row[3],
                            "ID_FILA": row[4],
                            "ID_CUADRO": row[5],
                            "CUADRO": row[6],
                            "ID_VARIEDAD": row[7],
                            "ID_QR": row[8],
                            "QR": row[9],
                            "TIPO_QR": row[10],
                            "TEMPORADA_QR": row[11],
                            "ALTA_QR": row[12],
                            "ESTADO_QR": row[13],
                            "ACTIVIDAD_QR": row[14],
                            "VALOR_REFERENCIA": row[15],
                            "AÑO_PLANTACION": row[16],
                            "NRO_PLANTAS": row[17],
                            "DIST_FILAS": row[18],
                            "DIST_PLANTAS": row[19],
                            "SUPERFICIE": row[20],
                            "ESTADO_FILA": row[21],
                            "VARIEDAD": row[22],
                            "V_PODA":row[23],
                            "V_RALEO":row[24]
                        })
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data, 'Chacras':lista_chacras})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    

def listado_Chacras(values):
    listado_chacras = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT CH.IdChacra AS ID_CHACRA, RTRIM(CH.Nombre) AS CHACRA, CH.IdProductor AS ID_PRODUCTOR, RTRIM(PR.Nombre) AS PRODUCTOR
                    FROM S3A.dbo.Chacra AS CH INNER JOIN
                        S3A.dbo.Productor AS PR ON PR.IdProductor = CH.IdProductor
                    WHERE CH.IdChacra IN (SELECT valor FROM dbo.fn_Split((SELECT Chacras FROM USUARIOS WHERE Usuario = %s), ','))
                    ORDER BY RTRIM(CH.Nombre)
                """
            cursor.execute(sql,values)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    listado_chacras.append({
                        "ID_CHACRA":row[0],
                        "CHACRA":row[1],
                        "ID_PRODUCTOR":row[2],
                        "PRODUCTOR":row[3]
                    })
            return listado_chacras
    except Exception as e:
        registroRealizado(values,"LISTADO_CHACRAS",str(e))
        return listado_chacras
    



@csrf_exempt
def data_sync_all(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            dataJsonBody = json.loads(body)
            USUARIO2 = dataJsonBody['Usuario']
            data_qrs = dataJsonBody['DataQrs']
            data_labores = dataJsonBody['DataLabores']
            debug_error(str("SIDESWIPE"),str(dataJsonBody))
            debug_error(str("LAB-"+USUARIO2),str(data_labores))
            debug_error(str("QRS-"+USUARIO2),str(data_qrs))
            lista_chacras = listado_Chacras([str(USUARIO2)])
            lista_data = []
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                #### INSERTA LOS QR ACTUALIZADOS
                insertQR = """ EXEC SP_INSERTA_QR_PERSONAL_FILAS %s, %s, %s, %s, %s, %s, %s, %s, %s, %s """
                #### INSERTA LAS LABORES
                insertLabores = """ EXEC SP_INSERTA_LABORES %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s """
                qr_insertados = 0
                labores_insertadas = 0
                errores_qr = []
                errores_labores = []

                # for qr in data_qrs:
                #     try:
                #         TIPO_QR = qr["TIPO_QR"] if qr["TIPO_QR"] != "" else None
                #         QR = qr["QR"] if qr["QR"] != "" else None
                #         ID_LEGAJO = qr["ID_LEGAJO"] if qr["ID_LEGAJO"] != "" else None
                #         ID_FILA = qr["ID_FILA"] if qr["ID_FILA"] != "" else None
                #         ID_CUADRO = qr["ID_CUADRO"] if qr["ID_CUADRO"] != "" else None
                #         ID_VARIEDAD = qr["ID_VARIEDAD"] if qr["ID_VARIEDAD"] != "" else None
                #         FECHA_ALTA = qr["FECHA_ALTA"] if qr["FECHA_ALTA"] != "" else None
                #         TEMPORADA = qr["TEMPORADA"] if qr["TEMPORADA"] != "" else None
                #         ESTADO = qr["ESTADO"] if qr["ESTADO"] != "" else None
                #         valuesQR = [TIPO_QR, QR, ID_LEGAJO, ID_FILA, ID_CUADRO, ID_VARIEDAD, FECHA_ALTA, TEMPORADA, ESTADO, USUARIO2]
                #         cursor.execute(insertQR,valuesQR)
                #         qr_insertados += 1
                #     except Exception as e:
                #         errores_qr.append(str(e))

                # for lb in data_labores:
                #     try:
                #         QR_FILA = lb["QR_FILA"] if lb["QR_FILA"] != "" else None
                #         QR_EMPLEADO = lb["QR_EMPLEADO"] if lb["QR_EMPLEADO"] != "" else None
                #         ID_LEGAJO = lb["ID_LEGAJO"] if lb["ID_LEGAJO"] != "" else None
                #         LABOR = lb["LABOR"] if lb["LABOR"] != "" else None
                #         ID_CHACRA = lb["ID_CHACRA"] if lb["ID_CHACRA"] != "" else None
                #         ID_CUADRO = lb["ID_CUADRO"] if lb["ID_CUADRO"] != "" else None
                #         ID_FILA = lb["ID_FILA"] if lb["ID_FILA"] != "" else None
                #         ID_VARIEDAD = lb["ID_VARIEDAD"] if lb["ID_VARIEDAD"] != "" else None
                #         CANTIDAD = lb["CANTIDAD"] if lb["CANTIDAD"] != "" else None
                #         UNIDAD = lb["UNIDAD"] if lb["UNIDAD"] != "" else None
                #         TEMPORADA = lb["TEMPORADA"] if lb["TEMPORADA"] != "" else None
                #         VALOR = lb["VALOR"] if lb["VALOR"] != "" else None
                #         FECHA_ALTA = lb["FECHA_ALTA"] if lb["FECHA_ALTA"] != "" else None
                #         USUARIO = lb["USUARIO"] if lb["USUARIO"] != "" else None
                #         ESTADO = lb["ESTADO"] if lb["ESTADO"] != "" else None
                #         valuesLabores = [QR_FILA, QR_EMPLEADO, LABOR, FECHA_ALTA, CANTIDAD, UNIDAD, VALOR, USUARIO, ID_CUADRO, ID_FILA, ID_LEGAJO]
                #         cursor.execute(insertLabores,valuesLabores)
                #         labores_insertadas += 1
                #     except Exception as e:
                #         errores_labores.append(str(e))


                sql2 = """ 
                        EXEC SP_SELECT_CHACRAS_FILAS_QR %s
                    """
                cursor.execute(sql2,[str(USUARIO2)])
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        lista_data.append({
                            "ID_PRODUCTOR": row[0],
                            "PRODUCTOR": row[1],
                            "ID_CHACRA": row[2],
                            "CHACRA": row[3],
                            "ID_FILA": row[4],
                            "ID_CUADRO": row[5],
                            "CUADRO": row[6],
                            "ID_VARIEDAD": row[7],
                            "ID_QR": row[8],
                            "QR": row[9],
                            "TIPO_QR": row[10],
                            "TEMPORADA_QR": row[11],
                            "ALTA_QR": row[12],
                            "ESTADO_QR": row[13],
                            "ACTIVIDAD_QR": row[14],
                            "VALOR_REFERENCIA": row[15],
                            "AÑO_PLANTACION": row[16],
                            "NRO_PLANTAS": row[17],
                            "DIST_FILAS": row[18],
                            "DIST_PLANTAS": row[19],
                            "SUPERFICIE": row[20],
                            "ESTADO_FILA": row[21],
                            "VARIEDAD": row[22],
                            "V_PODA":row[23],
                            "V_RALEO":row[24]
                        })

                nota = f"Se insertaron {qr_insertados} registros de QR y {labores_insertadas} registros de labores."
                
            if errores_qr or errores_labores:
                nota += " Sin embargo, se produjeron errores en algunos registros."
            return JsonResponse({'Message': 'Success', 'Datos': lista_data, 'Chacras':lista_chacras, 'Nota': nota, 'RegistrosInsertados': {'QR': qr_insertados, 'Labores': labores_insertadas}, 
                                'Errores': {'QR': errores_qr, 'Labores': errores_labores}})                  
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'}) 
    

@csrf_exempt
def detalle_labores_app(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            inicio = str(json.loads(body)['Inicio'])
            final = str(json.loads(body)['Final'])
            legajo = str(json.loads(body)['Legajo'])
            idChacra = str(json.loads(body)['IdChacra'])
            encargado = str(json.loads(body)['Encargado'])
            values = [inicio,final,legajo,idChacra,encargado]            
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        EXEC SP_SELECT_DETALLE_LABORES %s, %s, %s, %s, %s
                    """
                cursor.execute(sql,values)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    importe_total = 0
                    for row in consulta:
                        lista_data.append({
                            "LEGAJO": row[0],
                            "NOMBRES": (row[1] or "Sin Nombre"),
                            "FECHA": row[2],
                            "QR": row[3],
                            "ID_CUADRO": row[4],
                            "ID_CHACRA": row[5],
                            "ID_PRODUCTOR": row[6],
                            "PRODUCTOR": row[7],
                            "CHACRA": row[8],
                            "CUADRO": row[9],
                            "FILA": row[10],
                            "VARIEDADES": str(row[11]).replace(',','\n'),
                            "CANT_PLANTAS": row[12],
                            "LABOR": row[13],
                            "IMPORTE_FILA": formato_moneda("$",row[14])
                        })
                        importe_total += float(row[14] or 0) # Asumiendo que row[14] es un número
                    return JsonResponse({'Message': 'Success', 'ImporteTotal': formato_moneda("$",importe_total), 'Datos': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    


@csrf_exempt
def detalle_labores_app_pdf(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            inicio = str(json.loads(body)['Inicio'])
            final = str(json.loads(body)['Final'])
            legajo = str(json.loads(body)['Legajo'])#or 'TODOS'
            idChacra = str(json.loads(body)['IdChacra'])
            encargado = str(json.loads(body)['Encargado'])
            values = [inicio,final,legajo,idChacra,encargado]
        
            #debug_error(str(encargado),str(values))            
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        EXEC SP_SELECT_DETALLE_LABORES %s, %s, %s, %s, %s
                    """
                cursor.execute(sql,values)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    importe_total = 0
                    for row in consulta:
                        lista_data.append({
                            "LEGAJO": str(row[0]),
                            "NOMBRES": str(row[1] or "Sin Nombre"),
                            "FECHA": str(row[2]),
                            "QR": str(row[3]),
                            "ID_CUADRO": str(row[4]),
                            "ID_CHACRA": row[5],
                            "ID_PRODUCTOR": row[6],
                            "PRODUCTOR": str(row[7]),
                            "CHACRA": str(row[8]),
                            "CUADRO": str(row[9]),
                            "FILA": str(row[10]),
                            "VARIEDADES": str(row[11]),
                            "CANT_PLANTAS": str(row[12]),
                            "LABOR": str(row[13]),
                            "IMPORTE_FILA": formato_moneda("$",row[14])
                        })
                        importe_total += float(row[14] or 0)
                    nombrePDF = generar_pdf_detalle_labores(lista_data,legajo)
                    return JsonResponse({'Message': 'Success', 'NombrePDF': nombrePDF})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            debug_error("ERR EXCE",str(e))      
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    

def generar_pdf_detalle_labores(lista_data,nombre):
    try:
        pdf = FPDF_detalle_labores(orientation='L', unit='mm', format='A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 8)

        pdf.cell(15, 5, 'LEGAJO', 1, 0, 'C')
        pdf.cell(50, 5, 'NOMBRES', 1, 0, 'C')
        pdf.cell(16, 5, 'FECHA', 1, 0, 'C')
        pdf.cell(40, 5, 'PRODUCTOR', 1, 0, 'C')
        pdf.cell(30, 5, 'CHACRA', 1, 0, 'C')
        pdf.cell(16, 5, 'CUADRO', 1, 0, 'C')
        pdf.cell(16, 5, 'FILA', 1, 0, 'C')
        pdf.cell(38, 5, 'VARIEDADES', 1, 0, 'C')
        pdf.cell(10, 5, 'N° P.', 1, 0, 'C')
        pdf.cell(18, 5, 'LABOR', 1, 0, 'C')
        pdf.cell(30, 5, 'IMPORTE', 1, 0, 'C')
        pdf.ln(5)
        pdf.set_font('Arial', '', 8)

        for row in lista_data:
            pdf.cell(15, 5, row['LEGAJO'], 1, 0, 'C')
            pdf.cell(50, 5, str(row['NOMBRES'])[:25], 1, 0, 'L')
            pdf.cell(16, 5, row['FECHA'], 1, 0, 'C')
            pdf.cell(40, 5, str(row['PRODUCTOR'])[:20], 1, 0, 'L')
            pdf.cell(30, 5, row['CHACRA'], 1, 0, 'L')
            pdf.cell(16, 5, row['CUADRO'], 1, 0, 'C')
            pdf.cell(16, 5, row['FILA'], 1, 0, 'C')
            pdf.cell(38, 5, str(row['VARIEDADES'])[:20], 1, 0, 'L')
            pdf.cell(10, 5, row['CANT_PLANTAS'], 1, 0, 'C')
            pdf.cell(18, 5, row['LABOR'], 1, 0, 'C')
            pdf.multi_cell(30, 5, row['IMPORTE_FILA'], 1, 0, 'C')
            #pdf.ln(5)

        nombre_archivo = 'DetalleLabores_' + nombre + '_' + obtenerHorasArchivo() + '.pdf'  #/home/sides/MAIN S3A/S3A/Applications/Api/vistas/Sipreta/documentos
        pdf.output('Applications/Api/vistas/Sipreta/documentos/'+nombre_archivo)
        return nombre_archivo
    except Exception as e:
        debug_error("ERR PDF",str(e))   
        return "0"

class FPDF_detalle_labores(FPDF):
    def header(self):
        self.set_font('Arial', '', 15)
        self.rect(x=10,y=10,w=277,h=19)
        self.image('static/imagenes/TA.png', x=16, y=11, w=16, h=10)
        self.line(72,10,72,22)
        self.set_font('Arial', 'B', 13)
        self.text(x=130, y=18, txt= 'TRES ASES S.A.')
        self.set_font('Arial', '', 10)
        self.text(x=230, y=21, txt= 'Tipo de Documento:')
        self.set_font('Arial', 'B', 10)
        self.text(x=268, y=21, txt= 'REPORTE')
        self.line(10,22,287,22)
        self.set_font('Arial', '', 10)
        self.text(x=16, y=27, txt= 'Título de Documento:')
        self.set_font('Arial', 'B', 13)
        self.text(x=110, y=27, txt= 'DETALLE DE LABORES')
        self.line(228,10,228,29)
        self.set_font('Arial', 'B', 10)
        self.text(x=230, y=28, txt= 'Código: s/n')
        self.ln(25)

    def footer(self):
        self.set_font('Arial', '', 8)
        self.set_y(-16)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')
        self.rect(x=10,y=192,w=277,h=12)
        # self.text(x=18, y=286, txt= 'Realizó:')
        # self.text(x=48, y=286, txt= 'Fecha:')
        # self.text(x=100, y=286, txt= 'Revisó:')
        # self.text(x=92, y=286, txt= ' --- ')
        self.text(x=246, y=196, txt= 'Versión:')
        self.set_font('Arial', 'B', 8)
        self.text(x=248.5, y=202, txt= '1.0')
        self.line(40,278,40,293)
        self.line(70,278,70,293)
        self.line(242,192,242,204)
        self.line(262,192,262,204)
        self.ln(275)


def descarga_archivo_pdf(request, filename):
    nombre = filename
    filename = 'Applications/Api/vistas/Sipreta/documentos/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    else:
        raise Http404
    

def debug_error(usuario, body, error=None):
    try:
        with connections['BD_DEBUG'].cursor() as cursor:
            sql = """ 
                    INSERT INTO TB_DEBUG (USUARIO, FECHA, BODY)
                    VALUES (%s, NOW(), %s)
                """
            if error:
                body += f" - Error: {error}"
            cursor.execute(sql, (usuario, body))
            connections['BD_DEBUG'].commit()
    except Exception as e:
        print(f"Error al registrar en TB_DEBUG: {e}")