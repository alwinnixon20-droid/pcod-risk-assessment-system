import { useEffect, useState } from "react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { api } from "@/lib/api"
import { useAuth } from "@/contexts/AuthContext"
import { riskLevelColor, riskLevelLabel } from "@/lib/utils"

type Cycle = {
  result: number
  probability: number
}

export default function History() {
  const [cycles, setCycles] = useState<Cycle[]>([])
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()

  useEffect(() => {
    if (!user) return

    api.history(user)
      .then((data) => setCycles(Array.isArray(data) ? data : []))
      .catch(() => setCycles([]))
      .finally(() => setLoading(false))
  }, [user])

  if (loading) {
    return <div className="animate-pulse text-gray-500">Loading history...</div>
  }

  const riskData = cycles.map((c, i) => ({
    index: i + 1,
    score: c.probability * 100
  }))

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">History & analytics</h1>
        <p className="text-gray-600 mt-1">Cycle history and trends over time.</p>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk progression</h2>

        {riskData.length > 0 ? (
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={riskData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="index" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#7c3aed" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="text-gray-500 py-8 text-center">No risk data yet.</p>
        )}
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">History</h2>

        {cycles.length === 0 ? (
          <p className="text-gray-500 py-4">No data yet.</p>
        ) : (
          <ul className="divide-y divide-gray-200">
            {cycles.map((c, i) => {
              const level =
                c.probability > 0.7 ? "high" :
                c.probability > 0.4 ? "moderate" :
                "low"

              return (
                <li key={i} className="py-3 flex justify-between">
                  <span>Prediction #{i + 1}</span>

                  <span className={`px-2 py-1 rounded text-white ${riskLevelColor(level)}`}>
                    {riskLevelLabel(level)} ({(c.probability * 100).toFixed(1)}%)
                  </span>
                </li>
              )
            })}
          </ul>
        )}
      </div>
    </div>
  )
}