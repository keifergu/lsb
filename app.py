import wx
from lsb import embed, extract

class LBSFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(LBSFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        left = 100
        textLeft = 10
        wx.StaticText(pnl, label="原始图片", pos=(textLeft, 55))
        wx.StaticText(pnl, label="隐藏数据", pos=(textLeft, 105))
        self.inputImage = wx.FilePickerCtrl(pnl, pos=(left, 50))
        self.inputData = wx.FilePickerCtrl(pnl, pos=(left, 100))
        
        encryptBtn = wx.Button(pnl, label='加密', pos=(100, 150),size=(80,25))
        encryptBtn.Bind(wx.EVT_BUTTON, self.encrypt)

        wx.StaticText(pnl, label="隐藏数据图片", pos=(textLeft, 205))
        self.outputImage = wx.FilePickerCtrl(pnl, pos=(left, 200))
        # wx.StaticText(pnl, label="输出数据位置", pos=(textLeft, 255))
        # self.outputData = wx.DirPickerCtrl(pnl, pos=(left, 250))

        decryptBtn = wx.Button(pnl, label='解密', pos=(100, 250),size=(80,25))
        decryptBtn.Bind(wx.EVT_BUTTON, self.decrypt)

    def encrypt(self, event):
       embed(self.inputImage.GetPath(), self.inputData.GetPath())
       wx.MessageBox('数据隐藏成功，处理后图片存放于原图片目录')
 
    def decrypt(self, event):
       extract(self.outputImage.GetPath(), 'output.txt')
       wx.MessageBox('数据读取成功，存放于当前目录：output.txt')

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = LBSFrame(None, title='LBS 信息隐藏应用')
    frm.Show()
    app.MainLoop()
