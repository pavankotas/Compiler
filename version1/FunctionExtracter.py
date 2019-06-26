import ast
import astor


# Import Statements, fit, compile function parser
class Analyzer(ast.NodeVisitor):

    imports = []
    importFroms = []
    calls = []
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
                if value.attr in ["fit_generator","fit","compile"]:
                    # print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
                    Analyzer.calls.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
                if value.attr in ["compile"]:
                    Analyzer.nn_end_no = value.lineno
                    Analyzer.nn_target_id = value.value.id


# Neural Network Schema Analyser
class GlobalUseCollector(ast.NodeVisitor):
    occurances = []
    def __init__(self, name):
        self.name = name
        # track context name and set of names marked as `global`
        self.context = [('global', ())]

    def visit_FunctionDef(self, node):
        print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
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
    # file.write("\n"+ message+": \n")
    # print(message+": \n")
    for ob in ls:
        # print(ob)
        file.write(ob)

    file.close()


# main function
def main():
    tree = astor.code_to_ast.parse_file('poc.py')
    analyzer = Analyzer()
    analyzer.visit(tree)
    # iterator(analyzer.imports,"Import Statements","imports.txt")
    # iterator(analyzer.importFroms, "Import From Statements","imports.txt")
    # iterator(analyzer.calls, "Other call functions","calls.txt")
    GlobalUseCollector(Analyzer.nn_target_id).visit(tree)
    NNExtracter().visit(tree);
    # iterator(NNExtracter.cnnStatements, "Neural Network","nn.txt")


if __name__ == "__main__":
    main()
