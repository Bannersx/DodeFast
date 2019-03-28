from sly import Lexer as Lexer
from sly import Parser as Parser

class BasicLexer(Lexer):

    tokens = { DECLARATION, ASSIGNATION, ENCASO, CUANDO, PRINT, ENTONS, SINO, FINENCASO, VAR, INT,
                SEMI, LBRACK, RBRACK, GREATEREQ, LESSEREQ, EQ, GREATER, LESSER,
                MINUS, TWO_POINTS, INICIO, FINAL, PROC, LLAMAR,
                INC, DEC, INI, PARENTHESIS_LEFT, PARENTHESIS_RIGHT, COMA, MOVER, ALEATORIO,
                 REPITA, HASTAENCONTRAR, DESDE, HASTA, HAGA, FINDESDE}

    ignore = " \t"

#----Simbolos------
    SEMI = r";"
    LBRACK = r"{"
    RBRACK = r"}"
    EQ = r"="
    GREATEREQ = r">="
    LESSEREQ = r"<="
    GREATER = r">"
    LESSER = r"<"
    MINUS = r"-"
    COMA = r","
    PARENTHESIS_LEFT = r"\("
    PARENTHESIS_RIGHT = r"\)"
    TWO_POINTS = r":"

#----Palabras------
    INICIO = r'Inicio'
    FINAL = r'Final'
    INC = r'Inc'
    DEC = r'Dec'
    INI = r'Ini'
    MOVER = r'Mover'
    ALEATORIO = r'Aleatorio'
    PROC = r'Proc'
    LLAMAR = r'Llamar'
    DECLARATION = r"DCL"
    ASSIGNATION = "DEFAULT"
    ENCASO = r"EnCaso"
    CUANDO = r"Cuando"
    ENTONS = r"Entons"
    SINO = r"SiNo"
    FINENCASO = r"Fin-EnCaso"
    REPITA = 'Repita'
    HASTAENCONTRAR ='HastaEncontrar'
    DESDE = 'Desde'
    HASTA = 'Hasta'
    HAGA = 'Haga'
    FINDESDE= 'Fin-Desde'
    PRINT = "Print"
    VAR = r"[a-zA-Z_][a-zA-Z0-9_]*"


    @_(r"\d+")
    def INT(self, t):
        t.value = int(t.value)
        return t

