# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version:
"""
import confighandler as cfg


class WaferConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()
        self.dies = cfg.Field("MaskARY1_Jakob_full")
        self.structure_file = cfg.Field("../vas-files/list_of_structures_picasso.vas")
        self.wafermap_file = cfg.Field("../Wafermapary1_48dies.map")
        self.log_file = cfg.Field("{output_directory}/log_{date_time}.log")
        self.measurement_output = cfg.Field("{output_directory}/measurement/measurement_{date_time}.csv")
        self.measurement_mat_file = cfg.Field("{output_directory}/measurement/measurement_die_{die}_struct_{structure}_{date_time}_{it}.mat")
        self.scope_image_file = cfg.Field("{output_directory}/scope_shots/scope_{wafer_nr}_die_{die}_struct_{structure}_{time}.png")
        self.bookmark_file = cfg.Field("{output_directory}/klayout_bookmarks/bookmarks_{wafer_version}.lyb")



        self.register()

