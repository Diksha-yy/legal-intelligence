export function getRiskBand(score) {
  if (score == null || (typeof score === "string" && !score.trim())) return null;
  const value = Number(score);
  if (!Number.isFinite(value)) return null;
  if (value < 50) return "HIGH";
  if (value < 75) return "MEDIUM";
  return "LOW";
}

export function getRiskBandFromStatus(status) {
  const normalized = String(status || "").toUpperCase().replace(/[\s-]+/g, "_");
  if (normalized === "HIGH" || normalized.includes("HIGH_RISK")) return "HIGH";
  if (normalized === "MEDIUM" || normalized.includes("MEDIUM_RISK")) return "MEDIUM";
  if (normalized === "LOW" || normalized.includes("LOW_RISK")) return "LOW";
  return null;
}

export function getRiskColor(score) {
  const band = getRiskBand(score);
  if (band === "HIGH") return "#EF4444";
  if (band === "MEDIUM") return "#F59E0B";
  if (band === "LOW") return "#22C55E";
  return "#94a3b8";
}

export function getRiskTextClass(score) {
  const band = getRiskBand(score);
  if (band === "HIGH") return "text-danger";
  if (band === "MEDIUM") return "text-amber";
  if (band === "LOW") return "text-brandgreen";
  return "text-slate-500";
}

export function getRiskBadgeClass(band) {
  if (band === "HIGH") return "bg-danger/10 text-danger";
  if (band === "MEDIUM") return "bg-amber/10 text-amber";
  if (band === "LOW") return "bg-brandgreen/10 text-brandgreen";
  return null;
}
