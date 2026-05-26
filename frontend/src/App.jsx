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
        { task }
      );

      const receivedLogs = response.data.logs;

      for (let i = 0; i < receivedLogs.length; i++) {

        await new Promise(resolve =>
          setTimeout(resolve, 700)
        );

        setLogs(prev => [
          ...prev,
          receivedLogs[i]
        ]);
      }

      // Typing effect for summary
      const text = response.data.summary;

      let current = "";

      for (let i = 0; i < text.length; i++) {

        await new Promise(resolve =>
          setTimeout(resolve, 10)
        );

        current += text[i];

        setSummary(current);
      }

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="min-h-screen bg-black text-white overflow-hidden">

      {/* Background Glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-purple-500/10 to-pink-500/10 blur-3xl"></div>

      <div className="relative z-10 flex">

        {/* Sidebar */}
        <div className="w-72 min-h-screen border-r border-white/10 bg-white/5 backdrop-blur-xl p-6">

          <h1 className="text-3xl font-bold mb-10 bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
            AutoPilot OS
          </h1>

          <div className="space-y-4">

            <div className="bg-white/5 border border-white/10 rounded-2xl p-4 hover:scale-105 transition">

              <p className="text-gray-400 text-sm">
                Planner
              </p>

              <p className="text-green-400 font-semibold">
                {loading ? "Running..." : "Ready"}
              </p>

            </div>

            <div className="bg-white/5 border border-white/10 rounded-2xl p-4 hover:scale-105 transition">

              <p className="text-gray-400 text-sm">
                Executor
              </p>

              <p className="text-cyan-400 font-semibold">
                Browser Active
              </p>

            </div>

            <div className="bg-white/5 border border-white/10 rounded-2xl p-4 hover:scale-105 transition">

              <p className="text-gray-400 text-sm">
                Local Model
              </p>

              <p className="text-purple-400 font-semibold">
                Qwen 2.5
              </p>

            </div>

          </div>

        </div>

        {/* Main Content */}
        <div className="flex-1 p-10">

          {/* Header */}
          <div className="mb-10">

            <h2 className="text-5xl font-bold mb-4 leading-tight">
              Autonomous AI Research Agent
            </h2>

            <p className="text-gray-400 text-lg">
              Multi-agent AI system powered by LangGraph,
              Playwright, and Ollama.
            </p>

          </div>

          {/* Input */}
          <div className="flex gap-4 mb-8">

            <input
              type="text"
              placeholder="Ask your AI agent to do something..."
              className="flex-1 p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl outline-none focus:border-cyan-400 transition text-lg"
              value={task}
              onChange={(e) => setTask(e.target.value)}
            />

            <button
              onClick={runTask}
              className="px-8 rounded-2xl bg-gradient-to-r from-cyan-500 to-purple-500 font-bold hover:scale-105 transition-all duration-300 shadow-lg shadow-cyan-500/20"
            >
              {loading ? "Running..." : "Launch"}
            </button>

          </div>

          {/* Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

            {/* Logs */}
            <div className="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-xl h-[500px] overflow-y-auto">

              <div className="flex items-center justify-between mb-6">

                <h3 className="text-2xl font-bold">
                  Live Agent Logs
                </h3>

                <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div>

              </div>

              <div className="space-y-4">

                {logs.map((log, index) => (

                  <div
                    key={index}
                    className="bg-black/30 border border-white/5 rounded-xl p-3 font-mono text-sm animate-fadeIn"
                  >
                    {log}
                  </div>

                ))}

              </div>

            </div>

            {/* Summary */}
            <div className="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-xl h-[500px] overflow-y-auto">

              <div className="flex items-center justify-between mb-6">

                <h3 className="text-2xl font-bold">
                  AI Summary
                </h3>

                <div className="w-3 h-3 rounded-full bg-cyan-400 animate-pulse"></div>

              </div>

              <div className="text-gray-200 leading-8 whitespace-pre-wrap text-lg">

                {summary || "Waiting for task execution..."}

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default App;