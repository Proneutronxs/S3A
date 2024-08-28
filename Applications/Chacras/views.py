from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import os


# Create your views here.


@login_required
@permission_required('Chacras.puede_ingresar', raise_exception=True)
def Chacras(request):
    return render (request, 'Chacras/chacras.html')


@login_required
def planillas(request):
    return render (request, 'Chacras/Planillas/planillas.html')

@login_required
def general(request):
    return render (request, 'Chacras/Planillas/general.html')

@csrf_exempt
@login_required
@csrf_exempt
def listarAdicionales(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Chacra.puede_ver')
        if user_has_permission:
            desde = request.POST.get('Inicio')
            hasta = request.POST.get('Final')
            centros = request.POST.get('Centro')
            legajos = request.POST.get('Legajo')
            descripcion = request.POST.get('Descripcion')
            pagos = request.POST.get('Pago')
            values = [desde,hasta,centros,legajos,descripcion,pagos]
            try:
                with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                    sql = """  
                        DECLARE @@Inicio DATE;
                        DECLARE @@Final DATE;
                        DECLARE @@Centro INT;
                        DECLARE @@Pago VARCHAR(5);
                        DECLARE @@Legajo INT;
                        DECLARE @@Descripcion VARCHAR(5);

                        SET @@Inicio = %s
                        SET @@Final = %s
                        SET @@Centro = %s
                        SET @@Legajo = %s
                        SET @@Descripcion = %s 
                        SET @@Pago = %s

                        SELECT Planilla_Chacras.IdPlanilla AS ID, Planilla_Chacras.Legajo AS LEGAJO, CONVERT(VARCHAR(38),(TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple)) AS NOMBRE,
                                TresAses_ISISPayroll.dbo.CentrosCostos.AbrevCtroCosto AS CENTRO, Planilla_Chacras.Categoria AS CATEGORIA,
                                CASE Planilla_Chacras.Descripcion WHEN 'PT' THEN 'POR TANTO' WHEN 'PD' THEN 'POR DÍA' WHEN 'FE' THEN 'FERIADO' WHEN 'SD' THEN 'SAB/DOM' WHEN 'AR' THEN 'ARREGLO' END AS DESCRIPCION,
                                CASE Planilla_Chacras.Tarea WHEN 'P' THEN 'PODA' WHEN 'R' THEN 'RALEO' WHEN 'V' THEN 'VARIOS' WHEN 'T' THEN 'TRACTOR' END AS TAREA, Planilla_Chacras.Jornales AS CANT_DIAS,
                                CASE Planilla_Chacras.Tipo WHEN 'F' THEN ('FILA N°: ' + CONVERT(VARCHAR(10),Planilla_Chacras.NroFila)) WHEN 'P' THEN 'PLANTAS' WHEN 'M' THEN 'METROS' WHEN 'O' THEN 'OTROS' END AS TIPO,
                                CASE Planilla_Chacras.Pago WHEN 'R' THEN 'RECIBO' WHEN 'A' THEN 'ADICIONAL' WHEN 'D' THEN 'DIFERENCIA' END AS PAGO,
                                CONVERT(VARCHAR(20) ,RTRIM(S3A.dbo.Chacra.Nombre)) AS CHACRA,
                                CASE WHEN SUB_CONSULTA.CONTEO IS NULL THEN '0' ELSE SUB_CONSULTA.CONTEO END AS CONTEO_SUB,
                                CASE WHEN SUB_CONSULTA.CANTIDAD IS NULL THEN '1' ELSE SUB_CONSULTA.CANTIDAD END AS CANTIDAD_SUB,
                                CASE WHEN SUB_CONSULTA.IMPORTE IS NULL THEN CONVERT(VARCHAR,Planilla_Chacras.PrecioUnitario) ELSE CONVERT(VARCHAR,SUB_CONSULTA.IMPORTE) END AS IMPORTE_SUB,
                                CASE WHEN Planilla_Chacras.E IS NULL THEN '#fbbc05' WHEN Planilla_Chacras.E = 'P' THEN '#fbbc05' WHEN Planilla_Chacras.E = 'S' THEN '#34a853' END AS ESTADO
                        FROM   Planilla_Chacras INNER JOIN
                                    TresAses_ISISPayroll.dbo.Empleados ON Planilla_Chacras.Legajo = TresAses_ISISPayroll.dbo.Empleados.CodEmpleado INNER JOIN
                                    TresAses_ISISPayroll.dbo.CentrosCostos ON Planilla_Chacras.Centro = TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo INNER JOIN
                                    S3A.dbo.Chacra ON Planilla_Chacras.Lote = S3A.dbo.Chacra.IdChacra LEFT JOIN
                                    (SELECT CASE QR WHEN '' THEN NULL ELSE QR END AS QR, Tarea, COUNT(*) AS CONTEO, CASE WHEN COUNT(*) = 1 THEN '1' WHEN COUNT(*) = 2 THEN '0.5' WHEN COUNT(*) = 3 THEN '0.33' WHEN COUNT(*) = 4 THEN '0.25' END AS CANTIDAD,
                                            ROUND(CONVERT(DECIMAL(10, 2), PrecioUnitario / COUNT(*)), 2) AS IMPORTE
                                        FROM Planilla_Chacras
                                        GROUP BY QR, Tarea,PrecioUnitario) AS SUB_CONSULTA ON Planilla_Chacras.QR = SUB_CONSULTA.QR 
                        WHERE CONVERT(DATE, Planilla_Chacras.Fecha) >= @@Inicio AND CONVERT(DATE, Planilla_Chacras.Fecha) <= @@Final
                            AND (@@Centro = '0' OR Planilla_Chacras.Centro = @@Centro)
                            AND (@@Pago = '0' OR Planilla_Chacras.Pago = @@Pago)
                            AND (@@Legajo = '0' OR Planilla_Chacras.Legajo = @@Legajo)
                            AND (@@Descripcion  = '0' OR Planilla_Chacras.Descripcion = @@Descripcion)
                            AND (Planilla_Chacras.E <> 'E' OR Planilla_Chacras.E IS NULL)
                        ORDER BY NOMBRE
                    """
                    cursor.execute(sql, values)
                    results = cursor.fetchall()
                    if results:
                        listado_tabla = []
                        for row in results:
                            #ID	LEGAJO	NOMBRE	CENTRO	CATEGORIA	DESCRIPCION	TAREA	CANT_DIAS	TIPO	PAGO	CHACRA	CONTEO_SUB	CANTIDAD_SUB	IMPORTE_SUB	ESTADO
                            idAdiconal = str(row[0])
                            legajo = str(row[1])
                            nombre = str(row[2])
                            centro = str(row[3])
                            cat = str(row[4])
                            desc = str(row[5])
                            tarea = str(row[6])
                            dias = str(row[7])
                            tipo = str(row[8])
                            pago = str(row[9])
                            chacra = str(row[10])
                            cantidad = str(row[12])
                            importe = formatear_moneda(str(row[13]))
                            estado = str(row[14])
                            datos = {'Id': idAdiconal, 'Legajo': legajo, 'Nombre': nombre, 'Centro':centro, 'Categoria':cat, 'Descripcion':desc, 'Tarea':tarea, 'Dias':dias,
                                     'Tipo':tipo, 'Pago':pago, 'Chacra':chacra, 'Cantidad':cantidad, 'Importe':importe, 'Estado':estado}
                            listado_tabla.append(datos)
                        return JsonResponse({'Message': 'Success', 'Datos': listado_tabla})
                    else:
                        return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})

            except Exception as e:
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Hubo un error al intentar resolver la petición. ' + str(e) })
            finally:
                cursor.close()
                connections['TRESASES_APLICATIVO'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
