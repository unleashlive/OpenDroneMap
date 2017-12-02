import os
def resize_textures(project_path, outputGLTFFile):
    odm_texturing_folder = project_path + "/odm_texturing"
    resized_8x_folder = "resized_8x"
    resized_4x_folder = "resized_4x"
    # due to imagemagick bug, its impossible to have colon : in the -path param content, so use 'cd' to get relative path
    resize_8x_command = 'cd ' + odm_texturing_folder + ' && mkdir ' + resized_8x_folder + ' && mogrify -adaptive-resize 12.5% -path ' + resized_8x_folder + ' -format png ' + './*.png'
    resize_4x_command = 'cd ' + odm_texturing_folder + ' && mkdir ' + resized_4x_folder + ' && mogrify -adaptive-resize 25% -path ' + resized_4x_folder + ' -format png ' + './*.png'
    os.system(resize_8x_command)
    os.system(resize_4x_command)
    os.system('cd ' + odm_texturing_folder + ' && cp ' + outputGLTFFile + ' ' + resized_8x_folder)
    os.system('cd ' + odm_texturing_folder + ' && cp ' + outputGLTFFile + ' ' + resized_4x_folder)

def obj2gltf(inputFile, outputGLTFFile):
    os.system('obj2gltf -s --checkTransparency -i ' + inputFile + ' -o ' + outputGLTFFile)
    #outputFile = args.project_path + "/odm_texturing/odm_textured_model.js"
    #os.system('python /code/convert_obj_three.py -i' + inputFile + ' -o ' + outputFile + ' -a center ')

def tif2tiles(inputOrthoFile, outputOrthoTilesFolder):
    os.system('gdal2tiles.py -n ' + inputOrthoFile + ' ' + outputOrthoTilesFolder)
