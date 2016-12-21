# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 20:23:25 2016

@author: don
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from keyframe import KeyFrameItem

class QTimelineEditor(QGraphicsView):
    DEFAULTFRAMECOUNT = 60
    FRAMESIZE = QSize(8, 20)  #(height, width)
    BACKGROUNDPIXMAPPATH = './images/background.png'
    TEXT_ADDKEYFRAME = "Add keyframe"
    TEXT_REMOVEKEYFRAME = "Remove keyframe"
    
    def __init__(self, scene ,parent = None):
        super(QTimelineEditor, self).__init__(scene)
        self.m_keyFrames = []
        self.m_isDragging = False
        self.m_startFrame = 0
        
        self.setBackgroundBrush(QBrush(QPixmap(self.BACKGROUNDPIXMAPPATH)))
        self.setMaximumHeight(self.FRAMESIZE.height())
        self.setMinimumHeight(self.FRAMESIZE.height())
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setStyleSheet("QGraphicsView { border-style: none;}")
        
    # create the keyFrames and show up in the GUI
    # @param list keyFrames all of the keyFrames sequence
    def setKeyFrames(self, keyFrames):
        frameCount = self.maximumFrameCount()
        if (len(keyFrames) != 0 ):
            frameCount = max(frameCount, len(keyFrames))
        self.setMaximumFrameCount(frameCount)
        
        #Delete old data
        self.m_keyFrames = []
        
        for frame in keyFrames:
            self.createItem(frame)     #****
    
    
    # Auto adjusting the showing area of the timeline
    def setMaximumFrameCount(self, frameCount):
        #set the maximum widget width
        width = self.FRAMESIZE.width()*frameCount
        self.setMaximumWidth(width+2)
        
        #Set scene rect
        rect = QRectF(0, 0, width, self.FRAMESIZE.height())
        self.scene().setSceneRect(rect)
        
        
    
    def maximumFrameCount(self):
        return self.scene().sceneRect().width() / self.FRAMESIZE.width()
    
    def sizeHint(self):
        extra = QSize(1, 0)
        
        if (self.scene()):
            return self.scene().sceneRect().size().toSize() / self.FRAMESIZE.width()  #toSize QSizeF to QSize
        
        return self.sceneRect().size().toSize() + extra
    
    
    # Gain the mouse pos and 
    # @param pos the scene corrdinate point
    def frameAt(self, pos):
        frame = self.mapToScene(pos).toPoint().x()/ self.FRAMESIZE.width()
        return max(0, min(frame, self.maximumFrameCount()))
    
    # implemented virtual method for protected classes
    # @param QPainter painter
    # @param QRecF rect
    def drawBackground(self, painter, rect):
        super(QTimelineEditor, self).drawBackground(painter, rect.intersected(self.sceneRect()))
    
    # implemented virtual method for protected classes
    # @param QContextMenuEvent event
    def contextMenuEvent(self, event):
        pass
    
    # implemented virtual method for protected classes
    # @param QMouseEvent event
    def mousePressEvent(self, event):
        if event.isAccepted():
            self.m_isDragging = True
            self.m_startFrame = self.frameAt(event.pos())
            
    # implemented virtual method for protected classes
    # @param QMouseEvent event
    def mouseReleaseEvent(self, event):
       if self.m_isDragging:
           destFrame = self.frameAt(event.pos())
           if self.m_startFrame != destFrame and self.replaceKeyFrame(self.m_startFrame, destFrame):
               #exchange conditions
               self.replaceItem(self.m_startFrame, destFrame)
               
    # implemented virtual method for protected classes
    # allocate KeyFrame in the Timeline
    # @param int frame pos of the frame
    # @return True if success otherwise False
    def addKeyFrame(self, frame):
        return True

    # implemented virtual method for protected classes
    # remove KeyFrame in the Timeline
    # @param int frame pos of the frame
    # @return True if success otherwise False    
    def removeKeyFrame(self, frame):
        return True
    
    # implemented virtual method for protected classes
    # changeover KeyFrames in the Timeline
    # @param int origin  initial pos of the frame
    # @param int to    destination of the frame
    # @return True if success otherwise False     
    def replaceKeyFrame(self, origin, des):
        return True
    
    # internal function for the class
    def createItem(self, frame):
        #self.deleteItem(frame)
        
        item = KeyFrameItem()
        item.setPos(frame * self.FRAMESIZE.width(), 0)
        
        self.scene().addItem(item)    #parent -- child
        self.m_keyFrames.append(item)
        
    # internal function for the class
    def deleteItem(self, frame):
        tmp = self.m_keyFrames.pop(frame)  #frame-1?
    
        del tmp
    # internal function for the class
    # @param int origin  initial pos of the frame
    # @param int to    destination of the frame
    # @return True if success otherwise False    
    def replaceItem(self, origin, to):
        if (origin == to):
            return
        
        self.deleteItem(to)
        item = self.m_keyFrames.pop(origin)
        self.m_keyFrames.insert(to, item)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    scene = QGraphicsScene(-2000, 2000, 4000, 4000)
    timelineEditor = QTimelineEditor(scene)
    keyFrames = [15, 20, 23, 34]
    
    for i in range(10):
        keyFrame = i
        keyFrames.append(keyFrame)
    timelineEditor.setKeyFrames(keyFrames)
    timelineEditor.show()  
    sys.exit(app.exec_())  