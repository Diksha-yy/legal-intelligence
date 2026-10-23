import { Check } from "lucide-react";

// Horizontal N-node stepper. `currentIndex` is the 0-based index of the
// step that's currently active (in progress); everything before it is
// "done", everything after is "pending".
function Stepper({ steps, currentIndex }) {
  return (
    <div className="flex items-start">
      {steps.map((step, i) => {
        const isDone = i < currentIndex;
        const isActive = i === currentIndex;

        return (
          <div key={step} className="flex flex-1 flex-col items-center last:flex-none">
            <div className="flex w-full items-center">
              <div
                className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full border-2 text-sm font-semibold transition-colors ${
                  isDone
                    ? "border-teal bg-teal text-white"
                    : isActive
                    ? "border-royal bg-white text-royal"
                    : "border-slate-200 bg-white text-slate-300"
                }`}
              >
                {isDone ? <Check size={16} /> : i + 1}
              </div>
              {i < steps.length - 1 && (
                <div
                  className={`mx-1 h-0.5 flex-1 ${
                    i < currentIndex ? "bg-teal" : "bg-slate-200"
                  }`}
                />
              )}
            </div>
            <p
              className={`mt-2 text-center text-xs font-medium ${
                isActive ? "text-royal" : isDone ? "text-navy" : "text-slate-400"
              }`}
            >
              {step}
            </p>
          </div>
        );
      })}
    </div>
  );
}

export default Stepper;
