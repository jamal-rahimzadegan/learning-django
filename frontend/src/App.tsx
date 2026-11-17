import './App.css';
import { Route, Routes } from 'react-router-dom';
import Layout from './layout/layout.tsx';
import Login from './pages/login.tsx';
import Home from './pages/home.tsx';
import About from './pages/about.tsx';
import { checkIsLoggedIn } from './api/user.ts';
import EventDetails from './pages/event-details.tsx';
import PaymentSuccess from './pages/payment/success.tsx';
import PaymentCancel from './pages/payment/cancel.tsx';
import Tickets from './pages/tickets.tsx';

export default function App() {
  const isLoggedIn = checkIsLoggedIn();

  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/event/:id" element={<EventDetails />} />
        <Route path="/about" element={<About />} />
        <Route path="/tickets" element={<Tickets />} />
        <Route path="/payment/success" element={<PaymentSuccess />} />
        <Route path="/payment/cancel" element={<PaymentCancel />} />
        {isLoggedIn ? null : <Route path="/login" element={<Login />} />}
      </Route>
    </Routes>
  );
}
