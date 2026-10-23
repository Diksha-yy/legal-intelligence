import { FileX } from "lucide-react";

/**
 * EmptyState — shown when a list or section has no data.
 * Accepts optional title, description, and an action element (e.g. a Button).
 */
function EmptyState({ title = "Nothing here yet", description = "", action = null }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <span className="flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-100 text-slate-400">
        <FileX size={24} />
      </span>
      <h3 className="mt-4 font-semibold text-navy">{title}</h3>
      {description && (
        <p className="mt-1 max-w-xs text-sm text-slate-500">{description}</p>
      )}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}

export default EmptyState;
