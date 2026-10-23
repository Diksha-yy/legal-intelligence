function Button({
  children,
  variant = "royal",
  className = "",
  as: Component = "button",
  ...props
}) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-2xl px-6 py-3.5 font-semibold text-base transition-[transform,background-color,border-color,box-shadow] duration-200 ease-out hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 motion-reduce:transform-none motion-reduce:transition-none";

  const variants = {
    // Primary CTA — Teal filled (e.g. "Upload Document" on hero)
    teal: "bg-teal text-white shadow-lg shadow-teal/25 hover:bg-teal/90 hover:shadow-xl hover:shadow-teal/30",
    // Primary action inside light surfaces (e.g. "Sign In")
    royal: "bg-royal text-white shadow-lg shadow-royal/25 hover:bg-royal/90 hover:shadow-xl hover:shadow-royal/30",
    // Secondary — translucent, sits well on dark navy backgrounds
    translucent:
      "bg-white/10 text-white border border-white/20 backdrop-blur hover:bg-white/15",
    // Tertiary — outlined
    outline:
      "border border-slate-300 bg-white text-navy hover:bg-slate-50 hover:border-slate-400",
    // Outline on dark background
    outlineDark:
      "border border-white/30 text-white hover:bg-white/10 hover:border-white/50",
    ghost: "text-slate-600 hover:bg-slate-100",
  };

  return (
    <Component
      className={`${base} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </Component>
  );
}

export default Button;
