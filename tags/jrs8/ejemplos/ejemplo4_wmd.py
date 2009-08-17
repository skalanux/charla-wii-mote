import sys
import os
sys.path.append('./lib/wmd')

from wmd.Common import *
from wmd.Config import CFG
from wmd.UI.UIManager import UIManager
from wmd.Wiimote.WMManager import WMManager
from wmd.EVDispatcher import EVDispatcher
from wmd.MotionSensing import MSManager
from wmd.Pointer import POManager
from wmd.CommandMapper import CommandMapper

def wii_buttons(buttons):
    codeA = 65 #spacio
    codeB = 41 #f
    codeMas = 63 #*
    codeMinus = 112 #/
    codeH = 9 #escape
    code1 = 32 #o
    code2 = 55 #v
    codeU = 98 #flecha arriba
    codeD = 104 #flecha abajo
    codeL = 100 #flecha izquierda
    codeR = 102 #flecha derecha
    
    if buttons[1] == "DOWN":
        if buttons[0] == "A":
            os.popen2("xsendkeycode "+str(codeA)+" 1")
        elif buttons[0] == "B":
            os.popen2("xsendkeycode "+str(codeB)+" 1")
        elif buttons[0] == "+":
            os.popen2("xsendkeycode "+str(codeMas)+" 1")
        elif buttons[0] == "-":
            os.popen2("xsendkeycode "+str(codeMinus)+" 1")
        elif buttons[0] == "H":
            os.popen2("xsendkeycode "+str(codeH)+" 1")
        elif buttons[0] == "1":
            os.popen2("xsendkeycode "+str(code1)+" 1")
        elif buttons[0] == "2":
            os.popen2("xsendkeycode "+str(code2)+" 1")
        elif buttons[0] == "U":
            os.popen2("xsendkeycode "+str(codeU)+" 1")
        elif buttons[0] == "D":
            os.popen2("xsendkeycode "+str(codeD)+" 1")
        elif buttons[0] == "L":
            os.popen2("xsendkeycode "+str(codeL)+" 1")
        elif buttons[0] == "R":
            os.popen2("xsendkeycode "+str(codeR)+" 1")
    
    elif buttons[1] == "UP":
        if buttons[0] == "A":
            os.popen2("xsendkeycode "+str(codeA)+" 0")
        elif buttons[0] == "B":
            os.popen2("xsendkeycode "+str(codeB)+" 0")
        elif buttons[0] == "+":
            os.popen2("xsendkeycode "+str(codeMas)+" 0")
        elif buttons[0] == "-":
            os.popen2("xsendkeycode "+str(codeMinus)+" 0")
        elif buttons[0] == "H":
            os.popen2("xsendkeycode "+str(codeH)+" 0")
        elif buttons[0] == "1":
            os.popen2("xsendkeycode "+str(code1)+" 0")
        elif buttons[0] == "2":
            os.popen2("xsendkeycode "+str(code2)+" 0")
        elif buttons[0] == "U":
            os.popen2("xsendkeycode "+str(codeU)+" 0")
        elif buttons[0] == "D":
            os.popen2("xsendkeycode "+str(codeD)+" 0")
        elif buttons[0] == "L":
            os.popen2("xsendkeycode "+str(codeL)+" 0")
        elif buttons[0] == "R":
            os.popen2("xsendkeycode "+str(codeR)+" 0")

cf = CFG

ev = EVDispatcher(cf)

ev.subscribe( WM_BT, wii_buttons)
wm = WMManager(cf, ev)
wm.connect()
wm.setup()

wm.main_loop()
