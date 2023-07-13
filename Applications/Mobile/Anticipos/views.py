from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from S3A.conexionessql import *
import json

from django.db import connections
from django.http import JsonResponse

# Create your views here.


###  METODO POST PARA PODER INSERTAR LOS ANTICIPOS EN SQL
@csrf_exempt
def insert_anticipos(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            datos = json.loads(body)['Data']
            listaExistentes = []
            listaFechas = []
            verifica= 0
            for item in datos:
                Regis_Epl = item['Regis_Epl'] ### ID LEGAJO
                Fecha = item['Fecha']### FECHA DEL ADELANTO
                Importe = item['Importe'] ### IMPORTE ADELANTO
                Motivo = item['MotivoAd'] ### MOTIVO ADELANTO
                Estado = item['Regis_TEA'] ### EESTADO ADELANTO
                Tipo = item['Regis_TLE'] ### TIPO DE LIQUIDACIÓN ADELANTO               

                ### VERIFICAR SI OBTUVO MAS DE DOS ADELANTOS DENTRO DEL MES

                with connections['ISISPayroll'].cursor() as cursor:
                    sql = "SELECT COUNT(Regis_EAd) AS Cantidad "\
                        "FROM EmpleadoAdelantos "\
                        "WHERE Regis_Epl = %s AND MONTH(FechaAde) = MONTH(%s) AND YEAR(FechaAde) = YEAR(%s)"
                    cursor.execute(sql, [Regis_Epl, Fecha, Fecha])
                    consulta = cursor.fetchone()
                    if consulta:
                        cantidad = consulta[0]
                        if cantidad > 2:
                            #ACA INSERTA Y MANDA EL CORREO
                            with connections['ISISPayroll'].cursor() as cursor:
                                sql = "INSERT INTO EmpleadoAdelantos (Regis_Epl, FechaAde, ImporteAde, MotivoAde, SaldoAde, Regis_TEA, Regis_TLE, CantCuotasPrest, ImporteCuotaPrest, UltCuotaDesconPrest, SenDadoBajaPrest, LapsoReorganizado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                values = (Regis_Epl, Fecha, Importe, Motivo, Importe, Estado, Tipo, '0', '0.00', '0', '0', '0')
                                cursor.execute(sql, values)
                                cursor.close()
                            nota = "Los registros se guardaron exitosamente."
                            return JsonResponse({'Message': 'Success', 'Nota': nota})
                        else:
                            with connections['ISISPayroll'].cursor() as cursor:
                                sql = "INSERT INTO EmpleadoAdelantos (Regis_Epl, FechaAde, ImporteAde, MotivoAde, SaldoAde, Regis_TEA, Regis_TLE, CantCuotasPrest, ImporteCuotaPrest, UltCuotaDesconPrest, SenDadoBajaPrest, LapsoReorganizado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                values = (Regis_Epl, Fecha, Importe, Motivo, Importe, Estado, Tipo, '0', '0.00', '0', '0', '0')
                                cursor.execute(sql, values)
                                cursor.close()
                            nota = "Los registros se guardaron exitosamente."
                            return JsonResponse({'Message': 'Success', 'Nota': nota})
                    else:
                        verifica = verifica + 1
                        ### ACA ES PORQUE NO RECIBIÓ ADELANTO DENTRO DEL MES INSERTA EL ADELANTO
                        print("INSERTA: " + Regis_Epl + " - " + Fecha + " - " + Importe + " - " + Motivo + " - " + Estado + " - " + Tipo)
                        with connections['ISISPayroll'].cursor() as cursor:
                            sql = "INSERT INTO EmpleadoAdelantos (Regis_Epl, FechaAde, ImporteAde, MotivoAde, SaldoAde, Regis_TEA, Regis_TLE, CantCuotasPrest, ImporteCuotaPrest, UltCuotaDesconPrest, SenDadoBajaPrest, LapsoReorganizado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            values = (Regis_Epl, Fecha, Importe, Motivo, Importe, Estado, Tipo, '0', '0.00', '0', '0', '0')
                            cursor.execute(sql, values)
                            cursor.close()
                        nota = "Los registros se guardaron exitosamente."
                        return JsonResponse({'Message': 'Success', 'Nota': nota})

            # if len(listaExistentes) == 0:
            #     print("GUARDA ANTICIPOS!!!")
            #     nota = "Los registros se guardaron exitosamente."
            #     return JsonResponse({'Message': 'Success', 'Nota': nota})
            # else:
            #     if verifica != 0:
            #         Data = []
            #         index = 0
            #         for item in listaExistentes:
            #             fechaExistente = listaFechas[index]
            #             with connections['ISISPayroll'].cursor() as cursor:
            #                 sql = "SELECT Empleados.CodEmpleado AS LEGAJO, Empleados.ApellidoEmple AS APELLIDO, '$ ' + CONVERT(VARCHAR, EmpleadoAdelantos.ImporteAde) AS MONTO "\
            #                     "FROM Empleados INNER JOIN "\
            #                                             "EmpleadoAdelantos ON Empleados.Regis_Epl = EmpleadoAdelantos.Regis_Epl "\
            #                     "WHERE (Empleados.Regis_Epl = %s AND MONTH(EmpleadoAdelantos.FechaAde) = MONTH(%s) AND YEAR(EmpleadoAdelantos.FechaAde) = YEAR(%s)) "
            #                 cursor.execute(sql, [item, fechaExistente, fechaExistente])
            #                 consulta = cursor.fetchall()
            #                 if consulta:
            #                     for row in consulta:
            #                         leg = str(row[0])
            #                         apellido = str(row[1])
            #                         monto = str(row[2])
            #                         user = {'Legajo': leg, 'Apellido': apellido, 'Monto': monto}
            #                         Data.append(user)
            #         print("GUARDA ANTICIPOS Y DEVUELVE LOS YA CARGADOS")
            #         nota = "Se guardaron los anticipos, los siguientes ya tienen un adelanto este mes: "
            #         return JsonResponse({'Message': 'SuccessData', 'Nota': nota, 'Data' : Data})    
            #     else:
            #         Data = []
            #         index = 0
            #         for item in listaExistentes:
            #             fechaExistente = listaFechas[index]
            #             with connections['ISISPayroll'].cursor() as cursor:
            #                 sql = "SELECT Empleados.CodEmpleado AS LEGAJO, Empleados.ApellidoEmple AS APELLIDO, '$ ' + CONVERT(VARCHAR, EmpleadoAdelantos.ImporteAde) AS MONTO "\
            #                     "FROM Empleados INNER JOIN "\
            #                                             "EmpleadoAdelantos ON Empleados.Regis_Epl = EmpleadoAdelantos.Regis_Epl "\
            #                     "WHERE (Empleados.Regis_Epl = %s AND MONTH(EmpleadoAdelantos.FechaAde) = MONTH(%s) AND YEAR(EmpleadoAdelantos.FechaAde) = YEAR(%s)) "
            #                 cursor.execute(sql, [item, fechaExistente, fechaExistente])
            #                 consulta = cursor.fetchall()
            #                 if consulta:
            #                     for row in consulta:
            #                         leg = str(row[0])
            #                         apellido = str(row[1])
            #                         monto = str(row[2])
            #                         user = {'Legajo': leg, 'Apellido': apellido, 'Monto': monto}
            #                         Data.append(user)
            #         print("DEVUELVE LOS ANTICIPOS YA CARGADOS")
            #         nota = "No se cargaron los Anticipos, ya tienen el adelanto dentro del mes: "
            #         return JsonResponse({'Message': 'Success', 'Nota': nota, 'Data' : Data})           
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['ISISPayroll'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})