import { useState } from "react";
import { Link, useParams, useLocation, Navigate } from "react-router-dom";
import {
  ArrowLeft,
  AlertCircle,
  AlertTriangle,
  RefreshCw,
  ChevronLeft,
  ChevronRight,
  FileText
} from "lucide-react";
import Navbar from "../../components/Navbar";
import Button from "../../components/ui/Button";
import GaugeRing from "../../components/GaugeRing";
import useAnalysis from "./useAnalysis";
import { useLanguage } from "../../i18n/LanguageContext";
import { getRiskBand, getRiskColor } from "../../utils/risk";

const fairnessColor = (s) => (s == null ? "#94a3b8" : s < 40 ? "#EF4444" : s < 65 ? "#F59E0B" : "#22C55E");

function Status({ loading, error, children }) {
  const { t } = useLanguage();
  if (loading) {
    return (
      <div className="flex items-center gap-2 py-4 text-sm text-slate-400">
        <div className="h-4 w-4 animate-spin rounded-full border-2 border-royal border-t-transparent" />
        {t("common.running")}
      </div>
    );
  }
  if (error) {
    return (
      <div className="flex items-center gap-2 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-700">
        <AlertCircle size={14} className="shrink-0" /> {t(error)}
      </div>
    );
  }
  return children;
}

// idle / again are translation keys.
function RunButton({ busy, onClick, idle, again, done, disabled = false }) {
  const { t } = useLanguage();
  return (
    <Button variant="outline" className="!px-3 !py-1.5 !text-sm" onClick={onClick} disabled={busy || disabled}>
      {busy ? <><RefreshCw size={14} className="animate-spin" /> {t("common.running")}</> : t(done ? again : idle)}
    </Button>
  );
}

const Empty = ({ children }) => <p className="mt-4 text-sm italic text-slate-400">{children}</p>;

function SummaryView({ a }) {
  const { t } = useLanguage();
  return (
    <>
      <RunButton busy={a.summarizing} onClick={a.summarize} idle="common.generate" again="common.regenerate" done={!!a.summary} />
      <Status loading={a.summarizing} error={a.summaryErr}>
        {a.summary ? <p className="mt-4 text-sm leading-relaxed text-slate-600">{a.summary.summary}</p>
                   : <Empty>{t("section.summary.empty")}</Empty>}
      </Status>
    </>
  );
}

function ClausesView({ a }) {
  const { t, tx } = useLanguage();
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 6;

  const clauses = a.clauses || [];
  const totalClauses = clauses.length;
  const totalPages = Math.max(1, Math.ceil(totalClauses / pageSize));

  const validPage = Math.min(currentPage, totalPages);
  const startIndex = (validPage - 1) * pageSize;
  const endIndex = Math.min(startIndex + pageSize, totalClauses);
  const pagedClauses = clauses.slice(startIndex, endIndex);

  return (
    <>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <RunButton
          busy={a.classifying}
          onClick={() => {
            setCurrentPage(1);
            a.classify();
          }}
          idle="common.classify"
          again="common.reclassify"
          done={!!clauses.length}
        />
        {totalClauses > 0 && (
          <span className="text-xs font-medium text-slate-500">
            {tx("common.showingClauses", {
              start: startIndex + 1,
              end: endIndex,
              total: totalClauses,
            })}
          </span>
        )}
      </div>

      <Status loading={a.classifying} error={a.clausesErr}>
        {clauses.length ? (
          <div>
            <ul className="mt-4 divide-y divide-slate-100">
              {pagedClauses.map((c) => (
                <li key={c.id} className="py-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-navy">{c.clauseName}</span>
                    <span className="text-xs text-slate-400">
                      {c.confidence != null ? `${(c.confidence * 100).toFixed(0)}%` : "—"}
                    </span>
                  </div>
                  {c.clauseText && <p className="mt-1 text-xs text-slate-500">{c.clauseText}</p>}
                </li>
              ))}
            </ul>

            {totalPages > 1 && (
              <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 pt-4">
                <Button
                  variant="outline"
                  className="!px-3 !py-1.5 !text-xs"
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  disabled={validPage <= 1}
                >
                  <ChevronLeft size={14} /> {t("common.prevPage")}
                </Button>

                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                  {tx("common.pageOf", { page: validPage, total: totalPages })}
                </div>

                <Button
                  variant="outline"
                  className="!px-3 !py-1.5 !text-xs"
                  onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                  disabled={validPage >= totalPages}
                >
                  {t("common.nextPage")} <ChevronRight size={14} />
                </Button>
              </div>
            )}
          </div>
        ) : (
          <Empty>{t("section.clauses.empty")}</Empty>
        )}
      </Status>
    </>
  );
}

