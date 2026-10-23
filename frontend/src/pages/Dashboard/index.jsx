import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Upload,
  MessageSquare,
  GitCompareArrows,
  FileBarChart2,
  FileText,
  AlertCircle,
} from "lucide-react";
import Navbar from "../../components/Navbar";
import Button from "../../components/ui/Button";
import StatCard from "../../components/StatCard";
import EmptyState from "../../components/EmptyState";
import { useAuth } from "../../context/AuthContext";
import { getAllDocuments } from "../../api/documentApi";
import { extractErrorMessage } from "../../api/client";
import { useLanguage } from "../../i18n/LanguageContext";
import { getRiskBadgeClass, getRiskBandFromStatus } from "../../utils/risk";

// Title/description are translation keys: dashboard.qa.<id>.title / .desc
const QUICK_ACTIONS = [
  { icon: Upload,           id: "upload",  to: "/upload" },
  { icon: MessageSquare,    id: "ask",     to: "/qa" },
  { icon: GitCompareArrows, id: "compare", to: "/compare" },
  { icon: FileBarChart2,    id: "reports", to: "/reports" },
];

const STATUS_COLORS = {
  UPLOADED:    "text-blue-600 bg-blue-50",
  PROCESSING:  "text-purple-600 bg-purple-50",
  PROCESSED:   "text-green-600 bg-green-50",
  FAILED:      "text-red-600 bg-red-50",
};

function statusColor(status) {
  const riskClass = getRiskBadgeClass(getRiskBandFromStatus(status));
  if (riskClass) return riskClass;
  return STATUS_COLORS[String(status || "").toUpperCase()] || "text-slate-600 bg-slate-100";
}

