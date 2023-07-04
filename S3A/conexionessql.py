import pyodbc

ServerGeneral = "192.168.1.3\sql2012"
UserGeneral = "sa"
PasswordGeneral = ""

app = "TRESASES_APLICATIVO"

def App():
    try:
        Conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + ServerGeneral +'; DATABASE=' + app + '; UID=' + UserGeneral + '; PWD=' + PasswordGeneral)
        return Conexion
    except Exception as e:
        print(e)


s3a = "S3A"

def S3A():
    try:
        Conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + ServerGeneral +'; DATABASE=' + s3a + '; UID=' + UserGeneral + '; PWD=' + PasswordGeneral)
        return Conexion
    except Exception as e:
        print(e)

isis = "TresAses_ISISPayroll"

def ISIS():
    try:
        Conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + ServerGeneral +'; DATABASE=' + isis + '; UID=' + UserGeneral + '; PWD=' + PasswordGeneral)
        return Conexion
    except Exception as e:
        print(e)


principal = "Principal"

def Principal():
    try:
        Conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + ServerGeneral +'; DATABASE=' + principal + '; UID=' + UserGeneral + '; PWD=' + PasswordGeneral)
        return Conexion
    except Exception as e:
        print(e)
