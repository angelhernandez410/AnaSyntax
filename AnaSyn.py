def isint(n):
    try:
        val = int(n)
        return "int"
    except ValueError:
        try:
            val= float (n)
            return "float"
        except ValueError:
            return "none"

def lexdebug(code):
    print("-----Analizador Lexico-----\n\nAnalisis de Caracteres\n")

    tokenslist = [["print", "PRINTF"],["true","TRUE_BOOL"],['false',"FALSE_BOOL"],["0","CEROVAL"],[',',"SEPARATE"],['"',"DOUBLE_COMMIT"],[">","MAYORQ"],["<","MINORQ"],[">=","MAYANDEQUAL"],["<=","MINANDEQUAL"],["==","COMP_EQUAL"],["!=","DISTINCT"],["+","SUM"],["-","REST"],["*","MULTIPLY"],["/","DIVIDE"],["int","INTEGER"],["float","DEC_FLOAT"],["string","STRING"],["bool","BOOLEAN"],[";","ENDLINE"],["=","OPERADOR_EQUAL"],["(","BRACKOPNE"],[")","BRACKCLOSE"]] #Esta es la lista de tokens

    arreglo_espacios = []

    arreglo_saltosdelinea = code.split("\n")

    for idx,i in enumerate(arreglo_saltosdelinea):
        temp_revisiondecaracteres = list(i)

        temp_texto_nuevalinea =""
        print("\nLINEA "+str(idx+1)+":")
        for j in temp_revisiondecaracteres:
            if ord(j)<128:
                print(j+" ==> # ASCII: "+str(ord(j)))
                if(ord(j)>=33 and ord(j)<=47) or (ord(j)>=58 and ord(j)<=64) or (ord(j)>=91 and ord(j)<=96) or (ord(j)>=123 and ord(j)<=126):
                    if ord(j)==59:
                        temp_texto_nuevalinea = temp_texto_nuevalinea + " " + j
                    else:
                        temp_texto_nuevalinea = temp_texto_nuevalinea + " " + j + " "
                else:
                    temp_texto_nuevalinea = temp_texto_nuevalinea + j
            else: #ERROR
                print("Error: "+j+" ==> Caracter Invalido en la linea " + str(idx+1))
                exit() #El codigo se detiene
        
        arreglo_espacios.append(temp_texto_nuevalinea) #Este método nos permite agregar nuevos elementos a una lista

        array_final = []

        for i in arreglo_espacios:
            temp_linea = []
            temp_revisartokens= i.split()
            for j in temp_revisartokens:
                for token in tokenslist: #Compara con mi lista de tokens
                    tempchecker = False
                    if token[0] == j:
                        temp_linea.append([j,token[1]])
                        tempchecker = True
                        break
                    else:
                        tempchecker = False

                if tempchecker == False:
                    checkj = isint(j)
                    if checkj == "int":
                        temp_linea.append([j,"NUMERO_INT"])
                    elif checkj == "float":
                        temp_linea.append([j,"NUMERO_FLOAT"])
                    else:
                        temp_linea.append([j,"NOMBRE_VARIABLE"])

            array_final.append(temp_linea) #Se introducen a arreglo final, todos los arreglos guardados en temp_linea

    print("\nEn Tokens tenemos:") #A partir de aqui, se imprimen los tokens correspondientes a cada linea
    contador = 1
    for i in array_final: #en este for recorreremos cada uno de los arreglos, dentro de arreglo_final
        print("\nLINEA "+str(contador)+":")
        contador = contador + 1
        for j in i: #Se recorren cada uno de los arreglos y se imprimen los tokens uno debajo del otro
            print(j)

    print("\n")
	
    return array_final 
	
#A partir de aquí, comienza el Analizador Sintáctico

