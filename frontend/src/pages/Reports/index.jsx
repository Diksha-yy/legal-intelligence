import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { FileBarChart2, Download, AlertCircle, Languages } from "lucide-react";
import Navbar from "../../components/Navbar";
import Button from "../../components/ui/Button";
import { getAllDocuments, getDocumentById } from "../../api/documentApi";
import { getSummary } from "../../api/summaryApi";
import { getRiskScore } from "../../api/riskApi";
import { getFairnessScore } from "../../api/fairnessApi";
import { getClausesByDocument } from "../../api/clauseApi";
import { generateTranslation, getTranslation } from "../../api/translationApi";
import { extractErrorMessage } from "../../api/client";
import { useLanguage } from "../../i18n/LanguageContext";
import { getRiskBand, getRiskTextClass } from "../../utils/risk";

const LANGUAGE_OPTIONS = [
  { code: "en", label: "English" },
  { code: "hi", label: "Hindi" },
  { code: "mr", label: "Marathi" },
];

function Reports() {
  const { state } = useLocation();
  const { t, ts, locale } = useLanguage();

  const [documents, setDocuments]     = useState([]);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [documentsError, setDocumentsError] = useState("");
  const [selectedDocId, setSelectedDocId] = useState(state?.documentId ? String(state.documentId) : "");

  // Per-module data
  const [doc,       setDoc]       = useState(null);
  const [summary,   setSummary]   = useState(null);
  const [risk,      setRisk]      = useState(null);
  const [fairness,  setFairness]  = useState(null);
  const [clauses,   setClauses]   = useState([]);
  const [loading,   setLoading]   = useState(false);
  const [loadErrors, setLoadErrors] = useState([]);

  // Translation state
  const [sourceLang,    setSourceLang]    = useState("en");
  const [targetLang,    setTargetLang]    = useState("hi");
  const [translation,   setTranslation]   = useState(null);
  const [translating,   setTranslating]   = useState(false);
  const [transErr,      setTransErr]      = useState("");

  useEffect(() => {
    getAllDocuments()
      .then((docs) => setDocuments(docs || []))
      .catch((err) => setDocumentsError(extractErrorMessage(err)))
      .finally(() => setLoadingDocuments(false));
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function loadAll() {
      if (!selectedDocId) {
        setDoc(null); setSummary(null); setRisk(null); setFairness(null);
        setClauses([]); setTranslation(null);
        setLoadErrors([]);
        setLoading(false);
        return;
      }
      const id = Number(selectedDocId);
      setLoading(true);
      setLoadErrors([]);

      try {
        const [docR, sumR, riskR, fairR, clsR, transR] = await Promise.allSettled([
          getDocumentById(id),
          getSummary(id),
          getRiskScore(id),
          getFairnessScore(id),
          getClausesByDocument(id),
          getTranslation(id),
        ]);

        if (cancelled) return;
        if (docR.status === "fulfilled")    setDoc(docR.value);
        else {
          setDoc(null);
        }
        if (sumR.status === "fulfilled")    setSummary(sumR.value);
        else                                setSummary(null);
        if (riskR.status === "fulfilled")   setRisk(riskR.value);
        else                                setRisk(null);
        if (fairR.status === "fulfilled")   setFairness(fairR.value);
        else                                setFairness(null);
        if (clsR.status === "fulfilled")    setClauses(clsR.value || []);
        else                                setClauses([]);
        if (transR.status === "fulfilled")  setTranslation(transR.value);
        else                                setTranslation(null);
        const moduleResults = [
          ["reports.documentInfo", docR],
          ["reports.summary", sumR],
          ["reports.riskScore", riskR],
          ["reports.fairnessScore", fairR],
          ["reports.classifiedClausesLabel", clsR],
          ["reports.translationTitle", transR],
        ];
        setLoadErrors(moduleResults
          .filter(([, result]) => result.status === "rejected" && result.reason.response?.status !== 404)
          .map(([section, result]) => ({
            section,
            message: extractErrorMessage(result.reason),
          })));
      } catch (err) {
        if (!cancelled) setLoadErrors([{ section: "", message: extractErrorMessage(err) }]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadAll();
    return () => { cancelled = true; };
  }, [selectedDocId]);

  async function handleTranslate() {
    if (!selectedDocId || translating) return;
    if (sourceLang === targetLang) {
      setTransErr(t("reports.languageError"));
      return;
    }
    setTranslating(true);
    setTransErr("");
    try {
      const result = await generateTranslation(Number(selectedDocId), sourceLang, targetLang);
      setTranslation(result);
    } catch (err) {
      setTransErr(extractErrorMessage(err));
    } finally {
      setTranslating(false);
    }
  }

  function handleExportText() {
    if (!doc) return;
    const lines = [];
    lines.push(`Legal Assistant — ${t("reports.title")}`);
    lines.push(`${t("reports.field.title")}: ${doc.title || doc.fileName}`);
    lines.push(`${t("reports.field.status")}: ${ts(doc.status)}`);
    lines.push(`${t("reports.field.uploadedAt")}: ${doc.uploadedAt}`);
    lines.push("");
    if (summary) { lines.push(t("reports.summary").toUpperCase()); lines.push(summary.summary); lines.push(""); }
    if (risk) {
      lines.push(`${t("reports.riskScore").toUpperCase()}: ${risk.riskScore}/100 (${risk.riskLevel})`);
      if (risk.explanation) lines.push(risk.explanation);
      lines.push("");
    }
    if (fairness) {
      lines.push(`${t("reports.fairnessScore").toUpperCase()}: ${Math.round(fairness.fairnessScore)}/100`);
      if (fairness.explanation) lines.push(fairness.explanation);
      lines.push("");
    }
    if (clauses.length) {
      lines.push(`${t("reports.classifiedClauses", { count: clauses.length })}`);
      clauses.forEach((c) => lines.push(`- ${c.clauseName}: ${c.clauseText || ""}`));
      lines.push("");
    }
    if (translation) {
      lines.push(`${t("reports.translationTitle")} (${translation.sourceLanguage} → ${translation.targetLanguage})`);
      lines.push(translation.translatedText);
    }

    const blob = new Blob([lines.join("\n")], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Legal_Assistant_Report_${doc.title || doc.fileName}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <FileBarChart2 size={24} className="text-royal" />
            <div>
              <h1 className="text-2xl font-bold text-navy">{t("reports.title")}</h1>
              <p className="mt-0.5 text-sm text-slate-500">
                  {t("reports.description")}
              </p>
            </div>
          </div>
          {doc && (
            <Button variant="outline" onClick={handleExportText}>
              <Download size={16} /> {t("reports.export")}
            </Button>
          )}
        </div>

        {/* Document selector */}
        <div className="mt-6">
          <label className="mb-1.5 block text-sm font-medium text-navy">
            {t("reports.selectDocument")}
          </label>
          <select
            value={selectedDocId}
            onChange={(e) => setSelectedDocId(e.target.value)}
            disabled={loadingDocuments || documents.length === 0}
            className="w-full max-w-xl rounded-xl border border-slate-200 px-4 py-2.5 text-sm text-navy bg-white focus:outline-none focus:ring-2 focus:ring-royal/30"
          >
            <option value="">{t("reports.chooseDocument")}</option>
            {documents.map((d) => (
              <option key={d.id} value={d.id}>
                {d.title || d.fileName}
              </option>
            ))}
          </select>
          {documentsError && (
            <p className="mt-2 text-sm text-red-600">{t(documentsError)}</p>
          )}
          {loadingDocuments && (
            <p className="mt-2 text-sm text-slate-500">{t("reports.loadingDocuments")}</p>
          )}
          {!loadingDocuments && !documentsError && documents.length === 0 && (
            <p className="mt-2 text-sm text-slate-500">{t("reports.noDocuments")}</p>
          )}
        </div>

        {loading && (
          <div className="mt-6 flex items-center gap-2 text-slate-400 text-sm">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-royal border-t-transparent" />
            {t("reports.loading")}
          </div>
        )}

        {loadErrors.length > 0 && (
          <ul className="mt-4 space-y-2 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {loadErrors.map((item, index) => (
              <li key={`${item.section}-${index}`} className="flex items-start gap-2">
                <AlertCircle size={14} className="mt-0.5 shrink-0" />
                {item.section ? `${t(item.section)}: ` : ""}{t(item.message)}
              </li>
            ))}
          </ul>
        )}

        {!loading && doc && (
          <div className="mt-6 space-y-6">
            {/* Document info */}
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="font-semibold text-navy">{t("reports.documentInfo")}</h2>
              <dl className="mt-4 grid grid-cols-2 gap-4 text-sm sm:grid-cols-3">
                {[
                  { label: t("reports.field.title"), value: doc.title || doc.fileName },
                  { label: t("reports.field.fileName"), value: doc.fileName },
                  { label: t("reports.field.status"), value: ts(doc.status) },
                  { label: t("reports.field.uploadedBy"), value: doc.uploadedBy || "—" },
                  { label: t("reports.field.uploadedAt"), value: doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString(locale) : "—" },
                ].map(({ label, value }) => (
                  <div key={label}>
                    <dt className="text-xs font-medium text-slate-400 uppercase tracking-wide">{label}</dt>
                    <dd className="mt-1 text-navy">{value}</dd>
                  </div>
                ))}
              </dl>
            </div>

            {/* Summary */}
            {summary && (
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="font-semibold text-navy">{t("reports.summary")}</h2>
                <p className="mt-3 break-words text-sm leading-relaxed text-slate-600">{summary.summary}</p>
                {summary.summaryModel && <p className="mt-2 text-xs text-slate-400">{t("reports.model", { name: summary.summaryModel })}</p>}
              </div>
            )}

            {/* Risk */}
            {risk && (
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="font-semibold text-navy">{t("reports.riskScore")}</h2>
                <p className={`mt-3 text-3xl font-bold ${getRiskTextClass(risk.riskScore)}`}>{risk.riskScore}/100
                  <span className={`ml-3 text-base font-semibold ${getRiskTextClass(risk.riskScore)}`}>
                    {t(`risk.level.${getRiskBand(risk.riskScore) || "default"}`)}
                  </span>
                </p>
                {risk.explanation && <p className="mt-2 text-sm text-slate-600">{risk.explanation}</p>}
                {risk.riskFactors && risk.riskFactors.length > 0 && (
                  <ul className="mt-3 space-y-1">
                    {risk.riskFactors.map((rf, i) => (
                      <li key={i} className="flex items-center gap-2 text-sm text-slate-600">
                        <span className={getRiskTextClass(risk.riskScore)}>•</span>
                        <span className="font-medium">{rf.factor}</span>
                        {rf.description && <span className="text-slate-400">— {rf.description}</span>}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}

            {/* Fairness */}
            {fairness && (
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="font-semibold text-navy">{t("reports.fairnessScore")}</h2>
                <p className="mt-3 text-3xl font-bold text-amber">
                  {Math.round(fairness.fairnessScore)}/100
                </p>
                {fairness.explanation && <p className="mt-2 text-sm text-slate-600">{fairness.explanation}</p>}
              </div>
            )}

            {/* Clauses */}
            {clauses.length > 0 && (
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="font-semibold text-navy">{t("reports.classifiedClauses", { count: clauses.length })}</h2>
                <ul className="mt-4 divide-y divide-slate-100 max-h-64 overflow-y-auto">
                  {clauses.map((c) => (
                    <li key={c.id} className="py-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-navy">{c.clauseName}</span>
                        <span className="text-xs text-slate-400">
                          {c.confidence != null ? `${(c.confidence * 100).toFixed(0)}%` : ""}
                        </span>
                      </div>
                      {c.clauseText && (
                        <p className="mt-1 text-xs text-slate-500 line-clamp-2">{c.clauseText}</p>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Translation */}
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-2">
                <Languages size={18} className="text-royal" />
                <h2 className="font-semibold text-navy">{t("reports.translationTitle")}</h2>
              </div>
              <p className="mt-1 text-sm text-slate-500">
                {t("reports.translationDescription")}
              </p>

              <div className="mt-4 flex flex-wrap items-end gap-4">
                <div>
                  <label className="mb-1 block text-xs font-medium text-slate-500">{t("reports.from")}</label>
                  <select
                    value={sourceLang}
                    onChange={(e) => setSourceLang(e.target.value)}
                    className="rounded-xl border border-slate-200 px-3 py-2 text-sm text-navy bg-white focus:outline-none focus:ring-2 focus:ring-royal/30"
                  >
                    {LANGUAGE_OPTIONS.map((l) => (
                      <option key={l.code} value={l.code}>{l.label}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="mb-1 block text-xs font-medium text-slate-500">{t("reports.to")}</label>
                  <select
                    value={targetLang}
                    onChange={(e) => setTargetLang(e.target.value)}
                    className="rounded-xl border border-slate-200 px-3 py-2 text-sm text-navy bg-white focus:outline-none focus:ring-2 focus:ring-royal/30"
                  >
                    {LANGUAGE_OPTIONS.map((l) => (
                      <option key={l.code} value={l.code}>{l.label}</option>
                    ))}
                  </select>
                </div>
                <Button
                  variant="royal"
                  onClick={handleTranslate}
                  disabled={translating}
                  type="button"
                >
                  {translating ? (
                    <><div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" /> {t("reports.translating")}</>
                  ) : (
                    <><Languages size={16} /> {t("reports.translate")}</>
                  )}
                </Button>
              </div>

              {transErr && (
                <div className="mt-3 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-sm text-red-700">
                  <AlertCircle size={14} className="shrink-0" />
                  {t(transErr)}
                </div>
              )}

              {translation && (
                <div className="mt-4 rounded-xl bg-slate-50 p-5">
                  <div className="mb-2 flex items-center gap-2 text-xs text-slate-400">
                    <span className="font-medium">{translation.sourceLanguage?.toUpperCase()}</span>
                    <span>→</span>
                    <span className="font-medium">{translation.targetLanguage?.toUpperCase()}</span>
                    {translation.translationModel && (
                      <span className="ml-auto">{t("reports.translationModel", { name: translation.translationModel })}</span>
                    )}
                  </div>
                  <p className="text-sm leading-relaxed text-slate-700 whitespace-pre-wrap max-h-64 overflow-y-auto">
                    {translation.translatedText}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {!loading && !selectedDocId && (
          <div className="mt-10 flex flex-col items-center justify-center py-12 text-slate-400 gap-3">
            <FileBarChart2 size={40} className="text-slate-200" />
            <p className="text-sm">{t("reports.empty")}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Reports;
