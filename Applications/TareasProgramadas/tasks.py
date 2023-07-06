from django.db import connections
from datetime import datetime


def sumar_numeros():
    now = datetime.now()
    hora_actual = str(now.strftime("%H:%M:%S"))
    id = '34882177'
    legajo = '58015'
    user = "JCHAMBI " + hora_actual

    try:
        #print(legajo + " - " + tarjeta + " - " + fecha + " - " + hora + " - " + tipo + " - " + nodo + " - " + simulacion + " - " + legCodigo + " - " + estado + " - " + orden)
        with connections['default'].cursor() as cursor:
            sql = "INSERT INTO CopiaUsuarios (ID, legajo, usuario) VALUES (%s, %s, %s)"
            values = (id,legajo,user)
            cursor.execute(sql, values)

    except Exception as e:
        print(e)


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
        #"WHERE cc.DescrCtroCosto  LIKE 'C%' " \
        print(e)


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
        print(e)

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
        print(e)


def insertaLegajosDatos(legLegajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "INSERT INTO T_Legajos_Datos (legCodigo, tacCodigo01, tacCodigo02) VALUES ( %s, '-1', '-1')"
            cursor.execute(sql, [str(legLegajo)])
    except Exception as e:
        print(e)


def insertaLegajosTurnos_A(legLegajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = " INSERT INTO T_Legajos_Turnos (tltComienzo, tltFin, turCodigo, legCodigo, tltPrioridad) VALUES ('1900-01-01T00:00:00.000', '9999-12-31T00:00:00.000', '3', %s, '0')"
            cursor.execute(sql, [str(legLegajo)])
    except Exception as e:
        print(e)

def insertaLegajosTurnos_B(legLegajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "INSERT INTO T_Legajos_Turnos (tltComienzo, tltFin, turCodigo, legCodigo, tltPrioridad) VALUES ('1900-01-01T00:00:00.000', '9999-12-31T00:00:00.000', '1', %s, '1')"
            cursor.execute(sql, [str(legLegajo)])
    except Exception as e:
        print(e)

def insertaSonidosLegajos(legLegajo):
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "INSERT INTO T_SonidosLegajos (legCodigo, snlArchivo) VALUES (%s, '(Ninguno)')"
            cursor.execute(sql, [str(legLegajo)])
    except Exception as e:
        print(e)

def insertaTarjetaPeriodo_A(legLegajo):
    legTarjeta = str(legLegajo.zfill(8))
    try:
        with connections ['principal'].cursor() as cursor:
            sql = "INSERT INTO T_Tarjetas_Por_Periodo (legCodigo, tarNumero, tarDesde, tarHasta) VALUES (%s, %s, '1900-01-01T00:00:00.000', '9999-12-31T00:00:00.000')"
            values = (str(legLegajo), legTarjeta)
            cursor.execute(sql, values)
    except Exception as e:
        print(e)

def insertaTarjetaPeriodo_B(legLegajo):
    legTarjeta = str(legLegajo.zfill(8))
    try:
        with connections ['principal'].cursor() as cursor:
            sql = " INSERT INTO T_Tarjetas_Por_Periodo (legCodigo, tarNumero, tarDesde, tarHasta) VALUES (%s, %s, '2023-07-01T00:00:00.000', '9999-12-31T00:00:00.000')"
            values = (str(legLegajo), legTarjeta)
            cursor.execute(sql, values)
    except Exception as e:
        print(e)

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
        print(e)

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
            print(e)

        legLegajo = traeLegLegajo(legajo)

        if legLegajo != 0:
            insertaLegajosDatos(legLegajo)
            insertaLegajosTurnos_A(legLegajo)
            insertaLegajosTurnos_B(legLegajo)
            insertaSonidosLegajos(legLegajo)
            insertaTarjetaPeriodo_A(legLegajo)
            insertaTarjetaPeriodo_B(legLegajo)














































