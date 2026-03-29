import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function riskLevelColor(level: string | null | undefined): string {
  if (!level) return "bg-gray-400"
  switch (level) {
    case "low": return "bg-emerald-500"
    case "moderate": return "bg-amber-500"
    case "high": return "bg-rose-500"
    default: return "bg-gray-400"
  }
}

export function riskLevelLabel(level: string | null | undefined): string {
  if (!level) return "—"
  switch (level) {
    case "low": return "Low Risk"
    case "moderate": return "Moderate Risk"
    case "high": return "High Risk"
    default: return level
  }
}
