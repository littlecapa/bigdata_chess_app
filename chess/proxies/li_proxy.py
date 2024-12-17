import os
from datetime import datetime
from lcl.lcl.net_lib import get_local_ip
from lcl.lcl.singleton import SingletonMeta
from lcl.lcl.pgn_file_manager import PgnFileManager
from lcl.lcl.file import append_to_file
from lcl.lcl.lichess import game_ok_eco, game_ok_commented, get_eco_filename, ignore_event
from ..models import LichessConfigModel, LichessStatusModel, LichessFolderConfigModel, STATUS_UNZIPPED, STATUS_PROCESSED


class LiProxy(metaclass=SingletonMeta):

    def __init__(self):
        print("Init Lichess Proxy")
        print(get_local_ip())
        self.refresh()
        self.pfm = PgnFileManager(split_folder =self.unzip_folder_path, eco_folder = self.eco_split_folder_path, commented_folder = self.evaluated_folder_path)

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
        self.eco_complete_folder_path = self.li_folder.eco_complete_folder_path
        self.eco_split_folder_path = self.li_folder.eco_split_folder_path
        self.evaluated_complete_folder_path = self.li_folder.evaluated_complete_folder_path
        self.evaluated_folder_path = self.li_folder.evaluated_folder_path
        self.script_name_unzst = self.li_config.script_name_unzst
        self.script_name_concat = self.li_config.script_name_concat
        self.elo_min_eco = self.li_config.elo_min_eco
        self.elo_min_commented = self.li_config.elo_min_commented
        os.makedirs(self.unzip_folder_path, exist_ok=True)

    def unzip_started(self, year, month):
        try:
            self.twic_status_latest = LichessStatusModel.objects.create(year = year, month = month, status = STATUS_UNZIPPED)
            self.twic_status_latest.save()
        except Exception as e:
            print("Error in DB Update: ", e)
        self.refresh()

    def extract(self, year, month):
        count = 0
        try:
            for game, metadata in self.pfm.read_from_split_files(year, month):
                filename = get_eco_filename(year, month, metadata)
                if not ignore_event(metadata):
                    if game_ok_eco(metadata, self.elo_min_eco):
                        append_to_file(os.path.join(self.eco_split_folder_path, filename), game)
                    if game_ok_commented(metadata, self.elo_min_commented):
                        append_to_file(os.path.join(self.evaluated_folder_path, filename), game)  
                count += 1
                if (count % 1e4) == 0:
                    print(f"Finished Game: {count} {datetime.now()}")
            self.twic_status_latest = LichessStatusModel.objects.create(year = year, month = month, status = STATUS_PROCESSED)
            self.twic_status_latest.save()
        except Exception as e:
            print("Error Extracting Games: ", e)
        self.refresh()