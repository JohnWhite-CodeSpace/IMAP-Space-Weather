import ialirt_data_access as IDA_IMAP
from .Logger import Logger
from typing import Optional
import traceback as tb
import yaml
import requests
from pathlib import Path
class DataLoader:
    def __init__(self, config: str):
        self.logger = Logger(config, 'DataLoader')
        try:
            with open(config, "r", encoding="utf-8") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as ex:
            traceback = tb.format_exc()
            state = {"error_code": -1, "error_msg": str(ex)}
            self.logger.LogProcess(state, traceback)

    def _validate_query_params(self, year: str, doy: str, instance: Optional[str] = "1", hh: Optional[str]=None, mm: Optional[str]=None, ss: Optional[str]=None):

        if not(year.isdigit() and len(year)==4):
            self.logger.LogProcess({'error_code': '-1', 'error_message': 'Year must be four digits string'})
            return False
        if not(doy.isdigit() and 1<=int(doy)<=366):
            self.logger.LogProcess({'error_code': '-1', 'error_message': 'Day of the year must be string with a value between 1 and 366'})
            return False
        if instance is not None and(not instance.isdigit() or not instance in {"1", "2"}):
            self.logger.LogProcess({'error_code': '-1', 'error_message': 'Instance must be string with a value either set to 1 or 2'})
            return False

        if hh is not None and (not hh.isdigit() or not 0 <= int(hh) <= 23):
            self.logger.LogProcess(
                {'error_code': '-1', 'error_message': 'Hour must be a string between 00 and 23'})
            return False
        if mm is not None and (not mm.isdigit() or not 0 <= int(mm) <= 59):
            self.logger.LogProcess(
                {'error_code': '-1', 'error_message': 'Minute must be a string with a value between 00 and 59'})
            return False
        if ss is not None and (not ss.isdigit() or not 0 <= int(ss) <= 59):
            self.logger.LogProcess(
                {'error_code': '-1', 'error_message': 'seconds must be a string with a value between 00 and 59'})
            return False
        return True

    def getLogData(self, year: str, doy: str, instance: str):
        try:
            if self.config['IMAP_API']['api_key'] == 'secret':
                url = self.config['IMAP_API']['BaseUrl']
            else:
                url = f"{self.config['IMAP_API']['BaseUrl']}/{self.config['IMAP_API']['api_key']}"
            query_params = {"year": year, "doy": doy, "instance": instance,}
            self._validate_query_params(**query_params)
            url = url+self.config['IMAP_API']['endpoint']['log_data']
            response = requests.get(url, params=query_params)
            self.logger.LogProcess({'error_code': response.status_code, 'error_msg': response.text})
            return response.json()
        except Exception as ex:
            traceback = tb.format_exc()
            state = {"error_code": -1, "error_msg": str(ex)}
            self.logger.LogProcess(state, traceback)
            return {}

    def getPacketData(self, year: Optional[str] = None, doy: Optional[str] = None, hh: Optional[str] = None,
                      mm: Optional[str] = None, ss: Optional[str] = None, time_utc_start: Optional[str] = None,
                      time_utc_end: Optional[str] = None):
        try:
            if self.config['IMAP_API']['api_key'] == 'secret':
                url = self.config['IMAP_API']['BaseUrl']
            else:
                url = f"{self.config['IMAP_API']['BaseUrl']}/{self.config['IMAP_API']['api_key']}"

            utc_params = {utc_key: utc_value for utc_key, utc_value in
                          {"time_utc_start": time_utc_start, "time_utc_end": time_utc_end}.items()
                          if utc_value is not None}

            if utc_params:
                query_params = {"time_utc_start": utc_params["time_utc_start"]}
                if time_utc_end:
                    query_params["time_utc_end"] = time_utc_end
            else:
                query_params = {"year": year, "doy": doy}
                if hh:
                    query_params["hh"] = hh
                if mm:
                    query_params["mm"] = mm
                if ss:
                    query_params["ss"] = ss

            self._validate_query_params(**query_params)
            url = url +self.config['IMAP_API']['endpoint']['packet_data']
            response = requests.get(url, params=query_params)
            if response.status_code != 200:
                self.logger.LogProcess({'error_code': response.status_code, 'error_msg': response.text})
                return {}
            self.logger.LogProcess({'error_code': '0', 'error_msg': ''})
            return response.json()

        except Exception as ex:
            traceback = tb.format_exc()
            state = {"error_code": -1, "error_msg": str(ex)}
            self.logger.LogProcess(state, traceback)
            return {}

    def downloadData(self, filename: str, filetype: str, download_dir: Optional[Path] = None):
        if download_dir is None:
            download_dir = self.config['Data']['IMAP_DOWNLOAD_DIR']
        url = self.config['IMAP_API']['BaseUrl']