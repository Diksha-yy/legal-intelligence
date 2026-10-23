import { Link } from "react-router-dom";
import { ArrowUpRight } from "lucide-react";
import { motion } from "framer-motion";

// Equal-weight "quick action" tile used on the Dashboard (Upload / Ask /
// Compare / Reports) and reusable anywhere a labelled icon-link is needed.
function StatCard({ icon: Icon, title, description, to, iconClassName = "", delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.99 }}
      transition={{ duration: 0.24, delay, ease: "easeOut" }}
      className="h-full"
    >
    <Link
      to={to}
      target="_blank"
      rel="noopener noreferrer"
      className="group relative block h-full rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm shadow-slate-900/[0.02] transition-[border-color,box-shadow] duration-200 hover:border-royal/25 hover:shadow-lg hover:shadow-slate-900/[0.06] focus-visible:outline-royal"
    >
      <span
        className={`flex h-11 w-11 items-center justify-center rounded-xl bg-royal/10 text-royal transition-colors group-hover:bg-royal group-hover:text-white ${iconClassName}`}
      >
        <Icon size={18} />
      </span>
      <ArrowUpRight size={17} aria-hidden="true" className="absolute right-5 top-5 text-slate-300 transition-all group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-royal" />
      <h3 className="mt-4 font-semibold tracking-tight text-navy">{title}</h3>
      <p className="mt-1 text-sm text-slate-500">{description}</p>
    </Link>
    </motion.div>
  );
}

export default StatCard;
