import { useLanguage } from "../i18n/LanguageContext";

export default function LanguageToggle({ className = "" }) {
  const { lang, setLang, t } = useLanguage();
  const languages = [
    { code: "en", name: "English" },
    { code: "hi", name: "हिन्दी" },
    { code: "mr", name: "मराठी" },
  ];

  return (
    <label className="inline-flex items-center">
      <span className="sr-only">{t("lang.switchTo")}</span>
      <select
        value={lang}
        onChange={(event) => setLang(event.target.value)}
        aria-label={t("lang.switchTo")}
        className={`min-h-9 rounded-lg border border-slate-200 px-2.5 text-sm font-medium text-navy outline-none transition-colors focus:ring-2 focus:ring-royal/30 ${className}`}
      >
        {languages.map(({ code, name }) => (
          <option key={code} value={code}>{name}</option>
        ))}
      </select>
    </label>
  );
}
