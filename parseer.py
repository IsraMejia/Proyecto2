import sys  
from scanner import *
 
 
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner

        self.symbols = set()  # almacena todas las variables que se han declarado en el programa hasta el momento
        self.etiquetasdeclarada = set() # Para el seguimiento de todas las etiquetas que se han declarado
        self.etiquetasGotoed = set() #Almacena todas las etiquetas a las que se ha saltado en el programa. 
        #Esta información se utilizará para comprobar si hay etiquetas no definidas más adelante.

        self.tokenActual = None
        self.tokenObservandose = None
        self.siguienteToken()
        self.siguienteToken()# se Llama a esta función dos veces para inicializar current y peek.

     
    def revisarToken(self, kind):
        return kind == self.tokenActual.tipoToken

     
    def analizarToken(self, kind):
        return kind == self.tokenObservandose.tipoToken

     
    def comparaToken(self, kind):
        if not self.revisarToken(kind):
            self.terminarSintactico("No se encontro " + kind.name + ", el token " + self.tokenActual.tipoToken.name)
        self.siguienteToken()

    
    def siguienteToken(self):
        self.tokenActual = self.tokenObservandose
        self.tokenObservandose = self.scanner.caracterAToken()
        
    def revisaOperadorComparacion(self):
        return self.revisarToken(TipodeTokens.GT) or self.revisarToken(TipodeTokens.GTEQ) or self.revisarToken(TipodeTokens.LT) or self.revisarToken(TipodeTokens.LTEQ) or self.revisarToken(TipodeTokens.EQEQ) or self.revisarToken(TipodeTokens.NOTEQ)

    def terminarSintactico(self, message):
        sys.exit("Error. " + message)


    # Reglas de produccion
    def analizaEstructura(self): 

        #Si requieren algunos saltos de línea en nuestra gramática, es necesario omitir los "\n".
        while self.revisarToken(TipodeTokens.NUEVA_LINEA):
            self.siguienteToken()

         
        while not self.revisarToken(TipodeTokens.FIN_DE_LINEA):
            self.estado()

         
        for etiqueta in self.etiquetasGotoed:
            if etiqueta not in self.etiquetasdeclarada:
                self.terminarSintactico("Intentando saltar a una etiqueta no declarada: " + etiqueta)


     
    def estado(self): 
        if self.revisarToken(TipodeTokens.IMPRIMIR):
            print("estado-IMPRIMIR")
            self.siguienteToken()

            if self.revisarToken(TipodeTokens.STRING):
                # Simple string.
                self.siguienteToken()

            else:
                
                self.expresion()


        # "IF" comparacion "THEN" {estado} "ENDIF"
        elif self.revisarToken(TipodeTokens.IF):
            print("estado-IF")
            self.siguienteToken()
            self.comparacion()

            self.comparaToken(TipodeTokens.THEN)
            self.nuevaLinea()
 
            while not self.revisarToken(TipodeTokens.ENDIF):
                self.estado()

            self.comparaToken(TipodeTokens.ENDIF)


        # "WHILE" comparacion "REPITE" {estado} "ENDWHILE"
        elif self.revisarToken(TipodeTokens.WHILE):
            print("estado-WHILE")
            self.siguienteToken()
            self.comparacion()

            self.comparaToken(TipodeTokens.REPITE)
            self.nuevaLinea()

            # analiza estados internos del endwhile
            while not self.revisarToken(TipodeTokens.ENDWHILE):
                self.estado()

            self.comparaToken(TipodeTokens.ENDWHILE)


        # "etiqueta" instruccion
        elif self.revisarToken(TipodeTokens.etiqueta):
            print("estado-etiqueta")
            self.siguienteToken()

            # Revisa que la etiqueta no se haya detectado
            if self.tokenActual.text in self.etiquetasdeclarada:
                self.terminarSintactico("etiqueta detectada: " + self.tokenActual.text)
            self.etiquetasdeclarada.add(self.tokenActual.text)

            self.comparaToken(TipodeTokens.instruccion)

        # "GOTO" instruccion
        elif self.revisarToken(TipodeTokens.GOTO):
            print("estado-GOTO")
            self.siguienteToken()
            self.etiquetasGotoed.add(self.tokenActual.text)
            self.comparaToken(TipodeTokens.instruccion)

        # "LET" instruccion "=" expresion
        elif self.revisarToken(TipodeTokens.LET):
            print("estado-LET")
            self.siguienteToken()

             
            if self.tokenActual.text not in self.symbols:
                self.symbols.add(self.tokenActual.text)

            self.comparaToken(TipodeTokens.instruccion)
            self.comparaToken(TipodeTokens.EQ)
            
            self.expresion()

        # "ENTRADA" instruccion
        elif self.revisarToken(TipodeTokens.ENTRADA):
            print("estado-ENTRADA")
            self.siguienteToken()

             
            if self.tokenActual.text not in self.symbols:
                self.symbols.add(self.tokenActual.text)

            self.comparaToken(TipodeTokens.instruccion)

         
        else:
            mensajeFin =f"""
                Estado sintactico invalido : 
                    {self.tokenActual.text}  ( {self.tokenActual.tipoToken.name} )
            """
            self.terminarSintactico(mensajeFin)

        # NUEVA_LINEA.
        self.nuevaLinea()


    # comparacion ::= expresion (("==" | "!=" | ">" | ">=" | "<" | "<=") expresion)+
    def comparacion(self):
        print("comparacion")

        self.expresion()
        # Debe haber al menos un operador de comparación y otra expresión.
        if self.revisaOperadorComparacion():
            self.siguienteToken()
            self.expresion()
        else:
            self.terminarSintactico("Expected comparacion operator at: " + self.tokenActual.text)

        # Puede haber 0 o más operadores de comparación y expresiones.
        while self.revisaOperadorComparacion():
            self.siguienteToken()
            self.expresion()


    # expresion ::= term {( "-" | "+" ) term}
    def expresion(self):
        print("expresion")

        self.terminoMat()
        # Puede haber 0 o mas +/- y expresiones.
        while self.revisarToken(TipodeTokens.SUMA) or self.revisarToken(TipodeTokens.RESTA):
            self.siguienteToken()
            self.terminoMat()


    # term ::= unario {( "/" | "*" ) unario}
    def terminoMat(self):
        print("TERM")

        self.unario() 
        while self.revisarToken(TipodeTokens.ASTERISCO) or self.revisarToken(TipodeTokens.DIAGONAL):
            self.siguienteToken()
            self.unario()


    # unario ::= ["+" | "-"] primario
    def unario(self):
        print("unario")
        # Optional unario +/-
        if self.revisarToken(TipodeTokens.SUMA) or self.revisarToken(TipodeTokens.RESTA):
            self.siguienteToken()        
        self.primario()


    # primario ::= NUMERO | instruccion
    def primario(self):
        print("primario (" + self.tokenActual.text + ")")

        if self.revisarToken(TipodeTokens.NUMERO): 
            self.siguienteToken()
        elif self.revisarToken(TipodeTokens.instruccion):
            # Ensure the variable already exists.
            if self.tokenActual.text not in self.symbols:
                self.terminarSintactico("Referencing variable before assignment: " + self.tokenActual.text)

            self.siguienteToken()
        else:
            # Error!
            self.terminarSintactico("Unexpected token at " + self.tokenActual.text)

    
    

    def nuevaLinea(self):
        print("NUEVA_LINEA") 
        self.comparaToken(TipodeTokens.NUEVA_LINEA) 
        while self.revisarToken(TipodeTokens.NUEVA_LINEA):
            self.siguienteToken()