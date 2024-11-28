import os, zipfile, requests
from lclib.download import readZip
from lclib.net_lib import get_local_ip
import lclib.twic
from lclib.singleton import SingletonMeta

from ..models import TwicConfigModel, TwicFolderConfigModel, TwicStatusModel, STATUS_UNZIPPED

class TwicProxy(metaclass=SingletonMeta):

    def __init__(self):
        print("Init Proxy")
        print(get_local_ip())
        self.refresh()

    def refresh(self):
        try:
            ip = get_local_ip()
            self.twic_config = TwicConfigModel.load()
            self.twic_folder = TwicFolderConfigModel.objects.get(ip=ip)
            if not self.twic_folder:
                raise Exception(f"No TWIC folder found for this IP: {ip}")
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
        self.highest_issue = lclib.twic.get_highest_twic_issue(self.last_issue, self.base_url, self.twic_pattern)

        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.unzip_dir, exist_ok=True)

    def get_next_twic(self):
        while self.highest_issue > self.last_issue:
            self.highest_issue += 1
            lclib.twic.download_twic_file(self.base_url, self.highest_issue, self.download_dir, self.unzip_dir, self.twic_pattern)
            self.twic_status_latest = TwicStatusModel.objects(number = self.highest_issue, status = STATUS_UNZIPPED)
            self.twic_status_latest.save()