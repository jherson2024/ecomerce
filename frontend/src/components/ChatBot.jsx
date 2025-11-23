import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSanitize from 'rehype-sanitize';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState(() => {
    try {
      const saved = localStorage.getItem('chat_messages_v2_md');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
    localStorage.setItem('chat_messages_v2_md', JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    if (isOpen) inputRef.current?.focus();
  }, [isOpen]);

  const toggleChat = () => setIsOpen(prev => !prev);

  const formatMessage = (text, sender) => ({
    id: Date.now() + Math.random().toString(36).slice(2, 9),
    text,
    sender,
    ts: new Date().toISOString(),
  });

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = formatMessage(input.trim(), 'user');
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);
    setShowPreview(false);

    try {
      const res = await fetch(`${'http://localhost:3000'}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg.text }),
      });

      if (!res.ok) {
        setMessages(prev => [
          ...prev,
          { ...formatMessage(`Error del servidor: ${res.status} ${res.statusText}`, 'bot') },
        ]);
        return;
      }

      const data = await res.json();
      const botText = (data && (data.response || data.text)) || 'Respuesta vacía del servidor';
      setMessages(prev => [...prev, { ...formatMessage(botText, 'bot') }]);
    } catch (err) {
      const text = err.name === 'AbortError' ? 'La petición tardó demasiado (timeout).' : 'Error al conectar con el servidor.';
      setMessages(prev => [...prev, { ...formatMessage(text, 'bot') }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearConversation = () => {
    setMessages([]);
    localStorage.removeItem('chat_messages_v2_md');
    inputRef.current?.focus();
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <button
        aria-expanded={isOpen}
        aria-controls="chat-window"
        onClick={toggleChat}
        className="bg-blue-500 text-white p-4 rounded-full shadow-lg hover:bg-blue-600 transition"
        title="Abrir chat"
      >
        💬
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            id="chat-window"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            role="dialog"
            aria-label="Chatbot"
            className="absolute bottom-16 right-0 w-[360px] max-w-[95vw] h-[520px] bg-white rounded-lg shadow-xl overflow-hidden flex flex-col"
          >
            <div className="bg-blue-500 text-white p-2 flex justify-between items-center">
              <span className="font-medium">Chatbot RAG</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={clearConversation}
                  className="text-sm px-2 py-1 bg-blue-600/30 rounded hover:bg-blue-600/40"
                  title="Limpiar conversación"
                >
                  Limpiar
                </button>
                <button onClick={toggleChat} className="text-white text-xl leading-none px-2" aria-label="Cerrar chat">
                  ×
                </button>
              </div>
            </div>

            {/* Mensajes: renderizamos Markdown seguro */}
            <div
              className="flex-1 p-3 overflow-y-auto space-y-3"
              aria-live="polite"
              aria-atomic="false"
            >
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`max-w-[90%] p-2 rounded-lg break-words ${msg.sender === 'user' ? 'bg-blue-100 ml-auto text-right' : 'bg-gray-100 mr-auto text-left'}`}
                >
                  <div className="text-sm whitespace-pre-wrap">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      rehypePlugins={[rehypeSanitize]}
                      skipHtml={false}
                    >
                      {msg.text}
                    </ReactMarkdown>
                  </div>
                  <div className="text-[10px] opacity-60 mt-1">
                    {new Date(msg.ts).toLocaleTimeString()}
                  </div>
                </motion.div>
              ))}

              <div ref={messagesEndRef} />
              {isLoading && <div className="text-center text-sm">Cargando...</div>}
            </div>

            {/* Input con preview */}
            <div className="p-2 border-t flex flex-col gap-2">
              <div className="flex gap-2 items-start">
                <textarea
                  ref={inputRef}
                  rows={2}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  className="flex-1 p-2 border rounded-md focus:outline-none resize-none"
                  placeholder="Escribe tu consulta"
                  aria-label="Escribe tu mensaje"
                  disabled={isLoading}
                />
                <div className="flex flex-col gap-2">
                  <button
                    onClick={() => setShowPreview(p => !p)}
                    className="bg-gray-100 px-3 py-1 rounded-md text-sm hover:bg-gray-200"
                    title="Mostrar/ocultar vista previa"
                    type="button"
                  >
                    {showPreview ? 'Ocultar' : 'Vista previa'}
                  </button>
                  <button
                    onClick={handleSend}
                    disabled={isLoading || !input.trim()}
                    className="bg-blue-500 text-white px-3 py-1 rounded-md hover:bg-blue-600 disabled:opacity-60"
                    aria-label="Enviar mensaje"
                    type="button"
                  >
                    {isLoading ? '...' : 'Enviar'}
                  </button>
                </div>
              </div>

              {showPreview && (
                <div className="border rounded-md p-2 bg-gray-50 max-h-28 overflow-auto text-xs">
                  <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
                    {input || '_Vacío_'}
                  </ReactMarkdown>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Chatbot;
