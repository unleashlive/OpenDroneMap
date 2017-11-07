#!/usr/bin/python

from opendm import log
from opendm import config
from opendm import system
from opendm import io
import zip_results

import ecto
import os

from scripts.odm_app import ODMApp

if __name__ == '__main__':

    args = config.config()

    log.ODM_INFO('Initializing OpenDroneMap app - %s' % system.now())

    # Add project dir if doesn't exist
    args.project_path = io.join_paths(args.project_path, args.name)
    if not io.dir_exists(args.project_path):
        log.ODM_WARNING('Directory %s does not exist. Creating it now.' % args.name)
        system.mkdir_p(os.path.abspath(args.project_path))

    # If user asks to rerun everything, delete all of the existing progress directories.
    # TODO: Move this somewhere it's not hard-coded
    if args.rerun_all:
        log.ODM_DEBUG("Rerun all -- Removing old data")
        os.system("rm -rf "
                  + args.project_path + "/images_resize "
                  + args.project_path + "/odm_georeferencing "
                  + args.project_path + "/odm_meshing "
                  + args.project_path + "/odm_orthophoto "
                  + args.project_path + "/odm_texturing "
                  + args.project_path + "/opensfm "
                  + args.project_path + "/pmvs")

    # create an instance of my App BlackBox
    # internally configure all tasks
    app = ODMApp(args=args)

    # create a plasm that only contains the BlackBox
    plasm = ecto.Plasm()
    plasm.insert(app)

    # execute the plasm
    plasm.execute(niter=1)

    # CONVERT OBJ TO JS FOR THREEJS
    inputFile = args.project_path + "/odm_texturing/odm_textured_model.obj"
    outputGLTFFile = args.project_path + "/odm_texturing/odm_textured_model.gltf"
    os.system('obj2gltf -s -i ' + inputFile + ' ' + outputGLTFFile)

    #outputFile = args.project_path + "/odm_texturing/odm_textured_model.js"
    #os.system('python /code/convert_obj_three.py -i' + inputFile + ' -o ' + outputFile + ' -a center ')

    # CREATE TMS TILES FOR ORTHOPHOTO
    inputOrthoFile = args.project_path + "/odm_orthophoto/odm_orthophoto.tif"
    outputOrthoTilesFolder = args.project_path + "/odm_orthophoto/tiles/"
    os.system('gdal2tiles.py -n ' + inputOrthoFile + ' ' + outputOrthoTilesFolder)

    # ZIP RESULTS
    zip_results.zip_dirs([args.project_path + "/odm_georeferencing",
                    args.project_path + "/odm_meshing",
                    args.project_path + "/odm_orthophoto",
                    args.project_path + "/odm_texturing"])

    log.ODM_INFO('OpenDroneMap app finished - %s' % system.now())
