import os
from lcl.lcl.twic import download_twic_file, get_highest_twic_issue
from lcl.lcl.net_lib import get_local_ip
from lcl.lcl.singleton import SingletonMeta
from ..models import TwicConfigModel, TwicFolderConfigModel, TwicStatusModel, STATUS_UNZIPPED


class TwicProxy(metaclass=SingletonMeta):

    def __init__(self):
        print("Init Proxy")
        print(get_local_ip())
        self.refresh()

    def refresh(self):
        try:
            self.ip = get_local_ip()
            self.twic_config = TwicConfigModel.load()
            self.twic_folder = TwicFolderConfigModel.objects.get(ip=self.ip)
            if not self.twic_folder:
                raise Exception(f"No TWIC folder found for this IP: {self.ip}")
            self.twic_status_latest = TwicStatusModel.objects.filter(status__gt=0).order_by('-number').first()
            if not self.twic_status_latest:
                raise Exception(f"No TWIC status found")
        except Exception as e:
            raise Exception(e)
        self.base_url = self.twic_config.download_base_url
        self.twic_pattern = self.twic_config.download_number_pattern

        self.download_dir = self.twic_folder.download_folder_path
        self.unzip_dir = self.twic_folder.unzip_folder_path

        self.last_issue = self.twic_status_latest.number
        self.highest_issue = get_highest_twic_issue(self.last_issue, self.base_url, self.twic_pattern)

        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.unzip_dir, exist_ok=True)

    def get_next_twic(self):
        while self.highest_issue > self.last_issue:
            self.last_issue += 1
            download_twic_file(self.base_url, self.last_issue, self.download_dir, self.unzip_dir, self.twic_pattern)
            try:
                self.twic_status_latest = TwicStatusModel.objects.create(number = self.last_issue, status = STATUS_UNZIPPED)
                self.twic_status_latest.save()
            except Exception as e:
                print("Error in DB Update: ", e)