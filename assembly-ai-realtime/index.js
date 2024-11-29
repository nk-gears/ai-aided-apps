
const express = require('express');
const WebSocket = require('ws');
const http = require('http');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

wss.on('connection', (ws) => {
    console.log('New client connected');
    
    const API_KEY = 'b63b979b909f48fbb072eb6de1c47bb3';
    let assemblyWs = null;

    assemblyWs = new WebSocket('wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000', {
        headers: {
            Authorization: API_KEY
        }
    });

    assemblyWs.on('open', () => {
        console.log('Connected to AssemblyAI');
    });

    assemblyWs.on('message', (data) => {
        const response = JSON.parse(data);
        console.log(response);
        if (response.message_type === 'FinalTranscript') {
            ws.send(JSON.stringify({ text: response.text }));
        }
    });

    ws.on('message', (data) => {
        if (assemblyWs.readyState === WebSocket.OPEN) {
            assemblyWs.send(JSON.stringify({
                audio_data: data.toString()
            }));
        }
    });

    ws.on('close', () => {
        console.log('Client disconnected');
        if (assemblyWs) {
            assemblyWs.close();
        }
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

