import os
import json
import numpy as np

import awscli_util


# clean unnecessary heavy files
# this prepares syncing project folder to S3
def clean_project(project_path):
    objects_to_clean = [
        project_path + '/odm_orthophoto/odm_orthophoto.png',
        project_path + '/odm_orthophoto/odm_orthophoto.tif',
        project_path + '/odm_orthophoto/odm_orthophoto.original.tif'
    ]

    for o in objects_to_clean:
        try:
            os.remove(o)
        except:
            print('Failed to delete ' + o)
            pass


def upload_results(project_folder, images_dst_s3key):
    awscli_util.aws_cli(['s3', 'sync', '--quiet', project_folder, 's3://%s' % (images_dst_s3key)])


def resize_textures(project_path):
    odm_texturing_folder = project_path + "/odm_texturing/"
    inputObjFile = "odm_textured_model.obj"
    inputMtlFile = "odm_textured_model.mtl"
    resized_2x_folder = "resized_2x"
    resized_4x_folder = "resized_4x"

    # due to imagemagick bug, its impossible to have colon : in the -path param content, so use 'cd' to get relative path
    resize_2x_command = 'cd ' + odm_texturing_folder + ' && mkdir -p ' + resized_2x_folder + ' && mogrify -adaptive-resize 50% -path ' + resized_2x_folder + ' -format png ' + './*.png'
    resize_4x_command = 'cd ' + odm_texturing_folder + ' && mkdir -p ' + resized_4x_folder + ' && mogrify -adaptive-resize 25% -path ' + resized_4x_folder + ' -format png ' + './*.png'
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
    os.system(
        'obj2gltf -b --checkTransparency -i ' + resized_2x_folder + inputFile + ' -o ' + resized_2x_folder + outputGLBFile)
    os.system(
        'obj2gltf -b --checkTransparency -i ' + resized_4x_folder + inputFile + ' -o ' + resized_4x_folder + outputGLBFile)


# after converting obj to glb all the textures are redundant
def cleanTextures(project_path):
    odm_texturing_folder = project_path + "/odm_texturing/"
    resized_2x_images = "resized_2x/*.png"
    resized_4x_images = "resized_4x/*.png"
    os.system('rm -rv ' + odm_texturing_folder + resized_2x_images)
    os.system('rm -rv ' + odm_texturing_folder + resized_4x_images)


def tif2tiles(project_path):
    input_ortho_file = project_path + "/odm_orthophoto/odm_orthophoto.tif"
    output_ortho_tiles_folder = project_path + "/odm_orthophoto/tiles/"
    # os.system('gdal2tiles_parallel.py -e -p geodetic -n' + input_ortho_file + ' ' + output_ortho_tiles_folder)
    os.system('gdal2tiles.py -z 10-22 -n ' + input_ortho_file + ' ' + output_ortho_tiles_folder)


def calculate_mean_recon_error(reconstruction_json):
    """
    Computes the average error rate of an OpenSfM reconstruction.
    :param reconstruction_json path to OpenSfM's reconstruction.json
    :return mean recon error
    """
    if not os.path.isfile(reconstruction_json):
        raise IOError(reconstruction_json + " does not exist.")

    with open(reconstruction_json) as f:
        data = json.load(f)

    # Calculate median error from sparse reconstruction
    reconstruction = data[0]
    reprojection_errors = []

    for pointId in reconstruction['points']:
        point = reconstruction['points'][pointId]
        reprojection_errors.append(point['reprojection_error'])

    reprojection_error = np.median(reprojection_errors)
    return reprojection_error
