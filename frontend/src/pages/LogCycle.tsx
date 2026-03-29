import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { api } from "@/lib/api"
import { useAuth } from "@/contexts/AuthContext"

const initialForm = {
  cycle_length: "",
  irregular_cycle: false,
  missed_periods: 0,
  pain_level: 5,
  bleeding_duration: 5,
  acne: 0,
  excess_facial_hair: 0,
  hair_thinning: 0,
  dark_patches: 0,
  oily_skin: 0,
  weight_kg: "",
  height_cm: "",
  fatigue: 0,
  sugar_cravings: 0,
  physical_activity: 1,
  sleep_hours: 7,
  fast_food_frequency: 0,
  stress_level: 0,
}

export default function LogCycle() {
  const [form, setForm] = useState(initialForm)
  const [bmi, setBmi] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const navigate = useNavigate()
  const { user } = useAuth()

  useEffect(() => {
    const w = Number(form.weight_kg)
    const h = Number(form.height_cm)
    if (w > 0 && h > 0) {
      setBmi(Math.round((w / ((h / 100) ** 2)) * 10) / 10)
    } else {
      setBmi(null)
    }
  }, [form.weight_kg, form.height_cm])

  const update = (key: any, value: any) => {
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  const handleSubmit = async (e: any) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    try {
      const payload = {
        ...form,
        user_id: user
      }

      const res = await api.predict(payload)

      localStorage.setItem("prediction", JSON.stringify(res))

      navigate("/risk-assessment")
    } catch (err) {
      setError("Backend connection failed. Start Flask server.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">Log cycle & symptoms</h1>

      {error && (
        <div className="bg-red-100 text-red-700 p-2 rounded">{error}</div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">

        <input
          type="number"
          placeholder="Cycle length"
          className="input-field"
          onChange={(e) => update("cycle_length", e.target.value)}
        />

        <input
          type="number"
          placeholder="Weight"
          className="input-field"
          onChange={(e) => update("weight_kg", e.target.value)}
        />

        <input
          type="number"
          placeholder="Height"
          className="input-field"
          onChange={(e) => update("height_cm", e.target.value)}
        />

        <p>BMI: {bmi ?? "-"}</p>

        <button className="btn-primary" disabled={loading}>
          {loading ? "Processing..." : "Submit"}
        </button>

      </form>
    </div>
  )
}