/* eslint-disable react-refresh/only-export-components */

/**
 * AuthContext — real JWT-backed authentication.
 *
 * Token storage: sessionStorage (scoped to the browser tab, never logged).
 * isLoggedIn is derived exclusively from the presence of a valid token.
 *
 * login(token, user)  — called after a successful POST /api/auth/login
 * logout()            — clears token + user, redirects to /login
 */

import { createContext, useContext, useState } from "react";
import { TOKEN_KEY, USER_KEY } from "./authStorage";

const AuthContext = createContext(null);

function readSession() {
  try {
    const token = sessionStorage.getItem(TOKEN_KEY) || null;
    const raw = sessionStorage.getItem(USER_KEY);
    let user = null;
    if (raw) {
      try {
        user = JSON.parse(raw);
      } catch {
        sessionStorage.removeItem(USER_KEY);
      }
    }
    return { token, user };
  } catch {
    return { token: null, user: null };
  }
}

export function AuthProvider({ children }) {
  const [{ token, user }, setSession] = useState(readSession);

  const isLoggedIn = Boolean(token);

  /**
   * Store the JWT and optional user profile returned by the backend.
   * @param {string} jwtToken   — the raw token string from LoginResponse
   * @param {object} [userObj]  — optional user profile (name, email, etc.)
   */
   const login = (jwtToken, userObj = null) => {
     if (userObj) {
       sessionStorage.setItem(USER_KEY, JSON.stringify(userObj));
     } else {
       sessionStorage.removeItem(USER_KEY);
     }
     sessionStorage.setItem(TOKEN_KEY, jwtToken);
     setSession({ token: jwtToken, user: userObj });
   };

  const logout = () => {
    try {
      sessionStorage.removeItem(TOKEN_KEY);
      sessionStorage.removeItem(USER_KEY);
    } catch {
      // Ignore.
    }
    setSession({ token: null, user: null });
  };

  // Convenience display name — falls back gracefully when no profile is stored.
  const userName = user?.name || user?.email || "";

  return (
    <AuthContext.Provider value={{ isLoggedIn, token, user, userName, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
