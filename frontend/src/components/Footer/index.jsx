import { Link } from "react-router-dom";
import { useLanguage } from "../../i18n/LanguageContext";

function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="bg-navy">
      <div className="mx-auto max-w-7xl px-6 py-12">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
          <div>
            <p className="text-base font-bold text-white">{t("common.appName")}</p>
            <p className="mt-3 max-w-sm text-sm text-slate-400">
              {t("footer.description")}
            </p>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              {t("footer.product")}
            </p>
            <ul className="mt-3 space-y-2 text-sm text-slate-400">
              <li><Link to="/documents" className="hover:text-white">{t("nav.documents")}</Link></li>
              <li><Link to="/dashboard" className="hover:text-white">{t("nav.dashboard")}</Link></li>
              <li><Link to="/qa" className="hover:text-white">{t("nav.qa")}</Link></li>
              <li><Link to="/compare" className="hover:text-white">{t("nav.compare")}</Link></li>
            </ul>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              {t("footer.languages")}
            </p>
            <ul className="mt-3 space-y-2 text-sm text-slate-400">
              <li>{t("footer.english")}</li>
              <li>{t("footer.hindi")}</li>
              <li>{t("footer.marathi")}</li>
            </ul>
          </div>
        </div>

        <div className="mt-10 border-t border-white/10 pt-6 text-xs text-slate-500">
          © {new Date().getFullYear()}. {t("footer.copyright")}
        </div>
      </div>
    </footer>
  );
}

export default Footer;
