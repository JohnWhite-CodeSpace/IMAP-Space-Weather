import yaml
from datetime import datetime
import __main__ as main
class Logger:

    def __init__(self, config: str, object_name: str):
        try:
            with open(config, 'r') as log:
                self.config = yaml.load(log, Loader=yaml.FullLoader)
            self.filename = 'run_log_' + main.DATE_RUN
            self.object_name = object_name
        except Exception as ex:
            raise ex

    def LogProcess(self, object_response: dict, traceback: str = None):
        try:
            if traceback:
                log = f'{self.object_name} {datetime.now()}: {object_response} \n {traceback}'
            else:
                log = f'{self.object_name} {datetime.now()}: {object_response}'
            # print(log)
            self.saveLog(log)
        except Exception as ex:
            raise ex

    def saveLog(self, log: str):
        try:
            # print(f'{self.object_name} {datetime.now()}: {log}')
            with open(self.config['Logger']['LogFilePath']+self.filename, 'a') as log_file:
                log_file.write(log + '\n')
        except Exception as ex:
            raise ex
