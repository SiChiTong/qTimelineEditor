# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 16:52:53 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KeyFrameItem(QGraphicsPixmapItem):
    
    KEYFRAMEPIXMAP = './images/keyframe.png'
    
    def __init__(self):
        super(KeyFrameItem, self).__init__(parent = None, scene = None)
        self.setPixmap(QPixmap(self.KEYFRAMEPIXMAP))
        self.setFlags(QGraphicsPixmapItem.ItemIsMovable)
        self.setCacheMode(QGraphicsPixmapItem.DeviceCoordinateCache)
        
    def mouseMoveEvent(self, event):
        self.setPos(snapP(event.scenePos()))
    
    
    #private function 1
    #param pos QPoint of the mous clicking
    #Return a QPoint of the mouse snap position
    def snapP(self, pos):
        return QPointF(self.snapX(pos.x()), 0)
    
    #private function 2
    def snapX(self, x):
        #snap to grid
        x -=  (x % self.pixmap().width())
        
        #Remain in the scene rect
        if(self.scene()):
            return self.remainInSceneRect(x)
        else:
            return x
    
    #private function 3
    def remainInSceneRect(self, x):
        if( self.scene() == False ):
            return x
        else:
            sceneRect = self.scene().sceneRect()
            return max(sceneRect.left(), min(sceneRect.right()-self.pixmap().width, x))