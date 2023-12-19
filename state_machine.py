from typing_extensions import Self

from nodes import N


class Machine():
    def __init__(self):
        self.states = {}
        # TODO: обработка нескольких веток за один шаг с помощью курсоров/токенов?
        self.current_state_name = None
    
    def add_state(self, state):
        self.states[state.name] = state
    
    def set_current(self, state_name):
        self.current_state_name = state_name
        # TODO: валидация
       
    def step(self, context):
        current_state = self.states.get(self.current_state_name)
        next_state_name = current_state.get_next(context)
        next_state = self.states.get(next_state_name)
        if next_state is None:
            print("НЕТ СЛЕДУЮЩЕГО СОСТОЯНИЯ")
            return False
        current_state.on_exit(context)
        next_state.on_enter(context)
        self.current_state_name = next_state.name
        return True
        

class State():
    def __init__(self, name, next_logic=None, enter_logic=None, exit_logic=None):
        self.name = name
        self.next_logic = next_logic
        self.enter_logic = enter_logic
        self.exit_logic = exit_logic

    def on_enter(self, context) -> N:
        print(f"Вход в {self.name}")
        if self.enter_logic:
            return self.enter_logic(context) 

    def on_exit(self, context) -> N:
        print(f"Выход из {self.name}")  
        if self.exit_logic:
            return self.exit_logic(context) 
        
    def get_next(self, context) -> Self|None:
        if self.next_logic:
            return self.next_logic(context)   