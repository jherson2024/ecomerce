const OllamaProvider = require('../llm/OllamaProvider');
const OpenAIProvider = require('../llm/OpenAIProvider');
const { getSchema, executeQuery } = require('../db/db');

function getLLMProvider() {
  const provider = process.env.LLM_PROVIDER || 'ollama';
  if (provider === 'ollama') {
    return new OllamaProvider();
  } else if (provider === 'openai') {
    return new OpenAIProvider();
  }
  throw new Error('Proveedor LLM no soportado');
}

async function processQuery(userQuery) {
  const llm = getLLMProvider();
  const schema = await getSchema();
  
  // Prompt para generar SQL
  const sqlPrompt = `
Eres un experto en SQL. Basado en la pregunta del usuario y el esquema de la BD, genera SOLO una consulta SQL SELECT válida. No agregues explicaciones.
Pregunta: ${userQuery}
Esquema:
${schema}
Condiciones: Los campos que tengan que ver con "estado" en las tablas pueden variar entre 'A' o 'I'
SQL:`;

  const sqlQuery = await llm.generateResponse(sqlPrompt);
  console.log(sqlQuery);
  
  let results;
  try {
    results = await executeQuery(sqlQuery);
  } catch (error) {
    return `Error ejecutando consulta: ${error.message}`;
  }

  // Prompt para generar respuesta natural
  const responsePrompt = `
Basado en los resultados de la BD, responde a la pregunta del usuario de forma natural y amigable. Si no hay resultados, di que no se encontró nada.
Pregunta: ${userQuery}
Resultados: ${JSON.stringify(results, null, 2)}
Respuesta:`;

  return await llm.generateResponse(responsePrompt);
}

module.exports = { processQuery };