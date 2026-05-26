import { useState } from "react";
import axios from "axios";

function App() {

  const [task, setTask] = useState("");
  const [logs, setLogs] = useState([]);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const runTask = async () => {

    if (!task) return;
  
    setLoading(true);
  
    setLogs([]);
    setSummary("");
  
    try {
  
      const response = await axios.post(
        "http://127.0.0.1:8000/task",
        {
          task
        }
      );
  
      const receivedLogs = response.data.logs;
  
      // Animate logs one-by-one
      for (let i = 0; i < receivedLogs.length; i++) {
  
        await new Promise(resolve =>
          setTimeout(resolve, 800)
        );
  
        setLogs(prev => [
          ...prev,
          receivedLogs[i]
        ]);
      }
  
      setSummary(response.data.summary);
  
    } catch (error) {
  
      console.error(error);
  
    } finally {
  
      setLoading(false);
    }
  };

  return (

    <div className="min-h-screen bg-black text-green-400 p-8">

      <h1 className="text-5xl font-bold mb-8">
        AutoPilot OS
      </h1>

      {/* Input */}
      <div className="flex gap-4 mb-8">

        <input
          type="text"
          placeholder="Enter task..."
          className="flex-1 p-4 rounded bg-gray-900 border border-green-500"
          value={task}
          onChange={(e) => setTask(e.target.value)}
        />

        <button
          onClick={runTask}
          className="bg-green-500 text-black px-6 rounded font-bold"
        >
          {loading ? "Running..." : "Run"}
        </button>

      </div>

      {/* Logs */}
      <div className="bg-gray-900 p-4 rounded mb-8">

        <h2 className="text-2xl mb-4">
          Agent Logs
        </h2>

        {logs.map((log, index) => (

          <p
            key={index}
            className="mb-2 font-mono animate-pulse"
          >
            {log}
          </p>

        ))}

      </div>

      {/* Summary */}
      <div className="bg-gray-900 p-4 rounded">

        <h2 className="text-2xl mb-4">
          Final Summary
        </h2>

        <p className="text-white">
          {summary}
        </p>

      </div>

    </div>
  );
}

export default App;