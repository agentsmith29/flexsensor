class CSSPlayPushButton:
    @staticmethod
    def style_play():
        return """
                QPushButton {		
            background-color: rgb(36, 209, 21);
            background-position: left center;
            background-repeat: no-repeat;
            border: none;
            border-radius: 0px;
            border-left: 22px solid transparent;
            text-align: left;
            padding-left: 44px;
            background-image: url(:/icons/images/icons/cil-media-play.png);
        }
        
        QPushButton:hover {
            background-color: rgb(26, 153, 16);
        }
        
        QPushButton:pressed {	
            background-color: rgb(20, 120, 12);
            color: rgb(255, 255, 255);
        }
        
        QPushButton:disabled {	
            background-color: rgb(153, 153, 153);
            color: rgb(255, 255, 255);
        }
        
                """

    @staticmethod
    def style_pause():
        return """
            QPushButton {		
               background-color: rgb(255, 200,11);
                background-position: left center;
                background-repeat: no-repeat;
                border: none;
                border-radius: 0px;
                border-left: 22px solid transparent;
                text-align: left;
                padding-left: 44px;
                background-image: url(:/icons/images/icons/cil-media-pause.png)
            }
    
            QPushButton:hover {
                background-color: rgb(255, 182, 44);
            }
    
            QPushButton:pressed {	
                background-color: rgb(255, 146, 12);
                color: rgb(255, 255, 255);
            }
    
            QPushButton:disabled {	
                background-color: rgb(153, 153, 153);
                color: rgb(255, 255, 255);
            }
        """

    @staticmethod
    def style_stop():
        return """
            QPushButton {		
                background-color: rgb(242, 41, 41);
                background-position: left center;
                background-repeat: no-repeat;
                border: none;
                border-radius: 0px;
                border-left: 22px solid transparent;
                text-align: left;
                padding-left: 44px;
                background-image: url(:/icons/images/icons/cil-media-stop.png)
            }
            
            QPushButton:hover {
                background-color: rgb(235, 64, 52);
            }
            
            QPushButton:pressed {	
                background-color: rgb(201, 17, 4);
                color: rgb(255, 255, 255);
            }
            
            QPushButton:disabled {	
                background-color: rgb(153, 153, 153);
                color: rgb(255, 255, 255);
            }
        """
