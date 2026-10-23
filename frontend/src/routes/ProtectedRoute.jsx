import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/**
 * Wraps a route that requires the user to be authenticated.
 * If the user is not logged in, they are redirected to /login
 * with the attempted path saved in location state so they can
 * be redirected back after a successful login.
 */
function ProtectedRoute({ children }) {
  const { isLoggedIn } = useAuth();
  const location = useLocation();

  if (!isLoggedIn) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

export default ProtectedRoute;
