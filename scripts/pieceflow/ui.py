import os
import maya.cmds as mc
import core
import config

class PieceflowWin:
    WIN = 'PieceflowWIN'
    TIT = 'Pieceflow Tool' + ' v' + config.SCRIPT_VERSION
    WH = (360, 450)
    WORK_TFBG = 'pieceflowWorkTFBG'
    DATA_TSL = 'pieceflowWorkTSL'
    SEEK_TSL = 'pieceflowSeekTSL'
    def __init__(self):
        pass

    def build(self):
        self.destroy()
        self.WIN = mc.window(self.WIN, t=self.TIT, wh=self.WH)
        mc.columnLayout(adj=True, rs=5, cal='center', co=('both', 10))
        # Workspace field
        self.WORK_TFBG = mc.textFieldButtonGrp(self.WORK_TFBG, 
            l='Workspace', bl='...', tx='', cw3=(60, 240, 50), h=30,
            ct3=('left', 'left', 'left'), bc=lambda: self.browse())
        # Functions
        mc.button(l='Export Selected', w=120, h=36, c=lambda x: self.export())
        mc.button(l='Receive Outside', w=120, h=36, c=lambda x: self.receive())
        mc.button(l='Refresh List', w=120, h=36, c=lambda x: self.refresh())
        mc.button(l='Seek Items', w=120, h=36, c=lambda x:self.seek())
        # Show data list
        mc.text(l='Outside List', fn='fixedWidthFont')
        self.DATA_TSL = mc.textScrollList(self.DATA_TSL, ams=True,
            fn='fixedWidthFont', h=200)
        # Show seek items
        mc.text(l='Seek Items', fn='fixedWidthFont')
        self.SEEK_TSL = mc.textScrollList(self.SEEK_TSL, ams=True,
            fn='fixedWidthFont', h=100)
        mc.setParent('..')
        return self

    def destroy(self):
        if mc.window(self.WIN, q=True, ex=True):
            mc.deleteUI(self.WIN)

    def show(self):
        mc.showWindow(self.WIN)
        mc.window(self.WIN, e=True, wh=self.WH)

    def browse(self):
        directories = mc.fileDialog2(ds=2, fm=3)
        if directories:
            mc.textFieldButtonGrp(self.WORK_TFBG,
                e=True, tx=directories[0])
        self.refresh()

    def refresh(self):
        directory = mc.textFieldButtonGrp(self.WORK_TFBG,
            q=True, tx=True)
        file_list = []
        for (dirpath, dirname, filename) in os.walk(directory):
            file_list = filename; break
        mc.textScrollList(self.DATA_TSL, e=True, removeAll=True)
        file_list = filter(lambda f: f.endswith('.ma'), file_list)
        for f in file_list:
            mc.textScrollList(self.DATA_TSL, e=True, append=f.split('.')[0])

    def export(self):
        directory = mc.textFieldButtonGrp(self.WORK_TFBG,
            q=True, tx=True)
        selections = mc.ls(sl=True)
        for select in selections:
            core.export_to_outside(select, directory)
        self.refresh()

    def receive(self):
        directory = mc.textFieldButtonGrp(self.WORK_TFBG,
            q=True, tx=True)
        selected_items = mc.textScrollList(self.DATA_TSL,
            q=True, si=True)
        for item in selected_items:
            core.receive_from_outside(item, directory)

    def seek(self):
        directory = mc.textFieldButtonGrp(self.WORK_TFBG,
            q=True, tx=True)
        selected_items = mc.textScrollList(self.DATA_TSL,
            q=True, si=True)
        if not selected_items:
            return
        for item in selected_items:
            mc.textScrollList(self.SEEK_TSL, e=True,
                append='@{}'.format(item))
            with open('{0}/{1}.log'.format(directory, item, 'r')) as log:
                data = log.read()
            seek_items_set = data.split()
            for seek_item in seek_items_set:
                mc.textScrollList(self.SEEK_TSL, e=True,
                    append=seek_item)
