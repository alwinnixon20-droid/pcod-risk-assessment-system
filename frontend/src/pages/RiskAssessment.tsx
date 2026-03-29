import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { riskLevelColor, riskLevelLabel } from "@/lib/utils"

type RiskPreview = {
  prediction: number
  probability: number
}

export default function RiskAssessment() {
  const [result, setResult] = useState<RiskPreview | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const data = localStorage.getItem("prediction")

    if (data) {
      setResult(JSON.parse(data))
    }

    setLoading(false)
  }, [])

  if (loading) {
    return <div className="animate-pulse text-gray-500">Loading assessment...</div>
  }

  if (!result) {
    return (
      <div className="space-y-6 animate-fade-in">
        <h1 className="text-2xl font-bold text-gray-900">Risk assessment</h1>
        <div className="card max-w-xl">
          <p className="text-gray-600 mb-4">
            You don't have a risk assessment yet. Log a cycle to see your screening result.
          </p>
          <Link to="/log-cycle" className="btn-primary">
            Log cycle & get assessment
          </Link>
        </div>
        <Disclaimer />
      </div>
    )
  }

  // 🔥 Convert ML output → UI format
  const score = result.probability ?? 0

  const level =
    score > 70 ? "high" :
    score > 40 ? "moderate" :
    "low"

  const recommendations =
    level === "high"
      ? [
          "Consult a healthcare professional 👩‍⚕️",
          "Maintain a balanced diet 🥗",
          "Exercise regularly 🏃‍♀️",
        ]
      : level === "moderate"
      ? [
          "Monitor your symptoms regularly 📊",
          "Improve lifestyle habits 🌿",
        ]
      : [
          "Keep maintaining a healthy lifestyle ✅",
        ]

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Risk assessment</h1>
        <p className="text-gray-600 mt-1">
          Screening result based on your latest logged cycle (not a medical diagnosis).
        </p>
      </div>

      <div className="card max-w-2xl">
        <div className="flex items-center justify-between mb-6">
          <span className="text-sm font-medium text-gray-500">Risk score</span>
          <span className={`px-3 py-1 rounded-full text-sm font-medium text-white ${riskLevelColor(level)}`}>
            {riskLevelLabel(level)}
          </span>
        </div>

        <div className="mb-2 flex justify-between text-sm text-gray-600">
          <span>0</span>
          <span className="font-semibold text-gray-900">
            {score.toFixed(2)}%
          </span>
          <span>100</span>
        </div>

        <div className="h-4 rounded-full bg-gray-200 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${riskLevelColor(level)}`}
            style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
          />
        </div>
      </div>

      {/* 🔥 AI Recommendations */}
      <div className="card max-w-2xl">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h2>
        <ul className="list-disc list-inside space-y-2 text-gray-700">
          {recommendations.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      </div>

      <div className="flex gap-3">
        <Link to="/log-cycle" className="btn-primary">Log new cycle</Link>
        <Link to="/history" className="btn-secondary">View history</Link>
      </div>

      <Disclaimer />
    </div>
  )
}

function Disclaimer() {
  return (
    <div className="rounded-xl border-2 border-amber-200 bg-amber-50/80 p-4 max-w-2xl">
      <p className="text-sm font-medium text-amber-900">
        Medical disclaimer
      </p>
      <p className="text-sm text-amber-800 mt-1">
        This platform provides early risk screening and does not replace professional medical diagnosis. Always consult a healthcare provider.
      </p>
    </div>
  )
}