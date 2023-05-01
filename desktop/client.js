// get DOM elements
var iceConnectionLog = document.getElementById('ice-connection-state'),
    iceGatheringLog = document.getElementById('ice-gathering-state'),
    signalingLog = document.getElementById('signaling-state');
var host = 'http://127.0.0.1:8000';
var host_name = '127.0.0.1:8000';

// generate websocket id
var webSocketId = Date.now().toString(36) + Math.random().toString(36).substr(2);
// const socket = new WebSocket('wss://0.0.0.0:8000/video');
const socket = new WebSocket(`ws://${host_name}/video`);
socket.addEventListener('open', function (event) {
  console.log('WebSocket connection established');
  socket.send(webSocketId);
});

socket.addEventListener('close', function (event) {
  console.log('WebSocket connection closed');
});

socket.addEventListener('message', function (event) {
    data = JSON.parse(event.data);
    console.log()
    if(!!data.name){
        document.getElementById('person_name').innerHTML = `<strong>${data.name}</strong>`;
    }
    else {
        document.getElementById('person_name').innerHTML = 'Searching for people...';
    }
});
// peer connection
var pc = null;

// data channel
var dc = null, dcInterval = null;

function createPeerConnection() {
    var config = {
        sdpSemantics: 'unified-plan'
    };

    pc = new RTCPeerConnection(config);

    // register some listeners to help debugging
    pc.addEventListener('icegatheringstatechange', function() {
        iceGatheringLog.textContent += ' -> ' + pc.iceGatheringState;
    }, false);
    iceGatheringLog.textContent = pc.iceGatheringState;

    pc.addEventListener('iceconnectionstatechange', function() {
        iceConnectionLog.textContent += ' -> ' + pc.iceConnectionState;
    }, false);
    iceConnectionLog.textContent = pc.iceConnectionState;

    pc.addEventListener('signalingstatechange', function() {
        signalingLog.textContent += ' -> ' + pc.signalingState;
    }, false);
    signalingLog.textContent = pc.signalingState;

    // connect audio / video
    pc.addEventListener('track', function(evt) {
        if (evt.track.kind == 'video')
            document.getElementById('video').srcObject = evt.streams[0];
        else
            document.getElementById('audio').srcObject = evt.streams[0];
    });

    return pc;
}

function negotiate() {
    return pc.createOffer().then(function(offer) {
        return pc.setLocalDescription(offer);
    }).then(function() {
        // wait for ICE gathering to complete
        return new Promise(function(resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function() {
        var offer = pc.localDescription;
        var codec;

        // it can be optional
        offer.sdp = sdpFilterCodec('video', 'VP8/90000', offer.sdp);

        document.getElementById('offer-sdp').textContent = offer.sdp;
        return fetch(host + '/offer', {
            body: JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
                unique_id: webSocketId
            }),
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });
    }).then(function(response) {
        return response.json();
    }).then(function(answer) {
        document.getElementById('answer-sdp').textContent = answer.sdp;
        return pc.setRemoteDescription(answer);
    }).catch(function(e) {
        alert(e);
    });
}

function start() {
    document.getElementById('start').style.display = 'none';
    document.querySelector('.loader').style.display = 'block';

    pc = createPeerConnection();

    var time_start = null;

    function current_stamp() {
        if (time_start === null) {
            time_start = new Date().getTime();
            return 0;
        } else {
            return new Date().getTime() - time_start;
        }
    }

    // {"ordered": false, "maxRetransmits": 0}
    // {"ordered": false, "maxPacketLifetime": 500}
    var parameters = {"ordered": true}; 

    dc = pc.createDataChannel('chat', parameters);
    dc.onclose = function() {
        clearInterval(dcInterval);
    };
    dc.onopen = function() {
        dcInterval = setInterval(function() {
            var message = 'ping ' + current_stamp();
            dc.send(message);
        }, 1000);
    };
    dc.onmessage = function(evt) {
        if (evt.data.substring(0, 4) === 'pong') {
            var elapsed_ms = current_stamp() - parseInt(evt.data.substring(5), 10);
        }
    };

    var constraints = {
        audio: false,
        video: {
            width: { min: 640, ideal: 1280, max: 1920 },
            height: { min: 576, ideal: 720, max: 1080 },
            frameRate: {
                "max": "0.5"
            }
        }
        // video: true,
    };

    
    if (constraints.audio || constraints.video) {
        document.querySelector('#media').style.display = 'block';
        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            stream.getTracks().forEach(function(track) {
                document.querySelector('.loader').style.display = 'none';
                pc.addTrack(track, stream);
            });
            return negotiate();
        }, function(err) {
            alert('Could not acquire media: ' + err);
        });
    } else {
        negotiate();
    }

    document.getElementById('stop').style.display = 'inline-block';
}

function stop() {
    document.getElementById('stop').style.display = 'none';
    document.getElementById('start').style.display = 'inline-block';
    // close data channel
    if (dc) {
        dc.close();
    }

    // close transceivers
    if (pc.getTransceivers) {
        pc.getTransceivers().forEach(function(transceiver) {
            if (transceiver.stop) {
                transceiver.stop();
            }
        });
    }

    // close local audio / video
    pc.getSenders().forEach(function(sender) {
        sender.track.stop();
    });

    // close peer connection
    setTimeout(function() {
        pc.close();
    }, 500);
}

function sdpFilterCodec(kind, codec, realSdp) {
    var allowed = []
    var rtxRegex = new RegExp('a=fmtp:(\\d+) apt=(\\d+)\r$');
    var codecRegex = new RegExp('a=rtpmap:([0-9]+) ' + escapeRegExp(codec))
    var videoRegex = new RegExp('(m=' + kind + ' .*?)( ([0-9]+))*\\s*$')

    var lines = realSdp.split('\n');

    var isKind = false;
    for (var i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('m=' + kind + ' ')) {
            isKind = true;
        } else if (lines[i].startsWith('m=')) {
            isKind = false;
        }

        if (isKind) {
            var match = lines[i].match(codecRegex);
            if (match) {
                allowed.push(parseInt(match[1]));
            }

            match = lines[i].match(rtxRegex);
            if (match && allowed.includes(parseInt(match[2]))) {
                allowed.push(parseInt(match[1]));
            }
        }
    }

    var skipRegex = 'a=(fmtp|rtcp-fb|rtpmap):([0-9]+)';
    var sdp = '';

    isKind = false;
    for (var i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('m=' + kind + ' ')) {
            isKind = true;
        } else if (lines[i].startsWith('m=')) {
            isKind = false;
        }

        if (isKind) {
            var skipMatch = lines[i].match(skipRegex);
            if (skipMatch && !allowed.includes(parseInt(skipMatch[2]))) {
                continue;
            } else if (lines[i].match(videoRegex)) {
                sdp += lines[i].replace(videoRegex, '$1 ' + allowed.join(' ')) + '\n';
            } else {
                sdp += lines[i] + '\n';
            }
        } else {
            sdp += lines[i] + '\n';
        }
    }

    return sdp;
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}
