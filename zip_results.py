import os
import zipfile

def zipdir(foldername, ziph):
    for root, dirs, files in os.walk(foldername):
        for file in files:
            # add files to the archive directly
            ziph.write(os.path.abspath(os.path.join(root, file)), arcname=file)

# expect files to be an array of direct result folder paths
def zip_dirs(dirs):
    print(dirs)
    for dir in dirs:
        zipf = zipfile.ZipFile(dir+'.zip', 'w', zipfile.ZIP_DEFLATED, allowZip64 = True)
        zipdir(dir+'/', zipf)
        zipf.close()
