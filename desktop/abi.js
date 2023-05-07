// RUN: node abi.js
const nodeAbi = require('node-abi')

// get abi versions (for iohook -> package.json)
console.log(nodeAbi.getAbi('14.21.3', 'node'))
console.log(nodeAbi.getAbi('11.5.0', 'electron'))