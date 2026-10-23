// Small colored pill used for risk levels (High/Medium/Low) and status
// tags (Success/Info/Warning) — reused across Dashboard, Admin, Reports.
const VARIANTS = {
  high: "bg-danger/10 text-danger",
  medium: "bg-amber/10 text-amber",
  low: "bg-brandgreen/10 text-brandgreen",
  success: "bg-brandgreen/10 text-brandgreen",
  info: "bg-royal/10 text-royal",
  warning: "bg-amber/10 text-amber",
  neutral: "bg-slate-100 text-slate-600",
};

function Badge({ variant = "neutral", children, className = "" }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold whitespace-nowrap ${VARIANTS[variant]} ${className}`}
    >
      {children}
    </span>
  );
}

export default Badge;
