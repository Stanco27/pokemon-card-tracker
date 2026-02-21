import { Routes, Route } from 'react-router-dom';
import Home from '../components/Home';
import Dashboard from '../components/Dashboard';

const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<Home onEnter={function (): void {
              throw new Error('Function not implemented.');
          } } />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
};

export default AppRouter;