from sanic import response
import zipfile
from os.path import dirname, abspath, join, isdir, exists
from uuid import uuid4
import glob

_CURDIR = dirname(abspath(__file__))

class ZatiqARModelClient(object):
    def generate_unique_folder_name(self):
        folder_name = str(uuid4())
        if self.check_directory_exists(folder_name) == False:
            return(folder_name)
        else:
            self.generate_unique_folder_name()

    def check_directory_exists(self, folder_name):
        if isdir(join(_CURDIR, 'ARModels/'+folder_name)):
            return(True)
        else:
            return(False)

    async def save_ar_model_locally(self, ar_model_zip):
        if not ar_model_zip:
            return response.json({'message': "Internal server error! Client did not receive zip"}, status=500)
        
        unique_dir_name = self.generate_unique_folder_name()

        zip_ref = zipfile.ZipFile(ar_model_zip.read(), 'r')
        await zip_ref.extractall(join(_CURDIR, "ARModels"+unique_dir_name))
        zip_ref.close()

        #if exists(join(_CURDIR, 'ARModels'+unique_dir_name, ar_model_zip.name+'.htm'))            
        htm_file = glob.glob(join(_CURDIR, 'ARModels'+unique_dir_name+'*.htm'))
        if len(htm_file) > 0:
            return response.json({'message': "Success! AR Model is being served at:"+htm_file[0]}, status=200)
        else:
            return response.json({'message': "An error occurred while trying to extract this model"}, status=500)


        