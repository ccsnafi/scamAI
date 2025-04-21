let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        mediaRecorder.ondataavailable = e => {
            audioChunks.push(e.data);
        };
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const formData = new FormData();
            formData.append("audio", audioBlob, "recording.wav");

            fetch("/chat", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("transcription").innerText = data.transcription;
                document.getElementById("reply").innerText = data.reply;
                document.getElementById("voicePlayer").src = "data:audio/mp3;base64," + data.voice;
            });
        };
        mediaRecorder.start();
        setTimeout(() => {
            mediaRecorder.stop();
        }, 5000);
    });
}
