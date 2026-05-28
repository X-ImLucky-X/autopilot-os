import { useState, useEffect, useRef } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

import {
  Brain,
  Globe,
  Mail,
  Calendar,
  Sparkles,
  Terminal
} from "lucide-react";

import { motion } from "framer-motion";

const cards = [

  {
    title: "Planner Agent",
    icon: Brain,
    color: "from-cyan-500 to-blue-500"
  },

  {
    title: "Research Agent",
    icon: Globe,
    color: "from-purple-500 to-pink-500"
  },

  {
    title: "Email Agent",
    icon: Mail,
    color: "from-green-500 to-emerald-500"
  },

  {
    title: "Calendar Agent",
    icon: Calendar,
    color: "from-orange-500 to-red-500"
  }

];

function App() {

  const [task, setTask] = useState("");

  const [logs, setLogs] = useState([]);

  const [summary, setSummary] = useState("");

  const [loading, setLoading] = useState(false);

  const [history, setHistory] = useState([]);

  const logsEndRef = useRef(null);

  // Auto-scroll logs
  useEffect(() => {

    logsEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });

  }, [logs]);

  const runTask = async () => {

    if (!task.trim()) return;

    setLoading(true);

    setLogs([]);

    setSummary("");

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/task",
        { task }
      );

      const receivedLogs =
        response.data.logs || [];

      // Faster log animation
      for (let i = 0; i < receivedLogs.length; i++) {

        await new Promise(resolve =>
          setTimeout(resolve, 140)
        );

        setLogs(prev => [
          ...prev,
          receivedLogs[i]
        ]);
      }

      // Optimized summary animation
      const text =
        response.data.summary || "";

      const words =
        text.split(" ");

      let current = "";

      for (let i = 0; i < words.length; i++) {

        await new Promise(resolve =>
          setTimeout(resolve, 22)
        );

        current += words[i] + " ";

        setSummary(current);
      }

      // Save recent task history
      setHistory(prev => [
        task,
        ...prev.slice(0, 5)
      ]);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="min-h-screen bg-black text-white overflow-hidden relative">

      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-purple-500/10 to-pink-500/10 blur-3xl"></div>

      {/* Grid Glow */}
      <div className="absolute inset-0 opacity-10 bg-[linear-gradient(to_right,#ffffff10_1px,transparent_1px),linear-gradient(to_bottom,#ffffff10_1px,transparent_1px)] bg-[size:40px_40px]"></div>

      <div className="relative z-10 flex">

        {/* Sidebar */}
        <div className="w-80 min-h-screen border-r border-white/10 bg-white/5 backdrop-blur-2xl p-6">

          <div className="flex items-center gap-3 mb-10">

            <Sparkles className="text-cyan-400" />

            <h1 className="text-3xl font-black bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
              PilotOS
            </h1>

          </div>

          <div className="space-y-5">

            {cards.map((card, index) => {

              const Icon = card.icon;

              return (

                <motion.div
                  key={index}
                  whileHover={{ scale: 1.02 }}
                  className="bg-white/5 border border-white/10 rounded-3xl p-5"
                >

                  <div className="flex items-center justify-between mb-4">

                    <div className={`p-3 rounded-2xl bg-gradient-to-r ${card.color}`}>

                      <Icon size={22} />

                    </div>

                    <div className={`w-3 h-3 rounded-full ${
                      loading
                        ? "bg-green-400 animate-pulse"
                        : "bg-gray-500"
                    }`}></div>

                  </div>

                  <h3 className="font-bold text-lg">
                    {card.title}
                  </h3>

                  <p className="text-gray-400 text-sm mt-1">

                    {loading
                      ? "Active"
                      : "Ready"}

                  </p>

                </motion.div>
              );
            })}

          </div>

          {/* Recent Tasks */}
          <div className="mt-10">

            <h2 className="text-xl font-bold mb-4">
              Recent Tasks
            </h2>

            <div className="space-y-3">

              {history.map((item, index) => (

                <div
                  key={index}
                  className="bg-black/30 border border-white/5 rounded-xl p-3 text-sm text-gray-300"
                >
                  {item}
                </div>

              ))}

            </div>

          </div>

        </div>

        {/* Main */}
        <div className="flex-1 p-10">

          {/* Header */}
          <div className="mb-10">

            <h2 className="text-6xl font-black leading-tight mb-4">

              Autonomous
              <span className="bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
                {" "}AI OS
              </span>

            </h2>

            <p className="text-gray-400 text-xl max-w-3xl leading-8">

              Multi-agent orchestration platform powered by
              LangGraph, Ollama, Playwright,
              Gmail, and Google Calendar automation.

            </p>

          </div>

          {/* Input */}
          <div className="flex gap-4 mb-10">

            <input
              type="text"
              placeholder="Tell PilotOS to do something..."
              className="flex-1 p-6 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl outline-none focus:border-cyan-400 transition text-lg"
              value={task}

              onChange={(e) =>
                setTask(e.target.value)
              }

              onKeyDown={(e) => {

                if (
                  e.key === "Enter"
                ) {

                  runTask();
                }
              }}
            />

            <motion.button
              whileTap={{
                scale: 0.96
              }}

              whileHover={{
                scale: 1.02
              }}

              onClick={runTask}

              className="px-10 rounded-3xl bg-gradient-to-r from-cyan-500 to-purple-500 font-bold text-lg shadow-2xl shadow-cyan-500/20"
            >

              {loading
                ? "Running..."
                : "Launch"}

            </motion.button>

          </div>

          {/* Content */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">

            {/* Logs */}
            <motion.div
              initial={false}
              animate={{ opacity: 1 }}
              className="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-xl h-[550px] overflow-y-auto"
            >

              <div className="flex items-center justify-between mb-6">

                <div className="flex items-center gap-3">

                  <Terminal className="text-cyan-400" />

                  <h3 className="text-2xl font-bold">
                    Live Workflow Logs
                  </h3>

                </div>

                <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div>

              </div>

              <div className="space-y-4">

                {logs.map((log, index) => (

                  <div
                    key={index}
                    className="bg-black/40 border border-white/5 rounded-2xl p-4 font-mono text-sm"
                  >

                    {log}

                  </div>

                ))}

                <div ref={logsEndRef}></div>

              </div>

            </motion.div>

            {/* Summary */}
            <motion.div
              initial={false}
              animate={{ opacity: 1 }}
              className="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-xl h-[550px] overflow-y-auto"
            >

              <div className="flex items-center justify-between mb-6">

                <h3 className="text-2xl font-bold">
                  AI Generated Summary
                </h3>

                <div className="w-3 h-3 rounded-full bg-cyan-400 animate-pulse"></div>

              </div>

              <div className="text-gray-200 leading-9 text-lg prose prose-invert max-w-none">

                <ReactMarkdown>

                  {summary ||
                    "Waiting for autonomous execution..."}

                </ReactMarkdown>

              </div>

            </motion.div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default App;