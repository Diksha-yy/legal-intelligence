import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import { Send, Trash2, AlertCircle, MessageSquare } from "lucide-react";
import Navbar from "../../components/Navbar";
import { getAllDocuments } from "../../api/documentApi";
import { askQuestion, getQaHistory, deleteQaRecord, clearQaHistory } from "../../api/qaApi";
import { extractErrorMessage } from "../../api/client";
import { useLanguage } from "../../i18n/LanguageContext";

function formatTime(dt, locale) {
  if (!dt) return "";
  return new Date(dt).toLocaleTimeString(locale, { hour: "2-digit", minute: "2-digit" });
}

function Chat() {
  const { state } = useLocation();
  const { t, locale } = useLanguage();

  const [documents, setDocuments]     = useState([]);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [selectedDocId, setSelectedDocId] = useState(state?.documentId || "");
  const [history, setHistory]         = useState([]);
  const [question, setQuestion]       = useState("");
  const [sending, setSending]         = useState(false);
  const [error, setError]             = useState("");
  const [documentsError, setDocumentsError] = useState("");
  const [loadingHistory, setLoadingHistory] = useState(false);
  const bottomRef = useRef(null);

  // Load documents for selector
  useEffect(() => {
    getAllDocuments()
      .then((docs) => setDocuments(docs || []))
      .catch((err) => setDocumentsError(extractErrorMessage(err)))
      .finally(() => setLoadingDocuments(false));
  }, []);

  // Load history when document changes
  useEffect(() => {
    let cancelled = false;

    async function load() {
      if (!selectedDocId) {
        setHistory([]);
        return;
      }
      setLoadingHistory(true);
      setError("");
      try {
        const h = await getQaHistory(Number(selectedDocId));
        if (!cancelled) setHistory((h || []).reverse());
      } catch (err) {
        if (!cancelled) {
          setHistory([]);
          setError(extractErrorMessage(err));
        }
      } finally {
        if (!cancelled) setLoadingHistory(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [selectedDocId]);

  // Scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  async function handleSend(e) {
    e.preventDefault();
    if (!question.trim() || sending || !selectedDocId) return;
    setSending(true);
    setError("");

    try {
      const response = await askQuestion(Number(selectedDocId), question.trim());
      setHistory((prev) => [...prev, response]);
      setQuestion("");
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setSending(false);
    }
  }

  async function handleDeleteRecord(queryId) {
    try {
      await deleteQaRecord(queryId);
      setHistory((prev) => prev.filter((h) => h.id !== queryId));
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  }

  async function handleClearHistory() {
    if (!selectedDocId) return;
    try {
      await clearQaHistory(Number(selectedDocId));
      setHistory([]);
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />

      <div className="mx-auto flex w-full max-w-4xl flex-1 flex-col px-4 py-6 sm:px-6 sm:py-8">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="min-w-0">
            <h1 className="text-2xl font-bold text-navy">{t("chat.title")}</h1>
            <p className="mt-1 text-sm text-slate-500">
              {t("chat.description")}
            </p>
          </div>
          {history.length > 0 && (
            <button
              className="flex min-h-10 shrink-0 items-center justify-center gap-1.5 self-start rounded-lg border border-red-200 px-3 py-1.5 text-xs font-semibold text-red-600 hover:bg-red-50 sm:self-auto"
              onClick={handleClearHistory}
            >
              <Trash2 size={12} /> {t("chat.clearHistory")}
            </button>
          )}
        </div>

        {/* Document selector */}
        <div className="mt-5">
          <label className="mb-1.5 block text-sm font-medium text-navy">
            {t("chat.selectDocument")}
          </label>
          <select
            value={selectedDocId}
            onChange={(e) => setSelectedDocId(e.target.value)}
            disabled={loadingDocuments || documents.length === 0}
            className="w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm text-navy bg-white focus:outline-none focus:ring-2 focus:ring-royal/30"
          >
            <option value="">{t("chat.chooseDocument")}</option>
            {documents.map((doc) => (
              <option key={doc.id} value={doc.id}>
                {doc.title || doc.fileName}
              </option>
            ))}
          </select>
          {documentsError && (
            <p className="mt-2 text-sm text-red-600">            {t(documentsError)}</p>
          )}
          {loadingDocuments && (
            <p className="mt-2 text-sm text-slate-500">{t("chat.loadingDocuments")}</p>
          )}
          {!loadingDocuments && !documentsError && documents.length === 0 && (
            <p className="mt-2 text-sm text-slate-500">{t("chat.noDocuments")}</p>
          )}
        </div>

        {/* Chat window */}
        <div className="mt-5 flex min-h-[min(55vh,400px)] flex-1 flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
          <div className="flex-1 space-y-6 overflow-y-auto p-4 sm:p-6">
            {!selectedDocId && (
              <div className="flex flex-col items-center justify-center h-full text-slate-400 gap-3 py-10">
                <MessageSquare size={36} className="text-slate-200" />
                <p className="text-sm">{t("chat.selectToAsk")}</p>
              </div>
            )}

            {selectedDocId && loadingHistory && (
              <div className="flex items-center gap-2 text-sm text-slate-400">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-royal border-t-transparent" />
                {t("chat.loadingHistory")}
              </div>
            )}

            {selectedDocId && !loadingHistory && history.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-slate-400 gap-3 py-10">
                <MessageSquare size={36} className="text-slate-200" />
                <p className="text-sm">{t("chat.noQuestions")}</p>
              </div>
            )}

            {history.map((record) => (
              <div key={record.id} className="space-y-2">
                {/* Question bubble */}
                <div className="flex justify-end">
                  <div className="max-w-[90%] break-words rounded-2xl rounded-tr-sm bg-royal px-4 py-3 sm:max-w-[70%]">
                    <p className="text-sm text-white">{record.question}</p>
                    <p className="mt-1 text-right text-[10px] text-royal/50 text-white/60">
                      {formatTime(record.createdAt, locale)}
                    </p>
                  </div>
                </div>

                {/* Answer bubble */}
                <div className="flex justify-start gap-3">
                  <div className="max-w-[90%] break-words rounded-2xl rounded-tl-sm border border-slate-200 bg-slate-50 px-4 py-3 sm:max-w-[80%]">
                    <p className="text-sm text-navy leading-relaxed whitespace-pre-wrap">
                      {record.answer}
                    </p>
                    {record.confidenceScore != null && (
                      <p className="mt-2 text-xs text-slate-400">
                        {t("chat.confidence", { score: (record.confidenceScore * 100).toFixed(0) })}
                        {record.llmModel ? ` · ${record.llmModel}` : ""}
                      </p>
                    )}
                    {record.retrievedClauses && record.retrievedClauses.length > 0 && (
                      <details className="mt-2">
                        <summary className="text-xs font-medium text-royal cursor-pointer">
                          {t(record.retrievedClauses.length === 1 ? "chat.source.one" : "chat.source.other", { count: record.retrievedClauses.length })}
                        </summary>
                        <ul className="mt-2 space-y-1">
                          {record.retrievedClauses.map((c, i) => (
                            <li key={i} className="text-xs text-slate-500 pl-2 border-l-2 border-royal/20">
                              {c.clauseText || c.clauseNumber}
                            </li>
                          ))}
                        </ul>
                      </details>
                    )}
                  </div>
                  <button
                    className="mt-1 self-start text-slate-300 hover:text-red-400 transition-colors"
                    onClick={() => handleDeleteRecord(record.id)}
                    title={t("chat.delete")}
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
              </div>
            ))}

            <div ref={bottomRef} />
          </div>

          {/* Error banner */}
          {error && (
            <div className="mx-4 mb-2 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-sm text-red-700">
              <AlertCircle size={14} className="shrink-0" />
              {t(error)}
            </div>
          )}

          {/* Input */}
          <form
            onSubmit={handleSend}
            className="flex items-center gap-2 border-t border-slate-200 px-3 py-3 sm:gap-3 sm:px-4"
          >
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={selectedDocId ? t("chat.askPlaceholder") : t("chat.selectPlaceholder")}
              disabled={!selectedDocId || sending}
              className="min-w-0 flex-1 rounded-xl border border-slate-200 px-3 py-2.5 text-sm text-navy placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-royal/30 disabled:bg-slate-50 sm:px-4"
              maxLength={2000}
            />
            <button
              type="submit"
              disabled={!question.trim() || sending || !selectedDocId}
              className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-royal text-white hover:bg-royal/90 disabled:opacity-40 transition-opacity"
            >
              {sending ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              ) : (
                <Send size={16} />
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Chat;
