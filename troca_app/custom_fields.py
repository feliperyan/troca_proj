import os
import datetime

from mongoengine.python_support import str_types
from django.db.models.fields.files import FieldFile
from django.core.files.base import File
from django.core.files.storage import default_storage
from mongoengine.base import BaseField
from mongoengine.connection import get_db, DEFAULT_CONNECTION_NAME
from django.utils.encoding import force_text


class DJFileField(BaseField):
    
    proxy_class = FieldFile

    def __init__(self,
                 db_alias=DEFAULT_CONNECTION_NAME, 
                 name=None,
                 upload_to='',
                 storage=None,
                 **kwargs):

        self.db_alias = db_alias
        self.storage = storage or default_storage
        self.upload_to = upload_to

        if callable(upload_to):
            self.generate_filename = upload_to

        super(DJFileField, self).__init__(**kwargs)


    def __get__(self, instance, owner):
        # Lots of information on whats going on here can be found
        # on Django's FieldFile implementation, go over to GitHub to
        # read it.
        file = instance._data.get(self.name)

        if isinstance(file, str_types) or file is None:
            attr = self.proxy_class(instance, self, file)
            instance._data[self.name] = attr

        elif isinstance(file, File) and not isinstance(file, FieldFile):
            file_copy = self.proxy_class(instance, self, file.name)
            file_copy.file = file
            file_copy._committed = False
            instance._data[self.name] = file_copy

        elif isinstance(file, FieldFile) and not hasattr(file, 'field'):
            file.instance = instance
            file.field = self
            file.storage = self.storage

        
        return instance._data[self.name]


    def __set__(self, instance, value):
        instance._data[self.name] = value


    def get_directory_name(self):
        return os.path.normpath(force_text(datetime.datetime.now().strftime(self.upload_to)))

    def get_filename(self, filename):
        return os.path.normpath(self.storage.get_valid_name(os.path.basename(filename)))

    def generate_filename(self, instance, filename):
        return os.path.join(self.get_directory_name(), self.get_filename(filename))


    def to_mongo(self, value):
    # Store the path in MongoDB
    # I also used this bit to actually save the file to disk.
    # The value I'm getting here is a FileFiled and it all looks
    # pretty good at this stage even though I'm not 100% sure
    # of what's going on.

        if not value._committed and value is not None:
            value.save(value.name, value)
            return value.path

        return value.name    

    
    def to_python(self, value):
        eu = self
        return eu.proxy_class(eu.owner_document, eu, value)
       

        
        



