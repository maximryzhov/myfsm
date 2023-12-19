from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar

from utils import DotPath

# TODO: 1. логические операторы 2. циклы

N = TypeVar('N', bound='Node')

class Node(metaclass=ABCMeta):
    """
    Логический узел
    """  
    @abstractmethod
    def __call__(self, context=None, *args, **kwargs):
        raise NotImplementedError()

class Value(Node):
    """
    Возвращает переданное значение обратно
    """
    def __init__(self, val: Any):
        self.val  = val
    
    def __call__(self, context=None, *args, **kwargs):
        return self.val

class Var(Node):
    """
    Устанавливает переменную
    """
    def __init__(self, name: str):
        self.name  = name
    
    def __call__(self, context=None, *args, **kwargs):
        return DotPath.get_value(context.data, self.name)

class Op(Node, metaclass=ABCMeta):
    """
    Выполняет операцию над переменной
    """
    def __init__(self, var1: Var, var2:Any) -> None:
        self.var1 = var1
        self.var2 = var2

class Set(Op):  
    def __call__(self, context=None, *args, **kwargs):
        DotPath.set_value(context.data, self.var1.name, self.var2(context))
    
class Add(Op):
    def __call__(self, context=None, *args, **kwargs):
       DotPath.set_value(context.data, self.var1() + self.var2(context))

class Sub(Op):
    def __call__(self, context=None, *args, **kwargs):
        DotPath.set_value(context.data, self.var1() - self.var2(context))

class Mul(Op):
    def __call__(self, context=None, *args, **kwargs):
        DotPath.set_value(context.data, self.var1() * self.var2(context))

class Div(Op):
    def __call__(self, context=None, *args, **kwargs):
        DotPath.set_value(context.data, self.var1() / self.var2(context))

class Cmp(Node):
    """
    Сравнивает переменную со значением или другой переменной
    """
    def __init__(self, var1: Var, var2: N) -> None:
        self.var1 = var1
        self.var2 = var2


class IsEqual(Cmp):
    def __call__(self, context=None, *args, **kwargs):
        return self.var1(context) == self.var2(context)


class IsMore(Cmp):
    def __call__(self, context=None, *args, **kwargs):
        return self.var1(context) > self.var2(context)

class IsLess(Cmp):
    def __call__(self, context=None, *args, **kwargs):
        return self.var1(context) < self.var2(context)

class Func(Node):
    """
    Выполняет функцию и возвращает значение
    """
    def __init__(self, name="NoOp", *variables) -> None:
        self.vars = variables
        self.name = name

    def __call__(self, context=None, *args, **kwargs):
        func = context.callbacks.get(self.name)
        if func and callable(func):
            return func(context, *[v(context) for v in self.vars])


class NoOp(Func):
    def __call__(self, context=None, *args, **kwargs):
        pass


CMP = TypeVar('CMP', bound='Cmp')

class IfElse(Node):
    """
    Оператор ветвления
    """
    def __init__(
        self, cond: CMP, branch1: N|None = None, branch2: N|None = None
    ) -> None:
        self.cond = cond
        self.branch1 = branch1 or NoOp()
        self.branch2 = branch2 or NoOp()

    def __call__(self, context=None, *args, **kwargs):
        if self.cond(context):
            return self.branch1(context)
        else:
            return self.branch2(context)
  
class Root(Node):
    """
    Контейнер для последовательного выпонения нескольких узлов
    """
    def __init__(self) -> None:
        self.children = []
        
    def add_child(self: "Root", child: N | list[N]):
        if isinstance(child, list):
            self.children += child
        elif isinstance(child, Node):
            self.children.append(child)    

    def __call__(self, context=None, *args, **kwargs):
        for child in self.children:
            child(context)