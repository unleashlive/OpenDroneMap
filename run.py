#!/usr/bin/python

from opendm import log
from opendm import config
from opendm import system
from opendm import io
import zip_results

import ecto
import os
import ua_postprocessing
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
                  + args.project_path + "/mve")

    # create an instance of my App BlackBox
    # internally configure all tasks
    app = ODMApp(args=args)

    # create a plasm that only contains the BlackBox
    plasm = ecto.Plasm()
    plasm.insert(app)

    # execute the plasm
    plasm.execute(niter=1)


    # UA POSTPROCESSING CUSTOM CODE

    # CONVERT OBJ TO JS FOR THREEJS
    ua_postprocessing.obj2gltf(args.project_path)

    # RESIZE 3D MODEL TEXTURES - UNG-134
    ua_postprocessing.resize_textures(args.project_path)

    # CONVERT OBJ TO GLB FOR THREEJS
    ua_postprocessing.obj2glb(args.project_path)

    # CLEAN REDUNDANT TEXTURES
    # ua_postprocessing.cleanTextures(args.project_path)

    # CREATE TMS TILES FOR ORTHOPHOTO
    ua_postprocessing.tif2tiles(args.project_path)

    # ZIP RESULTS
    zip_results.zip_dirs([args.project_path + "/odm_georeferencing",
                    args.project_path + "/odm_meshing",
                    args.project_path + "/odm_orthophoto",
                    args.project_path + "/odm_dem",
                    args.project_path + "/odm_texturing"])

    log.ODM_INFO('OpenDroneMap app finished - %s' % system.now())
