import client from "./client";

/**
 * POST /api/auth/login
 * @param {{ email: string, password: string }} credentials
 * @returns {Promise<{ message: string, token: string }>}
 */
export function login(credentials) {
  return client.post("/api/auth/login", credentials).then((r) => r.data);
}
