import { Link, Outlet, useNavigate } from 'react-router-dom';
import { checkIsLoggedIn } from '../api/user.ts';

export default function Layout() {
  const isLoggedIn = checkIsLoggedIn();
  const navigate = useNavigate();

  const logout = () => {
    const isConfirmed = window.confirm('Are you sure you want to logout?');
    if (!isConfirmed) return;

    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');

    navigate(0);
  };

  return (
    <div className="flex min-h-screen flex-col bg-gray-50 text-gray-900">
      <header className="border-b bg-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link to="/" className="text-xl font-bold">
            Social Events
          </Link>
          <nav className="flex items-center gap-6 text-sm">
            <Link
              to="/"
              className="text-gray-600 transition hover:text-gray-900"
            >
              Home
            </Link>
            <Link
              to="/about"
              className="text-gray-600 transition hover:text-gray-900"
            >
              About
            </Link>
            {isLoggedIn ? (
              <button onClick={logout}>Logout</button>
            ) : (
              <Link
                to="/login"
                className="text-gray-600 transition hover:text-gray-900"
              >
                Login
              </Link>
            )}
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <div className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <Outlet />
        </div>
      </main>

      <footer className="border-t bg-white">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-2 px-4 py-6 text-sm text-gray-500 sm:flex-row sm:px-6 lg:px-8">
          <p>© {new Date().getFullYear()} Social Events</p>
          <div className="flex gap-4">
            <Link to="/privacy" className="hover:text-gray-900">
              Privacy
            </Link>
            <Link to="/terms" className="hover:text-gray-900">
              Terms
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
