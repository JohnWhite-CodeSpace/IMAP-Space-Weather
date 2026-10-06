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

    def getDataProducts(self, instrument: Optional[str] = None, time_utc_start: Optional[str] = None,
                            time_utc_end: Optional[str] = None, met_in_utc_start: Optional[str] = None,
                            met_in_utc_end: Optional[str] = None):
        try:
            query_params = {}
            if instrument is not None:
                query_params["instrument"] = met_in_utc_start
            if time_utc_start is not None:
                query_params["time_utc_start"] = time_utc_start
            if time_utc_end is not None:
                query_params["time_utc_end"] = time_utc_end
            if met_in_utc_start is not None:
                query_params["met_in_utc_start"] = met_in_utc_start
            if met_in_utc_end is not None:
                query_params["met_in_utc_end"] = met_in_utc_end

            url = self.config['IMAP_API']['BaseUrl']
            url += self.config['IMAP_API']['endpoint']['packet_data']
            response = requests.get(url, params=query_params)
            if response.status_code != 200:
                self.logger.LogProcess({'error_code': response.status_code, 'error_msg': response.text})
                return {}
            self.logger.LogProcess({'error_code': 0, 'error_msg': ''})
            return response.json()

        except Exception as ex:
            traceback = tb.format_exc()
            state = {"error_code": -1, "error_msg": str(ex)}
            self.logger.LogProcess(state, traceback)
            return False

    def getArchiveData(self, year: Optional[str] = None, month: Optional[str] = None, day: Optional[str] = None,
                      version: Optional[str] = None, since: Optional[str] = None,):
        try:
            if since and (year or month or day):
                self.logger.LogProcess({'error_code': -1, 'error_msg': 'Invalid parameter combination'})
                return False

            if not since and ((day and not month) or (month and not year)):
                self.logger.LogProcess({'error_code': -1, 'error_msg': 'Invalid parameter order'})
                return False

            query_params: dict = {}
            if since is not None:
                query_params["since"] = since
            if year is not None:
                query_params["year"] = year
            if month is not None:
                query_params["month"] = month
            if day is not None:
                query_params["day"] = day
            if version is not None:
                query_params["version"] = version

            url = self.config['IMAP_API']['BaseUrl']
            url += self.config['IMAP_API']['endpoint']['archive_data']
            response = requests.get(url, params=query_params)
            if response.status_code != 200:
                self.logger.LogProcess({'error_code': response.status_code, 'error_msg': response.text})
                return {}
            self.logger.LogProcess({'error_code': 0, 'error_msg': ''})
            return response.json()

        except Exception as ex:
            traceback = tb.format_exc()
            state = {"error_code": -1, "error_msg": str(ex)}
            self.logger.LogProcess(state, traceback)
            return False

    def downloadData(self, filename: str, filetype: str, instrument: Optional[str] = None, download_dir: Optional[Path] = None, dir_name: Optional[str] = None,):
        try:
            url = self.config['IMAP_API']['BaseUrl']
            if filetype in ("logs", "packets"):
                url+=f"/api-key{self.config['IMAP_API']['endpoint']['download_data']}{filetype}/{filename}"
                if download_dir is None:
                    download_dir = self.config['Data']['InstrumentDirMapping'][instrument.lower()]
            else:
                url+=f"{self.config['IMAP_API']['endpoint']['download_data']}{filetype}/{filename}"
                if download_dir is None:
                    download_dir = self.config['Data']['ArchivePath'] + (f'/{dir_name}' or '')
            download_dir = Path(download_dir)
            download_dir.mkdir(parents=True, exist_ok=True)
            destination = download_dir/filename
            if destination.exists():
                self.logger.LogProcess({"error_code": -1, "error_msg": "File already exists!"})
                return False, destination

            self.logger.LogProcess({"process_state": 0, "message": f"Downloading {filename} to {destination} with url {url}"})
            response = requests.get(url, stream=True)

            if response.status_code != 200:
                self.logger.LogProcess({'error_code': response.status_code, 'error_msg': response.text})
                return {}, destination

            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return True, destination

        except Exception as ex:
            traceback = tb.format_exc()
            state = {"error_code": -1, "error_msg": str(ex)}
            self.logger.LogProcess(state, traceback)
            return {}, None

