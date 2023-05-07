// send screenshot to main.js to process it
document.getElementById('screenshotBtn').addEventListener('click', (e) => {
    screenshot.send('screenshot', { 'test': true })
})

// receive the response from main, if screenshot processed
screenshot.receive('screenshot:done', () => {
    console.log('screenshot completed')
    tools.alert('Screenshot done!', 'success');
})