function RiskView({ a }) {
  const { t } = useLanguage();
  const { risk } = a;
  const levelKey = getRiskBand(risk?.riskScore);
  const levelLabel = levelKey ? t(`risk.level.${levelKey}`) : t("risk.level.default");
  return (
    <>
      <RunButton busy={a.analyzingR} onClick={a.runRisk} idle="common.runAnalysis" again="common.rerun" done={risk?.riskScore != null} />
      <Status loading={a.analyzingR} error={a.riskErr}>
        {risk?.riskScore != null ? (
          <div className="mt-6 grid gap-8 md:grid-cols-[180px_1fr]">
            <GaugeRing value={risk.riskScore} label={levelLabel} color={getRiskColor(risk.riskScore)} size={160} />
            <div>
              {risk.riskFactors?.length ? (
                <div className="space-y-4">
                  {risk.riskFactors.map((rf, i) => (
                    <div key={i}>
                      <div className="mb-1.5 flex justify-between text-sm">
                        <span className="font-medium text-navy">{rf.factor}</span>
                        <span className="text-slate-500">{rf.weight}</span>
                      </div>
                      <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                        <div className="h-full rounded-full bg-danger" style={{ width: `${Math.min(rf.weight, 100)}%` }} />
                      </div>
                      {rf.description && <p className="mt-1 text-xs text-slate-400">{rf.description}</p>}
                    </div>
                  ))}
                </div>
              ) : risk.explanation && <p className="text-sm text-slate-600">{risk.explanation}</p>}
            </div>
          </div>
        ) : <Empty>{t("section.risk.empty")}</Empty>}
      </Status>
    </>
  );
}

function FairnessView({ a }) {
  const { t } = useLanguage();
  const f = a.fairness;
  const score = f?.fairnessScore != null ? Math.round(f.fairnessScore) : null;
  return (
    <>
      <RunButton busy={a.analyzingF} onClick={a.runFairness} idle="common.runAnalysis" again="common.rerun" done={score != null} />
      <Status loading={a.analyzingF} error={a.fairnessErr}>
        {score != null ? (
          <div className="mt-6 grid gap-8 md:grid-cols-[180px_1fr]">
            <GaugeRing
              value={score}
              label={t(score < 40 ? "fairness.unfair" : score < 65 ? "fairness.fair" : "fairness.balanced")}
              color={fairnessColor(score)}
              size={160}
            />
            <div>
              <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
                {[
                  ["fairness.rightsA", f.rightsPartyA], ["fairness.rightsB", f.rightsPartyB],
                  ["fairness.obligationsA", f.obligationsPartyA], ["fairness.obligationsB", f.obligationsPartyB],
                  ["fairness.penaltiesA", f.penaltiesPartyA], ["fairness.penaltiesB", f.penaltiesPartyB],
                ].map(([labelKey, v]) => (
                  <div key={labelKey} className="rounded-xl bg-slate-50 p-4 text-center">
                    <p className="text-lg font-bold text-navy">{v ?? "—"}</p>
                    <p className="mt-1 text-xs text-slate-500">{t(labelKey)}</p>
                  </div>
                ))}
              </div>
              {f.explanation && <p className="mt-4 text-sm text-slate-600">{f.explanation}</p>}
            </div>
          </div>
        ) : <Empty>{t("section.fairness.empty")}</Empty>}
      </Status>
    </>
  );
}

function MissingView({ a }) {
  const { t, tx } = useLanguage();
  const m = a.missing;
  return (
    <>
      <div className="flex items-center gap-3">
        <label className="text-sm text-slate-500">{t("section.missing.label")}</label>
        <input
          type="number" min={1} value={a.docTypeId}
          onChange={(e) => a.setDocTypeId(e.target.value)}
          className="w-20 rounded-lg border border-slate-200 px-2 py-1.5 text-sm text-navy focus:outline-none focus:ring-2 focus:ring-royal/30"
        />
        <RunButton busy={a.detecting} onClick={a.detect} idle="common.detect" again="common.detectAgain" done={!!m} disabled={!(Number(a.docTypeId) >= 1)} />
      </div>
      <Status loading={a.detecting} error={a.missingErr}>
        {m ? (
          <div className="mt-4">
            <p className="text-sm text-slate-600">
              {tx("section.missing.result", {
                count: <span className="font-semibold text-danger">{m.missingCount}</span>,
                total: m.totalMandatoryClauses,
                type: <span className="font-medium text-navy">{m.documentType}</span>,
              })}
            </p>
            <ul className="mt-3 space-y-1">
              {m.missingClauses?.map((name, i) => (
                <li key={i} className="flex items-center gap-2 text-sm text-slate-600">
                  <AlertTriangle size={14} className="shrink-0 text-amber" /> {name}
                </li>
              ))}
            </ul>
          </div>
        ) : <Empty>{t("section.missing.empty")}</Empty>}
      </Status>
    </>
  );
}

