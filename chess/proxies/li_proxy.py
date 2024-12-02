import os
from libs.lcl.lcl.twic import download_twic_file, get_highest_twic_issue
from libs.lcl.lcl.net_lib import get_local_ip
from libs.lcl.lcl.singleton import SingletonMeta
from ..models import LichessConfigModel, LichessStatusModel, LichessFolderConfigModel, STATUS_UNZIPPED


class LiProxy(metaclass=SingletonMeta):

    def __init__(self):
        print("Init Lichess Proxy")
        print(get_local_ip())
        self.refresh()

    def refresh(self):
        try:
            self.ip = get_local_ip()
            self.li_config = LichessConfigModel.load()
            self.li_folder = LichessFolderConfigModel.objects.get(ip=self.ip)
            if not self.li_folder:
                raise Exception(f"No Lichess folder found for this IP: {self.ip}")
            #self.twic_status_latest = LichessStatusModel.objects.filter(status__gt=0).order_by('-number').first()
            #if not self.twic_status_latest:
                #raise Exception(f"No TWIC status found")
        except Exception as e:
            raise Exception(e)
        self.download_folder_path = self.li_folder.download_folder_path
        self.unzip_folder_path = self.li_folder.unzip_folder_path
        self.script_name_unzst = self.li_config.script_name_unzst
        os.makedirs(self.unzip_folder_path, exist_ok=True)

    def unzip_started(self, year, month):
        try:
            self.twic_status_latest = LichessStatusModel.objects.create(year = year, month = month, status = STATUS_UNZIPPED)
            self.twic_status_latest.save()
        except Exception as e:
            print("Error in DB Update: ", e)
        self.refresh()