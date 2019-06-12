import ast
import astor


def main():
    tree = astor.code_to_ast.parse_file('cnn.py')
    analyzer = Analyzer()
    analyzer.visit(tree)
    print(analyzer.nn_end_no)
    print(analyzer.nn_target_id)
    GlobalUseCollector(analyzer.nn_target_id).visit(tree)
    # analyzer.report()


class GlobalUseCollector(ast.NodeVisitor):
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
            print('{} used at line {}'.format(node.id, node.lineno))

class Analyzer(ast.NodeVisitor):
    nn_end_no = 0
    nn_target_id = ''


    # def __init__(self):
    #     self.stats = {"import": [], "from": []}

    # def visit_Import(self, node):
    #     print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
    #     # print(ast.dump(node,  annotate_fields=True))
        # for alias in node.names:
        #     self.stats["import"].append(alias.name)
        # self.generic_visit(node)

    # def visit_ImportFrom(self, node):
    #     print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
    # def visit_ImportFrom(self, node):
    #     for alias in node.names:
    #         self.stats["from"].append(alias.name)
    #     self.generic_visit(node)
    #
    # def report(self):
    #
    #     pprint(self.stats)

    def visit_Call(self,node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.Attribute):
                if value.attr in ["compile"]:
                    # print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
                    # print(ast.dump(node))
                    # print(value.attr)
                    # if isinstance(value.value, ast.Name):
                    # print(value.value.id)
                    # print(value.lineno)
                    Analyzer.nn_end_no = value.lineno
                    Analyzer.nn_target_id = value.value.id
                    # Analyzer.calls.append(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))

    # def visit_Call(self,node):
    #     for field, value in ast.iter_fields(node):
    #         if isinstance(value, ast.Name):
    #             print(value.id)
                # if isinstance(value.ctx, ast.Load):
                #     print(ast.Name(id='classifier', ctx=ast.Load()))
            #print(field)
            # if isinstance(value, ast.Attribute):
            #             print(value)


            # if isinstance(value, ast.Attribute):
            #     # list_name = "%s.%s" % (value.value.value.id, value.value.attr)
            #     if value.attr in ["fit_generator","fit","compile"]:
            #         print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
            # print(field)
            # print(field)
            # if isinstance(value, list):
            #    for a in value:
            #        if isinstance(a, ast.Name):
            #            print(a.id)

                #print(ast.dump(node))
        # if node.func == "classifier.fit_generator":
        #     print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
        # if node.func.id == "fit_generator":
        #     print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))



# print(ast.iter_fields(tree));


if __name__ == "__main__":
    main()

