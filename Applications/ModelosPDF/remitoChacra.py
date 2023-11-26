from fpdf import FPDF
import barcode # pip install python-barcode



class Remito_Movimiento_Chacras(FPDF):
    def __init__(self, fecha_remito, hora_remito, 
                 numero_chacra, numero_remito, productor, 
                 señor, domicilio, lote, especie, variedad, renspa, up_nq, chofer, 
                 camion, patente, total_bins, capataz, usuario):
        super().__init__('L', 'mm', 'A5')
        self.fecha_remito = fecha_remito
        self.hora_remito = hora_remito
        self.numero_chacra = numero_chacra
        self.numero_remito = numero_remito
        self.productor = productor
        self.señor = señor
        self.domicilio = domicilio
        self.lote = lote
        self.especie = especie
        self.variedad = variedad
        self.renspa = renspa
        self.up_nq = up_nq
        self.chofer = chofer
        self.camion = camion
        self.patente = patente
        self.total_bins = total_bins
        self.capataz = capataz
        self.usuario = usuario

    def header(self):
        self.rect(x=5,y=5,w=200,h=138)
        self.image('static/imagenes/TA.png', x=8, y=10, w=30, h=20)
        self.set_font('Arial', 'I', 8)
        self.text(x=50, y=12, txt= 'De TRES ASES S.A.')
        self.set_font('Arial', 'B', 8)
        self.text(x=42, y=15, txt= 'LISANDRO DE LA TORRE N° 100')
        self.text(x=44, y=18, txt= 'TEL: (0299) 4772183 / 4772139')
        self.text(x=39, y=21, txt= '4772183 / 4772139 FAX: (299) 4771573')
        self.text(x=49, y=24, txt= '(8324) CIPOLLETTI, R.N.')
        self.set_font('Arial', '', 7)
        self.text(x=46, y=29, txt= 'IVA RESPONSABLE INSCRIPTO')
        self.text(x=146, y=10, txt= 'DOCUMENTO NO VÁLIDO COMO FACTURA')
        self.rect(x=99,y=5,w=10,h=10)
        self.set_font('Arial', 'B', 26)
        self.text(x=101, y=13, txt= 'R')
        self.set_font('Arial', 'B', 16)
        self.text(x=118, y=11, txt= 'REMITO')
        self.set_font('Arial', '', 6)
        self.text(x=99, y=17, txt= 'Cod. N° 91')
        ##################################################
        self.set_font('Arial', 'B', 15)
        self.text(x=116, y=24, txt= 'MOVIMIENTO DE CHACRAS')
        self.text(x=170, y=32, txt= self.fecha_remito)
        self.set_font('Arial', 'B', 12)
        self.text(x=179, y=36, txt= self.hora_remito)
        self.set_font('Arial', '', 14)
        self.text(x=116, y=19, txt= 'N° ' + self.numero_chacra + ' - ' + self.numero_remito)
        self.set_font('Arial', '', 8)
        self.text(x=116, y=30, txt= 'C.U.I.T.: 30-53701387-3')
        self.text(x=116, y=33, txt= 'Ing. Btos.: C.M. 30537013873/901')
        self.text(x=116, y=36, txt= 'Inicio de Actividades: 22/03/1960')
        self.set_font('Arial', 'I', 9)
        self.text(x=141, y=42, txt= 'FRUTA CERTIFICADA GLOBAL G.A.P.')
        self.set_font('Arial', 'BI', 9)
        self.text(x=160, y=45, txt= 'GGN N°: 4049928936585')
        ##################################################
        self.set_font('Arial', '', 8)
        self.text(x=10, y=38, txt= 'PRODUCTOR: ')
        self.text(x=10, y=42, txt= 'Señor: ')
        self.text(x=10, y=46, txt= 'Domicilio: ')
        self.set_font('Arial', 'B', 9)
        self.text(x=30, y=38, txt= self.productor)
        self.text(x=20, y=42, txt= self.señor)
        self.text(x=24, y=46, txt= self.domicilio )
        ##################################################
        self.set_font('Arial', '', 8)
        self.text(x=10, y=52, txt= 'De Lote: ')
        self.text(x=10, y=57, txt= 'N° RENSPA:')
        self.text(x=80, y=57, txt= 'UP / NQ: ')
        self.text(x=140, y=52, txt= 'ESPECIE: ')
        self.text(x=140, y=57, txt= 'VARIEDAD: ')
        self.set_font('Arial', 'B', 9)
        self.text(x=22, y=52, txt= self.lote)
        self.text(x=154, y=52, txt= self.especie)
        self.text(x=28, y=57, txt= self.renspa)
        self.text(x=92, y=57, txt= self.up_nq)
        self.text(x=156, y=57, txt= self.variedad)
        ##################################################
        self.rect(x=10,y=60,w=190,h=5)
        self.set_font('Arial', 'B', 8)
        self.text(x=14, y=64, txt= 'CANTIDAD')
        self.line(34,60,34,65)
        self.text(x=70, y=64, txt= 'ENVASE')
        self.line(120,60,120,65)
        self.text(x=155, y=64, txt= 'MARCA')
        self.ln(55)

    def footer(self):
        self.set_font('Arial', '', 8)
        self.rect(x=10,y=112,w=92,h=14)
        self.line(10,117,102,117)
        self.text(x=24, y=116, txt= 'CHOFER')
        self.line(50,112,50,126)
        self.text(x=58, y=116, txt= 'CAMIÓN')
        self.line(80,112,80,126)
        self.text(x=84, y=116, txt= 'PATENTE')
        #### TOTAL BINS
        self.text(x=114, y=116, txt= 'CANT. TOTAL BINS')
        self.line(148,112,148,117)
        self.text(x=114, y=125, txt= 'CAPATAZ')
        self.line(148,121,148,126)
        self.set_font('Arial', 'B', 8)
        self.text(x=12, y=122, txt= self.chofer) 
        self.text(x=55, y=122, txt= self.camion) 
        self.text(x=84, y=122, txt= self.patente)
        self.rect(x=110,y=112,w=90,h=5)
        self.text(x=170, y=116, txt= self.total_bins) 
        self.rect(x=110,y=121,w=90,h=5)
        self.text(x=160, y=125, txt= self.capataz)
        self.set_y(-20)
        self.cell(0, 11, 'Página ' + str(self.page_no()) + '/{nb}', 15, 0, 'R')
        self.rect(x=10,y=128,w=190,h=12)
        #### CAI
        self.set_font('Arial', 'B', 10)
        self.text(x=110, y=133, txt= 'C.A.I.: 47503100328571')
        self.text(x=110, y=138, txt= 'FECHA VENCIMIENTO: 13/12/2024')
        self.ln(138)