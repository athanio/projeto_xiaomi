import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [message, setMessage] = useState('')

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!message.trim()) return

    setLoading(true)
    setError(null)
    
    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })

      if (!res.ok) {
        throw new Error(`Erro ${res.status}: ${res.statusText}`)
      }

      const data = await res.json()
      setResponse(data.response || data.message || JSON.stringify(data))
      setMessage('')
    } catch (err) {
      setError(err.message)
      console.error('Erro:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🤖 Xiaomi Proxy</h1>
          <p>Sistema de proxy inteligente para IA Xiaomi</p>
        </header>

        <main className="main">
          <div className="chat-box">
            {response && (
              <div className="response">
                <h3>Resposta:</h3>
                <p>{response}</p>
              </div>
            )}

            {error && (
              <div className="error">
                <p>❌ Erro: {error}</p>
              </div>
            )}

            {!response && !error && !loading && (
              <div className="welcome">
                <p>Bem-vindo! Digite uma mensagem para começar.</p>
              </div>
            )}

            {loading && (
              <div className="loading">
                <p>⏳ Carregando...</p>
              </div>
            )}
          </div>

          <form onSubmit={sendMessage} className="form">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Digite sua mensagem..."
              disabled={loading}
              className="input"
            />
            <button type="submit" disabled={loading} className="button">
              {loading ? 'Enviando...' : 'Enviar'}
            </button>
          </form>
        </main>

        <footer className="footer">
          <p>API URL: {API_URL}</p>
          <p>Status: {response ? '✅ Conectado' : '⏳ Aguardando'}</p>
        </footer>
      </div>
    </div>
  )
}

export default App
