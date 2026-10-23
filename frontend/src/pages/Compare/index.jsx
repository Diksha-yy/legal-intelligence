import { useEffect, useState } from "react";
import { GitCompareArrows, AlertCircle, Trash2 } from "lucide-react";
import Navbar from "../../components/Navbar";
import Button from "../../components/ui/Button";
import { getAllDocuments } from "../../api/documentApi";
import { compareAgreements, getComparisonHistory, deleteComparison } from "../../api/comparisonApi";
import { extractErrorMessage } from "../../api/client";
import { useLanguage } from "../../i18n/LanguageContext";

const CHANGE_COLORS = {
  ADDED:     "bg-green-50 border-green-200 text-green-700",
  REMOVED:   "bg-red-50 border-red-200 text-red-700",
  MODIFIED:  "bg-amber-50 border-amber-200 text-amber-700",
  UNCHANGED: "bg-slate-50 border-slate-200 text-slate-600",
};

function Compare() {
  const { t, locale } = useLanguage();
  const comparisonStatus = (status) => {
    const key = `compare.status.${status}`;
    return t(key) === key ? String(status || "").replace(/_/g, " ") : t(key);
  };
  const changeLabel = (change) => {
    const key = `compare.change.${change}`;
    return t(key) === key ? String(change || "").replace(/_/g, " ") : t(key);
  };
  const [documents, setDocuments]   = useState([]);
  const [documentsError, setDocumentsError] = useState("");
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [docAId, setDocAId]         = useState("");
  const [docBId, setDocBId]         = useState("");
  const [comparing, setComparing]   = useState(false);
  const [result, setResult]         = useState(null);
  const [error, setError]           = useState("");
  const [history, setHistory]       = useState([]);
  const [histDocId, setHistDocId]   = useState("");
  const [loadingHistory, setLoadingHistory] = useState(false);

  useEffect(() => {
    getAllDocuments()
      .then((docs) => setDocuments(docs || []))
      .catch((err) => setDocumentsError(extractErrorMessage(err)))
      .finally(() => setLoadingDocuments(false));
  }, []);

  async function handleCompare(e) {
    e.preventDefault();
    if (!docAId || !docBId) return;
    if (docAId === docBId) {
      setError(t("compare.differentDocuments"));
      return;
    }
    setComparing(true);
    setError("");
    setResult(null);
    try {
      const res = await compareAgreements({
        versionADocumentId: Number(docAId),
        versionBDocumentId: Number(docBId),
      });
      setResult(res);
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setComparing(false);
    }
  }

  async function loadHistory() {
    if (!histDocId) return;
    setError("");
    setHistory([]);
    setLoadingHistory(true);
    try {
      const h = await getComparisonHistory(Number(histDocId));
      setHistory(h || []);
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setLoadingHistory(false);
    }
  }

  async function handleDeleteComparison(comparisonId) {
    try {
      await deleteComparison(comparisonId);
      setHistory((prev) => prev.filter((c) => c.id !== comparisonId));
      if (result?.id === comparisonId) setResult(null);
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">
        <div className="flex items-start gap-3">
          <GitCompareArrows size={24} className="mt-1 shrink-0 text-royal" />
          <div className="min-w-0">
            <h1 className="text-2xl font-bold text-navy">{t("compare.title")}</h1>
            <p className="mt-0.5 text-sm text-slate-500">
              {t("compare.description")}
            </p>
          </div>
        </div>

        {/* Comparison form */}
        <form
          onSubmit={handleCompare}
          className="mt-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6"
        >
          <h2 className="font-semibold text-navy">{t("compare.selectTitle")}</h2>
          {documentsError && (
            <div className="mt-3 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
              <AlertCircle size={14} className="shrink-0" />
              {t(documentsError)}
            </div>
          )}
          <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-navy">
                {t("compare.documentA")}
              </label>
              <select
                value={docAId}
                onChange={(e) => setDocAId(e.target.value)}
                className="w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm text-navy bg-white focus:outline-none focus:ring-2 focus:ring-royal/30"
                required
                disabled={loadingDocuments || !!documentsError}
              >
                <option value="">{t("compare.chooseA")}</option>
                {documents.map((doc) => (
                  <option key={doc.id} value={doc.id}>
                    {doc.title || doc.fileName}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-navy">
                {t("compare.documentB")}
              </label>
              <select
                value={docBId}
                onChange={(e) => setDocBId(e.target.value)}
                className="w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm text-navy bg-white focus:outline-none focus:ring-2 focus:ring-royal/30"
                required
                disabled={loadingDocuments || !!documentsError}
              >
                <option value="">{t("compare.chooseB")}</option>
                {documents.map((doc) => (
                  <option key={doc.id} value={doc.id}>
                    {doc.title || doc.fileName}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {error && (
            <div className="mt-4 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
              <AlertCircle size={14} className="shrink-0" />
              {t(error)}
            </div>
          )}

          <div className="mt-5">
            <Button type="submit" variant="royal" disabled={comparing || !docAId || !docBId}>
              {comparing ? (
                <><div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" /> {t("compare.loading")}</>
              ) : (
                <><GitCompareArrows size={16} /> {t("compare.submit")}</>
              )}
            </Button>
          </div>
        </form>

        {/* Comparison result */}
        {result && (
          <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="font-semibold text-navy">{t("compare.result")}</h2>
              <span className={`rounded-full px-3 py-1 text-xs font-semibold ${
                result.comparisonStatus === "COMPLETED" ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"
              }`}>
                {comparisonStatus(result.comparisonStatus)}
              </span>
            </div>

            {result.comparisonSummary && (
              <p className="mt-3 text-sm text-slate-600 leading-relaxed">{result.comparisonSummary}</p>
            )}

            {/* Stats */}
            <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
              {[
                { label: t("compare.totalClauses"), value: result.totalClausesCompared },
                { label: t("compare.matched"), value: result.matchedClauses, color: "text-green-600" },
                { label: t("compare.modified"), value: result.modifiedClauses, color: "text-amber-600" },
                { label: t("compare.added"), value: result.addedClauses, color: "text-blue-600" },
                { label: t("compare.removed"), value: result.removedClauses, color: "text-red-600" },
              ].filter(s => s.value != null).map(({ label, value, color }) => (
                <div key={label} className="rounded-xl bg-slate-50 p-3 text-center">
                  <p className={`text-xl font-bold ${color || "text-navy"}`}>{value}</p>
                  <p className="mt-1 text-xs text-slate-500">{label}</p>
                </div>
              ))}
            </div>

            {/* Clause differences */}
            {result.clauseDifferences && result.clauseDifferences.length > 0 && (
              <div className="mt-6">
                <h3 className="text-sm font-semibold text-navy mb-3">
                  {t("compare.differences")}
                </h3>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {result.clauseDifferences.map((diff, i) => (
                    <div
                      key={i}
                      className={`rounded-xl border p-4 text-sm ${CHANGE_COLORS[diff.changeType] || CHANGE_COLORS.UNCHANGED}`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold">
                          {diff.clauseNumber || t("compare.clauseFallback", { number: i + 1 })}
                        </span>
                        <span className="rounded-full border px-2 py-0.5 text-xs font-semibold">
                          {changeLabel(diff.changeType)}
                        </span>
                      </div>
                      {diff.versionAText && (
                        <p className="mt-2 text-xs">
                          <span className="font-medium">{t("compare.versionA")}</span> {diff.versionAText}
                        </p>
                      )}
                      {diff.versionBText && (
                        <p className="mt-1 text-xs">
                          <span className="font-medium">{t("compare.versionB")}</span> {diff.versionBText}
                        </p>
                      )}
                      {diff.remarks && (
                        <p className="mt-1 text-xs italic opacity-80">{diff.remarks}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.comparisonModel && (
              <p className="mt-4 text-xs text-slate-400">{t("compare.model", { name: result.comparisonModel })}</p>
            )}
          </div>
        )}

        {/* History section */}
        <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="font-semibold text-navy">{t("compare.history")}</h2>
          <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center">
            <select
              value={histDocId}
              onChange={(e) => setHistDocId(e.target.value)}
              className="w-full min-w-0 flex-1 rounded-xl border border-slate-200 px-4 py-2.5 text-sm text-navy bg-white focus:outline-none focus:ring-2 focus:ring-royal/30"
            >
              <option value="">{t("compare.chooseHistory")}</option>
              {documents.map((doc) => (
                <option key={doc.id} value={doc.id}>
                  {doc.title || doc.fileName}
                </option>
              ))}
            </select>
            <Button variant="outline" type="button" onClick={loadHistory} disabled={!histDocId || loadingHistory}>
              {loadingHistory ? t("common.loading") : t("compare.loadHistory")}
            </Button>
          </div>

          {loadingHistory && (
            <p className="mt-3 text-sm text-slate-400">{t("common.loading")}</p>
          )}

          {history.length > 0 && (
            <ul className="mt-4 divide-y divide-slate-100">
              {history.map((h) => (
                <li key={h.id} className="flex items-center justify-between py-3">
                  <div>
                    <p className="text-sm font-medium text-navy">
                      {t("compare.historyItem", { id: h.id, a: h.versionADocumentId, b: h.versionBDocumentId })}
                    </p>
                    <p className="text-xs text-slate-400">
                      {t("compare.historyDetails", {
                        status: comparisonStatus(h.comparisonStatus),
                        count: h.totalClausesCompared,
                        date: new Date(h.createdAt).toLocaleDateString(locale),
                      })}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      className="text-xs font-medium text-royal hover:underline"
                      onClick={() => setResult(h)}
                    >
                      {t("compare.view")}
                    </button>
                    <button
                      className="text-slate-300 hover:text-red-400"
                      onClick={() => handleDeleteComparison(h.id)}
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
          {history.length === 0 && histDocId && !loadingHistory && !error && (
            <p className="mt-3 text-sm text-slate-400">{t("compare.noHistory")}</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Compare;
