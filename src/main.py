from datetime import datetime
from IMAP_Module.DataLoader import DataLoader
DATE_RUN = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


if __name__ == '__main__':
    print("Script Started")
    print(DATE_RUN)
    DataLoader = DataLoader('../configs/IMAP_Config.yml')
    data = DataLoader.getLogData('2026', '002', '1')
    data2 = DataLoader.getPacketData('2026', '200')
    print(data)
    print(data2)
    print("Script Ended")
