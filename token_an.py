import enum 

class Token:   
    def __init__(self, caracterToken, tipoToken):
        self.caracterToken = caracterToken   
        self.tipoToken = tipoToken   # El tipo de token en el que es clasificado.

    @staticmethod
    def ifPalabraReservada(caracterToken):
        for tipoToken in TipodeTokens: 
            
            if (tipoToken.name == caracterToken):
                return tipoToken
            
        return None
    

class TipodeTokens(enum.Enum):
     
	FIN = 1
	FIN_DE_LINEA = 2
	NUEVA_LINEA = 3
	NUMERO = 4
	VARIABLE = 5
	STRING = 6
	etiqueta = 7
	instruccion = 8 
	ENTRADA = 9
	GOTO = 10
     
	# PalabrasReservadas 
	IF = 50
	THEN = 51   
	WHILE = 52  
	INT = 53
	IMPRIMIR = 10
	ENDIF = 11
	ENDWHILE = 12
	REPITE = 13
     
	# Operadores
	ASIGNACION = 101  
	SUMA = 102 
	RESTA = 103
	ASTERISCO = 104
	DIAGONAL = 105
	IGUAL = 106
	DISTINTOA = 107
	MENORQUE = 108
	MENORIGUAL = 109
	MAYOR = 110
	MAYORIGUAL = 111  

