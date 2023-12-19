import random

from nodes  import *
from state_machine import State, Machine
from runners import Task, TaskRunner

if __name__ ==  "__main__":
    # Из состояния START переходим в STAGE1 без всяких условий
    start = State("start", next_logic=Value("stage_1"))
    # Из состояния STAGE1 переходим в  STAGE2, только когда переменная a>2
    stage_1 = State("stage_1", next_logic=IfElse(IsMore(Var("a"), Value(2)), Value("stage_2"),  Value("stage_1")))
    # При входе в состояние STAGE2 устанавливаем переменной a случайное значение от 0 до 1
    # Из состояния STAGE2 переходим в SUCCESS, если переменная some_data.b.0 > 0.5
    stage_2 = State("stage_2",  IfElse(IsMore(Var("some_data.b.0"), Value(0.5)), Value("success"),  Value("fail")), enter_logic=Set(Var("some_data.b.0"), Func("get_rand_val")))
    fail = State("fail")
    success = State("success")

    m = Machine()
    m.add_state(start)
    m.add_state(stage_1)
    m.add_state(stage_2)
    m.add_state(fail)
    m.add_state(success)
    m.set_current("start")

    # TODO: отделить логику от данных
    context = {
        "a": 0,
        "some_data": {"b": [0, 0, 0]},
        "get_rand_val": lambda: random.random()
    }
    
    main_task = Task("MAIN", m, context)

    event_queue = [
        {"name":  "idle", "task": "MAIN"},
        {"name":  "advance", "task": "MAIN"},
        {"name":  "change_state", "task": "MAIN",  "payload": {"path": "a", "value": 3}},
        {"name":  "advance", "task": "MAIN"},
        {"name":  "advance", "task": "MAIN"},
        {"name":  "advance", "task": "MAIN"},
        {"name":  "advance", "task": "MAIN"},
    ]

    runner = TaskRunner(event_queue)
    runner.add_task(main_task)
    runner.run()  