class BasicParser(Parser):
    tokens = BasicLexer.tokens

    X = 0

    def __init__(self):
        self.env = { }
    @_('')
    def statement(self, p):
        pass

    @_('sentencia')
    def statement(self,p):
        return p.sentencia

    @_("statement sentencia")
    def statement(self,p):

        return ["multStatements", p.statement] + [p.sentencia]

    @_('expr SEMI')
    def sentencia(self, p):
        return (p.expr)

    @_('var_assign')
    def sentencia(self, p):
        return p.var_assign

    @_('REPITA LBRACK statement RBRACK HASTAENCONTRAR Evaluation SEMI')
    def sentencia(self,p):
        return ('while_loop', p.statement, p.Evaluation)

    @_('DESDE var EQ expr HASTA expr HAGA LBRACK statement RBRACK FINDESDE SEMI')
    def sentencia(self, p):
        return ('for_loop', p.var, p.expr0, p.expr1, p.statement)

    @_('EnCasoA')
    def sentencia(self, p):
        return p.EnCasoA

    @_('EnCasoB')
    def sentencia(self, p):
        return p.EnCasoB

    @_('ENCASO CuandoA SiNo FINENCASO SEMI')
    def EnCasoA(self, p):
        return ("EnCasoA", p.CuandoA, p.SiNo)

    @_('ENCASO var CuandoC SiNo FINENCASO SEMI')
    def EnCasoB(self,p):
        self.X = p.var
        print(self.X)
        tree = ["EnCasoB", p.CuandoC, p.SiNo]
        tree[1][0][1][1] = self.X
        return tree

    @_('CuandoB CuandoA')
    def CuandoA(self, p):
        return [p.CuandoB] + p.CuandoA

    @_('CuandoB')
    def CuandoA(self, p):
        return [p.CuandoB]

    @_('CUANDO Evaluation Entons')
    def CuandoB(self, p):
        return ("Cuando",p.Evaluation, p.Entons)


    @_('CuandoD CuandoC')
    def CuandoC(self, p):
        return [p.CuandoD] + p.CuandoC

    @_('CuandoD')
    def CuandoC(self, p):
        return [p.CuandoD]

    @_('CUANDO EvaluationB Entons')
    def CuandoD(self, p):
        return ["Cuando", p.EvaluationB, p.Entons]

    @_('var Cond expr')
    def Evaluation(self,p):
        return(p.Cond, p.var, p.expr)

    @_('Cond expr')
    def EvaluationB(self,p):
        return [p.Cond, self.X, p.expr]


    @_('ENTONS LBRACK statement RBRACK')
    def Entons(self, p):
        return p.statement

    @_('SINO LBRACK statement RBRACK')
    def SiNo(self, p):
        return ("SiNo", p.statement)

    @_('EQ')
    def Cond(self, p):
        return "Equals"

    @_('GREATEREQ')
    def Cond(self, p):
        return "GreaterEq"

    @_('LESSEREQ')
    def Cond(self, p):
        return "LesserEq"

    @_('GREATER')
    def Cond(self, p):
        return "Greater"

    @_('LESSER')
    def Cond(self, p):
        return "Lesser"

    @_('DECLARATION VAR ASSIGNATION expr SEMI')
    def var_assign(self, p):
        return ('var_assign', p.VAR, p.expr)

    @_('DECLARATION VAR SEMI')
    def var_assign(self, p):
        return ('var_assign', p.VAR, 0)

    @_('INT')
    def expr(self, p):
        return ('num', p.INT)

    @_('MINUS INT')
    def expr(self, p):
        return ('num', -1*p.INT)

    @_('VAR')
    def expr(self, p):
        return ('var', p.VAR)

    @_('VAR')
    def var(self, p):
        return ('var', p.VAR)

    @_('PRINT PARENTHESIS_LEFT expr PARENTHESIS_RIGHT SEMI')
    def sentencia(self, p):
        return ("print", p.expr)

    @_('INC PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def sentencia(self, p):
        return ('fun_call', p.INC, p.var, p.expr)

    @_('DEC PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def sentencia(self, p):
        return ('fun_call', p.DEC, p.var, p.expr)

    @_('INI PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def sentencia(self, p):
        return ('fun_call', p.INI, p.var, p.expr)

    @_('MOVER PARENTHESIS_LEFT expr PARENTHESIS_RIGHT')
    def sentencia(self, p):
        return ('fun_call', p.MOVER, p.expr)

    @_('ALEATORIO PARENTHESIS_LEFT PARENTHESIS_RIGHT')
    def sentencia(self, p):
        return ('fun_call', p.ALEATORIO)

    @_('PROC VAR PARENTHESIS_LEFT PARENTHESIS_RIGHT INICIO TWO_POINTS statement FINAL SEMI')
    def sentencia(self, p):
        return ('process_def', p.VAR, p.statement)

    @_('PROC VAR PARENTHESIS_LEFT expr PARENTHESIS_RIGHT INICIO TWO_POINTS statement FINAL SEMI')
    def sentencia(self, p):
        return ('process_def_parameters', p.VAR, p.expr, p.statement)

    @_('LLAMAR VAR PARENTHESIS_LEFT PARENTHESIS_RIGHT')
    def sentencia(self, p):
        return ('process_call', p.VAR)

    @_('LLAMAR VAR PARENTHESIS_LEFT expr PARENTHESIS_RIGHT')
    def sentencia(self, p):
        return ('process_call_parameters', p.VAR, p.expr)

    def error(self, p):
        return ("error", "Parsing Error! Maybe you mixed the order or misspelled something")

class BasicExecute:

    def __init__(self, env):
        self.env = env


    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == "multStatements":
            print(node)
            result = []
            for i in range(1, len(node)):
                result.append(self.walkTree(node[i]))

            return result

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == "error":
            return node[1]

        if node[0] == 'EnCasoA':


            for i in range(len(node[1])):
                result = self.walkTree(node[1][i])
                if result:
                    return self.walkTree(node[1][i][2])
                    break

            return self.walkTree(node[len(node)-1])

        if node[0] == 'EnCasoB':

            for i in range(len(node[1])):
                result = self.walkTree(node[1][i])
                if result:
                    return self.walkTree(node[1][i][2])
                    break

            return self.walkTree(node[len(node)-1])


        if node[0] == "Cuando":
            return self.walkTree(node[1])

        if node[0] == "print":
            return ("print", self.walkTree(node[1]))

        if node[0] == "SiNo":
            return self.walkTree(node[1])

        if node[0] == 'Equals':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == "Greater":
            try:
                return self.walkTree(node[1]) > self.walkTree(node[2])
            except:
                return("Error in comparation. Check if the data types are comparable.")

        if node[0] == "Lesser":
            try:
                return self.walkTree(node[1]) < self.walkTree(node[2])
            except:
                return("Error in comparation. Check if the data types are comparable.")

        if node[0] == "LesserEq":
            try:
                return self.walkTree(node[1]) <= self.walkTree(node[2])
            except:
                return("Error in comparation. Check if the data types are comparable.")
        if node[0] == "GreaterEq":
            try:
                return self.walkTree(node[1]) >= self.walkTree(node[2])
            except:
                return "Error in comparation. Check if the data types are comparable."

        if node[0] == 'fun_call':
            if node[1] == 'Inc':
                self.env[node[2][1]] = self.walkTree(node[2]) + self.walkTree(node[3])
                return(self.env[node[2][1]])
            elif node[1] == 'Dec':
                self.env[node[2][1]] = self.walkTree(node[2]) - self.walkTree(node[3])
                return(self.env[node[2][1]])
            elif node[1] == 'Ini':
                self.env[node[2][1]] = self.walkTree(node[3])
                return(self.env[node[2][1]])
            else:
                return("Function not defined")

        if node[0] == 'process_def':
            if 'var_assign' in node[2]:
                print("After Inicio:, only expressions are allowed, which represent any element of the language, with the exception of the declaration of variables.")
            else:
                self.env[node[1]] = node[2]

        if node[0] == 'process_call':
            try:
                return self.walkTree(self.env[node[1]])
            except:
                print("The called function is not defined")

        if node[0] == 'process_def_parameters':
            if 'var_assign' in node[3]:
                print("After Inicio:, only expressions are allowed, which represent any element of the language, with the exception of the declaration of variables.")
            else:
                if node[2] in node[3]:
                    self.env[node[1]] = tuple([node[3],node[2]])
                    print("Se guardo")
                else:
                    print("Error, the defined procedure does not use the set parameter")

        if node[0] == 'process_call_parameters':
            try:
                x = list(self.env[node[1]])
                y = list(x[0])
                z = x[1]
                cont = 0
                while z != y[cont]:
                    cont+=1
                y[cont] = node[2]
                return self.walkTree(tuple(y))
            except:
                print("The called function is not defined")


        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return "Undefined variable '"+node[1]+"' found!"
        if node[0]== 'while_loop':
            loop_sentence = node[1][1]
            loop_setup = self.walkTree(node[2])
            val= node[2][1][1]
            i= self.walkTree(node[2][1])
            print (i)
            while True:
                #self.walkTree(loop_sentence)
                print(node[1])
                self.walkTree(node[1])
                if self.walkTree(node[2]):
                    print ("Se cumple la condición")
                    break
                #i+=1
                #del env[node[2][1][1]]
                #self.env[val] = i


        if node[0] == 'for_loop':
            #return ('for_loop', p.var, p.expr, p.expr, p.statement)
            try:
                tempKey = node[1][1]
                tempVal = self.env[node[1][1]]
            except:
                pass

            self.env[node[1][1]] = node[2][1]

            try:
                loop_count = self.env[node[2][0]]
            except:
                loop_count = node[2][1]

            val = node[2][0]
            print(val)
            loop_limit = node[3][1]
            res = self.walkTree(node[2])
            for i in range(loop_count+1, loop_limit+1):
                self.env[node[1][1]] = self.env[node[1][1]] + 1
                if res is not None:
                    self.walkTree(node[4])

            del self.env[node[1][1]]
            try:
                self.env[tempKey] = tempVal
            except:
                pass
#----------------------Lexing run--------------------
'''
if __name__ == '__main__':
    lexer = BasicLexer()
    env = {}
    while True:
        try:
            text = input('DodeFast >>> ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)

#--------------------Parsing run----------------------

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('DodeFast >>> ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
    '''
#---------------------Full run-----------------------

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('DodeFast >>> ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            tree = parser.parse(lex)
            BasicExecute(tree, env)
#            print(tree)
