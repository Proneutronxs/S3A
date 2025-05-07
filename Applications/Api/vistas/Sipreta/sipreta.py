
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import json
import math
import os






def chacras_filas_qr(request):
    if request.method == 'GET':
        try:
            lista_data = []
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        EXEC SP_SELECT_CHACRAS_FILAS_QR
                    """
                cursor.execute(sql)
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
                            "ESTADO_FILA": row[21]
                        })
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    

# ID_PRODUCTOR	PRODUCTOR	ID_CHACRA	CHACRA	ID_FILA	ID_CUADRO	CUADRO	ID_VARIEDAD	ID_QR	QR	TIPO_QR	TEMPORADA_QR	ALTA_QR	ESTADO_QR	ACTIVIDAD_QR	VALOR_REFERENCIA	AÑO_PLANTACION	NRO_PLANTAS	DIST_FILAS	DIST_PLANTAS	SUPERFICIE	ESTADO_FILA
# 5200	ROM - MIK S.A.	1000001	LOTE 1	1	1	50	27	NULL	NULL	NULL	NULL	NULL	NULL	P	2500.00	2006	58	4.000	1.000	0.023	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	2	1	50	27	NULL	NULL	NULL	NULL	NULL	NULL	P	2507.00	2006	58	4.000	1.500	0.035	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	1	2	2	27	NULL	NULL	NULL	NULL	NULL	NULL	P	2501.00	1970	16	4.000	6.500	0.042	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	2	2	2	27	NULL	NULL	NULL	NULL	NULL	NULL	P	2506.00	2006	55	4.000	2.000	0.044	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	1	3	3	27	NULL	NULL	NULL	NULL	NULL	NULL	P	2502.00	1970	17	4.000	6.500	0.044	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	2	3	3	51	NULL	NULL	NULL	NULL	NULL	NULL	P	2505.00	2005	57	4.000	2.000	0.046	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	7	4	4	51	NULL	NULL	NULL	NULL	NULL	NULL	P	2508.00	2005	57	4.000	2.000	0.046	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	8	4	4	51	NULL	NULL	NULL	NULL	NULL	NULL	P	5500.00	2005	35	4.000	3.000	0.042	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	8	4	4	51	NULL	NULL	NULL	NULL	NULL	NULL	R	1200.00	2005	35	4.000	3.000	0.042	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	1	7	1	27	NULL	NULL	NULL	NULL	NULL	NULL	P	2503.00	2006	58	4.000	1.000	0.023	A
# 5200	ROM - MIK S.A.	1000001	LOTE 1	2	7	1	27	NULL	NULL	NULL	NULL	NULL	NULL	P	2504.00	2006	58	4.000	1.500	0.035	A