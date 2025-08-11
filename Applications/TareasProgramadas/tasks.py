from django.db import connections
from Applications.NotificacionesPush.notificaciones_push import notificaciones_Fruit_Truck, enviar_notificacion_Tres_Ases
from S3A.funcionesGenerales import *
from django.core.mail import send_mail
import datetime
import locale


def traeLegajosISIS():
    try:
        with connections['ISISPayroll'].cursor() as cursor:
            sql = "SELECT        Empleados.CodEmpleado AS LEGAJO " \
                "FROM            Empleados INNER JOIN " \
                                        "CentrosCostos CC  ON Empleados.Regis_CCo = CC.Regis_CCo " \
                "WHERE CC.DescrCtroCosto  LIKE 'C%' AND Empleados.BajaDefinitivaEmple = '2' " \
                "ORDER BY Empleados.CodEmpleado "
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                lista_Legajos_ISIS = []
                for row in consulta:
                    lista_Legajos_ISIS.append(str(row[0]))
            return lista_Legajos_ISIS
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","traeLegajosISIS","request.user",str(e))
    finally:
        connections['ISISPayroll'].close()

def buscaLegajosPRINCIPAL():
    try:
        legajos_no_principal = []
        legajos_de_ISIS = traeLegajosISIS()
        for i in legajos_de_ISIS:
            with connections['principal'].cursor() as cursor:
                sql = "SELECT legLegajo " \
                "FROM T_Legajos " \
                "WHERE legLegajo = %s"
                cursor.execute(sql, [i])
                consulta = cursor.fetchone()
                if consulta:
                    pass
                else:
                    legajos_no_principal.append(i)
        return legajos_no_principal
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","traeLegajosPRINCIPAL","request.user",str(e))
    finally:
        connections['principal'].close()