const VIEWS = { summary: SummaryView, clauses: ClausesView, risk: RiskView, fairness: FairnessView, missing: MissingView };
const TITLE_KEYS = {
  summary: "analysis.summary.title",
  clauses: "analysis.clauses.title",
  risk: "analysis.risk.title",
  fairness: "analysis.fairness.title",
  missing: "section.missing.title",
};

const SECTION_ORDER = [
  { slug: "summary", titleKey: "analysis.summary.title" },
  { slug: "clauses", titleKey: "analysis.clauses.title" },
  { slug: "risk", titleKey: "analysis.risk.title" },
  { slug: "fairness", titleKey: "analysis.fairness.title" },
  { slug: "missing", titleKey: "section.missing.title" },
];

export default function Section() {
  const { t } = useLanguage();
  const { documentId, section } = useParams();
  const { state } = useLocation();
  const a = useAnalysis(documentId);
  const View = VIEWS[section];

  if (!View) return <Navigate to={`/analysis/${documentId}`} replace />;

  const fileName = a.doc?.title || a.doc?.fileName || state?.fileName || t("common.document");

  const currentIdx = SECTION_ORDER.findIndex((s) => s.slug === section);
  const prevSectionObj = currentIdx > 0 ? SECTION_ORDER[currentIdx - 1] : null;
  const nextSectionObj = currentIdx < SECTION_ORDER.length - 1 ? SECTION_ORDER[currentIdx + 1] : null;

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="mx-auto max-w-5xl px-4 py-6 sm:px-6 sm:py-8">
        <Link
          to={`/analysis/${documentId}`}
          state={{ fileName }}
          className="inline-flex items-center gap-1.5 text-sm font-medium text-royal hover:underline"
        >
          <ArrowLeft size={14} /> {t("common.backToAnalysis")}
        </Link>
        <h1 className="mt-3 break-words text-2xl font-bold text-navy">{t(TITLE_KEYS[section])}</h1>
        <p className="mt-1 text-sm text-slate-500">{fileName}</p>

        <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
          <View a={a} />

          {/* Workflow Stepper: Previous / Next Section navigation */}
          <div className="mt-8 flex flex-wrap items-center justify-between gap-4 border-t border-slate-200 pt-5">
            {prevSectionObj ? (
              <Link
                to={`/analysis/${documentId}/${prevSectionObj.slug}`}
                state={{ fileName }}
                className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-navy shadow-sm transition hover:bg-slate-50"
              >
                <ChevronLeft size={16} />
                <span>{t(prevSectionObj.titleKey)}</span>
              </Link>
            ) : (
              <Link
                to={`/analysis/${documentId}`}
                state={{ fileName }}
                className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-600 shadow-sm transition hover:bg-slate-50"
              >
                <ArrowLeft size={16} />
                <span>{t("common.backToAnalysis")}</span>
              </Link>
            )}

            {nextSectionObj ? (
              <Link
                to={`/analysis/${documentId}/${nextSectionObj.slug}`}
                state={{ fileName }}
                className="inline-flex items-center gap-2 rounded-xl bg-royal px-4 py-2 text-sm font-semibold text-white shadow transition hover:bg-royal/90"
              >
                <span>{t(nextSectionObj.titleKey)}</span>
                <ChevronRight size={16} />
              </Link>
            ) : (
              <Link
                to="/reports"
                state={{ documentId, fileName }}
                className="inline-flex items-center gap-2 rounded-xl bg-teal px-4 py-2 text-sm font-semibold text-white shadow transition hover:bg-teal/90"
              >
                <FileText size={16} />
                <span>{t("common.finishToReport")}</span>
                <ChevronRight size={16} />
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
