const dotenv = require('dotenv');
dotenv.config();

const mysql = require('mysql2/promise'); // Usamos la versión con promesas

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '3306'),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  connectionLimit: 20,
  acquireTimeout: 120000,  // 2 minutos
  connectTimeout: 120000, // 2 minutos
  timeout: 180000, // 3 minutos
  waitForConnections: true,
  queueLimit: 0
});

async function getSchema() {
  const dbName = process.env.DB_NAME;
  const connection = await pool.getConnection();
  try {
    const [tables] = await connection.query(
      "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = 'BASE TABLE'",
      [dbName]
    );

    let schema = 'Esquema de la BD:\n';
    for (const { TABLE_NAME: table_name } of tables) {
      schema += `Tabla: ${table_name}\n`;
      const [columns] = await connection.query(
        'SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?',
        [dbName, table_name]
      );
      for (const { COLUMN_NAME: column_name, DATA_TYPE: data_type } of columns) {
        schema += `  - ${column_name}: ${data_type}\n`;
      }
    }
    return schema;
  } finally {
    connection.release(); // Siempre libera la conexión
  }
}

async function executeQuery(sql) {
  if (!sql.trim().toUpperCase().startsWith('SELECT')) {
    throw new Error('Solo consultas SELECT permitidas');
  }
  const connection = await pool.getConnection();
  try {
    const [rows] = await connection.query(sql);
    return rows;
  } finally {
    connection.release(); // Libera para evitar leaks
  }
}

module.exports = { getSchema, executeQuery };