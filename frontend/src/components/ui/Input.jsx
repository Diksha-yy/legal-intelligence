function Input({ className = "", ...props }) {
  return (
    <input
      className={`w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-navy outline-none placeholder:text-slate-400 focus:border-royal focus:ring-2 focus:ring-royal/20 ${className}`}
      {...props}
    />
  );
}

export default Input;
