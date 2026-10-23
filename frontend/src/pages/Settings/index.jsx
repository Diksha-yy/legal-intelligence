import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";
import Button from "../../components/ui/Button";
import { useLanguage } from "../../i18n/LanguageContext";

function Settings() {
  const { user, userName, logout } = useAuth();
  const navigate = useNavigate();
  const { t } = useLanguage();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="mx-auto max-w-2xl px-4 py-6 sm:px-6 sm:py-8">
        <h1 className="text-2xl font-bold text-navy">{t("settings.title")}</h1>
        <p className="mt-1 text-sm text-slate-500">{t("settings.description")}</p>

        <div className="mt-6 space-y-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{t("settings.displayName")}</p>
            <p className="mt-1 break-words text-sm font-semibold text-navy">{userName || "—"}</p>
          </div>
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{t("settings.email")}</p>
            <p className="mt-1 break-words text-sm text-navy">{user?.email || "—"}</p>
          </div>
        </div>

        <div className="mt-6">
          <Button variant="outline" onClick={handleLogout}>
            {t("settings.logout")}
          </Button>
        </div>
      </div>
    </div>
  );
}

export default Settings;
