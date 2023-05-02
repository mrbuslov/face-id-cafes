// we use join() instead of path.join(), because it works
const { join } = require('path');
const {
    app,
    BrowserWindow,
    ipcMain,
    Menu,
    globalShortcut,
    screen,
    desktopCapturer,
} = require('electron');
const fs = require('fs')

// --- this should be in env ---
process.env.NODE_ENV = 'development';
// --- ---
const isDev = process.env.NODE_ENV !== 'production';

let mainWindow;
function createMainWindow() {
    mainWindow = new BrowserWindow({
        title: 'Face ID',
        width: isDev ? 1000 : 500,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: true,
            preload: join(__dirname, 'preload.js'),
            devTools: true,
            alwaysOnTop: true,
        }
    });

    mainWindow.loadFile('index.html')

    // Open the DevTools
    if (isDev) mainWindow.webContents.openDevTools();
    if (!isDev) mainWindow.setAlwaysOnTop(true, 'screen');

    // Add event listener to detect screen clicks
    mainWindow.on('mousedown', (event) => {
        console.log('Screen clicked at', event.x, event.y)
    })
}

app.whenReady().then(() => {
    createMainWindow();

    // Create custom menu
    const mainMenu = Menu.buildFromTemplate(menu);
    Menu.setApplicationMenu(mainMenu)

    // remove main window on close
    mainWindow.on('close', () => mainWindow = null)

    app.on('activate', () => {
        // On macOS it's common to re-create a window in the app when the dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})


// Quit the app when all windows are closed
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})

// Menu template
const menu = [{
    label: 'Program',
    submenu: [{
        label: 'Quit',
        click: () => app.quit(),
        accelerator: 'CmdOrCtrl+W'
    }]
}];


// receive messages from client.js
ipcMain.on('screenshot', (e, options) => {
    desktopCapturer.getSources({
        types: ['screen'], thumbnailSize: {
            height: 2160,
            width: 3840
        }
    })
        .then(sources => {
            fs.writeFile(`test.png`, sources[0].thumbnail.toPNG(), (err) => {
                if (err) throw err
                console.log('Image Saved')
            })
        })
    // mainWindow.webContents.send('screenshot:done')
    e.sender.send('screenshot:done')
})

