#
# Utilities used throughout the app
from django.conf import settings
from zipfile import ZipFile
from django.core.files.uploadedfile import UploadedFile

# Determine the extension of the file uploaded


def handle_uploaded_file(file):
    with(open(settings.MEDIA_ROOT+'name.jpg', 'wb+')) as dest:
        for chunk in file.chunks():
            dest.write(chunk)

# Check if file is archive type
def is_zip(file):
    import zipfile
    if zipfile.is_zipfile(file):
        return True
    else:
        return False


# compress file to zip
def compress_file(file):
    zf = ZipFile('topsecret.zip')


# change upload path
def change_upload_path(instance, filename):
    return '/'.join([instance.repo_name, filename])

# check file type
def is_file_supported(file):
    if file.content_type in settings.SUPPORTED_FILES:
        return True
    else:
        return False

# unzips files and checks files for complaince
def handle_zip_file(file):
    supported = ['pdf', 'txt', 'zip', 'doc', 'odt', 'xls']
    with ZipFile(file) as zipf:
        if zipf is not None:
            # list contents in zip
            for file in zipf.namelist():
                with zipf.open(file) as f:
                    name = f.name
                    ext = name[name.find('.')+1:len(name)]
                    if ext in supported:
                        return True
                    else:
                        return False
        else:
            return False

