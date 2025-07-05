const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const screenVideo = document.getElementById('screenVideo');

const peerConnection = new RTCPeerConnection();

navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        localVideo.srcObject = stream;
        stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));
    })
    .catch(error => console.error('Error accessing media devices:', error));

navigator.mediaDevices.getDisplayMedia({ video: true, audio: true })
    .then(stream => {
        screenVideo.srcObject = stream;
        stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));
    })
    .catch(error => console.error('Error accessing screen:', error));

const remoteStreams = new Map();

peerConnection.ontrack = event => {
    remoteVideo.srcObject = event.streams[0];

    if (!remoteStreams.has(stream.id)) {
        remoteStreams.set(stream.id, stream);
    }
    remoteVideo.srcObject = stream;
};

peerConnection.onicecandidate = event => {
    if (event.candidate) {
        // Send ICE candidate to the signaling server
        sendMessage({
            type: 'ice_candidate',
            candidate: event.candidate
        });
    }
};

async function createOffer() {
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    // Send offer to the signaling server
    sendMessage({
        type: 'offer',
        offer: offer
    });
}

// Function to send messages to the signaling server
function sendMessage(message) {
    websocket.send(JSON.stringify(message));
}

// Handle incoming messages from the signaling server
websocket.onmessage = event => {
    const message = JSON.parse(event.data);
    if (message.type === 'offer') {
        handleOffer(message.offer);
    } else if (message.type === 'answer') {
        handleAnswer(message.answer);
    } else if (message.type === 'ice_candidate') {
        handleIceCandidate(message.candidate);
    }
};

async function handleOffer(offer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    // Send answer to the signaling server
    sendMessage({
        type: 'answer',
        answer: answer
    });
}

async function handleAnswer(answer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
}

async function handleIceCandidate(candidate) {
    await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
}

// Create offer when the page loads
createOffer();

peerConnection.ontrack = event => {
    remoteVideo.srcObject = event.streams[0];
};
