# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version:
"""
import confighandler as cfg


class AppSettings(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()
        # APP SETTINGS
        # ///////////////////////////////////////////////////////////////
        self.ENABLE_CUSTOM_TITLE_BAR = cfg.Field(True)
        self.MENU_WIDTH = cfg.Field(240)
        self.LEFT_BOX_WIDTH = cfg.Field(240)
        self.RIGHT_BOX_WIDTH = cfg.Field(240)
        self.TIME_ANIMATION = cfg.Field(500)

        # BTNS LEFT AND RIGHT BOX COLORS
        self.BTN_LEFT_BOX_COLOR = cfg.Field("background-color: rgb(44, 49, 58);")
        self.BTN_RIGHT_BOX_COLOR = cfg.Field("background-color: #ff79c6;")

        # MENU SELECTED STYLESHEET
        self.MENU_SELECTED_STYLESHEET = cfg.Field("""
           border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
           background-color: rgb(40, 44, 52);
           """)

        self.register()

