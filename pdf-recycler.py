from os.path import exists
from os import remove
from pdf2image import convert_from_path
import PySimpleGUI as sg

# Functions
fileName = 'paths.txt'

# replaces a given line with the given string in file
def __changeLine(line, string):
    if not exists(fileName):
        with open(fileName, 'w') as f:
            f.write('')
            print('clear')
    with open(fileName, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
    with open(fileName, 'w') as f:
        if (line < len(lines)):
            lines[line] = string
        else:
            lines.append(string)
        f.writelines('\n'.join(lines))

# saves the last used fetch path
def setFetchPath(path):
    path = path[:path.rfind('/') + 1]
    __changeLine(0, path)

# gets the last used fetch path
def getFetchPath():
    if exists(fileName):
        with open(fileName, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                return lines[0].rstrip()
    return '~/'

# saves the last used save path
def setSavePath(path):
    __changeLine(1, path)

# gets the last used save path
def getSavePath():
    if exists(fileName):
        with open(fileName, 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:
                return lines[1].rstrip()
    return '~/'

# checks if filename is valid
def isValid(name):
    try:
        with open(name, 'x') as tempfile: # OSError if file exists or is invalid
            pass
        remove(name)
        return True
    except OSError:
        return False

# Main

sg.theme('DarkGrey2')

# page 0

page0 = [   [sg.Text('PDF file')],
            [sg.InputText(key='-filepath-', expand_x=True), sg.FileBrowse('Browse', key='-filebrowse-', file_types=(('PDF Files', '*.pdf'),), initial_folder=getFetchPath())],
            [sg.Text('Import and configure file')],
            [sg.Button('Recycle')] ]

# page 1

page1 = [   [sg.Text('Choose name')],
            [sg.InputText(key='-name-')],
            [sg.Text('Select DPI of jpeg')],
            [sg.Radio('150', '-dpi-', key='-150-'), sg.Radio('200', '-dpi-', key='-200-', default=True), sg.Radio('250', '-dpi-', key='-250-'), sg.Radio('300', '-dpi-', key='-300-')],
            [sg.Text('Export images to')],
            [sg.InputText(getSavePath(), key='-folderpath-', expand_x=True), sg.FolderBrowse('Browse', key='-folderbrowse-', initial_folder=getSavePath())],
            [sg.Button('Back'), sg.Text(expand_x=True), sg.Button('Export')] ]

# main layout

layout = [  [sg.Column(page0, key='-col0-'), sg.Column(page1, key='-col1-', visible=False)] ]

window = sg.Window('PDF Recycler', layout, icon='./recycling.png')

while True:
    event, values = window.read()
    # handles close event
    if event == sg.WIN_CLOSED:
        break
    # confirms the pdf and continues to second page
    if event == 'Recycle':
        filePath = values['-filepath-']
        # check if file is a pdf and exists
        if exists(filePath) and filePath[-4:] == ".pdf":
            # saves the folder from the pdf for next use
            setFetchPath(filePath)
            # switches the pages
            window['-col0-'].update(visible=False)
            window['-col1-'].update(visible=True)
            # updates the name
            window['-name-'].update(filePath[filePath.rfind('/') + 1:-4])
        else:
            sg.popup('The specified PDF file does not exist!', title='Wrong Input')

    # swiches back to first page
    if event == 'Back':
        window['-col0-'].update(visible=True)
        window['-col1-'].update(visible=False)

    # Exports the Images
    if event == 'Export':
        # get values
        name = values['-name-']
        dpi = 150
        filePath = values['-filepath-']
        savePath = values['-folderpath-']
        # set dpi
        if values['-200-']:
            dpi = 200
        elif values['-250-']:
            dpi = 250
        elif values['-300-']:
            dpi = 300
        # check if savePath is empty
        if (len(savePath) > 1):
            # checks if the name is valid and exists
            if isValid(savePath + '/' + name + '-0.jpg'):
                # checks if the path exists on the system
                if exists(savePath):
                    # converts the images
                    images = convert_from_path(filePath, dpi=dpi)
                    # saves the images with added page count
                    for i in range(len(images)):
                        images[i].save(savePath + '/' + name + '-' + str(i) +'.jpg', 'JPEG')
                    # saves the save path for the next use
                    setSavePath(savePath)
                    # tells the user that it was succesful
                    sg.popup('Images have been exported!', title='Successful')
                    # swichtes back to first page
                    window['-col0-'].update(visible=True)
                    window['-col1-'].update(visible=False)
                else:
                    sg.popup('The export folder does not exist!', title='Wrong Path')
            else:
                sg.popup('The name is invalid or already exists!', title='Invalid Name')
        else:
            sg.popup('The export folder does not exist!', title='Wrong Path')

window.close()
