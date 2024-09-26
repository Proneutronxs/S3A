
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
        vapor = data.get('Vapor')
        especie = data.get('Especie')
        variedad = data.get('Variedad')
        envase = data.get('Envase')
        marca = data.get('Marca')
        values = [desde,hasta,mercado,cliente,vapor,especie,variedad,envase,marca]

        #insertar_registro_error_sql("API","DATA CRC","usuario",str(values))
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """ 
                    
                    DECLARE @@Inicio DATE;
                    DECLARE @@Final DATE;
                    DECLARE @@Mercado VARCHAR(10);
                    DECLARE @@Cliente INT;
                    DECLARE @@Vapor VARCHAR(10);
                    DECLARE @@Especie INT;
                    DECLARE @@Variedad INT;
                    DECLARE @@Envase INT;
                    DECLARE @@Marca INT;

                    SET @@Inicio = %s;
                    SET @@Final = %s;
                    SET @@Mercado = %s;
                    SET @@Cliente = %s;
                    SET @@Vapor = %s;
                    SET @@Especie = %s;
                    SET @@Variedad = %s;
                    SET @@Envase = %s;
                    SET @@Marca = %s;

                    SELECT 
                        Mercado AS MERCADO, ISNULL(NombreEmbarque, '') AS VAPOR, PaisDestino AS DESTINO, CONVERT(VARCHAR,IdCliente) AS ID_CLIENTE, Cliente AS CLIENTE, CONVERT(VARCHAR(10), FECH_FAC, 103) AS FECHA_FACTURA, 
                        CONVERT(VARCHAR,IdEspecie) AS ID_ESPECIE, Especie AS ESPECIE, IdVariedad AS ID_VARIEDAD, Variedad AS VARIEDAD, IdEnvase AS ID_ENVASE, Envase AS ENVASE, IdEtiqueta AS ID_MARCA, Etiqueta AS MARCA, 
                        Calibres AS CALIBRES, FORMAT(PesoEnvase, 'N2') AS PESO_ENVASE, FORMAT(PesoEnvase * Bultos, 'N2') AS TOTAL_KGS, 
                        FORMAT(Bultos, 'N0') AS CANT_BULTOS, CONVERT(DECIMAL(18, 2), SUM(Precio2)) AS IMP_UNI, CONVERT(DECIMAL(18, 2), SUM(Total2)) AS IMP_TOTAL, DATEPART(wk, FECH_FAC) AS ID_SEMANA, 
                        'SEMANA - ' + CONVERT(VARCHAR(3), DATEPART(wk, FECH_FAC)) AS CHAR_SEMANA, ISNULL(NRO_FAC,'-') AS NRO_FAC, CONVERT(VARCHAR,(NroRemito)) AS NRO_REM, CONVERT(VARCHAR, SUM(ISNULL(CRCT01, 0) + ISNULL(CRCT02, 0) + ISNULL(CRCT03, 0) + ISNULL(CRCT04, 0) + 
                        ISNULL(CRCT05, 0) + ISNULL(CRCT06, 0) + ISNULL(CRCT07, 0) + ISNULL(CRCT08, 0) + ISNULL(CRCT09, 0) + ISNULL(CRCT10, 0) + ISNULL(CRCT11, 0))) AS CRC_TOTAL, DATEPART(SECOND, ALTA_REMITO) AS SEGUNDOS,
                        (CONVERT(VARCHAR(5),T01) + '-' + CONVERT(VARCHAR(5),T02) + '-' + CONVERT(VARCHAR(5),T03) + '-' + CONVERT(VARCHAR(5),T04) + '-' + CONVERT(VARCHAR(5),T05) + '-' + CONVERT(VARCHAR(5),T06) + '-' + 
                        CONVERT(VARCHAR(5),T07) + '-' + CONVERT(VARCHAR(5),T08) + '-' + CONVERT(VARCHAR(5),T09) + '-' + CONVERT(VARCHAR(5),T10) + '-' + CONVERT(VARCHAR(5),T11)) AS LIST_T_CALIBRES,
                        (CONVERT(VARCHAR(20), CRCT01) + '-' + CONVERT(VARCHAR(20), CRCT02) + '-' + CONVERT(VARCHAR(20), CRCT03) + '-' + CONVERT(VARCHAR(20), CRCT04) + '-' + CONVERT(VARCHAR(20), CRCT05) + '-' + 
                        CONVERT(VARCHAR(20), CRCT06) + '-' + CONVERT(VARCHAR(20), CRCT07) + '-' + CONVERT(VARCHAR(20), CRCT08) + '-' + CONVERT(VARCHAR(20), CRCT09) + '-' + CONVERT(VARCHAR(20), CRCT10) + '-' + 
                        CONVERT(VARCHAR(20), CRCT11)) AS LISTA_CRC
                    FROM 
                        VistaDemoDLC
                    WHERE 
                        CONVERT(DATE, FECH_FAC) >= @@Inicio
                        AND CONVERT(DATE, FECH_FAC) <= @@Final 
                        AND (@@Mercado = '0' OR @@Mercado = Mercado)
                        AND (@@Cliente = '0' OR IdCliente = @@Cliente)
                        AND (@@Vapor = '0' OR NombreEmbarque = @@Vapor)
                        AND (@@Especie = '0' OR IdEspecie = @@Especie)
                        AND (@@Variedad = '0' OR IdVariedad = @@Variedad)
                        AND (@@Envase = '0' OR IdEnvase = @@Envase)
                        AND (@@Marca = '0' OR IdEtiqueta = @@Marca)
                    GROUP BY 
                        IdCliente, Cliente, IdEspecie, Especie, IdVariedad, Variedad, IdEnvase, Envase, IdEtiqueta, Etiqueta, Mercado, DATEPART(wk, FECH_FAC), Calibres, NRO_FAC, NombreEmbarque, CONVERT(VARCHAR(10), FECH_FAC, 103), PaisDestino, 
                        PesoEnvase, PesoEnvase * Bultos, Bultos, NroRemito,DATEPART(SECOND, ALTA_REMITO),(CONVERT(VARCHAR(5),T01) + '-' + CONVERT(VARCHAR(5),T02) + '-' + CONVERT(VARCHAR(5),T03) + '-' + CONVERT(VARCHAR(5),T04) + '-' + 
                        CONVERT(VARCHAR(5),T05) + '-' + CONVERT(VARCHAR(5),T06) + '-' + CONVERT(VARCHAR(5),T07) + '-' + CONVERT(VARCHAR(5),T08) + '-' + CONVERT(VARCHAR(5),T09) + '-' + CONVERT(VARCHAR(5),T10) + '-' + CONVERT(VARCHAR(5),T11)),
                        (CONVERT(VARCHAR(20), CRCT01) + '-' + CONVERT(VARCHAR(20), CRCT02) + '-' + CONVERT(VARCHAR(20), CRCT03) + '-' + CONVERT(VARCHAR(20), CRCT04) + '-' + CONVERT(VARCHAR(20), CRCT05) + '-' + CONVERT(VARCHAR(20), CRCT06) + '-' + 
                        CONVERT(VARCHAR(20), CRCT07) + '-' + CONVERT(VARCHAR(20), CRCT08) + '-' + CONVERT(VARCHAR(20), CRCT09) + '-' + CONVERT(VARCHAR(20), CRCT10) + '-' + CONVERT(VARCHAR(20), CRCT11))

                    """
                cursor.execute(sql, values)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = {}
                    resumen = {"SumaImporteTotal": 0, "SumaImporteCRCTotal": 0}
                    for row in consulta:
                        empresa = row[4]
                        segundos = row[25]
                        calibres = str(row[14])
                        cantidades = str(row[26])
                        crcs = str(row[27])
                        total, individual = retornaCRC(cantidades,crcs,calibres,segundos)
                        resumen["SumaImporteTotal"] += float(row[19])
                        resumen["SumaImporteCRCTotal"] += float(total)
                        
                        if empresa not in lista_data:
                            lista_data[empresa] = {"datos": [], "subtotal": {"SumaImporteTotal": 0, "SumaImporteCRCTotal": 0}}
                        
                        lista_data[empresa]["datos"].append({
                            "Mercado":str(row[0]),
                            "Vapor": str(row[1]),
                            "Destino":str(row[2]),
                            "IdCliente":str(row[3]),
                            "Cliente":str(row[4]),
                            "FechaFac":str(row[5]),
                            "IdEspecie":str(row[6]),
                            "Especie":str(row[7]),
                            "IdVariedad":str(row[8]),
                            "Variedad":str(row[9]),
                            "IdEnvase":str(row[10]),
                            "Envase":str(row[11]),
                            "IdMarca":str(row[12]),
                            "Marca":str(row[13]),
                            "Calibres":str(row[14]),
                            "PesoEnvase":str(row[15]),
                            "TotalKG":str(row[16]),
                            "CantBultos":str(row[17]),
                            "ImporteUnitario":formato_moneda_usd(row[18]),
                            "ImporteTotal":str(row[19]),
                            "IdSemana":str(row[20]),
                            "Semana":str(row[21]),
                            "NroFactura":str(row[22]),
                            "NroRemito":str(row[23]),
                            "ImporteCRCIndi":str(individual),
                            "ImporteCRCTotal":str(total)
                        })
                        
                        lista_data[empresa]["subtotal"]["SumaImporteTotal"] += float(row[19])
                        lista_data[empresa]["subtotal"]["SumaImporteCRCTotal"] += float(total)
                    
                    resumen["TotalGeneral"] = resumen["SumaImporteTotal"] + resumen["SumaImporteCRCTotal"]

                    resumen = {k: formato_moneda_usd(str(v)) for k, v in resumen.items()}
                    
                    for empresa in lista_data:
                        lista_data[empresa]["subtotal"]["TotalGeneral"] = lista_data[empresa]["subtotal"]["SumaImporteTotal"] + lista_data[empresa]["subtotal"]["SumaImporteCRCTotal"]
                        lista_data[empresa]["subtotal"] = {k: formato_moneda_usd(str(v)) for k, v in lista_data[empresa]["subtotal"].items()}
                    
                    lista_data["Resumen"] = resumen
                    
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                    #return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("API","DATA CRC","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


def retornaCRC(principal,crcs,calibres,segundos):
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

    valores_moneda = [formato_moneda_usd(valor) for valor in listado_Original_CRC]
    original_crc = " - ".join(valores_moneda)

    return sum(resultado), original_crc















