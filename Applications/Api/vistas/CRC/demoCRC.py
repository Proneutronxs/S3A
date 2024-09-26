
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
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
        desde = request.POST.get('Inicio')
        hasta = request.POST.get('Final')
        mercado = request.POST.get('Mercado')
        cliente = request.POST.get('Cliente')
        vapor = request.POST.get('Vapor')
        especie = request.POST.get('Especie')
        variedad = request.POST.get('Variedad')
        envase = request.POST.get('Envase')
        marca = request.POST.get('Marca')
        values = [desde,hasta,mercado,cliente,vapor,especie,variedad,envase,marca]
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
                        FORMAT(Bultos, 'N0') AS CANT_BULTOS, FORMAT(SUM(Precio2), 'N2') AS IMP_UNI, FORMAT(SUM(Total2), 'N2') AS IMP_TOTAL, DATEPART(wk, FECH_FAC) AS ID_SEMANA, 
                        'SEMANA - ' + CONVERT(VARCHAR(3), DATEPART(wk, FECH_FAC)) AS CHAR_SEMANA, ISNULL(NRO_FAC,'-') AS NRO_FAC, CONVERT(VARCHAR,(NroRemito)) AS NRO_REM, CONVERT(VARCHAR, SUM(ISNULL(CRCT01, 0) + ISNULL(CRCT02, 0) + ISNULL(CRCT03, 0) + ISNULL(CRCT04, 0) + 
                        ISNULL(CRCT05, 0) + ISNULL(CRCT06, 0) + ISNULL(CRCT07, 0) + ISNULL(CRCT08, 0) + ISNULL(CRCT09, 0) + ISNULL(CRCT10, 0) + ISNULL(CRCT11, 0))) AS CRC_TOTAL, DATEPART(SECOND, ALTA_REMITO) AS SEGUNDOS
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
                        PesoEnvase, PesoEnvase * Bultos, Bultos, NroRemito,DATEPART(SECOND, ALTA_REMITO)

                    """
                cursor.execute(sql, values)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        empresa = row[4]
                        Calibres = int(row[14])
                        Segundos = str(row[25])
                        CRCTotal = float(row[24])
                        sumaCalibres = sumar_calibres(Calibres.replace(" ", ""))
                        cantidadCalibres = contar_calibres(Calibres.replace(" ", ""))
                        SegundosTotales = Segundos + cantidadCalibres
                        importeCRC = decode_crc(CRCTotal, sumaCalibres, SegundosTotales)
                        if empresa not in lista_data:
                            lista_data[empresa] = []
                        lista_data[empresa].append({
                            # MERCADO	VAPOR	DESTINO	ID_CLIENTE	CLIENTE	FECHA_FACTURA	ID_ESPECIE	ESPECIE	ID_VARIEDAD	VARIEDAD	ID_ENVASE	ENVASE	ID_MARCA	
                            # MARCA	CALIBRES	PESO_ENVASE	TOTAL_KGS	CANT_BULTOS	IMP_UNI	IMP_TOTAL	ID_SEMANA	CHAR_SEMANA	NRO_FAC	NRO_REM	CRC_TOTAL	SEGUNDOS (TOTAL 25)
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
                            "ImporteUnitario":str(row[18]),
                            "ImporteTotal":str(row[19]),
                            "IdSemana":str(row[20]),
                            "Semana":str(row[21]),
                            "NroFactura":str(row[22]),
                            "NroRemito":str(row[23]),
                            "ImporteCRC":str(importeCRC)
                        })

                    return JsonResponse({'Message': 'Success', 'Datos': lista_data}, safe=False)
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


def sumar_calibres(calibres):
    calibre_map = {
        "AAAA": 90,
        "AAA": 80,
        "AA": 70,
        "A": 60,
        "B": 50,
        "C": 40
    }
    if "-" in calibres:
        return sum(int(c) if c.isdigit() else calibre_map.get(c, 0) for c in calibres.split("-"))
    else:
        return int(calibres)


def contar_calibres(calibres):
    if "-" in calibres:
        return len(calibres.split("-"))
    else:
        return 1
    

def decode_crc(resultado, p_calibre, p_segundo):
    if isinstance(p_calibre, str):  
        calibre_map = {
            "AAAA": 90,
            "AAA": 80,
            "AA": 70,
            "A": 60,
            "B": 50,
            "C": 40
        }
        int_calibre = calibre_map.get(p_calibre, 10)
    else:  
        int_calibre = p_calibre

    if resultado == 0:
        return 0
    else:
        return round((resultado * 100 * int_calibre) / (3.1415 * (p_segundo)))

















