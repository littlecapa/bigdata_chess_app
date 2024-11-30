from django.db import models

class LichessFolderConfigModel(models.Model):

    ip = models.GenericIPAddressField(primary_key=True)  # IP as the primary key
    download_folder_path = models.CharField(max_length=255)
    unzip_folder_path = models.CharField(max_length=255)
    eco_split_folder_path = models.CharField(max_length=255)
    reduced_folder_path = models.CharField(max_length=255)
    evaluated_folder_path = models.CharField(max_length=255)
    script_folder_path  = models.CharField(max_length=255) 

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        abstract = False  # Ensures this isn't treated as an abstract model.

    def __str__(self):
        return self.ip

class TwicFolderConfigModel(models.Model):

    ip = models.GenericIPAddressField(primary_key=True)  # IP as the primary key
    download_folder_path = models.CharField(max_length=255)
    unzip_folder_path = models.CharField(max_length=255)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        abstract = False  # Ensures this isn't treated as an abstract model.

    def __str__(self):
        return self.ip

class LichessConfigModel(models.Model):

    download_base_url = models.CharField(max_length=255, default = "https://database.lichess.org/")
    download_month_pattern = models.CharField(max_length=255, default = "standard/lichess_db_standard_rated_<<year>>-<<month>>.pgn.zst")
    script_name_unzst = models.CharField(max_length=255, default = "lichess_unzst.sh")

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        abstract = False  # Ensures this isn't treated as an abstract model.

    def __str__(self):
        return self.download_base_url

class TwicConfigModel(models.Model):

    download_base_url = models.CharField(max_length=255, default = "https://theweekinchess.com/zips/")
    download_number_pattern = models.CharField(max_length=255, default = "twic<<number>>g.zip")

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        abstract = False  # Ensures this isn't treated as an abstract model.

    def __str__(self):
        return self.download_base_url
    
STATUS_NEW = 0
STATUS_DOWNLOADED = 1
STATUS_UNZIPPED = 2
STATUS_SPLITTED = 3
STATUS_PROCESSED = 4

class LichessStatusModel(models.Model):
    year = models.PositiveIntegerField()  # Year field
    month = models.PositiveIntegerField()  # Month field
    status = models.PositiveIntegerField(default = STATUS_NEW)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'month'], name='unique_year_month')
        ]
        verbose_name = "Year and Month Entry"
        verbose_name_plural = "Year and Month Entries"

    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.year}-{self.month:02d}: {self.status}" 

class TwicStatusModel(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    status = models.PositiveIntegerField(default = STATUS_NEW)

    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.number}: {self.status}" 