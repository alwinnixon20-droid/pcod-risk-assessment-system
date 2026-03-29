import { createContext, useContext, useState, ReactNode } from "react";
import { api } from "@/lib/api";

type AuthContextType = {
  user: number | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<number | null>(null);

  // LOGIN
  const login = async (email: string, password: string) => {
    const res = await api.login({ email, password });

    if (res.user_id) {
      setUser(res.user_id);
      return;
    }

    throw new Error(res.error || "Login failed");
  };

  // REGISTER (name removed since backend not using it)
  const register = async (email: string, password: string) => {
    const res = await api.register({ email, password });

    if (res.message) {
      await login(email, password); // auto login
      return;
    }

    throw new Error(res.error || "Register failed");
  };

  return (
    <AuthContext.Provider value={{ user, login, register }}>
      {children}
    </AuthContext.Provider>
  );
};

// CUSTOM HOOK
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
};