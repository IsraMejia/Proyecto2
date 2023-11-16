from scanner import *
from parseer import *

def main():
    intro = """
        \n\t\tAnalizador Lexico . Proyecto 2 compiladores 
    """
    print(intro)
    
    
    codigo = """
        PRINT "hello world"
        PRINT "second line"
        PRINT "and a third"
    """ 
    codigo = codigo + "\n"     
    scanner = Scanner(codigo)
    print(f' A continuacion se muestra el codigo ingresado: \n {codigo} \n\n\nAnalizando ...')
    print("\nSe ha analizado el codigo ingresado, retornando los siguientes tokens:\n")

    token = scanner.caracterAToken() 
    while token.tipoToken != TipodeTokens.FIN_DE_LINEA: 
        print(f"\tLeido\t\t{token.caracterToken}\t\t----Tokenizado a --->\t\t{token.tipoToken} \n")
        token = scanner.caracterAToken()
 
    print("\n\n Analizador Lexico finalizado  \n")

    print('Iniciando analisis sintactico')

    parser = Parser(scanner)

    parser.analizaEstructura()  
    print("Parsing completed.")

main()