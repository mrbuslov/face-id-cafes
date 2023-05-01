// we use join() instead of path.join(), because it works
const { join } = require('path');
const { app, BrowserWindow } = require('electron');

function createMainWindow() {
    const mainWindows = new BrowserWindow({
        title: 'Face ID',
        width: 500,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            preload: join(__dirname, 'client.js'),
            devTools: true,
        }
    });

    mainWindows.setAlwaysOnTop(true, 'screen');
    mainWindows.setMinimizable(false);
    mainWindows.loadFile('index.html')
}

app.whenReady().then(() => {
    createMainWindow()

    app.on('activate', () => {
      // On macOS it's common to re-create a window in the app when the dock icon is clicked and there are no other windows open.
      if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
}) 


// Quit the app when all windows are closed
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})