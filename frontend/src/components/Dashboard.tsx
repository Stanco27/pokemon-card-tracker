import React, { useState } from "react";
import { Settings, Activity, Terminal, Play, Square, Layers, FlaskConical } from "lucide-react";
import type { SniperConfig } from "../types";
import { botApi } from "../api";

const Dashboard: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [testResponse, setTestResponse] = useState<string | null>(null); // State for the API output
  const [config, setConfig] = useState<SniperConfig>({
    tcin: "54244241",
    interval: 5,
    session_id: "target_user_1",
    auto_checkout: true,
  });

  const toggleSniper = () => {
    setIsRunning(!isRunning);
  };

  // The new Test Function
  const handleTestApi = async () => {
    setTestResponse("Sending request to Python...");
    try {
      const data = await botApi.test(config);
      setTestResponse(JSON.stringify(data, null, 2)); // Display pretty JSON
    } catch (err: any) {
      setTestResponse(`Error: ${err.message}`);
    }
  };

  return (
    <div className="flex h-[calc(100vh-64px)] bg-[#020617] text-slate-200">
      <div className="w-64 border-r border-slate-800 p-6 flex flex-col gap-8">
        <div className="font-black text-xl tracking-tighter text-red-500 uppercase">
          Engine_V2
        </div>
        <nav className="space-y-2">
          <div className="flex items-center gap-3 p-3 bg-slate-900 rounded-lg text-white font-bold">
            <Activity size={18} /> Dashboard
          </div>
        </nav>
      </div>

      <main className="flex-1 p-10 overflow-y-auto flex flex-col gap-6">
        <header className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Control Panel</h1>
            <p className="text-slate-500 text-sm">Active Profile: {config.session_id}</p>
          </div>
          <div className="flex gap-4">
            {/* NEW TEST BUTTON */}
            <button
              onClick={handleTestApi}
              className="flex items-center gap-2 px-6 py-4 rounded-xl font-bold bg-amber-600/10 text-amber-500 border border-amber-600/30 hover:bg-amber-600/20 transition-all active:scale-95"
            >
              <FlaskConical size={18} /> TEST CONNECTION
            </button>

            <button
              onClick={toggleSniper}
              className={`flex items-center gap-2 px-8 py-4 rounded-xl font-bold transition-all active:scale-95 ${
                isRunning
                  ? "bg-slate-800 text-red-500 border border-red-500/50"
                  : "bg-red-600 text-white hover:bg-red-500 shadow-xl shadow-red-900/20"
              }`}
            >
              {isRunning ? <><Square size={18} /> KILL ENGINE</> : <><Play size={18} /> RUN SNIPER</>}
            </button>
          </div>
        </header>

        <div className="grid grid-cols-12 gap-8 flex-1">
          <div className="col-span-5 space-y-6">
            <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl">
              <div className="flex items-center gap-2 mb-6">
                <Layers size={18} className="text-red-500" />
                <h2 className="text-sm font-bold uppercase tracking-widest text-slate-400">Targeting Configuration</h2>
              </div>
              
              <div className="space-y-5">
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase mb-2 block">Product TCIN</label>
                  <input
                    type="text"
                    placeholder="e.g. 54244241"
                    value={config.tcin}
                    onChange={(e) => setConfig({ ...config, tcin: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 focus:border-red-500 outline-none transition font-mono text-red-400"
                  />
                  <p className="text-[10px] text-slate-600 mt-2 italic">Found in the Target URL after /A-</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs font-bold text-slate-500 uppercase mb-2 block">Poll Rate (s)</label>
                    <input
                      type="number"
                      value={config.interval}
                      onChange={(e) => setConfig({ ...config, interval: parseFloat(e.target.value) })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 focus:border-red-500 outline-none transition"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-bold text-slate-500 uppercase mb-2 block">Max Retries</label>
                    <input
                      type="number"
                      placeholder="999"
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 focus:border-red-500 outline-none transition"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 bg-slate-950 rounded-xl border border-slate-800">
                  <div className="flex flex-col">
                    <span className="text-sm font-bold text-slate-300">Auto Checkout</span>
                    <span className="text-[10px] text-slate-500">Attempt purchase if stock found</span>
                  </div>
                  <input
                    type="checkbox"
                    checked={config.auto_checkout}
                    onChange={(e) => setConfig({ ...config, auto_checkout: e.target.checked })}
                    className="accent-red-500 h-5 w-5 cursor-pointer"
                  />
                </div>
              </div>
            </div>

            <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl">
               <div className="flex items-center gap-2 mb-4">
                <Settings size={18} className="text-slate-500" />
                <h2 className="text-sm font-bold uppercase tracking-widest text-slate-400">Advanced Engine Stats</h2>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Avg Latency</div>
                  <div className="text-lg font-bold text-green-400">42ms</div>
                </div>
                <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Proxy Status</div>
                  <div className="text-lg font-bold text-blue-400">Active</div>
                </div>
              </div>
            </div>
          </div>

          <div className="col-span-7 bg-black border border-slate-800 rounded-3xl flex flex-col overflow-hidden shadow-2xl">
            <div className="bg-slate-900/80 px-5 py-3 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                <Terminal size={14} className="text-green-500" /> SYSTEM_OUTPUT
              </div>
              <div className="flex gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-slate-800"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-slate-800"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-slate-800"></div>
              </div>
            </div>
            <div className="p-8 font-mono text-sm space-y-3 overflow-y-auto bg-[#020617]/50 h-full">
              <p className="text-slate-600 border-b border-slate-800 pb-2 mb-4">--- INITIALIZING POKÉMON TARGET SNIPER ---</p>
              
              {/* DISPLAY REAL API RESPONSE HERE */}
              {testResponse && (
                <div className="mb-4 p-4 bg-slate-950 border border-slate-800 rounded-lg">
                  <p className="text-xs text-slate-500 mb-2 uppercase font-bold tracking-tighter">API Response:</p>
                  <pre className="text-amber-400 whitespace-pre-wrap">{testResponse}</pre>
                </div>
              )}

              {isRunning ? (
                <div className="space-y-2">
                  <p className="text-blue-400">[{new Date().toLocaleTimeString()}] Fetching Browser Context...</p>
                  <p className="text-green-400">[{new Date().toLocaleTimeString()}] Target Session "{config.session_id}" Validated.</p>
                  <p className="text-white">[{new Date().toLocaleTimeString()}] Monitoring TCIN: <span className="text-yellow-400">{config.tcin}</span></p>
                  <p className="animate-pulse text-red-500">[{new Date().toLocaleTimeString()}] Scanning DOM for "Add to Cart"...</p>
                </div>
              ) : (
                <p className="text-slate-700 italic">Standby... Awaiting initialization.</p>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;