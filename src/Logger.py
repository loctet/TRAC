from MiniTimer import *
from Z3Runner import Z3Runner

class Logger(MiniTimer):
    
    def __init__(self, log, non_stop) -> None:
        """
        Extends MiniTimer to provide logging functionality with the option to stop execution based on specific conditions.

        :param log: If True, enables logging of messages.
        :type log: bool
        :param non_stop: If True, execution will not stop even if conditions to stop are met.
        :type non_stop: bool
        """
        self.log = log
        self.non_stop = non_stop
        pass

    def logIt(self, message):
        """
        Logs a message if logging is enabled.

        :param message: The message to log.
        :type message: str
        :return: None
        :rtype: NoneType
        """
        if self.log:
            print(message)

    def should_stop_if_time_out(self, o):
        """
        Checks if execution should stop due to a timeout.

        :param o: An object that contains a `time_out` attribute and a `transition_processor` with timing information.
        :type o: object
        :return: True if execution should stop due to a timeout, False otherwise.
        :rtype: bool
        """
        if o.time_out == 0: 
            return False
        if o.transition_processor.infos["is_time_out"] :
            self.info["is_time_out"] = True
            return True
        if self.get_ellapsed_time() > self.time_out:
            self.info["is_time_out"] = True
            return True
        
    def should_stop(self, path, item, trGrinder):
        """
        Checks if execution should stop based on the outcome of Z3 model execution.

        :param path: The path of the Z3 model file.
        :type path: str
        :param item: The transition item being processed.
        :param trGrinder: An instance of `TransactionsGrinder` containing execution details and output.
        :type trGrinder: TransactionsGrinder
        :return: True if execution should stop due to a failure in Z3 model execution, False otherwise.
        :rtype: bool
        """
        if self.non_stop:
            return False
        
        if not Z3Runner.execute_model(trGrinder, path):
            print(f"Error from this transitions:{item['from']}_{item['actionLabel']}({item['input']})_{item['to']}")
            print(trGrinder.output)
            return True