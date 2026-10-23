import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { CheckCircle2, ShieldCheck, FileText, AlertCircle } from "lucide-react";
import Navbar from "../../components/Navbar";
import FileUpload from "../../components/FileUpload";
import Badge from "../../components/Badge";
import Button from "../../components/ui/Button";
import { uploadDocument, getAllDocuments } from "../../api/documentApi";
import { extractErrorMessage } from "../../api/client";
import { useLanguage } from "../../i18n/LanguageContext";

const GUIDELINES = ["size", "quality", "single", "ocr"];
const FORMATS = ["pdf", "jpg", "png", "scanned"];
const MAX_FILE_SIZE = 20 * 1024 * 1024;

function statusVariant(status) {
  if (!status) return "default";
  if (status.includes("HIGH") || status === "FAILED") return "high";
  if (status.includes("MEDIUM")) return "medium";
  if (status.includes("LOW"))    return "low";
  return "default";
}

function Upload() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const { t, ts } = useLanguage();
  const isDocumentsPage = pathname === "/documents";
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [recentUploads, setRecentUploads] = useState([]);
  const [loadingRecent, setLoadingRecent] = useState(true);
  const [recentError, setRecentError] = useState("");
  const [titleInput, setTitleInput] = useState("");

  // Load recent uploads
  useEffect(() => {
    getAllDocuments()
      .then((docs) => setRecentUploads(isDocumentsPage ? docs || [] : (docs || []).slice(0, 5)))
      .catch((err) => setRecentError(extractErrorMessage(err)))
      .finally(() => setLoadingRecent(false));
  }, [isDocumentsPage]);

  async function handleFileSelected(file) {
    if (uploading) return;
    const extension = file.name.split(".").pop()?.toLowerCase();
    const acceptedExtension = ["pdf", "jpg", "jpeg", "png"].includes(extension);
    if (!acceptedExtension) {
      setUploadError(t("upload.chooseSupported"));
      return;
    }
    if (file.size > MAX_FILE_SIZE) {
      setUploadError(t("upload.maxSize"));
      return;
    }
    const title = titleInput.trim() || file.name.replace(/\.[^.]+$/, "");
    setUploadError("");
    setUploading(true);

    try {
      const doc = await uploadDocument(file, title);
      if (doc?.id == null) {
        throw new Error(t("upload.invalidResponse"));
      }
      // Navigate to processing with the real document ID
      const query = new URLSearchParams({
        documentId: String(doc.id),
        fileName: doc.title || doc.fileName || file.name,
      });
      navigate(`/processing?${query}`, {
        state: { documentId: doc.id, fileName: doc.title || doc.fileName },
      });
    } catch (err) {
      setUploadError(extractErrorMessage(err));
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">
        <h1 className="text-2xl font-bold text-navy">
          {isDocumentsPage ? t("upload.allDocuments") : t("upload.title")}
        </h1>
        {isDocumentsPage && (
          <Button variant="royal" className="mt-4" onClick={() => navigate("/upload")}>
            {t("dashboard.newUpload")}
          </Button>
        )}
        {!isDocumentsPage && <p className="mt-1 text-slate-500">{t("upload.subtitle")}</p>}

        {!isDocumentsPage && (
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Dropzone + title + formats */}
          <div className="lg:col-span-2 space-y-4">
            {/* Optional title */}
            <div>
              <label className="mb-1.5 block text-sm font-medium text-navy">
                {t("upload.documentTitle")} <span className="text-slate-400 font-normal">{t("upload.optional")}</span>
              </label>
              <input
                type="text"
                value={titleInput}
                onChange={(e) => setTitleInput(e.target.value)}
                placeholder={t("upload.titlePlaceholder")}
                className="w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm text-navy placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-royal/30"
              />
            </div>

            {uploading ? (
              <div className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-royal/30 bg-royal/5 px-6 py-16 text-center">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-royal border-t-transparent" />
                <p className="mt-4 text-sm font-medium text-navy">
                  {t("upload.uploading")}
                </p>
              </div>
            ) : (
              <FileUpload onFileSelected={handleFileSelected} />
            )}

            {uploadError && (
              <div className="flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
                <AlertCircle size={16} className="shrink-0" />
                {t(uploadError)}
              </div>
            )}

            <div className="flex flex-wrap gap-2">
              {FORMATS.map((format) => (
                <span
                  key={format}
                  className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600"
                >
                  {t(`upload.${format}`)}
                </span>
              ))}
            </div>
          </div>

          {/* Right rail */}
          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="font-semibold text-navy">{t("upload.guidelines")}</h2>
              <ul className="mt-4 space-y-3">
                {GUIDELINES.map((guideline) => (
                  <li key={guideline} className="flex items-start gap-2 text-sm text-slate-600">
                    <CheckCircle2 size={16} className="mt-0.5 shrink-0 text-brandgreen" />
                    {t(`upload.guideline.${guideline}`)}
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-2xl bg-navy p-6 text-white">
              <div className="flex items-center gap-2">
                <ShieldCheck size={16} className="text-teal" />
                <h2 className="font-semibold">{t("upload.privateTitle")}</h2>
              </div>
              <p className="mt-2 text-sm text-slate-300">
                {t("upload.privateDescription")}
              </p>
            </div>
          </div>
        </div>
        )}

        {/* Recent uploads */}
        <div className="mt-8">
          <h2 className="font-semibold text-navy">
            {isDocumentsPage ? t("upload.allDocuments") : t("upload.recent")}
          </h2>
          {loadingRecent && (
            <p className="mt-3 text-sm text-slate-400">{t("upload.loadingRecent")}</p>
          )}
          {!loadingRecent && recentError && (
            <div className="mt-3 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
              <AlertCircle size={16} className="shrink-0" />
              {t(recentError)}
            </div>
          )}
          {!loadingRecent && !recentError && recentUploads.length === 0 && (
            <p className="mt-3 text-sm text-slate-400">
              {t("upload.noDocuments")}
            </p>
          )}
          <div className="mt-4 space-y-3">
            {recentUploads.map((doc) => (
              <button
                key={doc.id}
                type="button"
                onClick={() => navigate(`/analysis/${doc.id}`, { state: { fileName: doc.title || doc.fileName } })}
                aria-label={`${t("upload.openAnalysis")}: ${doc.title || doc.fileName}`}
                className="flex w-full min-w-0 items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-royal/30 hover:shadow-md"
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-royal/10 text-royal">
                    <FileText size={16} />
                  </span>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-navy">
                      {doc.title || doc.fileName}
                    </p>
                    <p className="break-all text-xs text-slate-400">{doc.fileName}</p>
                  </div>
                </div>
                <Badge variant={statusVariant(doc.status)}>
                  {ts(doc.status || "UPLOADED")}
                </Badge>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Upload;
