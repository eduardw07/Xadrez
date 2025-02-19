<template>
  <div class="chess-container">
    <h1>Tabuleiro de Xadrez - Detecção</h1>
    <video ref="video" autoplay></video>
    <canvas ref="canvas" style="display: none;"></canvas>
    <button @click="detectPieces">Detectar Peças</button>
    <div v-if="detections.length > 0">
      <h2>Peças Detectadas:</h2>
      <div v-for="(piece, index) in detections" :key="index" class="detection-box"
           :style="getBoxStyle(piece)">
        {{ piece.nome }} <!-- Agora exibe o nome da peça -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      detections: [],
      cameraUrl: "http://192.168.0.2:4747/video" // URL da câmera IP
    };
  },
  mounted() {
    this.startCamera();
  },
  methods: {
    startCamera() {
      const video = this.$refs.video;
      video.src = this.cameraUrl;
    },
    async detectPieces() {
      try {
        const video = this.$refs.video;
        const canvas = this.$refs.canvas;
        const ctx = canvas.getContext("2d");

        // Ajustar dimensões do canvas
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Capturar um frame da câmera
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Converter para Blob e criar um FormData para enviar ao backend
        canvas.toBlob(async (blob) => {
          const formData = new FormData();
          formData.append("image", blob, "frame.jpg");

          const response = await axios.post("http://127.0.0.1:8000/upload", formData, {
            headers: { "Content-Type": "multipart/form-data" }
          });

          this.detections = response.data.detections;
        }, "image/jpeg");
      } catch (error) {
        console.error("Erro ao detectar peças:", error);
      }
    },
    getBoxStyle(piece) {
      return {
        position: "absolute",
        left: `${piece.x1}px`,
        top: `${piece.y1}px`,
        width: `${piece.x2 - piece.x1}px`,
        height: `${piece.y2 - piece.y1}px`,
        border: "2px solid red",
        backgroundColor: "rgba(255, 0, 0, 0.5)",
        color: "white",
        fontSize: "14px",
        textAlign: "center",
        lineHeight: "20px"
      };
    }
  }
};
</script>

<style>
.chess-container {
  position: relative;
  width: 640px;
  margin: auto;
}
video {
  width: 100%;
}
.detection-box {
  position: absolute;
  background-color: rgba(255, 0, 0, 0.5);
  text-align: center;
  line-height: 20px;
}
</style>
