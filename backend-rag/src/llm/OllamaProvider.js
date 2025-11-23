const axios = require('axios');

class OllamaProvider {
  constructor() {
    this.url = process.env.OLLAMA_URL || 'http://localhost:11434/api/generate';
    this.model = process.env.OLLAMA_MODEL || 'llama3';
  }

  async generateResponse(prompt) {
    try {
      console.log("generateResponse ollama");
      const response = await axios.post(this.url, {
        model: this.model,
        prompt: prompt,
        stream: false,
      });
      console.log("return pllama response");
      return response.data.response.trim();
    } catch (error) {
      console.error('Error en Ollama:', error);
      throw new Error('Fallo al generar respuesta con Ollama');
    }
  }
}

module.exports = OllamaProvider;