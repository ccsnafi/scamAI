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

                const player = document.getElementById("voicePlayer");
                const audioSrc = "data:audio/mp3;base64," + data.voice;

                player.pause();   // Arrête le son précédent s'il y en a un
                player.src = audioSrc;  // Charge la nouvelle source
                player.load();   // Recharge la balise <audio>
                player.play();   // Joue automatiquement
            });
        };

        mediaRecorder.start();

        // Stop l'enregistrement après 5 secondes
        setTimeout(() => {
            mediaRecorder.stop();
        }, 5000);
    });
}