def syntaxdebug(code):
    print("--Analizador Sintactico--\n\nSimplificar Arreglo de Tokens: \n")
    arreglo_simplificartokens = { "COMPARERS" : ["MAYORQ", "MINORQ", "MAYANDEQUAL", "MINANDEQUAL", "COMP_EQUAL", "DISTINCT"], "VALUE": ["NUMERO_INT", "NUMERO_FLOAT", "TRUE_BOOL", "FALSE_BOOL", "STRLINE", "CEROVAL"], "TIPO_VAR": ["INTEGER", "DEC_FLOAT", "STRING", "BOOLEAN"], "MATH_SIMB": ["SUM", "REST", "MULTIPLY", "DIVIDE", "OPERADOR_EQUAL"]}
    arreglo_simplificado = []

    for i,idx in enumerate(code):
        temptext = ""
        checknumcommit = 0
        for j,jdx in enumerate(code[i]):
            if (code[i][j][1]=="DOUBLE_COMMIT"):
                checknumcommit = checknumcommit + 1
        if checknumcommit>0:
            if checknumcommit % 2 == 0:
                for j,jdx in enumerate(code[i]):
                    if (code[i][j][1]=="DOUBLE_COMMIT"):
                        ting = '"'
                        l= j+1
                        while (True):
                            if (code[i][l+1][1]=="DOUBLE_COMMIT"):
                                code[i][j][1] = "STRLINE"
                                code[i][j][0] = '"' + temptext + code [i][l][0]+'"'
                                code[i][l:3] = []
                                break
                            else:
                                temptext = temptext + code [i][l][0] + " "
                                code[i][l:2] = []
                                l = l-1
                            l = l+1
            else:
                print("--Analizador Sintáctico--\n\nError Sintactico en la linea "+str(i+1)+": String mal declarado. Revisar comillas.")
                return False

    for i,idx in enumerate(code):
        arreglo_simplificado_temp = []
        for j,jdx in enumerate(code[i]):
            varchecker = False
            tempinfo = ""
            for key in arreglo_simplificartokens.keys():
                for l,ldx in enumerate(arreglo_simplificartokens[key]):
                    if (code[i][j][1]==arreglo_simplificartokens[key][l]):
                        varchecker = True
                        tempinfo = key
                        break
            
            if (varchecker == False):
                arreglo_simplificado_temp.append([code[i][j][0],code[i][j][1]])
            else:
                arreglo_simplificado_temp.append([code[i][j][0],tempinfo])

        arreglo_simplificado.append([arreglo_simplificado_temp])

    for idx,i in enumerate(arreglo_simplificado):
        tempcode = ""
        for idx2,j in enumerate(arreglo_simplificado[idx][0]):
            tempcode = tempcode + arreglo_simplificado[idx][0][idx2][0]+" "
            if (idx2==0):
                if not(arreglo_simplificado[idx][0][idx2][1]=="TIPO_VAR" or arreglo_simplificado [idx][0][idx2][1]=="NOMBRE_VARIABLE" or arreglo_simplificado[idx][0][idx2][1]=="PRINTF"):
                    print("Error en la linea: "+str(idx+1)+": Se esperaba un TIPO_VAR, NOMBRE_VARIABLE o PRINTF al inicio")
                    return False
            else:
                if (arreglo_simplificado[idx][0][idx2][1] == "TIPO_VAR"):
                    if (arreglo_simplificado[idx][0][idx2-1][1]!="ENDLINE"):
                        print("Error en la linea "+str(idx+1)+": Se esperana un ENDLINE (;) antes de " + arreglo_simplificado [idx][0][idx2][0])
                        return False
                elif (arreglo_simplificado[idx][0][idx2][1] == "NOMBRE_VARIABLE"):
                    if not(arreglo_simplificado[idx][0][idx2-1][1]=="TIPO_VAR" or arreglo_simplificado[idx][0][idx2-1][1]=="COMPARERS" or arreglo_simplificado[idx][0][idx2-1][1]=="MATH_SIMB"):
                        print("Error en la linea "+str(idx+1)+": Se esperaba un TIPO_VAR (Tipo de variable) o un SEPARATE (,) o un operador matematico antes de "+arreglo_simplificado[idx][0][idx2][1]+ " (" + arreglo_simplificado[idx][0][idx2][0]+")")
                        return False
                elif (arreglo_simplificado[idx][0][idx2][1] == "MATH_SIMB"):
                    if not(arreglo_simplificado[idx][0][idx2-1][1]=="NOMBRE_VARIABLE" or arreglo_simplificado[idx][0][idx2-1][1]=="VALUE"):
                        print("Error en la linea "+str(idx+1)+": Se esperana un Nombre de Variable o un Valor antes de "+arreglo_simplificado[idx][0][idx2][1]+ " (" + arreglo_simplificado[idx][0][idx2][0]+")")
                        return False
                elif (arreglo_simplificado[idx][0][idx2][1] == "VALUE"):
                    if not(arreglo_simplificado[idx][0][idx2-1][1]=="MATH_SIMB" or arreglo_simplificado[idx][0][idx2-1][1]=="COMPARERS"):
                        print("Error en la linea "+str(idx+1)+": Se esperaba un Operador Matematico antes de "+arreglo_simplificado[idx][0][idx2][1]+ " (" + arreglo_simplificado[idx][0][idx2][0]+")")
                        return False
                elif (arreglo_simplificado[idx][0][idx2][1] == "ENDLINE"):
                    if not(arreglo_simplificado[idx][0][idx2-1][1]=="NOMBRE_VARIABLE" or arreglo_simplificado[idx][0][idx2-1][1]=="VALUE"):
                        print("Error en la linea "+str(idx+1)+": Se esperaba un nombre de variable o un valor antes de "+arreglo_simplificado[idx][0][idx2][1]+ " (" + arreglo_simplificado[idx][0][idx2][0]+")")
                        return False
                elif (arreglo_simplificado[idx][0][idx2][1] == "SEPARATE"):
                    if not(arreglo_simplificado[idx][0][idx2-1][1]=="NOMBRE_VARIABLE" or arreglo_simplificado[idx][0][idx2-1][1]=="VALUE"):
                        print("Error en la linea "+str(idx+1)+": Se esperaba un nombre de variable o un valor antes de "+arreglo_simplificado[idx][0][idx2][1]+ " (" + arreglo_simplificado[idx][0][idx2][0]+")")
                        return False
                elif (arreglo_simplificado[idx][0][idx2][1] == "COMPARERS"):
                    if not(arreglo_simplificado[idx][0][idx2-1][1]=="NOMBRE_VARIABLE" or arreglo_simplificado[idx][0][idx2-1][1]=="VALUE"):
                        print("Error en la linea "+str(idx+1)+": Se esperaba un nombre de variable o un valor antes de "+arreglo_simplificado[idx][0][idx2][1]+ " (" + arreglo_simplificado[idx][0][idx2][0]+")")
                        return False
        
        print("\nLinea "+ str(idx+1)+ " ( "+tempcode+"): OK.")
        temptext = ""

        for j,jdx in enumerate(arreglo_simplificado[idx][0]):
            print("\n     "+arreglo_simplificado[idx][0][j][1])

    print("\nAnalisis Sintactico Terminado\n")

    return code
	
f = open("comandos.txt", "r") #con esta instrucción, leemos la información del documento comandos.txt
tokenarrfinal = []
tokenarrfinal = lexdebug(f.read())
syntaxdebug(tokenarrfinal)