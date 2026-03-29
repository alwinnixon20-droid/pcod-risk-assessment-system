import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "@/contexts/AuthContext"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)
    try {
      await login(email, password)
      navigate("/dashboard")
    } catch (err: unknown) {
      const axErr = err as { response?: { status?: number; data?: { error?: string; message?: string }; statusText?: string }; message?: string; code?: string }
      if (!axErr.response) {
        // Network error or backend not running
        setError(`Cannot connect to server. Make sure the backend is running at ${import.meta.env.VITE_API_URL || "http://localhost:5000"}`)
        return
      }
      const data = axErr.response.data
      const msg = (typeof data === "object" && data !== null && (data.error || data.message)) || axErr.response.statusText || "Login failed"
      setError(typeof msg === "string" ? msg : "Login failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="card w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Welcome back</h1>
        <p className="text-gray-600 mb-6">Sign in to your PCOS Risk Assessment account.</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="rounded-lg bg-red-50 text-red-700 px-3 py-2 text-sm">{error}</div>
          )}
          <div>
            <label className="label">Email</label>
            <input
              type="email"
              className="input-field"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>
          <div>
            <label className="label">Password</label>
            <input
              type="password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-primary w-full" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">
          Don't have an account?{" "}
          <Link to="/register" className="font-medium text-primary-600 hover:text-primary-700">Register</Link>
        </p>
      </div>
    </div>
  )
}
