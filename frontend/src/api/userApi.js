import client from "./client";

/**
 * POST /api/users/register
 * @param {{ name: string, email: string, password: string, role: string }} data
 * @returns {Promise<UserResponse>}
 */
export function register(data) {
  return client.post("/api/users/register", data).then((r) => r.data);
}

/**
 * GET /api/users/{id}
 */
export function getUserById(id) {
  return client.get(`/api/users/${id}`).then((r) => r.data);
}
