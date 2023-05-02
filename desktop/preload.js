const { contextBridge, ipcRenderer } = require('electron')
const Toastify = require('toastify-js')


// channel: str, data: any, func: function
contextBridge.exposeInMainWorld('screenshot', {
  send: (channel, data) => ipcRenderer.send(channel, data),
  receive: (channel, func) => ipcRenderer.on(channel, (event, ...args) => func(...args)),
})

contextBridge.exposeInMainWorld('tools', {
  alert: (text, status) => Toastify({
    text: text,
    duration: '3000',
    close: false,
    style: {
      background: status == 'success' ? 'green' : 'red',
      color: 'white',
      textAlign: 'center',
    },
    gravity: "top", 
  }).showToast(),
})
