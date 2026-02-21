import { Link } from 'react-router-dom';
import { Crosshair, LayoutDashboard, Home as HomeIcon } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="bg-[#020617] border-b border-slate-800 px-8 py-4 flex justify-between items-center sticky top-0 z-50">
      <div className="flex items-center gap-2">
        <Crosshair className="text-red-500" size={20} />
        <span className="font-bold tracking-tighter text-white">POKE_SNIPE</span>
      </div>
      
      <div className="flex gap-6">
        <Link to="/" className="text-slate-400 hover:text-white flex items-center gap-2 text-sm transition">
          <HomeIcon size={16} /> Home
        </Link>
        <Link to="/dashboard" className="text-slate-400 hover:text-white flex items-center gap-2 text-sm transition">
          <LayoutDashboard size={16} /> Dashboard
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;