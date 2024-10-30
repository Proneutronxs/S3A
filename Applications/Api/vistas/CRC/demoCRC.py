
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import json
import os











@csrf_exempt
def dataGeneral(request):
    if request.method == 'POST':
        desde = request.POST.get('Inicio')
        hasta = request.POST.get('Final')
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """ 

                    """
                cursor.execute(sql, [desde,hasta])
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        legajo = str(row[0])
                        nombre = str(row[1])
                        datos = {'Legajo': legajo, 'Nombre': nombre}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
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
    

@csrf_exempt
def dataConCRC(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        desde = data.get('Inicio')
        hasta = data.get('Final')
        mercado = data.get('Mercado')
        cliente = data.get('Cliente')
        especie = data.get('Especie')
        variedad = data.get('Variedad')
        envase = data.get('Envase')
        marca = data.get('Marca')
        calibres = data.get('Calibres')
        listaCalibres = calibres.split(',')
        calibres_str = ','.join(listaCalibres)
        calibre = "0" if listaCalibres == ['0'] else "1"
        values = [desde,hasta,mercado,cliente,especie,variedad,envase,marca,calibre]

        #insertar_registro_error_sql("API",str(calibres) + ' - ' + calibres_str,"usuario",str(values))
        try:
            with connections['S3A'].cursor() as cursor:
                sql = f""" 
                    
                    DECLARE @@Inicio DATE;
                    DECLARE @@Final DATE;
                    DECLARE @@Mercado VARCHAR(10);
                    DECLARE @@Cliente INT;
                    DECLARE @@Especie INT;
                    DECLARE @@Variedad INT;
                    DECLARE @@Envase INT;
                    DECLARE @@Marca INT;
                    DECLARE @@Calibre VARCHAR(255);

                    SET @@Inicio = %s;
                    SET @@Final = %s;
                    SET @@Mercado = %s;
                    SET @@Cliente = %s;
                    SET @@Especie = %s;
                    SET @@Variedad = %s;
                    SET @@Envase = %s;
                    SET @@Marca = %s;
                    SET @@Calibre = %s;

                    SELECT 
                        Mercado AS MERCADO, ISNULL(NombreEmbarque, '') AS VAPOR, PaisDestino AS DESTINO, IdCliente AS ID_CLIENTE, CONVERT(VARCHAR(30),Cliente) AS CLIENTE, CONVERT(VARCHAR(10), FECH_FAC, 103) AS FECHA_FACTURA, 
                        CONVERT(VARCHAR,IdEspecie) AS ID_ESPECIE, Especie AS ESPECIE, IdVariedad AS ID_VARIEDAD, Variedad AS VARIEDAD, IdEnvase AS ID_ENVASE, Envase AS ENVASE, IdEtiqueta AS ID_MARCA, Etiqueta AS MARCA, 
                        Calibres AS CALIBRES, FORMAT(PesoEnvase, 'N2') AS PESO_ENVASE, FORMAT(PesoEnvase * Bultos, 'N2') AS TOTAL_KGS, 
                        FORMAT(Bultos, 'N0') AS CANT_BULTOS, CONVERT(DECIMAL(18, 2), SUM(Precio2)) AS IMP_UNI, CONVERT(DECIMAL(18, 2), (SUM(Precio2) * TPC.Cantidad)) AS IMP_TOTAL, DATEPART(wk, FECH_FAC) AS ID_SEMANA, 
                        'SEMANA - ' + CONVERT(VARCHAR(3), DATEPART(wk, FECH_FAC)) AS CHAR_SEMANA, ISNULL(NRO_FAC,'-') AS NRO_FAC, CONVERT(VARCHAR,(VistaDemoDLC.NroRemito)) AS NRO_REM, CONVERT(VARCHAR, SUM(ISNULL(CRCT01, 0) + ISNULL(CRCT02, 0) + ISNULL(CRCT03, 0) + ISNULL(CRCT04, 0) + 
                        ISNULL(CRCT05, 0) + ISNULL(CRCT06, 0) + ISNULL(CRCT07, 0) + ISNULL(CRCT08, 0) + ISNULL(CRCT09, 0) + ISNULL(CRCT10, 0) + ISNULL(CRCT11, 0))) AS CRC_TOTAL, DATEPART(SECOND, ALTA_REMITO) AS SEGUNDOS,
                        (CONVERT(VARCHAR(5),T01) + '-' + CONVERT(VARCHAR(5),T02) + '-' + CONVERT(VARCHAR(5),T03) + '-' + CONVERT(VARCHAR(5),T04) + '-' + CONVERT(VARCHAR(5),T05) + '-' + CONVERT(VARCHAR(5),T06) + '-' + 
                        CONVERT(VARCHAR(5),T07) + '-' + CONVERT(VARCHAR(5),T08) + '-' + CONVERT(VARCHAR(5),T09) + '-' + CONVERT(VARCHAR(5),T10) + '-' + CONVERT(VARCHAR(5),T11)) AS LIST_T_CALIBRES,
                        (CONVERT(VARCHAR(20), CRCT01) + '-' + CONVERT(VARCHAR(20), CRCT02) + '-' + CONVERT(VARCHAR(20), CRCT03) + '-' + CONVERT(VARCHAR(20), CRCT04) + '-' + CONVERT(VARCHAR(20), CRCT05) + '-' + 
                        CONVERT(VARCHAR(20), CRCT06) + '-' + CONVERT(VARCHAR(20), CRCT07) + '-' + CONVERT(VARCHAR(20), CRCT08) + '-' + CONVERT(VARCHAR(20), CRCT09) + '-' + CONVERT(VARCHAR(20), CRCT10) + '-' + 
                        CONVERT(VARCHAR(20), CRCT11)) AS LISTA_CRC, CASE CONVERT(VARCHAR,TPC.Tamaño) WHEN 'AAAA' THEN '90' WHEN 'AAA' THEN '80' WHEN 'AA' THEN '70' WHEN 'A' THEN '60' WHEN 'B' THEN '50' WHEN 'C' THEN '40' ELSE CONVERT(VARCHAR,TPC.Tamaño) END AS CALIBRE, 
	                    TPC.Cantidad AS CANTIDAD, CONVERT(VARCHAR,TPC.crc) AS CRC, Moneda AS TIPO_MONEDA
                    FROM 
                        VistaDemoDLC
                        LEFT OUTER JOIN		
                            VistaTamañoPorPC AS TPC on TPC.NroRemito = VistaDemoDLC.NroRemito and TPC.NroItem=VistaDemoDLC.NroItem and TPC.NroSubitem=VistaDemoDLC.NroSubitem
                    WHERE 
                        CONVERT(DATE, FECH_FAC) >= @@Inicio
                        AND CONVERT(DATE, FECH_FAC) <= @@Final 
                        AND (@@Mercado = '0' OR @@Mercado = Mercado)
                        AND (@@Cliente = '0' OR IdCliente = @@Cliente)
                        AND (@@Especie = '0' OR IdEspecie = @@Especie)
                        AND (@@Variedad = '0' OR IdVariedad = @@Variedad)
                        AND (@@Envase = '0' OR IdEnvase = @@Envase)
                        AND (@@Marca = '0' OR IdEtiqueta = @@Marca)
                        AND (@@Calibre = '0' or TPC.Tamaño IN ({calibres_str}))
                    GROUP BY 
                        IdCliente, Cliente, IdEspecie, Especie, IdVariedad, Variedad, IdEnvase, Envase, IdEtiqueta, Etiqueta, Mercado, DATEPART(wk, FECH_FAC), Calibres, NRO_FAC, NombreEmbarque, CONVERT(VARCHAR(10), FECH_FAC, 103), PaisDestino, 
                        PesoEnvase, PesoEnvase * Bultos, Bultos, VistaDemoDLC.NroRemito,DATEPART(SECOND, ALTA_REMITO),(CONVERT(VARCHAR(5),T01) + '-' + CONVERT(VARCHAR(5),T02) + '-' + CONVERT(VARCHAR(5),T03) + '-' + CONVERT(VARCHAR(5),T04) + '-' + 
                        CONVERT(VARCHAR(5),T05) + '-' + CONVERT(VARCHAR(5),T06) + '-' + CONVERT(VARCHAR(5),T07) + '-' + CONVERT(VARCHAR(5),T08) + '-' + CONVERT(VARCHAR(5),T09) + '-' + CONVERT(VARCHAR(5),T10) + '-' + CONVERT(VARCHAR(5),T11)),
                        (CONVERT(VARCHAR(20), CRCT01) + '-' + CONVERT(VARCHAR(20), CRCT02) + '-' + CONVERT(VARCHAR(20), CRCT03) + '-' + CONVERT(VARCHAR(20), CRCT04) + '-' + CONVERT(VARCHAR(20), CRCT05) + '-' + CONVERT(VARCHAR(20), CRCT06) + '-' + 
                        CONVERT(VARCHAR(20), CRCT07) + '-' + CONVERT(VARCHAR(20), CRCT08) + '-' + CONVERT(VARCHAR(20), CRCT09) + '-' + CONVERT(VARCHAR(20), CRCT10) + '-' + CONVERT(VARCHAR(20), CRCT11)),TPC.Tamaño, TPC.crc,TPC.Cantidad, Moneda
                    ORDER BY CONVERT(VARCHAR(10), FECH_FAC, 103), CONVERT(VARCHAR(30),Cliente), TPC.Tamaño
                    """
                cursor.execute(sql, values)
                consulta = cursor.fetchall()
                if consulta:
                    empresas = {}
                    resumen = {"SumaImporteTotal": 0, "SumaImporteCRCTotal": 0}
                    for row in consulta:
                        empresa = row[4]
                        tipo = str(row[31])
                        # Usar diccionario en lugar de lista
                        if empresa not in empresas:
                            empresas[empresa] = {"Nombre": empresa, "Datos": [], "Subtotal": {"SumaImporteTotal": 0, "SumaImporteCRCTotal": 0}}

                        datos_empresa = empresas[empresa]
                        crc = decode_crc(float(row[30]), int(row[28]), int(row[25]))

                        datos_empresa["Datos"].append({
                            "Mercado": str(row[0]),
                            "Vapor": str(row[1]),
                            "Destino": str(row[2]),
                            "IdCliente": str(row[3]),
                            "Cliente": str(row[4]),
                            "FechaFac": str(row[5]),
                            "IdEspecie": str(row[6]),
                            "Especie": str(row[7]),
                            "IdVariedad": str(row[8]),
                            "Variedad": str(row[9]),
                            "IdEnvase": str(row[10]),
                            "Envase": str(row[11]),
                            "IdMarca": str(row[12]),
                            "Marca": str(row[13]),
                            "Calibres": str(row[14]),
                            "PesoEnvase": str(row[15]),
                            "TotalKG": str(row[16]),
                            "CantBultos": str(row[17]),
                            "ImporteUnitario": str(float(row[18]) + crc),  # Sumar el CRC
                            "ImporteTotal": str(row[19]),
                            "IdSemana": str(row[20]),
                            "Semana": str(row[21]),
                            "NroFactura": str(row[22]),
                            "NroRemito": str(row[23]),
                            "ImporteCRCIndi": "0",
                            "ImporteCRCTotal": "0",
                            "Calibre": str(row[28]),
                            "Cantidad": str(row[29]),
                            "CRC": str(crc),
                            "Moneda": str(row[31])
                        })

                        # Actualizar subtotales
                        datos_empresa["Subtotal"]["SumaImporteTotal"] += float(row[19])
                        datos_empresa["Subtotal"]["SumaImporteCRCTotal"] += float(crc * int(row[29]))
                        resumen["SumaImporteTotal"] += float(row[19])
                        resumen["SumaImporteCRCTotal"] += float(crc * int(row[29]))

                    # Convertir empresas en lista y aplicar formato
                    empresas = list(empresas.values())
                    resumen["TotalGeneral"] = resumen["SumaImporteTotal"] + resumen["SumaImporteCRCTotal"]
                    resumen = {k: formato_moneda(tipo,str(v)) for k, v in resumen.items()}

                    for empresa in empresas:
                        empresa["Subtotal"]["TotalGeneral"] = empresa["Subtotal"]["SumaImporteTotal"] + empresa["Subtotal"]["SumaImporteCRCTotal"]
                        empresa["Subtotal"] = {k: formato_moneda(tipo,str(v)) for k, v in empresa["Subtotal"].items()}

                    return JsonResponse({'Message': 'Success', 'Empresas': empresas, 'Resumen': resumen}, safe=False)

                return JsonResponse({'Message': 'No data found', 'Nota':'No se encontraron datos.'}, safe=False)
        
        except Exception as e:
            return JsonResponse({'Message': 'Error', 'nota': str(e)}, safe=False)
        finally:
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})



def decode_crc(p_crc, p_calibre, p_segundo):
    if p_crc > 0:
        return round((p_crc * 100) / (3.1415 * (p_segundo +1)) * p_calibre)
    else:
        return 0


def retornaCRC(tipo,principal,crcs,calibres,segundos):
    principal_lista = [int(x) for x in principal.split("-")]
    crcs_lista = [float(x) for x in crcs.split("-")]
    lista_principal = [principal for principal in principal_lista if principal != 0]
    lista_crc = [crc for principal, crc in zip(principal_lista, crcs_lista) if principal != 0]
    lista_calibres = obtener_calibres(calibres)
    listado_Original_CRC = []
    for calibre, crc in zip(lista_calibres, lista_crc):
        valor = decode_crc(crc,calibre,segundos)
        listado_Original_CRC.append(valor)
    resultado = [p * c for p, c in zip(lista_principal, listado_Original_CRC)]

    valores_moneda = [formato_moneda(tipo,valor) for valor in listado_Original_CRC]
    original_crc = " - ".join(valores_moneda)

    return sum(resultado), original_crc















