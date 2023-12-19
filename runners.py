import time

from utils import DotPath

class Task:
    def __init__(self, name, machine, context) -> None:
        self.name = name
        self.machine = machine
        self.context = context

class TaskRunner:
    def __init__(self, event_queue) -> None:
        self.event_queue = event_queue
        self.tasks = {}
    
    def add_task(self, task):
        self.tasks[task.name] = task
    
    def run(self):
        # TODO: сохранять состояние контекста при каждом изменении/переходе

        for event in self.event_queue:
            task_name = event["task"]
            task = self.tasks.get(task_name)
            if task is None:
                print(f"ПОЛУЧЕНО СОБЫТИЕ, НО ЗАДАЧА {task_name} НЕ ЗАРЕГИСТРИРОВАНА")
                continue

            if event["name"] == "idle":
                print("ОЖИДАНИЕ")

            elif event["name"] == "advance":
                result = task.machine.advance(task.context)
                if result is False:
                    print(f"ЗАДАЧА {task_name} ЗАВЕРШЕНА")
                    del self.tasks[task_name]

            elif event["name"] == "change_state":
                DotPath.set_value(task.context, event["payload"]["path"], event["payload"]["value"]) 
            
            else:
                print("НЕИЗВЕСТНОЕ СОБЫТИЕ")

            time.sleep(0.2)
        
        print("ОЧЕРЕДЬ СОБЫТИЙ ИСЧЕРПАНА")
