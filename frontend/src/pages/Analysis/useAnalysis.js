import { useEffect, useState, useCallback } from "react";
import { getDocumentById } from "../../api/documentApi";
import { getClausesByDocument, classifyClauses } from "../../api/clauseApi";
import { getSummary, generateSummary } from "../../api/summaryApi";
import { getRiskScore, analyzeRisk } from "../../api/riskApi";
import { getFairnessScore, analyzeFairness } from "../../api/fairnessApi";
import { detectMissingClauses } from "../../api/missingClauseApi";
import { extractErrorMessage } from "../../api/client";

// Shared by the Analysis hub and every section page. Each page mounts this
// hook, so the data is re-fetched from the backend when the route changes.
export default function useAnalysis(documentId) {
  const [doc, setDoc] = useState(null);
  const [docErr, setDocErr] = useState("");

  const [clauses, setClauses] = useState(null);
  const [clausesErr, setClausesErr] = useState("");
  const [classifying, setClassifying] = useState(false);

  const [summary, setSummary] = useState(null);
  const [summaryErr, setSummaryErr] = useState("");
  const [summarizing, setSummarizing] = useState(false);

  const [risk, setRisk] = useState(null);
  const [riskErr, setRiskErr] = useState("");
  const [analyzingR, setAnalyzingR] = useState(false);

  const [fairness, setFairness] = useState(null);
  const [fairnessErr, setFairnessErr] = useState("");
  const [analyzingF, setAnalyzingF] = useState(false);

  const [missing, setMissing] = useState(null);
  const [missingErr, setMissingErr] = useState("");
  const [detecting, setDetecting] = useState(false);
  const [docTypeId, setDocTypeId] = useState(""); // chosen by the user; no assumed default
  const [loadedDocumentId, setLoadedDocumentId] = useState(null);

  useEffect(() => {
    if (!documentId) return;
    let cancelled = false;

    async function load() {
      const results = await Promise.allSettled([
        getDocumentById(documentId),
        getClausesByDocument(documentId),
        getSummary(documentId),
        getRiskScore(documentId),
        getFairnessScore(documentId),
      ]);
      if (cancelled) return;

      const [docResult, clausesResult, summaryResult, riskResult, fairnessResult] = results;
      setDoc(docResult.status === "fulfilled" ? docResult.value : null);
      setDocErr(docResult.status === "rejected" ? extractErrorMessage(docResult.reason) : "");
      setClauses(clausesResult.status === "fulfilled" ? clausesResult.value || [] : []);
      setClausesErr(
        clausesResult.status === "rejected" && clausesResult.reason.response?.status !== 404
          ? extractErrorMessage(clausesResult.reason)
          : ""
      );
      setSummary(summaryResult.status === "fulfilled" ? summaryResult.value : null);
      setSummaryErr(
        summaryResult.status === "rejected" && summaryResult.reason.response?.status !== 404
          ? extractErrorMessage(summaryResult.reason)
          : ""
      );
      setRisk(riskResult.status === "fulfilled" ? riskResult.value : null);
      setRiskErr(
        riskResult.status === "rejected" && riskResult.reason.response?.status !== 404
          ? extractErrorMessage(riskResult.reason)
          : ""
      );
      setFairness(fairnessResult.status === "fulfilled" ? fairnessResult.value : null);
      setFairnessErr(
        fairnessResult.status === "rejected" && fairnessResult.reason.response?.status !== 404
          ? extractErrorMessage(fairnessResult.reason)
          : ""
      );
      setMissing(null);
      setMissingErr("");
      setDocTypeId("");
      setLoadedDocumentId(documentId);
    }

    load();

    return () => { cancelled = true; };
  }, [documentId]);

  const run = useCallback(async (fn, setData, setErr, setBusy) => {
    setBusy(true);
    setErr("");
    try {
      setData(await fn());
    } catch (e) {
      setErr(extractErrorMessage(e));
    } finally {
      setBusy(false);
    }
  }, []);

  const dataIsCurrent = loadedDocumentId === documentId;

  return {
    doc: dataIsCurrent ? doc : null,
    docErr: dataIsCurrent ? docErr : "",
    clauses: dataIsCurrent ? clauses : null,
    clausesErr: dataIsCurrent ? clausesErr : "",
    classifying,
    classify: () => run(async () => (await classifyClauses(documentId)) || [], setClauses, setClausesErr, setClassifying),
    summary: dataIsCurrent ? summary : null,
    summaryErr: dataIsCurrent ? summaryErr : "",
    summarizing,
    summarize: () => run(() => generateSummary(documentId), setSummary, setSummaryErr, setSummarizing),
    risk: dataIsCurrent ? risk : null,
    riskErr: dataIsCurrent ? riskErr : "",
    analyzingR,
    runRisk: () => run(() => analyzeRisk(documentId), setRisk, setRiskErr, setAnalyzingR),
    fairness: dataIsCurrent ? fairness : null,
    fairnessErr: dataIsCurrent ? fairnessErr : "",
    analyzingF,
    runFairness: () => run(() => analyzeFairness(documentId), setFairness, setFairnessErr, setAnalyzingF),
    missing: dataIsCurrent ? missing : null,
    missingErr: dataIsCurrent ? missingErr : "",
    detecting,
    docTypeId: dataIsCurrent ? docTypeId : "",
    setDocTypeId,
    detect: () => run(() => detectMissingClauses(documentId, Number(docTypeId)), setMissing, setMissingErr, setDetecting),
  };
}
