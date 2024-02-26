from MiniTimer import *
from Z3Runner import Z3Runner

class Logger(MiniTimer):
    def __init__(self, log, non_stop) -> None:
        self.log = log
        self.non_stop = non_stop
        pass

    def logIt(self, message):
        if self.log:
            print(message)

    def should_stop_if_time_out(self, o):
        if o.time_out == 0: 
            return False
        if o.transition_processor.infos["is_time_out"] :
            self.info["is_time_out"] = True
            return True
        if self.get_ellapsed_time() > self.time_out:
            self.info["is_time_out"] = True
            return True
        
    def should_stop(self, path, item, trGrinder):
        if self.non_stop:
            return False
        
        if not Z3Runner.execute_model(trGrinder, path):
            print(f"Error from this transitions:{item['from']}_{item['actionLabel']}({item['input']})_{item['to']}")
            print(trGrinder.output)
            return True