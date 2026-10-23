// Circular progress gauge used for Risk Score / Fairness Score everywhere
// in the app (hero preview card, Analysis dashboard, Risk & Fairness pages).
function GaugeRing({
  value = 0,
  label = "",
  sublabel = "",
  color = "#EF4444",
  size = 96,
  strokeWidth = 8,
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (Math.min(value, 100) / 100) * circumference;

  return (
    <div
      className="relative inline-flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#E2E8F0"
          strokeWidth={strokeWidth}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.6s ease" }}
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center">
        <span className="font-bold text-navy leading-none" style={{ fontSize: size * 0.28 }}>
          {value}
        </span>
        {label && (
          <span
            className="uppercase tracking-wide text-slate-400 font-semibold"
            style={{ fontSize: size * 0.11 }}
          >
            {label}
          </span>
        )}
      </div>
      {sublabel && (
        <span className="absolute -bottom-6 text-xs text-slate-500 whitespace-nowrap">
          {sublabel}
        </span>
      )}
    </div>
  );
}

export default GaugeRing;
