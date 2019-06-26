import ast
from ast import parse, Call, walk
import importlib
import inspect
import astor



# Global Variable that stores the traceable paramaters of fit or fit_gen functions.
traceParams= []


# This class takes tree as input and walks through
# all the nodes are pulls out Import Statements, fit, fit_gen compile functions
class Analyzer(ast.NodeVisitor):

    imports = []
    importFroms = []
    calls = []
    fitParams = []

    nn_end_no = 0
    nn_target_id = ''

    # Parser function that collects all import statements
    def visit_Import(self, node):
        # print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
        Analyzer.imports.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))

    #  Parser function that collects all import from statements
    def visit_ImportFrom(self, node):
        # print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
        Analyzer.importFroms.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))


    # Fit Generator, compile functions are collected here
    def visit_Call(self,node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.Attribute):
                if value.attr in ["compile"]:
                    Analyzer.calls.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
                if value.attr in ["fit","fit_generator"]:
                    # print('-----------------')
                    # print(value.attr)
                    # print('-----------------')
                    Analyzer.calls.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
                    args = node.args
                    for arg in args:
                        if isinstance(arg, ast.Str):
                            traceParams.append(arg.s)
                            Analyzer.fitParams.append(arg.s)
                        if isinstance(arg, ast.Name):
                            traceParams.append(arg.id)
                            Analyzer.fitParams.append(arg.id)
                    kws = node.keywords
                    for kw in kws:
                        if isinstance(kw.value, ast.Tuple):
                            pars = []
                            for k in kw.value.elts:
                                if isinstance(k, ast.Name):
                                    pars.append(k.id)
                                if isinstance(k, ast.Num):
                                    pars.append(k.n)
                            Analyzer.fitParams.append((kw.arg, pars))
                        if isinstance(kw.value, ast.Num):
                            traceParams.append(kw.arg) #epochs
                            Analyzer.fitParams.append((kw.arg, kw.value.n))
                        if isinstance(kw.value, ast.Name):
                            traceParams.append(kw.value.id)
                            Analyzer.fitParams.append((kw.arg, kw.value.id))
                        if isinstance(kw.value, ast.List):
                            pars = []
                            for k in kw.value.elts:
                                if isinstance(k, ast.Name):
                                    pars.append(k.id)
                                if isinstance(k, ast.Num):
                                    pars.append(k.n)
                            Analyzer.fitParams.append((kw.arg, pars))
                if value.attr in ["compile"]:
                    Analyzer.nn_end_no = value.lineno
                    Analyzer.nn_target_id = value.value.id


#This class takes the tree as input and
# traces back the variables of fit functions
class Tracker(ast.NodeVisitor):

    paramsStatements = []
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in traceParams:
                Tracker.paramsStatements.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
        elif isinstance(node.targets[0], ast.Tuple):
            for k in node.targets[0].elts:
                if isinstance(k.id, ast.Name):
                    if k.id in traceParams:
                        Tracker.paramsStatements(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
        else:
            Tracker.paramsStatements(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
        # if node.targets[0].id in traceParams:
        #     print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))



# Neural Network Schema Analyser
class GlobalUseCollector(ast.NodeVisitor):
    occurances = []
    def __init__(self, name):
        self.name = name
        # track context name and set of names marked as `global`
        self.context = [('global', ())]

    def visit_FunctionDef(self, node):
        self.context.append(('function', set()))
        self.generic_visit(node)
        self.context.pop()

    def visit_ClassDef(self, node):
        self.context.append(('class', ()))
        self.generic_visit(node)
        self.context.pop()

    def visit_Lambda(self, node):
        # lambdas are just functions, albeit with no statements
        self.context.append(('function', ()))
        self.generic_visit(node)
        self.context.pop()

    def visit_Global(self, node):
        assert self.context[-1][0] == 'function'
        self.context[-1][1].update(node.names)

    def visit_Name(self, node):
        ctx, g = self.context[-1]
        if node.id == self.name and (ctx == 'global' or node.id in g):
            # print('{} used at line {}'.format(node.id, node.lineno))
            GlobalUseCollector.occurances.append(node.lineno)


# Neural Network Extracter
class NNExtracter(ast.NodeVisitor):

    cnnStatements = []

    def visit_Assign(self, node):
        if node.lineno in GlobalUseCollector.occurances and node.lineno < Analyzer.nn_end_no:
            NNExtracter.cnnStatements.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))

    def visit_Call(self,node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.Attribute):
                if value.lineno in GlobalUseCollector.occurances and value.lineno < Analyzer.nn_end_no:
                    NNExtracter.cnnStatements.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))


# Iterator utility function. It has 3 params
# list to be written to file - ls
# message to be shown on the top of the file
# filename- filename to be created in the output
def iterator(ls, message, filename):
    file = open(filename,'a');
    file.write("\n\n"+ message+": \n")
    file.write("-------------------------- \n")
    for ob in ls:
        # print(ob)
        file.write(str(ob))

    file.close()


# main function
def main():
    tree = astor.code_to_ast.parse_file('cnn.py')
    analyzer = Analyzer()
    analyzer.visit(tree)
    # iterator(analyzer.imports,"Import Statements","imports.txt")
    # iterator(analyzer.importFroms, "Import From Statements","imports.txt")
    iterator(analyzer.calls, "Function calls","calls.txt")
    iterator(analyzer.fitParams,"Fit Parameters","fitparams.txt")
    tracker = Tracker()
    tracker.visit(tree)
    iterator(tracker.paramsStatements,"Parameters backtrack","fitparams.txt")
    GlobalUseCollector(Analyzer.nn_target_id).visit(tree)
    NNExtracter().visit(tree);
    iterator(NNExtracter.cnnStatements, "Neural Network","nn.txt")


if __name__ == "__main__":
    main()
