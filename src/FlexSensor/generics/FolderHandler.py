import logging
import os

from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig
from ConfigHandler.controller.VFSObject import VFSObject


class FolderHandler(object):

    @staticmethod
    def create_output_folder():
        VAutomatorConfig.output_dir = FolderHandler.create_folder(VAutomatorConfig.output_dir)

        return VAutomatorConfig.output_dir

    @staticmethod
    def create_folder(vfs_obj: VFSObject):
        '''
        Check if the folder exists, if not create it
        '''
        # Check if the given argument is a file
        if os.path.isfile(vfs_obj.absolute):
            folder = os.path.dirname(vfs_obj.absolute)

        # Try creating the output directory
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as exc:
                logging.error("Could not create folder {folder}. Exception: {exc}")
                raise exc
        return folder

    @staticmethod
    def set_and_create_file(filename):
        '''
        Check if the folder for file exists, if not create it
        '''
        logging.info("Setting file: %s" % filename)
        # Try creating the output directory
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                raise  Exception("Could not create folder %s/%s for path." % (os.path.dirname(filename), filename))
        # create the file
        return filename