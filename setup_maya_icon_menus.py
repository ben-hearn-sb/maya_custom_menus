"""
	Author: Ben Hearn
	Set up maya icon tools and maya custom menus
	Adds a tearable toolbar and 2 clickable iconswith example scripts attached to them
"""

import maya.OpenMayaUI as apiUI
import maya.mel as mel
from PySide import QtGui, QtCore
import shiboken
#import sip
#from PyQt4 import QtGui

import os

import maya.cmds as cmds

def getMayaStatusLine():
	gStatusLine = mel.eval('$temp=$gStatusLine')
	ptr = apiUI.MQtUtil.findControl(gStatusLine)
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QtGui.QWidget) # PySide command
		#return sip.wrapinstance(long(ptr), QtGui.QWidget) # PyQt command


""" Add menus to Maya """
def addMenuItem(parentMenu=None, labelName='', callback=None, sub=False, tearable=False):
	# If we do not specify a callback we are making a new sub-menu
	if callback == None:
		newMenu = cmds.menuItem(parent=parentMenu, label=labelName, subMenu=sub, tearOff=tearable)
		return newMenu
	else:
		cmds.menuItem(p=parentMenu, label=labelName, command=callback)

def addSeparator(parentMenu):
	cmds.menuItem(parent=parentMenu, divider=True)

def addToolBarFunction(icon, statusLine, callback):
	""" Sets up a toolbar icon and function  """
	pixmap   = QtGui.QPixmap(icon)
	icon     = QtGui.QIcon(pixmap)
	iconSize = QtCore.QSize(32, 32)
	btnSize  = QtCore.QSize(32, 32)

	btn = QtGui.QPushButton(statusLine)
	btn.setFlat(True)
	btn.setText("")
	btn.setIcon(icon)
	btn.setMinimumSize(btnSize)
	btn.setMaximumSize(btnSize)
	btn.setIconSize   (iconSize)
	btn.clicked.connect(callback)
	statusLine.layout().addWidget(btn)

def setupMenuBar():
	""" Sets up a menu bar  """

	# Create a main menu that we will place on the main maya toolbar
	MAIN_MENU = cmds.menu(label='CUSTOM MENU', parent='MayaWindow', tearOff=True)

	# Sub Menus of Main Menu
	POLY_ACTIONS    = addMenuItem(parentMenu=MAIN_MENU, labelName='Poly Actions',  sub=True,  tearable=True)
	QT_ACTIONS      = addMenuItem(parentMenu=MAIN_MENU, labelName='Qt Actions',    sub=True,  tearable=True)

	# Add our sub menus to the main menu
	# Poly actions
	addMenuItem(parentMenu=POLY_ACTIONS, labelName='Create Cube', callback='createCube()')
	addSeparator(parentMenu=POLY_ACTIONS) # Adding a separator example
	addMenuItem(parentMenu=POLY_ACTIONS, labelName='Create Sphere', callback='createSphere()')

	# Qt Actions
	addMenuItem(parentMenu=QT_ACTIONS, labelName='Display Message Box', callback='createInfoBox()')

	# Print Actions
	addSeparator(parentMenu=MAIN_MENU)
	addMenuItem(parentMenu=MAIN_MENU, labelName='Display Dummy Dialog', callback='printExample()')


def setupToolBar():
	statusLine = getMayaStatusLine()

	#currentDir = os.path.dirname(os.path.realpath('__file__'))
	iconDirectory = r'C:\projects\git_projects\maya_custom_menus\icons'

	clickMeIcon  = os.path.join(iconDirectory, 'click_me.png')
	thumbsUpIcon = os.path.join(iconDirectory, 'thumb_up.png')
	print thumbsUpIcon

	addToolBarFunction(icon=clickMeIcon,  statusLine=statusLine, callback=clickMe)
	addToolBarFunction(icon=thumbsUpIcon, statusLine=statusLine, callback=thumbsUp)

""" Simple Menu Functions """
def createCube():
	cmds.polyCube()

def createSphere():
	cmds.polySphere()

def createInfoBox(parent=None):
	QtGui.QMessageBox.information(parent, 'Hello there', 'I am a message box')
	return

def printExample():
	print 'I am printing!'

def clickMe():
	print 'I have been clicked!!!'

def thumbsUp(parent=None):
	QtGui.QMessageBox.information(parent, 'Well Then', 'Thumbs up!!!')
	return


if __name__ == '__main__':
	setupToolBar()
	setupMenuBar()
