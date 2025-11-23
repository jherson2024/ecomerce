const axios = require('axios');

class OpenAIProvider {
  constructor() {
    this.apiKey = process.env.OPENAI_API_KEY || '';
    this.model = process.env.OPENAI_MODEL || 'gpt-4o-mini';
    if (!this.apiKey) {
      throw new Error('OPENAI_API_KEY no configurada');
    }
  }

  async generateResponse(prompt) {
    try {
      const response = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
          model: this.model,
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
        },
        {
          headers: {
            Authorization: `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data.choices[0].message.content.trim();
    } catch (error) {
      console.error('Error en OpenAI:', error);
      throw new Error('Fallo al generar respuesta con OpenAI');
    }
  }
}

module.exports = OpenAIProvider;