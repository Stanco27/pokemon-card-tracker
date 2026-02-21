import React from 'react';
import { Crosshair, Zap, Shield, ArrowRight } from 'lucide-react';

interface HomeProps {
  onEnter: () => void;
}

const Home: React.FC<HomeProps> = ({ onEnter }) => {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-50 selection:bg-red-500/30">
      <nav className="flex justify-between items-center px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 group cursor-default">
          <div className="p-2 bg-red-600 rounded-lg group-hover:rotate-12 transition-transform">
            <Crosshair size={24} className="text-white" />
          </div>
          <span className="text-xl font-black tracking-tight uppercase">Target_Poke_Snipe</span>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-6 pt-24 pb-20 text-center">
        <div className="inline-block px-4 py-1.5 mb-6 rounded-full border border-red-500/20 bg-red-500/5 text-sm font-medium text-red-400">
          <span className="mr-2">⚡</span> Target Exclusive Engine
        </div>

        <h1 className="text-7xl font-extrabold tracking-tighter mb-8 leading-[1.1]">
          Secure the <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-orange-400 to-yellow-500">
            Next Pokémon Drop.
          </span>
        </h1>

        <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-12 leading-relaxed">
          Optimized specifically for <span className="font-bold">Target.com</span> Pokémon TCG listings. 
          Automated stock polling and instant checkout logic designed to beat the scalper bots.
        </p>

        <button 
          onClick={onEnter}
          className="group relative inline-flex items-center gap-3 bg-red-600 px-8 py-4 rounded-xl font-bold text-lg hover:bg-red-500 transition-all active:scale-95 shadow-2xl shadow-red-900/20"
        >
          Initialize Sniper
          <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
        </button>

        <div className="grid md:grid-cols-3 gap-6 mt-32">
          <FeatureCard 
            icon={<Zap className="text-yellow-400" />} 
            title="Target Optimized" 
            desc="Custom logic built only for Target's checkout flow and DOM structure."
          />
          <FeatureCard 
            icon={<Shield className="text-blue-400" />} 
            title="TCG Ready" 
            desc="Hard-coded to handle Pokémon product variations and high-traffic drops."
          />
          <FeatureCard 
            icon={<Crosshair className="text-red-400" />} 
            title="Session Lock" 
            desc="Stays logged into your Target account to bypass 'Add to Cart' login walls."
          />
        </div>
      </main>

      <footer className="py-10 text-center text-slate-600 text-xs border-t border-slate-900">
        This tool is specialized for Target.com Pokémon card products only.
      </footer>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) => (
  <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 text-left hover:border-slate-700 transition">
    <div className="mb-4">{icon}</div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-slate-400 text-sm leading-relaxed">{desc}</p>
  </div>
);

export default Home;