import sys
from token_an import *

class Scanner:

    palabras_reservadas = {
        "asignacion"    : ["=", "Simbolo de asignacion, dos seguidos es comparacion de igualdad"],
        "menor_que"     : ["<", "Comparacion de menor que"],
        "mayor_que"     : [">", "Comparacion de mayor que"], 
        "suma"          : ["+", "operador de suma"],
        "resta"         : ["-", "operador de resta"],
        "asterisco"     : ["*", "operador de asterisco"],
        "diagonal"      : ["/", "operador diagonal o slash"], 
        "porcentaje"    : ["%", "operador de porcentaje"],
        "comillas"      : ['\"', "signo de comillas"], 
        "dob_diagonal_inv"  : ['\\', "operador de doble diagonal invertida o slash invertido"], 
        "admiracion"    : ["!", "Signo de admiracion, si tiene un != sera distinto a "],
        "a_parentesis"  : ['(', "abrir parentesis"],
        "c_parentesis"  : [')', "cerrar parentesis"],
        "punto"         : [".", "Simbolo de punto"], 
        "salto_linea"   : ["\n", "Salto de linea"], 
        "fin_linea"     : ["\0", "Fin de linea"],  
        "sangria"       : ["\t", "Fin de linea"],  
        "retorno_carro" : ["\r", "retorno de carro, sobreescribe el inicio de la linea"], 
        "fin_sentencia" : [";", "Fin de una sentencia"]
    }

    def __init__(self, codigo):
        self.codigo = codigo 
        self.caracterActual = ''    
        self.posicionActual = -1    
        self.sigCaracter()


    def sigCaracter(self):
        self.posicionActual += 1
        if self.posicionActual >= len(self.codigo):
            self.caracterActual = '\0'   
        else:
            self.caracterActual = self.codigo[self.posicionActual]


    def revisaSigCaracter(self):
        if self.posicionActual + 1 >= len(self.codigo):
            return '\0'
        return self.codigo[self.posicionActual+1]
 
    def eTerminarAnalisis(self, message):
        sys.exit("Se encontro un Error Lexico en el codigo proporcionado: " + message)
		

    def caracterAToken(self):
        self.omitirEspaciosVacios()
        self.omitirComentarios()
        token = None

        if self.caracterActual == self.palabras_reservadas['suma'][0]:
            token = Token(self.caracterActual, TipodeTokens.SUMA)
        elif self.caracterActual == self.palabras_reservadas['resta'][0]:
            token = Token(self.caracterActual, TipodeTokens.RESTA)
        elif self.caracterActual == self.palabras_reservadas['asterisco'][0]:
            token = Token(self.caracterActual, TipodeTokens.ASTERISCO)
        elif self.caracterActual == self.palabras_reservadas['diagonal'][0] :
            token = Token(self.caracterActual, TipodeTokens.DIAGONAL)
        elif self.caracterActual == self.palabras_reservadas['asignacion'][0] : 
            if self.sigCaracter() == self.palabras_reservadas['asignacion'][0] :
                ultimoCaracter = self.caracterActual
                self.revisaSigCaracter()
                token = Token(ultimoCaracter + self.caracterActual, TipodeTokens.IGUAL)
            else:
                token = Token(self.caracterActual, TipodeTokens.ASIGNACION)
        elif self.caracterActual == self.palabras_reservadas['mayor_que'][0]  : 
            if self.sigCaracter() == self.palabras_reservadas['asignacion'][0] :
                ultimoCaracter = self.caracterActual
                self.revisaSigCaracter()
                token = Token(ultimoCaracter + self.caracterActual, TipodeTokens.GTEQ)
            else:
                token = Token(self.caracterActual, TipodeTokens.GT)
        elif self.caracterActual == '<': 
            if self.sigCaracter() == self.palabras_reservadas['asignacion'][0] :
                ultimoCaracter = self.caracterActual
                self.revisaSigCaracter()
                token = Token(ultimoCaracter + self.caracterActual, TipodeTokens.MENORIGUAL)
            else:
                token = Token(self.caracterActual, TipodeTokens.MENORQUE)
        elif self.caracterActual == self.palabras_reservadas['admiracion'][0] :
            if self.sigCaracter() == self.palabras_reservadas['asignacion'][0] :
                ultimoCaracter = self.caracterActual
                self.revisaSigCaracter()
                token = Token(ultimoCaracter + self.caracterActual, TipodeTokens.DISTINTOA)
            else:
                self.eTerminarAnalisis("Expected !=, got !" + self.sigCaracter())

        elif self.caracterActual == '\"': 
            self.revisaSigCaracter()
            posicionInicial = self.posicionActual

            while self.caracterActual != '\"': 
                if (self.caracterActual == self.palabras_reservadas['retorno_carro'][0] 
                    or self.palabras_reservadas['salto_linea'][0]
                    or self.palabras_reservadas['sangria'][0]  
                    or self.palabras_reservadas['dob_diagonal_inv'][0]
                    or self.palabras_reservadas['porcentaje'][0] ):
                    self.eTerminarAnalisis("No se perrmite caracteres especiales en cadenas")
                self.revisaSigCaracter()

                self.sigCaracter()
            textoIdentificado = self.codigo[ posicionInicial : self.posicionActual]  
            token = Token(textoIdentificado, TipodeTokens.STRING)

        elif self.caracterActual.isdigit(): 
            posicionInicial = self.posicionActual
            while self.sigCaracter().isdigit():
                self.revisaSigCaracter()
            if self.sigCaracter() == '.':  
                self.revisaSigCaracter() 

                if not self.sigCaracter().isdigit():  
                    self.eTerminarAnalisis("Illegal character in number.")
                while self.sigCaracter().isdigit():
                    self.revisaSigCaracter()

            tokText = self.source[posicionInicial : self.posicionActual + 1]  
            token = Token(tokText, TipodeTokens.NUMBER)

         
        elif self.caracterActual.isalpha(): 
            posicionInicial = self.posicionActual
            while self.revisaSigCaracter().isalnum():
                self.sigCaracter() #En caso de ser alfanumerico continua revisando cada los caracteres

            #Se guarda la cadena de alfanumericos que tienen que iniciar con una letra
            textoIdentificado = self.codigo[posicionInicial : self.posicionActual + 1]  
            
            palabraReservada = Token.ifPalabraReservada(textoIdentificado) 
            if palabraReservada == None: # Es instruccion
                token = Token(textoIdentificado, TipodeTokens.instruccion)
            else:   # palabraReservada
                token = Token(textoIdentificado, palabraReservada)

        elif self.caracterActual == self.palabras_reservadas['salto_linea'][0]  : 
            token = Token('\\n', TipodeTokens.NUEVA_LINEA)
        
        elif self.caracterActual == self.palabras_reservadas['fin_linea'][0]  :
            token = Token('', TipodeTokens.FIN_DE_LINEA)
        else: #Token desconosido
            self.eTerminarAnalisis("Token no valido " + self.caracterActual)
			
        self.sigCaracter()
        return token

    def omitirEspaciosVacios(self):
        while (self.caracterActual == ' ' or 
               self.caracterActual == '\t' or 
               self.caracterActual == '\r'):
                self.sigCaracter()
		
     
    def omitirComentarios(self):
        if self.caracterActual == '#':
            while self.caracterActual != '\n':
                self.sigCaracter()