function formatDate(dt, locale) {
  if (!dt) return "—";
  return new Date(dt).toLocaleDateString(locale, {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function Dashboard() {
  const { t, ts, locale } = useLanguage();
  const { userName } = useAuth();
  const navigate = useNavigate();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getAllDocuments()
      .then((docs) => setDocuments(docs || []))
      .catch((err) => setError(extractErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  const firstName = (userName || "").trim().split(/\s+/)[0] || "there";
  const recentDocs = documents.slice(0, 5);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="mx-auto max-w-7xl px-4 py-7 sm:px-6 sm:py-10">
        {/* Welcome banner */}
        <motion.section
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, ease: "easeOut" }}
          className="relative isolate flex flex-col gap-5 overflow-hidden rounded-3xl bg-gradient-to-br from-navy via-navy to-secondary px-5 py-7 shadow-xl shadow-navy/10 sm:px-8 sm:py-8 sm:flex-row sm:items-center sm:justify-between"
        >
          <div className="pointer-events-none absolute -right-12 -top-24 -z-10 h-64 w-64 rounded-full bg-royal/20 blur-3xl" />
          <div>
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-teal">
              {t("common.appName")}
            </p>
            <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
              {userName ? t("dashboard.welcomeName", { name: firstName }) : t("dashboard.welcome")}
            </h1>
            <p className="mt-2 text-sm text-slate-300 sm:text-base">
              {loading
                ? t("dashboard.loadingDocs")
                : t(documents.length === 1 ? "dashboard.docCount.one" : "dashboard.docCount.other", { n: documents.length })}
            </p>
          </div>
          <Button as={Link} to="/upload" variant="teal" className="shrink-0 !rounded-xl !px-5 !py-3 !text-sm">
            <Upload size={16} /> {t("dashboard.newUpload")}
          </Button>
        </motion.section>

        {/* Quick actions */}
        <section className="mt-7 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {QUICK_ACTIONS.map(({ icon, id, to }, index) => (
            <StatCard
              key={id}
              icon={icon}
              to={to}
              delay={index * 0.06}
              title={t(`dashboard.qa.${id}.title`)}
              description={t(`dashboard.qa.${id}.desc`)}
            />
          ))}
        </section>

        {/* Recent documents */}
        <section className="mt-7 rounded-3xl border border-slate-200/80 bg-white p-5 shadow-sm shadow-slate-900/[0.03] sm:p-7">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">{t("common.document")}</p>
              <h2 className="mt-1 text-lg font-semibold tracking-tight text-navy">{t("dashboard.recent")}</h2>
            </div>
            <Link
              to="/documents"
              className="rounded-lg px-3 py-2 text-sm font-semibold text-royal transition-colors hover:bg-royal/5 hover:underline"
            >
              {t("dashboard.viewAll")}
            </Link>
          </div>

          {loading && (
            <div className="mt-6 flex items-center justify-center py-8 text-slate-400 text-sm">
              {t("dashboard.loadingDocsShort")}
            </div>
          )}

          {!loading && error && (
            <div className="mt-4 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
              <AlertCircle size={16} className="shrink-0" />
              {t(error)}
            </div>
          )}

          {!loading && !error && documents.length === 0 && (
            <div className="mt-4">
              <EmptyState
                title={t("dashboard.empty.title")}
                description={t("dashboard.empty.desc")}
                action={
                  <Button variant="royal" onClick={() => navigate("/upload")}>
                    <Upload size={16} /> {t("dashboard.uploadBtn")}
                  </Button>
                }
              />
            </div>
          )}

          {!loading && !error && recentDocs.length > 0 && (
            <>
              <div className="mt-4 space-y-3 md:hidden">
                {recentDocs.map((doc) => (
                  <article
                    key={doc.id}
                    className="rounded-xl border border-slate-100 p-4 transition-colors hover:bg-slate-50"
                  >
                    <div className="flex min-w-0 items-start gap-3">
                      <FileText size={18} className="mt-0.5 shrink-0 text-royal" />
                      <div className="min-w-0 flex-1">
                        <p className="break-words text-sm font-semibold text-navy">
                          {doc.title || doc.fileName}
                        </p>
                        <p className="mt-0.5 break-all text-xs text-slate-400">{doc.fileName}</p>
                        <div className="mt-3 flex flex-wrap items-center justify-between gap-2">
                          <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${statusColor(doc.status)}`}>
                            {ts(doc.status)}
                          </span>
                          <span className="text-xs text-slate-500">{formatDate(doc.uploadedAt, locale)}</span>
                        </div>
                        <button
                          className="mt-3 min-h-10 text-sm font-semibold text-royal hover:underline"
                          onClick={() => navigate(`/analysis/${doc.id}`, { state: { fileName: doc.title || doc.fileName } })}
                        >
                          {t("dashboard.analyse")}
                        </button>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
              <div className="mt-4 hidden overflow-x-auto md:block">
              <table className="w-full min-w-[680px] border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/80 text-left text-[11px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    <th className="pb-2 pr-4 font-semibold">{t("dashboard.col.document")}</th>
                    <th className="pb-2 pr-4 font-semibold">{t("dashboard.col.status")}</th>
                    <th className="pb-2 pr-4 font-semibold">{t("dashboard.col.uploadedBy")}</th>
                    <th className="pb-2 font-semibold">{t("dashboard.col.date")}</th>
                    <th className="pb-2 font-semibold">{t("dashboard.col.actions")}</th>
                  </tr>
                </thead>
                <tbody>
                  {recentDocs.map((doc) => (
                    <tr
                      key={doc.id}
                      className="cursor-pointer border-b border-slate-100 transition-colors hover:bg-blue-50/40"
                      onClick={() =>
                        navigate(`/analysis/${doc.id}`, { state: { fileName: doc.title || doc.fileName } })
                      }
                    >
                      <td className="py-3 pr-4">
                        <div className="flex items-center gap-2">
                          <FileText size={16} className="shrink-0 text-royal" />
                          <div>
                            <p className="text-sm font-medium text-navy">
                              {doc.title || doc.fileName}
                            </p>
                            <p className="text-xs text-slate-400">{doc.fileName}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-3 pr-4">
                        <span
                          className={`rounded-full px-2.5 py-1 text-xs font-semibold ${statusColor(doc.status)}`}
                        >
                          {ts(doc.status)}
                        </span>
                      </td>
                      <td className="py-3 pr-4 text-sm text-slate-500">
                        {doc.uploadedBy || "—"}
                      </td>
                      <td className="py-3 text-sm text-slate-500">
                        {formatDate(doc.uploadedAt, locale)}
                      </td>
                      <td className="py-3">
                        <button
                          className="text-xs font-medium text-royal hover:underline"
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/analysis/${doc.id}`, { state: { fileName: doc.title || doc.fileName } });
                          }}
                        >
                          {t("dashboard.analyse")}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
