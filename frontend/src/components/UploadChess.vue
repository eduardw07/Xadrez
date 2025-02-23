<template>
  <div class="tabuleiro-container">
    <h2>Sistema de Xadrez Inteligente</h2>

    <div class="controls-container">
      <h3>Tabuleiro Virtual - Upload</h3>
      <div class="input-group">
        <input type="file" @change="onFileChange" accept="image/*" />
        <button @click="uploadImage">Detectar Peças</button>
      </div>
    </div>

    <div class="images-container">
      <!-- Imagem original na esquerda -->
      <div class="image-section left" v-if="imageUrl">
        <h3>Imagem Original</h3>
        <img :src="imageUrl" alt="Imagem Original" class="resized-image">
      </div>

      <!-- Tabuleiro virtual atualizado na direita -->
      <div class="image-section right" v-if="updatedBoardImage">
        <h3>Tabuleiro Atualizado</h3>
        <img :src="updatedBoardImage" alt="Tabuleiro Virtual" class="resized-image">
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      file: null,
      imageUrl: null,
      updatedBoardImage: null
    };
  },
  methods: {
    onFileChange(event) {
      this.file = event.target.files[0];

      // Criar URL temporária para exibir a imagem original imediatamente
      if (this.file) {
        this.imageUrl = URL.createObjectURL(this.file);
      }
    },
    async uploadImage() {
      if (!this.file) {
        alert("Escolha uma imagem primeiro!");
        return;
      }

      let formData = new FormData();
      formData.append("image", this.file);

      try {
        const response = await axios.post("http://192.168.30.88:8000/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
          responseType: "blob" // Receber imagem como resposta
        });

        // Criar URL temporária para exibir o tabuleiro atualizado
        this.updatedBoardImage = URL.createObjectURL(response.data);
      } catch (error) {
        console.error("Erro ao enviar a imagem:", error);
      }
    }
  }
};
</script>

<style>
.tabuleiro-container {
  padding: 20px;
  text-align: center;
}

/* Centraliza os textos e botões */
.controls-container {
  text-align: center;
  margin-bottom: 20px;
}

/* Alinha input e botão na mesma linha */
.input-group {
  display: flex;
  justify-content: center;
  gap: 10px;
  align-items: center;
}

/* Alinha as imagens lado a lado */
.images-container {
  display: flex;
  justify-content: center; /* Centraliza no eixo horizontal */
  gap: 30px; /* Espaço entre a imagem original e o tabuleiro virtual */
  margin-top: 20px;
}

/* Estiliza as seções das imagens */
.image-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%; /* Define a largura para cada imagem */
}

/* Redimensiona as imagens */
.resized-image {
  max-width: 400px; /* Ajusta o tamanho para ambas as imagens */
  height: auto;
  border: 2px solid #ddd;
  border-radius: 5px;
}
</style>
