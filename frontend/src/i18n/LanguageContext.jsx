/* eslint-disable react-refresh/only-export-components */

import { createContext, useCallback, useContext, useEffect, useMemo, useState, Fragment } from "react";
import { translations } from "./translations";

const STORAGE_KEY = "lang";
const SUPPORTED = ["en", "hi", "mr"];

const LanguageContext = createContext(null);

function readInitialLang() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (SUPPORTED.includes(saved)) return saved;
  } catch { /* storage unavailable */ }
  return "en";
}

function fill(str, vars = {}) {
  return str.replace(/\{(\w+)\}/g, (m, k) => (vars[k] != null ? String(vars[k]) : m));
}

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(readInitialLang);

  const setLang = useCallback((next) => {
    if (SUPPORTED.includes(next)) setLangState(next);
  }, []);
  const toggleLang = useCallback(
    () => setLangState((current) => SUPPORTED[(SUPPORTED.indexOf(current) + 1) % SUPPORTED.length]),
    []
  );

  // Persist, and tell the browser the page language (fonts, screen readers, translate prompts).
  useEffect(() => {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch { /* ignore */ }
    document.documentElement.lang = lang;
    document.title = translations[lang]["common.appName"];
  }, [lang]);

  const value = useMemo(() => {
    const dict = translations[lang];
    const raw = (key) => dict[key] ?? translations.en[key] ?? key;

    // t("key", { n: 3 }) → string. Unknown keys return the key itself,
    // so backend-supplied text passes through unchanged.
    const t = (key, vars) => fill(raw(key), vars);

    // ts("HIGH_RISK") → translated status label; unknown statuses show as-is (underscores → spaces).
    const ts = (status) => {
      const label = String(status || "UPLOADED").replace(/_/g, " ");
      const key = `status.${label}`;
      return dict[key] ?? translations.en[key] ?? label;
    };

    // tx("key", { count: <b>3</b> }) → array of nodes, for sentences that embed JSX.
    const tx = (key, vars = {}) =>
      raw(key).split(/(\{\w+\})/).map((part, i) => {
        const m = part.match(/^\{(\w+)\}$/);
        return <Fragment key={i}>{m && vars[m[1]] != null ? vars[m[1]] : part}</Fragment>;
      });

    return {
      lang, setLang, toggleLang, t, tx, ts,
      locale: { en: "en-IN", hi: "hi-IN", mr: "mr-IN" }[lang],
    };
  }, [lang, setLang, toggleLang]);

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLanguage must be used inside <LanguageProvider>");
  return ctx;
}
