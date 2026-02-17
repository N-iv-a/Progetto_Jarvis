// App.jsx - Componente principale di Jarvis
import { useState, useEffect } from 'react'
import axios from 'axios'

// URL del backend FastAPI
const API_URL = 'http://localhost:8000'

function App() {
  // === STATE ===
  // useState crea variabili "reattive" - quando cambiano, React aggiorna la UI
  const [tasks, setTasks] = useState([])           // Lista task
  const [nuovoTitolo, setNuovoTitolo] = useState('') // Input per nuova task
  const [loading, setLoading] = useState(true)     // Stato caricamento

  // === EFFETTI ===
  // useEffect esegue codice quando il componente si monta (carica)
  // L'array vuoto [] significa "esegui solo una volta all'avvio"
  useEffect(() => {
    fetchTasks()
  }, [])

  // === FUNZIONI ===
  
  // Recupera tutte le task dal backend
  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${API_URL}/tasks`)
      setTasks(response.data)  // Aggiorna lo state con i dati ricevuti
    } catch (error) {
      console.error('Errore nel recupero task:', error)
    } finally {
      setLoading(false)  // Fine caricamento (sia successo che errore)
    }
  }

  // Crea una nuova task
  const creaTask = async (e) => {
    e.preventDefault()  // Previene il refresh della pagina
    
    if (!nuovoTitolo.trim()) return  // Non creare task vuote
    
    try {
      await axios.post(`${API_URL}/tasks`, {
        titolo: nuovoTitolo,
        categoria: 'INU'  // Default
      })
      setNuovoTitolo('')  // Pulisce l'input
      fetchTasks()        // Ricarica la lista
    } catch (error) {
      console.error('Errore nella creazione:', error)
    }
  }

  // Cambia stato di una task
  const cambiaStato = async (taskId, nuovoStato) => {
    try {
      await axios.patch(`${API_URL}/tasks/${taskId}/status?nuovo_stato=${nuovoStato}`)
      fetchTasks()  // Ricarica la lista
    } catch (error) {
      console.error('Errore nel cambio stato:', error)
    }
  }

  // Elimina una task
  const eliminaTask = async (taskId) => {
    try {
      await axios.delete(`${API_URL}/tasks/${taskId}`)
      fetchTasks()
    } catch (error) {
      console.error('Errore eliminazione:', error)
    }
  }

  // === RENDER ===
  // Mostra "Caricamento..." mentre aspettiamo i dati
  if (loading) return <div>Caricamento...</div>

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>🤖 Jarvis Task Manager</h1>
      
      {/* Form per nuova task */}
      <form onSubmit={creaTask} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={nuovoTitolo}
          onChange={(e) => setNuovoTitolo(e.target.value)}
          placeholder="Nuova task..."
          style={{ padding: '10px', width: '70%', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '10px 20px' }}>
          Aggiungi
        </button>
      </form>

      {/* Lista task */}
      {tasks.length === 0 ? (
        <p>Nessuna task. Creane una!</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {tasks.map((task) => (
            <li 
              key={task.id} 
              style={{ 
                padding: '15px', 
                marginBottom: '10px', 
                border: '1px solid #ccc',
                borderRadius: '5px',
                backgroundColor: task.stato === 'completato' ? '#1e4d3a' : '#16213e'              }}
            >
              <strong>{task.titolo}</strong>
              <br />
              <small>
                Categoria: {task.categoria} | Stato: {task.stato}
              </small>
              <div style={{ marginTop: '10px' }}>
                {/* Bottoni cambio stato */}
                {task.stato !== 'completato' && (
                  <button 
                    onClick={() => cambiaStato(task.id, 'completato')}
                    style={{ marginRight: '5px' }}
                  >
                    ✓ Completa
                  </button>
                )}
                {task.stato === 'aperto' && (
                  <button 
                    onClick={() => cambiaStato(task.id, 'earning')}
                    style={{ marginRight: '5px' }}
                  >
                    🔄 In corso
                  </button>
                )}
                <button 
                  onClick={() => eliminaTask(task.id)}
                  style={{ color: 'red' }}
                >
                  🗑️ Elimina
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default App