def traeLegLegajo(legajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "SELECT legCodigo FROM T_Legajos WHERE legLegajo = %s "
            cursor.execute(sql, [str(legajo)])
            consulta = cursor.fetchone()
            if consulta:
                legCodigo = str(consulta[0])
                return legCodigo
            else:
                return 0
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","traeLegLegajo","request.user",str(e))
    finally:
        connections['principal'].close()

def insertaLegajosDatos(legLegajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "INSERT INTO T_Legajos_Datos (legCodigo, tacCodigo01, tacCodigo02) VALUES ( %s, '-1', '-1')"
            cursor.execute(sql, [str(legLegajo)])
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","insertaLegajosDatos","request.user",str(e))
    finally:
        connections['principal'].close()

def insertaLegajosTurnos_A(legLegajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = " INSERT INTO T_Legajos_Turnos (tltComienzo, tltFin, turCodigo, legCodigo, tltPrioridad) VALUES ('1900-01-01T00:00:00.000', '9999-12-31T00:00:00.000', '3', %s, '0')"
            cursor.execute(sql, [str(legLegajo)])
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","insertaLegajosTurnos_A","request.user",str(e))
    finally:
        connections['principal'].close()

def insertaLegajosTurnos_B(legLegajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "INSERT INTO T_Legajos_Turnos (tltComienzo, tltFin, turCodigo, legCodigo, tltPrioridad) VALUES ('1900-01-01T00:00:00.000', '9999-12-31T00:00:00.000', '1', %s, '1')"
            cursor.execute(sql, [str(legLegajo)])
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","insertaLegajosTurnos_B","request.user",str(e))
    finally:
        connections['principal'].close()

def insertaSonidosLegajos(legLegajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "INSERT INTO T_SonidosLegajos (legCodigo, snlArchivo) VALUES (%s, '(Ninguno)')"
            cursor.execute(sql, [str(legLegajo)])
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","insertaSonidosLegajos","request.user",str(e))
    finally:
        connections['principal'].close()

def insertaTarjetaPeriodo_A(legLegajo):
    legTarjeta = str(legLegajo.zfill(8))
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "INSERT INTO T_Tarjetas_Por_Periodo (legCodigo, tarNumero, tarDesde, tarHasta) VALUES (%s, %s, '1900-01-01T00:00:00.000', '9999-12-31T00:00:00.000')"
            values = (str(legLegajo), legTarjeta)
            cursor.execute(sql, values)
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","insertaTarjetaPeriodo_A","request.user",str(e))
    finally:
        connections['principal'].close()

def insertaTarjetaPeriodo_B(legLegajo):
    legTarjeta = str(legLegajo.zfill(8))
    try:
        with connections ['principal'].cursor() as cursor:
            sql = " INSERT INTO T_Tarjetas_Por_Periodo (legCodigo, tarNumero, tarDesde, tarHasta) VALUES (%s, %s, '2023-07-01T00:00:00.000', '9999-12-31T00:00:00.000')"
            values = (str(legLegajo), legTarjeta)
            cursor.execute(sql, values)
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","insertaTarjetaPeriodo_B","request.user",str(e))
    finally:
        connections['principal'].close()

def traeNombreISIS(legajo):
    try:
        with connections ['ISISPayroll'].cursor() as cursor:
            sql = "SELECT CONVERT(VARCHAR(40),RTRIM(ApellidoEmple) + ' ' + RTRIM(NombresEmple)) AS NOMBREyAPELLIDO " \
            "FROM Empleados " \
            "WHERE CodEmpleado = %s "
            cursor.execute(sql, [str(legajo)])
            consulta = cursor.fetchone()
            if consulta:
                nombre = str(consulta[0])
                return nombre
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","traeNombreISIS","request.user",str(e))
    finally:
        connections['ISISPayroll'].close()

def actualiza(codigo):
    legTarjeta = completar_ceros(codigo)
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "UPDATE T_Legajos SET legTarjeta = %s WHERE legCodigo = %s"
            cursor.execute(sql, [legTarjeta,codigo])

    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","actualiza","request.user",str(e))
    finally:
        connections['principal'].close()

def completar_ceros(numero_str):
    longitud_deseada = 8
    ceros_faltantes = longitud_deseada - len(numero_str)
    if ceros_faltantes > 0:
        numero_completo = "0" * ceros_faltantes + numero_str
    else:
        numero_completo = numero_str
    return numero_completo

def TrasladoLegajos():
    legajos_no_principal = buscaLegajosPRINCIPAL()
    for i in legajos_no_principal:
        legajo = str(i)
        try:
            nombres = traeNombreISIS(legajo)
            with connections ['principal'].cursor() as cursor:
                sql = "INSERT INTO T_Legajos (legLegajo, legNombre, tdpCodigo, legActivo, secCodigo, tdcCodigo, legValorHora, legFechaDeIngreso, legTarjeta, legCUIL, legDireccion, legLocalidad, legTelefono, legDocumento, " \
                            "legLimitarTarde, legMinutosTarde, legAplicarTolerancia, legToleranciaEntrada, legToleranciaSalida, horCodigo, tdhCodigoHoraAusente, tdhCodigoHoraTarde, tdhCodigoHoraComision, tdhCodigoHoraPorDefecto, " \
                            "tdhCodigoHoraAusenteFeriado, tdhCodigoHoraAlmuerzo, legAutoimputarAusenteFeriado, legObservaciones, legFoto, msgNumero, legSuspendido, legClave, legIdentificacion, empCodigo, legAlmuerzo, legES, legIntermedias, " \
                            "legPrimerYUltimaFichada, ccoCodigo, legFeriados, legAntiPassBack, legTicketMostrar, legTicketTexto1, legTicketTexto2, carCodigo, legTipoDeDocumento, legSexo, legEstadoCivil, legBarrio, legCP, " \
                            "proCodigo, legFax, osoCodigo, legNroObraSocial, afjpCodigo, legNroAFJP, legNroANSES, legDireccionEventual, legLocalidadEventual, legCPEventual, proCodigoEventual, legBarrioEventual, legTelefonoEventual, " \
                            "legFaxEventual, legEMailPersonal, legEMailLaboral, legEntreCalles, legEntreCallesEventual, legCalle1, legCalle2, legCalle3, legCalle4, legSeleccionDeTurno, legPermitirVisitas, legPermitirMultiplesVisitas, " \
                            "legIDIN1, legTicket, legSubTicket, legInterno, legPermitirControlAcceso, legPermitirControlHorario, legIdentificacionIN1, legSecurityLevelIN1, legMostrarNombreIN1, legMensajeIN1, legFuncionContratista, tdhCodigoHoraAlmFueraDeHorario, " \
                            "tdhCodigoHoraExcesoAlmuerzo, tdhCodigoHoraSalidaAnticipada, tdhCodigoHoraIncongruenciaRegistro, tdhCodigoHoraRegistracionIncompleta, repCodigo, legNroDeRolMETA4, legExcluirAPICentral, legEnviarBioTarjeta, legEnviarBioID) VALUES " \
                            "(%s, %s, '10', '1', '19', '49', '0', '2023-07-01T00:00:00.000', %s, '', '', '', '', '', '1', '15', '1', '0', '0', '0', '2', '1', '5', '3', '11', '18', '1', '', '', '0', '0', '', '0', '1', '0', '0', '2', " \
                            "'0', '17', '0', '0', '1', '', '', '-1', '-1', '-1', '-1', '', '', '-1', '', '-1', '', '-1', '', '', '', '', '', '-1', '', '', '', '', '', '', '', '', '', '', '', '0', '0', '0', '', '-1', '-1', '', '1', '1', '2', '1', '0', '', '0', " \
                            "'16', '15', '14', '17', '14', '-1', '0', '0', '1', '1')"
                values = (legajo, nombres, str(legajo.zfill(8)))
                cursor.execute(sql, values)
        except Exception as e:
            insertar_registro_error_sql("TareasProgramadas","TrasladoLegajos","request.user",str(e))
        finally:
            connections['principal'].close()

        legLegajo = traeLegLegajo(legajo)

        if legLegajo != 0:
            insertaLegajosDatos(legLegajo)
            insertaLegajosTurnos_A(legLegajo)
            insertaLegajosTurnos_B(legLegajo)
            insertaSonidosLegajos(legLegajo)
            #insertaTarjetaPeriodo_A(legLegajo)
            #insertaTarjetaPeriodo_B(legLegajo)
            actualiza(legLegajo)





############################################################################################################################
############################################################################################################################
###################################### PROCESA HORAS EXTRAS ################################################################
############################################################################################################################
############################################################################################################################


def obtener_solo_fecha(fechaYhora):
    fecha = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    fecha_str = fecha.strftime("%Y-%m-%d")
    return fecha_str

##### DOMINGO HORAS INICIALES
def Domingo_HoraExtraNocturna_00_a_05_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 0)  
    hora_fin = datetime.time(4, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    
def Domingo_HoraExtra100_05_a_20_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(5, 0)  
    hora_fin = datetime.time(19, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    
def Domingo_HoraExtraNocturna_20_a_00_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(20, 0)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False

##### DOMINGO HORAS FINALES
def Domingo_HoraExtraNocturna_00_a_05_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 1)  
    hora_fin = datetime.time(5, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
    
def Domingo_HoraExtra100_05_a_20_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(5, 1)  
    hora_fin = datetime.time(20, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
    
def Domingo_HoraExtraNocturna_20_a_00_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(20, 1)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    
##### SÁBADO HORAS INICIALES
def Sabado_HoraExtraNocturna_00_a_05_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 0)  
    hora_fin = datetime.time(4, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    
def Sabado_HoraExtraAl50_05_a_13_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(5, 0)  
    hora_fin = datetime.time(12, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    

def Sabado_HoraExtraAl100_13_a_20_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(13, 0)  
    hora_fin = datetime.time(19, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    
def Sabado_HoraExtraNocturnas_20_a_00_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(20, 0)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    
##### SÁBADO HORAS FINALES
def Sabado_HoraExtraNocturna_00_a_05_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 1)  
    hora_fin = datetime.time(5, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
    
def Sabado_HoraExtraAl50_05_a_13_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(5, 1)  
    hora_fin = datetime.time(13, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False

def Sabado_HoraExtraAl100_13_a_20_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(13, 1)  
    hora_fin = datetime.time(20, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
    
def Sabado_HoraExtraNocturnas_20_a_00_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(20, 1)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
    
##### LUNES A VIERNES INICIALES
def LV_HoraExtraNocturna_00_a_05_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 0)  
    hora_fin = datetime.time(4, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    
def LV_HoraExtraAl50_05_a_20_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(5, 0)  
    hora_fin = datetime.time(19, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False
    
def LV_HoraExtraNocturna_20_a_00_Inicio(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(20, 0)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False

##### LUNES A VIERNES HORAS
def LV_HoraExtraNocturna_00_a_05_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 1)  
    hora_fin = datetime.time(5, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
    
def LV_HoraExtraAl50_05_a_20_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(5, 1)  
    hora_fin = datetime.time(20, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
    
def LV_HoraExtraNocturna_20_a_00_Final(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(20, 1)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False


##### EMPAQUE HORAS A PROCESAR DE EMPAQUE
def LV_Hora100_00_a_04_Inicio_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 0)  
    hora_fin = datetime.time(3, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False

def LV_Hora100_00_a_04_Final_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 1)  
    hora_fin = datetime.time(4, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False

def LV_Hora50_04_a_00_Inicio_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(4, 0)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False

def LV_Hora50_04_a_00_Final_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(4, 1)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
        
def Sabado_Hora50_04_a_13_Inicio_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(4, 0)  
    hora_fin = datetime.time(12, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False

def Sabado_Hora50_04_a_13_Final_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(4, 1)  
    hora_fin = datetime.time(13, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False

def Sabado_Hora100_13_a_00_Inicio_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(13, 0)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False

def Sabado_Hora100_13_a_00_Final_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(13, 1)  
    hora_fin = datetime.time(23, 59)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
 
def Sabado_Hora100_00_a_04_Inicio_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 0)  
    hora_fin = datetime.time(3, 59)  
    hora = fecha_hora.time()

    if hora >= hora_inicio and hora < hora_fin:
        return True
    else:
        return False

def Sabado_Hora100_00_a_04_Final_Empaque(fechaYhora):
    fecha_hora = datetime.datetime.strptime(fechaYhora, "%Y-%m-%d %H:%M")
    hora_inicio = datetime.time(0, 1)  
    hora_fin = datetime.time(4, 0)  
    hora = fecha_hora.time()

    if hora > hora_inicio and hora <= hora_fin:
        return True
    else:
        return False
 

### OBTENGO EL DIA SIGUIENTE SI LA HORA ES 23:59
def obtener_dia_siguiente(fechaHora):
    from datetime import datetime, timedelta
    fechaHora = datetime.strptime(fechaHora, '%Y-%m-%d %H:%M')
    if fechaHora.hour == 23 and fechaHora.minute == 59:
        dia_siguiente = fechaHora + timedelta(days=1)
        dia_siguiente = dia_siguiente.replace(hour=0, minute=0)
        return dia_siguiente.strftime('%Y-%m-%d %H:%M')
    else:
        return fechaHora.strftime('%Y-%m-%d %H:%M')

### CALCULA LA CANTIDAD DE HORAS
def calcular_diferencia_horas(hora_inicial, hora_final):
    formato = "%Y-%m-%d %H:%M"
    hora_inicial_dt = datetime.datetime.strptime(hora_inicial, formato)
    hora_final_dt = datetime.datetime.strptime(hora_final, formato)
    diferencia = hora_final_dt - hora_inicial_dt
    horas = diferencia.total_seconds() / 3600
    return round(horas, 2)

### VERFICO SI LA HORA ESTA EN EL MISMO O DIFERENTE DÍA
def Mismo_o_Diferente_dia(ID,fecha1, fecha2):
    formato = "%Y-%m-%d %H:%M"
    f1 = datetime.datetime.strptime(fecha1, formato)
    f2 = datetime.datetime.strptime(fecha2, formato)

    # VERIFICA SI LAS FECHAS ESTÁN EN DIFERENTE DIA
    if f1.date() != f2.date():
        # SI ESTÁN EN DIFERENTE DÍA MANDA 4 FECHAS
        f1_a = f1
        f1_b = datetime.datetime(f1.year, f1.month, f1.day, 23, 59)
        f2_a = datetime.datetime(f2.year, f2.month, f2.day, 0, 0)
        f2_b = f2
        lista_diferente_dia = [ID + "*" + str(f1_a.strftime(formato)), ID + "*" + str(f1_b.strftime(formato)), ID + "*" + str(f2_a.strftime(formato)), ID + "*" + str(f2_b.strftime(formato))]
        
        return lista_diferente_dia
    
    lista_mismo_dia = [ID + "*" + str(fecha1),ID + "*" + str(fecha2)]

    return lista_mismo_dia

### OBTENGO EL DÍA DE LA SEMANA DADO LA CADENA DE FECHA HORA
def obtener_dia_semana(fecha):
    fechas = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M")
    locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
    dia_semana = fechas.strftime("%A")
    return dia_semana.capitalize()

### ME TRAE UNA LISTA QUE CONTIENE LISTAS CON LA CANTIDAD DE DÍAS QUE ENCUENTRA1d95d463cee8958b17d1186a697a3ac1
def trae_lista_con_listado():
    listado_HE_por_dia = []
    lista_HE_sin_proceso = llama_horas_extras_no_procesadas()
    for item in lista_HE_sin_proceso:
        ID = str(item[0])
        Desde = str(item[1])
        Hasta = str(item[2])
        listado_dias = Mismo_o_Diferente_dia(ID,Desde,Hasta)
        listado_HE_por_dia.append(listado_dias)
    return listado_HE_por_dia

#### LLAMA A LOS DATOS CON EL ID DE LA HORA SIN PROCESAR PAA INSRTAR EN LA HORA PROCESADA
def insertaEnProcesados(legajo, desde, hasta, idMotivo, descripcion, autorizado, user, tipoHora, CantidadHoras, id_HESP, estado):
    sector = buscaSector(legajo)
    if sector == 'E' or sector == 'F' or sector == 'O':
        estado = '3'
    values = [legajo, desde, hasta, idMotivo, descripcion, autorizado, user, tipoHora, CantidadHoras, sector, id_HESP, estado]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            # Realizar la inserción en la tabla HorasExtras_Procesadas
            sql_insert = "INSERT INTO HorasExtras_Procesadas (Legajo, FechaHoraDesde, FechaHoraHasta, IdMotivo, DescripcionMotivo, Autorizado, UsuarioEncargado, TipoHoraExtra, CantidadHoras, Sector, ID_HESP, EstadoEnvia) "\
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_insert, values)

            # Realizar la actualización en la tabla HorasExtras_Sin_Procesar
            sql_update = "UPDATE HorasExtras_Sin_Procesar SET Estado = '0' WHERE ID_HESP = %s"
            cursor.execute(sql_update, [id_HESP])

    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","insertaEnProcesados","request.user",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

### BUSCA SECTOR A INSERTAR 
def buscaSector(legajo):
    sector = "N/S"
    try:
        with connections['ISISPayroll'].cursor() as cursor:
            sql = "SELECT        SUBSTRING(LTRIM(CentrosCostos.DescrCtroCosto), 1, 1) AS SECTOR " \
                    "FROM            Empleados INNER JOIN " \
                                            "CentrosCostos ON Empleados.Regis_CCo = CentrosCostos.Regis_CCo " \
                    "WHERE        (Empleados.CodEmpleado = %s)"
            cursor.execute(sql, [legajo])
            consulta = cursor.fetchone()
            if consulta:
                sector = str(consulta[0])
            return sector
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","buscaSector","request.user",str(e))
    finally:
        cursor.close()
        connections['ISISPayroll'].close()

### CAMBIAR LA CONSULTA PARA OBTENER EL SECTOR DE LA HORA CON EL ID_HESP
def buscaSectorEnHorasExtrasSinProceso(ID_HESP):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT RTRIM(Sector) FROM HorasExtras_Sin_Procesar WHERE ID_HESP = %s "
            cursor.execute(sql, [str(ID_HESP)])
            consulta = cursor.fetchone()
            if consulta:
                sector = str(consulta[0])
            return sector
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","buscaSectorEnHorasExtrasSinProceso","request.user",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

#### LLAMA A LOS DATOS CON EL ID DE LA HORA SIN PROCESAR PAA INSERTAR EN LA HORA PROCESADA
def buscaDatos_paraInsertar(id):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Legajo AS LEGAJO,IdMotivo AS IDMOTIVO, DescripcionMotivo AS DESCRIPCION, Autorizado AS AUTORIZADO, UsuarioEncargado AS ENCARGADO, ID_HESP AS ID " \
                "FROM HorasExtras_Sin_Procesar " \
                "WHERE ID_HESP = %s "
            cursor.execute(sql, [id])
            consulta = cursor.fetchone()
            if consulta:
                legajo = str(consulta[0])
                idMotivo = str(consulta[1])
                descripcion = str(consulta[2])
                autorizado = str(consulta[3])
                encargado = str(consulta[4])
                idSinProceso = str(consulta[5])
            return legajo, idMotivo, descripcion, autorizado, encargado, idSinProceso
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","buscaDatos_paraInsertar","request.user",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

#### LLAMA LAS HORAS EXTRAS NO PROCESADAS
def llama_horas_extras_no_procesadas():
    listado_horas_extras_sin_proceso = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT ID_HESP AS ID, CONVERT(VARCHAR(16), DateTimeDesde, 120) AS DESDE, CONVERT(VARCHAR(16), DateTimeHasta, 120) AS HASTA " \
                "FROM HorasExtras_Sin_Procesar " \
                "WHERE Arreglo = '0' AND Estado <> '0' AND Estado <> '8'"
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                for i in consulta:
                    horas = [str(i[0]), str(i[1]), str(i[2])]
                    listado_horas_extras_sin_proceso.append(horas)
            return listado_horas_extras_sin_proceso
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","llama_horas_extras_no_procesadas","request.user",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

def procesa_arreglos():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Legajo AS LEGAJO, CONVERT(VARCHAR(16), DateTimeDesde, 120) AS DESDE, CONVERT(VARCHAR(16), DateTimeHasta, 120) AS HASTA, " \
                        "IdMotivo AS ID_MOTIVO, DescripcionMotivo AS DESCRIPCION, Autorizado AS AUTORIZADO, UsuarioEncargado AS USUARIO, ID_HESP AS ID, ImpArreglo AS IMPORTE " \
                "FROM HorasExtras_Sin_Procesar " \
                "WHERE Arreglo = '1' AND Estado <> '0' AND Estado <> '8'"
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                for i in consulta:
                    legajo = str(i[0])
                    desde = str(i[1]) + ":00.000".replace(' ','T')
                    hasta = str(i[2]) + ":00.000".replace(' ','T')
                    motivo = str(i[3])
                    descripcion = str(i[4])
                    autorizado = str(i[5])
                    user = str(i[6])
                    tipoHora = "A"
                    cantidadHoras = calcular_diferencia_horas(str(i[1]),str(i[2]))
                    ID_HESP = str(i[7])
                    Importe = str(i[8])
                    estado = "1"
                    insertaArreglosEnProcesados(legajo,desde,hasta,motivo,descripcion,autorizado,user,tipoHora,cantidadHoras,ID_HESP,estado,Importe)

    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","procesa_arreglos","request.user",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

def insertaArreglosEnProcesados(legajo, desde, hasta, idMotivo, descripcion, autorizado, user, tipoHora, CantidadHoras, id_HESP, estado, importe):
    sector = buscaSector(legajo)
    if sector == 'E' or sector == 'O' or sector == 'F':
        estado = '3'
    values = [legajo, desde, hasta, idMotivo, descripcion, autorizado, user, tipoHora, CantidadHoras, sector, id_HESP, estado, importe]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            # Realizar la inserción en la tabla HorasExtras_Procesadas
            sql_insert = "INSERT INTO HorasExtras_Procesadas (Legajo, FechaHoraDesde, FechaHoraHasta, IdMotivo, DescripcionMotivo, Autorizado, UsuarioEncargado, TipoHoraExtra, CantidadHoras, Sector, ID_HESP, EstadoEnvia, ImpArreglo) "\
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_insert, values)

            # Realizar la actualización en la tabla HorasExtras_Sin_Procesar
            sql_update = "UPDATE HorasExtras_Sin_Procesar SET Estado = '0' WHERE ID_HESP = %s"
            cursor.execute(sql_update, [id_HESP])

    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","insertaEnProcesados","request.user",str(e))
    finally:
        cursor.close()
        connections['TRESASES_APLICATIVO'].close()

### FUNCION QUE INSERTA LOS DATOS CUANDO SE EJECUTA LA TAREA
def InsertaInicioFinal(ID,Inicio,Final):
    diaSemana = obtener_dia_semana(Inicio)
    sector = str(buscaSectorEnHorasExtrasSinProceso(ID))

################################# LUNES A VIERNES ##################################
    if diaSemana in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
        if sector == 'C':
            soloFecha = obtener_solo_fecha(Inicio)

            Inicio_Nocturna_00_05 = LV_HoraExtraNocturna_00_a_05_Inicio(Inicio)
            Inicio_Al50_05_20 = LV_HoraExtraAl50_05_a_20_Inicio(Inicio)
            Inicio_Nocturna_20_00 = LV_HoraExtraNocturna_20_a_00_Inicio(Inicio)

            Final_Nocturna_00_05 = LV_HoraExtraNocturna_00_a_05_Final(Final)
            Final_Al50_05_20 = LV_HoraExtraAl50_05_a_20_Final(Final)
            Final_Nocturna_20_00 = LV_HoraExtraNocturna_20_a_00_Final(Final)

            if Inicio_Nocturna_00_05:
                if Final_Nocturna_00_05:
                    ##### HORA EMPIEZA Y TERMINA ENTRE LAS 00/05
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                if Final_Al50_05_20:
                    #### EMPIEZA ENTRE 00/05 Y TERMINA ENTRE 05/20 AL 50%
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 05:00"
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 05:00"
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                if Final_Nocturna_20_00:
                    #### EMPIEZA 00/05 PASA POR 05/20 Y TERMINA EN 20/00
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 05:00"
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 05:00"
                    horaFinal = soloFecha + " 20:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 20:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)               

            if Inicio_Al50_05_20:
                if Final_Al50_05_20:
                    #### INICIA EN 05/20 Y TERMINE 05/20
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                if Final_Nocturna_20_00:
                    #### INICIA 05/20 Y TERMINA 20/00
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 20:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 20:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                            
            if Inicio_Nocturna_20_00:
                #### INICIA 20/00 Y TERMINA 20/00
                horaInicio = Inicio
                horaFinal = obtener_dia_siguiente(Final)
                estado = "1"
                tipoHora = "N"
                cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                desdeSin = horaInicio.replace(' ', 'T')
                hastaSin = horaFinal.replace(' ', 'T')
                desde = desdeSin + ":00.000"
                hasta = hastaSin + ":00.000"
                insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
        if sector == 'E' or sector == 'F' or sector == 'O':
            ###PROCESAR LAS HORAS DE EMPAQUE
            soloFecha = obtener_solo_fecha(Inicio)

            Inicio_100_00_04_Empaque = LV_Hora100_00_a_04_Inicio_Empaque(Inicio)
            Final_100_00_04_Empaque = LV_Hora100_00_a_04_Final_Empaque(Final)

            Inicio_50_04_00_Empaque = LV_Hora50_04_a_00_Inicio_Empaque(Inicio)
            Final_50_04_00_Empaque = LV_Hora50_04_a_00_Final_Empaque(Final)

            # data = str(ID) + " - " + str(Inicio_100_00_04_Empaque) + "-" + str(Final_100_00_04_Empaque)+ "-" + str(Inicio_50_04_13_Empaque) + "-" + str(Final_50_04_13_Empaque) + "-" + str(Inicio_100_13_00_Empaque) + "-" + str(Final_100_13_00_Empaque)
            # inyectaData("InsertaInicioFinal-Semana",data,str(Inicio), str(soloFecha),str(Final),diaSemana, sector)

            if Inicio_100_00_04_Empaque:
                if Final_100_00_04_Empaque:
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                if Final_50_04_00_Empaque:
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 04:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)

                    horaInicio = soloFecha + " 04:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
            if Inicio_50_04_00_Empaque:
                horaInicio = Inicio
                horaFinal = obtener_dia_siguiente(Final)
                estado = "1"
                tipoHora = "50"
                cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                desdeSin = horaInicio.replace(' ', 'T')
                hastaSin = horaFinal.replace(' ', 'T')
                desde = desdeSin + ":00.000"
                hasta = hastaSin + ":00.000"
                insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
################################## SÁBADO #########################################
    if diaSemana == "Sábado":
        if sector == 'C':
            soloFecha = obtener_solo_fecha(Inicio)

            Inicio_Nocturna_00_05 = Sabado_HoraExtraNocturna_00_a_05_Inicio(Inicio)
            Inicio_Al50_05_13 = Sabado_HoraExtraAl50_05_a_13_Inicio(Inicio)
            Inicio_Al100_13_20 = Sabado_HoraExtraAl100_13_a_20_Inicio(Inicio)
            Inicio_Nocturna_20_00 = Sabado_HoraExtraNocturnas_20_a_00_Inicio(Inicio)

            Final_Nocturna_00_05 = Sabado_HoraExtraNocturna_00_a_05_Final(Final)
            Final_Al50_05_13 = Sabado_HoraExtraAl50_05_a_13_Final(Final)
            Final_Al100_13_20 = Sabado_HoraExtraAl100_13_a_20_Final(Final)
            Final_Nocturna_20_00 = Sabado_HoraExtraNocturnas_20_a_00_Final(Final)

            if Inicio_Nocturna_00_05:
                if Final_Nocturna_00_05:
                    #### INICIA Y TERMINA ENTRE 00/05
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                            
                if Final_Al50_05_13:
                    #### INICIA ENTRE 00/05 Y TERMINA ENTRE 05/13
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 05:00"
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    print(diaSemana)
                    horaInicio = soloFecha + " 05:00"
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                
                if Final_Al100_13_20:
                    #### INICIA ENTRE 00/05, PASA ENTRE 05/13 Y TERMINA ENTRE LAS 13/20
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 05:00"
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 05:00"
                    horaFinal = soloFecha + " 13:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 13:00"
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                if Final_Nocturna_20_00:
                    #### INICIA EN 00/05 PASA POR 05/13, 13/20 Y TERMINA 20/00
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 05:00"
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 05:00"
                    horaFinal = soloFecha + " 13:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 13:00"
                    horaFinal = soloFecha + " 20:00"
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 20:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
            if Inicio_Al50_05_13:
                if Final_Al50_05_13:
                    #### INICIA  Y TERMINA ENTRE 05/13
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                                
                if Final_Al100_13_20:
                    #### INICIA ENTRE  05/13 Y TERMINA ENTRE LAS 13/20
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 13:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 13:00"
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                if Final_Nocturna_20_00:
                    #### INICIA EN 05/13 PASA  13/20 Y TERMINA 20/00
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 13:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 13:00"
                    horaFinal = soloFecha + " 20:00"
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 20:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
            if Inicio_Al100_13_20:
                if Final_Al100_13_20:
                    #### INICIA Y TERMINA ENTRE LAS 13/20
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                if Final_Nocturna_20_00:
                    #### INICIA EN  13/20 Y TERMINA 20/00
                    horaInicio = Inicio
                    #horaInicio = soloFecha + " 13:00"
                    horaFinal = soloFecha + " 20:00"
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 20:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
            if Inicio_Nocturna_20_00:
                #### INICIA Y TERMINA ENTRE LAS 20/00
                horaInicio = Inicio
                horaFinal = obtener_dia_siguiente(Final)
                estado = "1"
                tipoHora = "N"
                cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                desdeSin = horaInicio.replace(' ', 'T')
                hastaSin = horaFinal.replace(' ', 'T')
                desde = desdeSin + ":00.000"
                hasta = hastaSin + ":00.000"
                insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
        if sector == 'E' or sector == 'F' or sector == 'O':
            ### PROCESAR EMPAQUE SABADO
            soloFecha = obtener_solo_fecha(Inicio)

            Inicio_100_00_04_Empaque = Sabado_Hora100_00_a_04_Inicio_Empaque(Inicio)
            Final_100_00_04_Empaque = Sabado_Hora100_00_a_04_Final_Empaque(Final)

            Inicio_50_04_13_Empaque = Sabado_Hora50_04_a_13_Inicio_Empaque(Inicio)
            Final_50_04_13_Empaque = Sabado_Hora50_04_a_13_Final_Empaque(Final)

            Inicio_100_13_00_Empaque = Sabado_Hora100_13_a_00_Inicio_Empaque(Inicio)
            Final_100_13_00_Empaque = Sabado_Hora100_13_a_00_Final_Empaque(Final)

            # data = str(ID) + " - " + str(Inicio_100_00_04_Empaque) + "-" + str(Final_100_00_04_Empaque)+ "-" + str(Inicio_50_04_13_Empaque) + "-" + str(Final_50_04_13_Empaque) + "-" + str(Inicio_100_13_00_Empaque) + "-" + str(Final_100_13_00_Empaque)
            # inyectaData("InsertaInicioFinal-Sabado",data,str(Inicio), str(soloFecha),str(Final),diaSemana, sector)

            if Inicio_100_00_04_Empaque:
                if Final_100_00_04_Empaque:
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                if Final_50_04_13_Empaque:
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 04:00"
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)

                    horaInicio = soloFecha + " 04:00"
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                if Final_100_13_00_Empaque:
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 04:00"
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)

                    horaInicio = soloFecha + " 04:00"
                    horaFinal = soloFecha + " 13:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)

                    horaInicio = soloFecha + " 13:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
            if Inicio_50_04_13_Empaque:
                if Final_50_04_13_Empaque:
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                if Final_100_13_00_Empaque:
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 13:00"
                    estado = "1"
                    tipoHora = "50"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)

                    horaInicio = soloFecha + " 13:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
            if Inicio_100_13_00_Empaque:
                horaInicio = Inicio
                horaFinal = obtener_dia_siguiente(Final)
                estado = "1"
                tipoHora = "100"
                cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                desdeSin = horaInicio.replace(' ', 'T')
                hastaSin = horaFinal.replace(' ', 'T')
                desde = desdeSin + ":00.000"
                hasta = hastaSin + ":00.000"
                insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
################################ DOMINGO ##########################################
    if diaSemana == "Domingo":
        if sector == 'C':
            soloFecha = obtener_solo_fecha(Inicio)
            
            Inicio_Nocturna_00_05 = Domingo_HoraExtraNocturna_00_a_05_Inicio(Inicio)
            Inicio_Al100_05_20 = Domingo_HoraExtra100_05_a_20_Inicio(Inicio)
            Inicio_Nocturna_20_00 = Domingo_HoraExtraNocturna_20_a_00_Inicio(Inicio)

            Final_Nocturna_00_05 = Domingo_HoraExtraNocturna_00_a_05_Final(Final)
            Final_Al100_05_20 = Domingo_HoraExtra100_05_a_20_Final(Final)
            Final_Nocturna_20_00 = Domingo_HoraExtraNocturna_20_a_00_Final(Final)

            if Inicio_Nocturna_00_05:
                if Final_Nocturna_00_05:
                    ##### HORA EMPIEZA Y TERMINA ENTRE LAS 00/05
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                if Final_Al100_05_20:
                    ##### EMPIEZA ENTRE 00/05 Y TERMINA ENTRE 05/20
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 05:00"
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 05:00"
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)

                if Final_Nocturna_20_00:
                    #### INICIA EN 00/05 PASA POR 05/20 Y TERMINA EN 20/00
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 05:00"
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 05:00"
                    horaFinal = soloFecha + " 20:00"
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 20:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
            if Inicio_Al100_05_20:
                if Final_Al100_05_20:
                    horaInicio = Inicio
                    horaFinal = Final
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                if Final_Nocturna_20_00:
                    horaInicio = Inicio
                    horaFinal = soloFecha + " 20:00"
                    estado = "1"
                    tipoHora = "100"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
                    horaInicio = soloFecha + " 20:00"
                    horaFinal = obtener_dia_siguiente(Final)
                    estado = "1"
                    tipoHora = "N"
                    cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                    legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                    desdeSin = horaInicio.replace(' ', 'T')
                    hastaSin = horaFinal.replace(' ', 'T')
                    desde = desdeSin + ":00.000"
                    hasta = hastaSin + ":00.000"
                    insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
                    
            if Inicio_Nocturna_20_00:
                horaInicio = Inicio
                horaFinal = obtener_dia_siguiente(Final)
                estado = "1"
                tipoHora = "N"
                cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
                legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
                desdeSin = horaInicio.replace(' ', 'T')
                hastaSin = horaFinal.replace(' ', 'T')
                desde = desdeSin + ":00.000"
                hasta = hastaSin + ":00.000"
                insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
        if sector == 'E' or sector == 'F' or sector == 'O':
            ### PROCESA DOMINGOS EMPAQUE
            horaInicio = Inicio
            horaFinal = obtener_dia_siguiente(Final)
            estado = "1"
            tipoHora = "100"
            cantidadHoras = str(calcular_diferencia_horas(horaInicio,horaFinal))
            legajo, idMotivo, descripcion, idAutorizado, encargado, idSinProceso = buscaDatos_paraInsertar(ID)
            desdeSin = horaInicio.replace(' ', 'T')
            hastaSin = horaFinal.replace(' ', 'T')
            desde = desdeSin + ":00.000"
            hasta = hastaSin + ":00.000"
            insertaEnProcesados(legajo,desde,hasta,idMotivo,descripcion,idAutorizado,encargado,tipoHora,cantidadHoras,idSinProceso,estado)
#### FUNCION PAR APROCESAR CADA 30 MINUTOS
def procesoHorasExtras():
    if ProcesaActivo() == 1:
        listado_de_listado_de_HE = trae_lista_con_listado()
        for diasLista in listado_de_listado_de_HE:
            cantidad = len(diasLista)

            if cantidad == 2:
                DT1 = str(diasLista[0])
                DT2 = str(diasLista[1])
                ListaDiaUno = DT1.split('*')
                ListaDiaDos = DT2.split('*')
                ID_HoraExtra_MD = str(ListaDiaUno[0])
                Inicio = str(ListaDiaUno[1])
                Final = str(ListaDiaDos[1])
                InsertaInicioFinal(ID_HoraExtra_MD,Inicio,Final)

            if cantidad == 4:
                DT1A = str(diasLista[0])
                DT1B = str(diasLista[1])
                DT2A = str(diasLista[2])
                DT2B = str(diasLista[3])
                ListaDiaUnoA = DT1A.split('*')
                ListaDiaUnoB = DT1B.split('*')
                ListaDiaDosA = DT2A.split('*')
                ListaDiaDosB = DT2B.split('*')
                ID_HoraExtra_DD = str(ListaDiaUnoA[0])
                Inicio_Uno_A = str(ListaDiaUnoA[1])
                Final_Uno_B = str(ListaDiaUnoB[1])
                Inicio_Dos_A = str(ListaDiaDosA[1])
                Final_Dos_B = str(ListaDiaDosB[1])
                InsertaInicioFinal(ID_HoraExtra_DD,Inicio_Uno_A,Final_Uno_B)
                InsertaInicioFinal(ID_HoraExtra_DD,Inicio_Dos_A,Final_Dos_B)

def ProcesaActivo():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Numerico " \
                    "FROM Parametros_Aplicativo " \
                    "WHERE Codigo = 'PROCESA-HE' "
            cursor.execute(sql)
            consulta = cursor.fetchone()
            if consulta:
                data = int(consulta[0])
                return data
        return 0
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","correosChacras","request.user",str(e))
        return 0
    finally:
        connections['TRESASES_APLICATIVO'].close()    



############################################################################################################################
############################################################################################################################
###################################### FINAL PROCESA HORAS EXTRAS ##########################################################
############################################################################################################################
############################################################################################################################



##########################   INICIO DE ENVÍO DE CORREOS #############################################################
# " \
def listadoAnticipos():
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT   CONVERT(VARCHAR(8), TresAses_ISISPayroll.dbo.Empleados.CodEmpleado) + ' - ' + CONVERT(VARCHAR(20), " \
                            "TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) + ' - ' + TresAses_ISISPayroll.dbo.CentrosCostos.AbrevCtroCosto + ' - $ ' + CONVERT(VARCHAR(20), Auditoria_Anticipos.Monto, 2)   " \
                            "+ ' - ' + Auditoria_Anticipos.Tipo + ' - Fecha Solicitud: ' + CONVERT(VARCHAR(10), Auditoria_Anticipos.FechaHora, 103) + ' ' + CONVERT(VARCHAR(5), Auditoria_Anticipos.FechaHora, 108) + ' Hs. - Solicita: ' +  " \
                            "Auditoria_Anticipos.Usuario AS COLUMNA  " \
                    "FROM         TresAses_ISISPayroll.dbo.CentrosCostos INNER JOIN  " \
                                "TresAses_ISISPayroll.dbo.Empleados INNER JOIN  " \
                                "Auditoria_Anticipos ON TresAses_ISISPayroll.dbo.Empleados.Regis_Epl = Auditoria_Anticipos.Destino ON  " \
                                "TresAses_ISISPayroll.dbo.CentrosCostos.Regis_CCo = TresAses_ISISPayroll.dbo.Empleados.Regis_CCo  " \
                    "WHERE     (Auditoria_Anticipos.EstadoCorreo = '1') " \
                    "ORDER BY TresAses_ISISPayroll.dbo.Empleados.CodEmpleado"
            cursor.execute(sql)
            consulta = cursor.fetchall()
            lista_data = []
            if consulta:
                for row in consulta:
                    datos = str(row[0])
                    lista_data.append(datos)
                return lista_data
            else:
                return lista_data
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","listadoAnticipos","request.user",str(e))
        return lista_data
    finally:
        connections['TRESASES_APLICATIVO'].close()

def correosChacras():
    listadoCorreos = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "SELECT Correo " \
                    "FROM Correos " \
                    "WHERE Sector = 'CHACRA' "
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                for i in consulta:
                    correo = str(i[0])
                    listadoCorreos.append(correo)
        return listadoCorreos
    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","correosChacras","request.user",str(e))
        return listadoCorreos
    finally:
        connections['TRESASES_APLICATIVO'].close()

def enviar_correo_sendMail(asunto, mensaje, destinatario):
    remitente = 'aplicativo@tresases.com.ar'
    asunto = 'No Responder - ' + asunto

    send_mail(
        asunto,
        mensaje,
        remitente,
        [destinatario],
        fail_silently=False,
    )

def enviaCorreosAnticipos():
    listado = listadoAnticipos()
    if listado:
        try:
            contenido = 'Se cargaron anticipos de las siguientes personas: \n \n' + ', \n'.join(listado) + '.'
            asunto = 'Carga de Anticipos.'
            listadoCorreos = correosChacras()
            for correo in listadoCorreos:
                enviar_correo_sendMail(asunto,contenido,correo)
            actualizaEstadoAnticipo()
        except Exception as e:
            insertar_registro_error_sql("TareasProgramadas","enviaCorreosAnticipos","request.user",str(e))

def actualizaEstadoAnticipo():
    try:
        with connections ['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "UPDATE Auditoria_Anticipos SET EstadoCorreo = '0' WHERE EstadoCorreo = '1'"
            cursor.execute(sql)

    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","actualizaEstadoAnticipo","request.user",str(e))
    finally:
        connections['TRESASES_APLICATIVO'].close()

def Registro_Errores_SQL(funcion, error):
    try:
        with connections ['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Log_Errores_SQL (Funcion, Error) VALUES (%s, %s)"
            cursor.execute(sql,[funcion,error])

    except Exception as e:
        insertar_registro_error_sql("TareasProgramadas","Registro_Errores_SQL","request.user",str(e))


############################################################################################################################
############################################################################################################################
###################################### INICIO DE NOTIFICACIONES ############################################################
############################################################################################################################
############################################################################################################################


def inserta_resgistros_al_canal():
    try:
        with connections ['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """
                INSERT INTO Canal_Notificaciones_Generales (Titulo, Body, Pestaña, CodEmpleado, FechaAlta, Estado)

                SELECT 'TRES ASES', 'ASISTENCIA NO ENVÍADA - Es necesario envíar la asistencia para registrar los días del trabajador.', 'AS', US.CodEmpleado, GETDATE(), 'P'
                FROM 
                    USUARIOS AS US
                LEFT JOIN 
                    Auditoria_Aplicacion_Android AS AAA 
                    ON US.Usuario = AAA.Usuario 
                    AND AAA.TipoRegistro = '2'
                    AND AAA.Estado = 'E'
                    AND CONVERT(DATE, AAA.FechaHora) = CONVERT(DATE, GETDATE())
                    AND CONVERT(TIME, AAA.FechaHora) <= CONVERT(TIME, GETDATE())
                    AND CONVERT(TIME, AAA.FechaHora) >= DATEADD(HOUR, -2, CONVERT(TIME, GETDATE()))
                WHERE 
                    US.Chacras IS NOT NULL
                GROUP BY 
                    US.CodEmpleado, US.Usuario
                HAVING COALESCE(COUNT(AAA.Usuario), 0) = 0
                """
            cursor.execute(sql)

    except Exception as e:
        pass


def envio_notificaciones_al_canal():
    try:
        with connections ['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """
                SELECT CNG.ID_CNG, CNG.Titulo, CNG.Body, CNG.Pestaña, CNG.CodEmpleado, US.IdAndroid
                FROM Canal_Notificaciones_Generales AS CNG INNER JOIN
                    USUARIOS AS US ON US.CodEmpleado = CNG.CodEmpleado
                WHERE CONVERT(DATE,CNG.FechaAlta) = CONVERT(DATE,GETDATE())
                    AND CNG.Estado = 'P'
                    AND CNG.CodEmpleado = '58015'
                """
            cursor.execute(sql)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    ID_CNG = str(row[0])
                    Body = str(row[1])
                    Pestaña = str(row[2])
                    Legajo = str(row[3])
                    Id_Firebase = str(row[4])
                    enviar_notificacion_Tres_Ases(Id_Firebase,Body,Pestaña,ID_CNG)

    except Exception as e:
        pass





























