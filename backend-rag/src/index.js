const express = require('express');
const dotenv = require('dotenv');
const { processQuery } = require('./rag/rag');

dotenv.config();

const app = express();
app.use(express.json());

app.post('/chat', async (req, res) => {
  const { query } = req.body;
  if (!query) {
    return res.status(400).json({ error: 'Query requerida' });
  }

  try {
    const response = await processQuery(query);
    res.json({ response });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});