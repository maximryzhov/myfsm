import time

class SimulationRunner:
    def __init__(self, machine, context, event_queue) -> None:
        self.machine = machine
        self.context = context
        self.event_queue = event_queue
    
    def run(self):
        # TODO: сохранять состояние контекста при каждом изменении/переходе
        for event in self.event_queue:
            if event["name"] == "idle":
                print("ОЖИДАНИЕ")
            elif event["name"] == "next":
                result = self.machine.step(self.context)
                if result is False:
                    break
            elif event["name"] == "set_var":
                self.context[event["payload"]["name"]] = event["payload"]["value"]
            else:
                print("НЕИЗВЕСТНОЕ СОБЫТИЕ")
            time.sleep(0.2)
        
        print("ОЧЕРЕДЬ СОБЫТИЙ ИСЧЕРПАНА")
