from sre_parse import State
from lark import Transformer, Tree
from llvmlite import ir
from . import __classes as _


def StepOneTransformer() -> Transformer:
    return (
        TypeTransformer() *
        LiteralTransformer() *
        IdentifierTransformer() *
        OperationTransformer() *
        FunctionTransformer()
    )


def StepTwoTransformer() -> Transformer:
    return (
        StatementTransformer() *
        AssignmentTransformer()
    )


class TypeTransformer(Transformer):
    def integer(self, args):
        return _.integer_type(32)

    def decimal(self, args):
        return _.decimal_type()

    def boolean(self, args):
        return _.boolean_type()

    def string(self, args):
        return _.string_type(-1)

    def raw(self, args):
        return _.raw_type()


class LiteralTransformer(Transformer):
    def lstring(self, args):
        return _.Literal(_.string_type(len(args[0])), args[0])

    def lnumber(self, args):
        if args[0].isdigit():
            return _.Literal(_.integer_type(32), int(args[0]))
        else:
            return _.Literal(_.decimal_type(), float(args[0]))

    def lraw(self, args):
        return _.Literal(_.raw_type(), bytes(args[0]))

    def lboolean(self, args):
        return _.Literal(_.boolean_type(), args[0] == 'true')


class IdentifierTransformer(Transformer):
    def identifier(self, args):
        return _.Identifier(args[0])


class OperationTransformer(Transformer):
    def operation(self, args):
        lhs = args[0]
        rhs = args[2]
        op = args[1].children[0]

        # Compile time eval here?
        ltree = isinstance(lhs, Tree) and not isinstance(
            lhs, _.FaerieStructure)
        rtree = isinstance(rhs, Tree) and not isinstance(
            rhs, _.FaerieStructure)

        if ltree and rtree:
            tr = StepOneTransformer()
            if ltree:
                lhs = tr.transform(lhs)
            if rtree:
                rhs = tr.transform(rhs)

        return _.Operation(op, lhs, rhs)


class AssignmentTransformer(Transformer):
    def assignment(self, args):
        kind = args[0].data
        lhs = args[1]
        rhs = args[2]

        return _.Assignment(kind, lhs, rhs)

    def function_definition(self, args):
        return _.FunctionDefinition(args[0], args[1].children[0], args[2])


class FunctionTransformer(Transformer):
    def function_call_arguments(self, args):
        arglist = {}
        i = 0
        previous: _.Identifier | _.Literal | None = None
        while i < len(args):
            arg = args[i]
            if type(arg) in [_.Literal, _.Operation, _.FunctionCall] and not isinstance(previous, _.Identifier):
                arglist[f'_{i}'] = arg
            elif isinstance(arg, _.Literal) and isinstance(previous, _.Identifier):
                arglist[previous.name] = arg
            elif isinstance(arg, Tree) and not (isinstance(arg, _.Literal) or isinstance(arg, _.Identifier)):
                arg = StepOneTransformer().transform(arg)
                continue

            i += 1
            previous = arg

        return _.FunctionCallArguments(**arglist)

    def function_call(self, args):
        return _.FunctionCall(args[0], args[1])

    def function_definition_arguments(self, args):
        # 0 - type; 1 - identifier; 2 - default
        return [_.FunctionDefinitionArgument(args[i], args[i+1], args[i+2]) for i in range(0, len(args), 3)]


class StatementTransformer(Transformer):
    def if_(self, args):
        _previous = _.IfThenStatement(args[-3], args[-2], args[-1])
        for i in range(-4, -len(args), -2):
            _previous = _.IfThenStatement(args[i - 1], args[i], _previous)
        return _previous
