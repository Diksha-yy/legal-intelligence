import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AlertCircle } from "lucide-react";
import Navbar from "../../components/Navbar";
import Stepper from "../../components/Stepper";
import { startOcr, getOcrStatus } from "../../api/ocrApi";
import { extractErrorMessage } from "../../api/client";
import { useLanguage } from "../../i18n/LanguageContext";

// The visible pipeline steps presented to the user.
// The frontend drives steps 1-2 (upload + OCR) via real APIs.
// Steps 3-6 are shown as subsequent phases the user can trigger on the Analysis page.
// Values are translation keys (processing.step.*).
const STEPS = ["upload", "ocr", "clauses", "risk", "fairness", "report"];

// OCR polling interval in milliseconds
const POLL_INTERVAL_MS = 3000;
// Maximum number of polls before giving up
const MAX_POLLS = 60;

function Processing() {
  const { t } = useLanguage();
  const { state, search } = useLocation();
  const navigate = useNavigate();

  const query = new URLSearchParams(search);
  const documentId = state?.documentId || query.get("documentId");
  const fileName   = state?.fileName || query.get("fileName") || t("common.document");

  const [currentStep, setCurrentStep]   = useState(0); // 0 = Upload (done), 1 = OCR running
  const [ocrStatus, setOcrStatus]       = useState("PENDING");
  const [ocrStarted, setOcrStarted]     = useState(false);
  const [errorMsg, setErrorMsg]         = useState("");
  const [extractedPreview, setExtractedPreview] = useState("");

  const pollRef = useRef(null);
  const navigationRef = useRef(null);
  const ocrStartRef = useRef(null);

  // ── Step 1: trigger OCR on mount ──────────────────────────────────────────
  useEffect(() => {
    let cancelled = false;

    async function init() {
      if (!documentId) {
        setErrorMsg("processing.err.noDoc");
        return;
      }
      setCurrentStep(1);
      setOcrStatus("PENDING");
      setErrorMsg("");
      setExtractedPreview("");
      setOcrStarted(false);
      try {
        const key = String(documentId);
        if (ocrStartRef.current?.documentId !== key) {
          ocrStartRef.current = {
            documentId: key,
            promise: startOcr(documentId),
          };
        }
        await ocrStartRef.current.promise;
        if (!cancelled) setOcrStarted(true);
      } catch (err) {
        if (ocrStartRef.current?.documentId === String(documentId)) {
          ocrStartRef.current = null;
        }
        if (!cancelled) setErrorMsg(extractErrorMessage(err));
      }
    }

    init();
    return () => {
      cancelled = true;
      clearTimeout(pollRef.current);
      clearTimeout(navigationRef.current);
    };
  }, [documentId]);

  // ── Step 2: poll OCR status ────────────────────────────────────────────────
  useEffect(() => {
    if (!documentId || !ocrStarted || errorMsg) return;

    let cancelled = false;
    let pollCount = 0;

    async function poll() {
      if (cancelled) return;
      pollCount += 1;
      if (pollCount > MAX_POLLS) {
        setErrorMsg("processing.err.timeout");
        return;
      }

      try {
        const job = await getOcrStatus(documentId);
        if (cancelled) return;
        const rawStatus = (job.status || "PENDING").toUpperCase();
        const status = ["DONE", "SUCCESS", "SUCCEEDED"].includes(rawStatus)
          ? "COMPLETED"
          : ["ERROR", "CANCELLED"].includes(rawStatus)
          ? "FAILED"
          : ["RUNNING", "IN_PROGRESS", "QUEUED"].includes(rawStatus)
          ? "PROCESSING"
          : rawStatus;
        setOcrStatus(status);

        if (status === "COMPLETED") {
          setCurrentStep(2); // OCR done — all further steps run on Analysis page
          if (job.extractedText) {
            setExtractedPreview(job.extractedText.slice(0, 600));
          }
          navigationRef.current = setTimeout(() => {
            navigate(`/analysis/${documentId}`, {
              state: { documentId, fileName },
            });
          }, 1500);
        } else if (status === "FAILED") {
          setErrorMsg("processing.err.ocrFailed");
        } else {
          pollRef.current = setTimeout(poll, POLL_INTERVAL_MS);
        }
      } catch (err) {
        if (!cancelled) setErrorMsg(extractErrorMessage(err));
      }
    }

    pollRef.current = setTimeout(poll, POLL_INTERVAL_MS);

    return () => {
      cancelled = true;
      clearTimeout(pollRef.current);
      clearTimeout(navigationRef.current);
    };
  }, [documentId, ocrStarted, errorMsg, navigate, fileName]);

  const progress = Math.round(((currentStep) / (STEPS.length - 1)) * 100);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">
        <h1 className="text-2xl font-bold text-navy">
          {t("processing.title")}
        </h1>
        <p className="mt-1 text-slate-500">
          {t("processing.subtitle", { fileName })}
        </p>

        {/* Error state */}
        {errorMsg && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 p-4 sm:p-6">
            <AlertCircle size={20} className="mt-0.5 shrink-0 text-red-600" />
            <div>
              <p className="font-semibold text-red-700">{t("processing.errorTitle")}</p>
              {/* errorMsg is a translation key for local errors; backend messages pass through t() unchanged */}
              <p className="mt-1 text-sm text-red-600">{t(errorMsg)}</p>
              <button
                className="mt-3 text-sm font-medium text-royal hover:underline"
                onClick={() => navigate("/upload")}
              >
                {t("processing.backToUpload")}
              </button>
            </div>
          </div>
        )}

        {!errorMsg && (
          <>
            {/* Stepper card */}
            <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
              <Stepper steps={STEPS.map((s) => t(`processing.step.${s}`))} currentIndex={currentStep} />

              <div className="mt-8 flex items-center justify-between text-sm">
                <span className="font-medium text-navy">
                  {ocrStatus === "COMPLETED"
                    ? t("processing.ocrComplete")
                    : ocrStatus === "PROCESSING"
                    ? t("processing.ocrExtracting")
                    : ocrStatus === "FAILED"
                    ? t("processing.ocrFailed")
                    : t("processing.ocrStarting")}
                </span>
                <span className="text-slate-500">{progress}%</span>
              </div>
              <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-slate-100">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-royal to-teal transition-all duration-700"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>

            <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
              {/* Document info */}
              <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
                <h2 className="font-semibold text-navy">{t("processing.docInfo")}</h2>
                <div className="mt-4 rounded-xl bg-slate-50 p-5">
                  <p className="break-words text-sm font-semibold text-navy">{fileName}</p>
                  <p className="mt-2 text-xs text-slate-400">
                    {t("processing.docId", { id: documentId })}
                  </p>
                  {extractedPreview && (
                    <p className="mt-3 text-sm text-slate-500 line-clamp-5 leading-relaxed">
                      {extractedPreview}…
                    </p>
                  )}
                  {!extractedPreview && ocrStatus !== "COMPLETED" && (
                    <p className="mt-3 text-sm text-slate-400 italic">
                      {t("processing.previewHint")}
                    </p>
                  )}
                </div>
              </div>

              {/* Processing status checklist */}
              <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
                <h2 className="font-semibold text-navy">{t("processing.statusTitle")}</h2>
                <ul className="mt-4 divide-y divide-slate-100">
                  {STEPS.map((step, i) => {
                    const done    = i < currentStep;
                    const running = i === currentStep;
                    const failed  = running && ocrStatus === "FAILED";
                    return (
                      <li key={step} className="flex items-center justify-between py-3">
                        <span className="text-sm text-navy">{t(`processing.step.${step}`)}</span>
                        <span
                          className={`rounded-full px-2.5 py-1 text-xs font-semibold ${
                            failed
                              ? "bg-red-100 text-red-600"
                              : done
                              ? "bg-brandgreen/10 text-brandgreen"
                              : running
                              ? "bg-royal/10 text-royal"
                              : "bg-slate-100 text-slate-500"
                          }`}
                        >
                          {failed ? t("processing.s.failed") : done ? t("processing.s.done") : running ? t("processing.s.running") : t("processing.s.queued")}
                        </span>
                      </li>
                    );
                  })}
                </ul>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Processing;
