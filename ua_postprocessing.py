import os

def resize_textures(project_path):
    odm_texturing_folder = project_path + "/odm_texturing/"
    inputObjFile = "odm_textured_model.obj"
    inputMtlFile = "odm_textured_model.mtl"
    resized_2x_folder = "resized_2x"
    resized_4x_folder = "resized_4x"

    # due to imagemagick bug, its impossible to have colon : in the -path param content, so use 'cd' to get relative path
    resize_2x_command = 'cd ' + odm_texturing_folder + ' && mkdir ' + resized_2x_folder + ' && mogrify -adaptive-resize 50% -path ' + resized_2x_folder + ' -format png ' + './*.png'
    resize_4x_command = 'cd ' + odm_texturing_folder + ' && mkdir ' + resized_4x_folder + ' && mogrify -adaptive-resize 25% -path ' + resized_4x_folder + ' -format png ' + './*.png'
    os.system(resize_2x_command)
    os.system(resize_4x_command)
    # create symlinks that are needed to generate glb files
    os.system('cp ' + odm_texturing_folder + inputObjFile + ' ' + odm_texturing_folder + resized_2x_folder)
    os.system('cp ' + odm_texturing_folder + inputMtlFile + ' ' + odm_texturing_folder + resized_4x_folder)
    outputGLTFFile = project_path + "/odm_texturing/odm_textured_model.gltf"
    outputBINFile = project_path + "/odm_texturing/odm_textured_model.bin"
    os.system('cp ' + outputGLTFFile + ' ' + odm_texturing_folder + resized_2x_folder)
    os.system('cp ' + outputGLTFFile + ' ' + odm_texturing_folder + resized_4x_folder)
    os.system('cp ' + outputBINFile + ' ' + odm_texturing_folder + resized_2x_folder)
    os.system('cp ' + outputBINFile + ' ' + odm_texturing_folder + resized_4x_folder)

def obj2gltf(project_path):
    inputFile = project_path + "/odm_texturing/odm_textured_model.obj"
    outputGLTFFile = project_path + "/odm_texturing/odm_textured_model.gltf"
    os.system('obj2gltf -s --checkTransparency -i ' + inputFile + ' -o ' + outputGLTFFile)

def obj2glb(project_path):
    odm_texturing_folder = project_path + "/odm_texturing/"
    inputFile = "odm_textured_model.obj"
    outputGLBFile = "odm_textured_model.glb"
    resized_2x_folder = odm_texturing_folder + "resized_2x/"
    resized_4x_folder = odm_texturing_folder + "resized_4x/"
    os.system('obj2gltf -b --checkTransparency -i ' + resized_2x_folder + inputFile + ' -o ' + resized_2x_folder + outputGLBFile)
    os.system('obj2gltf -b --checkTransparency -i ' + resized_4x_folder + inputFile + ' -o ' + resized_4x_folder + outputGLBFile)

# after converting obj to glb all the textures are redundant
def cleanTextures(project_path):
    odm_texturing_folder = project_path + "/odm_texturing/"
    resized_2x_images = "resized_2x/*.png"
    resized_4x_images = "resized_4x/*.png"
    os.system('rm -rv ' + odm_texturing_folder + resized_2x_images)
    os.system('rm -rv ' + odm_texturing_folder + resized_4x_images)


def tif2tiles(project_path):
    inputOrthoFile = project_path + "/odm_orthophoto/odm_orthophoto.tif"
    outputOrthoTilesFolder = project_path + "/odm_orthophoto/tiles/"
    os.system('gdal2tiles.py -n ' + inputOrthoFile + ' ' + outputOrthoTilesFolder)
