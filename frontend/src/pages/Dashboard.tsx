const BASE_URL = "http://127.0.0.1:5000";

// COMMON FETCH HELPER
const request = async (url: string, options?: RequestInit) => {
  const res = await fetch(url, options);
  const data = await res.json();
  return { data };
};

// MAIN API
export const api = {
  predict: (data: any) =>
    request(`${BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),

  login: (data: any) =>
    request(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),

  register: (data: any) =>
    request(`${BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),

  history: (userId: number) =>
    request(`${BASE_URL}/history/${userId}`),
};

// ✅ CLEAN ANALYTICS API (NO HACKS)
export const analyticsApi = {
  summary: async () => {
    const { data } = await api.history(1); // later replace with real user

    const cycles = Array.isArray(data) ? data : [];

    return {
      data: {
        total_cycles: cycles.length,
        latest_risk_score: cycles[0]?.risk_score ?? null,
        latest_risk_level: cycles[0]?.risk_level ?? null,
        cycle_lengths: cycles.map((c: any) => ({
          created_at: c.created_at,
          cycle_length: c.cycle_length,
        })),
        risk_progression: cycles.map((c: any) => ({
          created_at: c.created_at,
          risk_score: c.risk_score,
          risk_level: c.risk_level,
        })),
      },
    };
  },
};