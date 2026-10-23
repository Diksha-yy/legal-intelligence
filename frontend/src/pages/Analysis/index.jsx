import { Link, Navigate, useLocation, useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Download, FileText, AlertTriangle, AlertCircle, ShieldAlert, Scale, ScrollText, ListChecks, ChevronRight,
} from "lucide-react";
import Navbar from "../../components/Navbar";
import Button from "../../components/ui/Button";
import useAnalysis from "./useAnalysis";
import { useLanguage } from "../../i18n/LanguageContext";
import { getRiskTextClass } from "../../utils/risk";

const MotionLink = motion.create(Link);

// Each tile below opens its own page: /analysis/:documentId/<slug>
// Titles and blurbs come from translations: analysis.<slug>.title / .blurb
const SECTIONS = [
  { slug: "summary",  icon: ScrollText },
  { slug: "clauses",  icon: ListChecks },
  { slug: "risk",     icon: ShieldAlert },
  { slug: "fairness", icon: Scale },
  { slug: "missing",  icon: AlertTriangle },
];

function Analysis() {
  const { t, tx, ts, locale } = useLanguage();
  const { documentId } = useParams();
  const { state } = useLocation();
  const navigate = useNavigate();
  const a = useAnalysis(documentId);

  // Legacy entry point: /analysis with router state (or from the navbar).
  if (!documentId) {
    if (state?.documentId) {
      return <Navigate to={`/analysis/${state.documentId}`} state={state} replace />;
    }
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="mx-auto max-w-7xl px-4 py-10 text-center sm:px-6 sm:py-12">
          <AlertCircle size={40} className="mx-auto text-slate-300" />
          <p className="mt-4 text-slate-500">
            {tx("analysis.noDoc", {
              link: (
                <button className="font-medium text-royal hover:underline" onClick={() => navigate("/dashboard")}>
                  {t("analysis.dashboard")}
                </button>
              ),
            })}
          </p>
        </div>
      </div>
    );
  }

  const fileName = a.doc?.title || a.doc?.fileName || state?.fileName || t("common.document");
  const fairScore = a.fairness?.fairnessScore != null ? Math.round(a.fairness.fairnessScore) : null;

  // Short preview shown on each tile
  const preview = {
    summary:  a.summary ? t("analysis.preview.ready") : t("analysis.preview.notGenerated"),
    clauses:  a.clauses ? t("analysis.preview.clauses", { n: a.clauses.length }) : "—",
    risk:     a.risk?.riskScore != null ? `${a.risk.riskScore}/100` : t("common.notRun"),
    fairness: fairScore != null ? `${fairScore}/100` : t("common.notRun"),
    missing:  a.missing ? t("analysis.preview.missing", { n: a.missing.missingCount }) : t("common.notRun"),
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="min-w-0">
            <h1 className="break-words text-2xl font-bold text-navy">{t("analysis.heading", { fileName })}</h1>
            <p className="mt-1 text-sm text-slate-500">
              {a.doc
                ? t("analysis.uploaded", {
                    date: new Date(a.doc.uploadedAt).toLocaleDateString(locale),
                    status: ts(a.doc.status),
                  })
                : a.docErr || t("analysis.loadingInfo")}
            </p>
          </div>
          <Button variant="outline" className="self-start sm:self-auto" onClick={() => navigate("/reports", { state: { documentId, fileName } })}>
            <Download size={16} /> {t("common.export")}
          </Button>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {SECTIONS.map(({ slug, icon: Icon }, index) => (
            <MotionLink
              key={slug}
              to={`/analysis/${documentId}/${slug}`}
              state={{ fileName }}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              whileHover={{ y: -4 }}
              whileTap={{ scale: 0.99 }}
              transition={{ duration: 0.22, delay: index * 0.04, ease: "easeOut" }}
              className="group flex min-w-0 items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-[border-color,box-shadow] hover:border-royal/20 hover:shadow-lg sm:p-6"
            >
              <div className="min-w-0">
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-royal/10 text-royal">
                  <Icon size={18} />
                </span>
                <h3 className="mt-4 font-semibold text-navy">{t(`analysis.${slug}.title`)}</h3>
                <p className="mt-1 text-sm text-slate-500">{t(`analysis.${slug}.blurb`)}</p>
                <p className={`mt-3 text-sm font-semibold ${slug === "risk" && a.risk?.riskScore != null ? getRiskTextClass(a.risk.riskScore) : "text-royal"}`}>
                  {preview[slug]}
                </p>
              </div>
              <ChevronRight size={20} className="text-slate-300 transition-colors group-hover:text-royal" />
            </MotionLink>
          ))}

          <MotionLink
            to="/reports"
            state={{ documentId, fileName }}
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            whileHover={{ y: -4 }}
            whileTap={{ scale: 0.99 }}
            transition={{ duration: 0.22, delay: SECTIONS.length * 0.04, ease: "easeOut" }}
            className="group flex min-w-0 items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-[border-color,box-shadow] hover:border-teal/20 hover:shadow-lg sm:p-6"
          >
            <div className="min-w-0">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal/10 text-teal">
                <FileText size={18} />
              </span>
              <h3 className="mt-4 font-semibold text-navy">{t("analysis.fullReport")}</h3>
              <p className="mt-1 text-sm text-slate-500">{t("analysis.fullReport.blurb")}</p>
            </div>
            <ChevronRight size={20} className="text-slate-300 transition-colors group-hover:text-teal" />
          </MotionLink>
        </div>
      </div>
    </div>
  );
}

export default Analysis;
