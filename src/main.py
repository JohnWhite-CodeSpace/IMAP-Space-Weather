from datetime import datetime, timedelta
from IMAP_Module.DataLoader import DataLoader

DATE_RUN = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def download_products(loader,  products, instrument: str = None, dir_name: str = None):
    files = products["files"]
    total = len(files)

    for num, product in enumerate(files, start=1):
        if instrument:
            loader.downloadData(instrument, product, "packets", dir_name=dir_name)
        else:
            loader.downloadData(product, 'archive', dir_name=dir_name)
        progress = num / total
        bar_length = 40
        filled = int(bar_length * progress)
        bar = "#" * filled + "-" * (bar_length - filled)
        if instrument:
            print(f"\r{instrument.upper()} packet download: [{bar}] {progress:.0%}", end="", flush=True)
        else:
            print(f"\rARCHIVE packet download: [{bar}] {progress:.0%}", end="", flush=True)
    print()

if __name__ == '__main__':
    print("Script Started")
    print(DATE_RUN)
    DataLoader = DataLoader('../configs/IMAP_Config.yml')
    # log_data = DataLoader.getLogData("2026", "100", "1")
    #
    # print(f"LOG DATA: \n {log_data}\n\n")
    # packet_data = DataLoader.getPacketData("2026", "100", "12", "00")
    # print(f"PACKET DATA: \n {packet_data}\n\n")
    # packet_data_utc = DataLoader.getPacketData(time_utc_start="2026-04-10T12:00:00", time_utc_end="2026-04-10T12:10:00")
    # print(f"PACKET DATA UTC: \n {packet_data_utc}\n\n")
    # archive_ok = DataLoader.getArchiveData("2026", "04", "10")
    # print(f"ARCHIVE OK: \n {archive_ok}\n\n")
    # archive_since_ok = DataLoader.getArchiveData(since="20260410")
    # print(f"ARCHIVE SINCE OK: \n {archive_since_ok}\n\n")
    # download_ok = DataLoader.downloadData("2026", "100", "10")

    ####################################################################################################################
    ## THIS PIPELINE NEEDS A VALID API KEY
    # instruments = ["swe", "glows", "codice", "mag", "hit"]
    # year = 2026
    # month = 4
    # start_date = datetime(year, month, 1)
    # if month == 12:
    #     end_date = datetime(year + 1, 1, 1)
    # else:
    #     end_date = datetime(year, month + 1, 1)
    # for instrument in instruments:
    #
    #     all_products = {"files": []}
    #     current_date = start_date
    #     while current_date < end_date:
    #         next_date = current_date + timedelta(days=1)
    #         products = DataLoader.getDataProducts(instrument, time_utc_start=current_date.strftime("%Y-%m-%dT%H:%M:%S"), time_utc_end=next_date.strftime("%Y-%m-%dT%H:%M:%S"))
    #         if products and "files" in products:
    #             all_products["files"].extend(products["files"])
    #         current_date = next_date
    #
    #     print(f"PRODUCTS OK {instrument.upper()}:\n" f"{all_products}\n")
    #     download_products(DataLoader,instrument, all_products)

    ####################################################################################################################
    ##### ARCHIVE DATA DOWNLOAD #####
    archive_since_ok = DataLoader.getArchiveData(since="20260401")
    download_products(DataLoader, archive_since_ok, dir_name="All")

    print("Script Ended")
