import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import LanguageToggle from "../LanguageToggle";
import { useLanguage } from "../../i18n/LanguageContext";
import { useAuth } from "../../context/AuthContext";
import Button from "../ui/Button";

const MODULE_LINKS = [
  { key: "nav.dashboard", to: "/dashboard" },
  { key: "nav.documents", to: "/documents" },
  { key: "nav.upload", to: "/upload" },
  { key: "nav.processing", to: "/processing" },
  { key: "nav.analysis", to: "/analysis" },
  { key: "nav.compare", to: "/compare" },
  { key: "nav.qa", to: "/qa" },
  { key: "nav.reports", to: "/reports" },
  { key: "nav.profile", to: "/settings" },
];

function Navbar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { isLoggedIn, logout, userName } = useAuth();
  const { t } = useLanguage();
  const [menuOpen, setMenuOpen] = useState(false);
  const firstName = (userName || "").trim().split(/\s+/)[0] || t("common.user");

  function handleLogout() {
    logout();
    setMenuOpen(false);
    navigate("/login");
  }

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-navy/95 shadow-sm shadow-slate-950/10 backdrop-blur-xl">
      <div className="mx-auto flex h-[4.5rem] max-w-7xl items-center justify-between gap-2 px-3 sm:gap-4 sm:px-6">
        <Link to={isLoggedIn ? "/dashboard" : "/"} aria-label={t("common.appName")} className="flex shrink-0 items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-royal text-xs font-bold text-white shadow-md shadow-royal/25">
            AI
          </span>
          <span className="hidden text-base font-bold tracking-tight text-white sm:inline">{t("common.appName")}</span>
        </Link>

        {/* Right cluster */}
        <div className="flex items-center gap-1 shrink-0 sm:gap-2">
          <LanguageToggle className="bg-white" />

          {isLoggedIn ? (
            <div className="hidden items-center gap-2 2xl:flex">
              <span className="text-sm font-medium text-slate-200">
                {t("nav.greeting", { name: firstName })}
              </span>
              <button
                onClick={handleLogout}
                className="rounded-lg border border-white/15 bg-white/10 px-3 py-1.5 text-sm font-semibold text-white hover:bg-white/10"
                aria-label={t("nav.logout")}
                title={t("nav.logout")}
              >
                {t("nav.logout")}
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-1 sm:gap-2">
              <Button as={Link} to="/login" variant="ghost" className="!text-slate-200 !px-2 !py-2 !text-xs hover:!text-white sm:!px-3.5 sm:!text-sm">
                {t("nav.login")}
              </Button>
              <Button as={Link} to="/register" variant="teal" className="!px-2 !py-2 !text-xs sm:!px-3.5 sm:!text-sm">
                {t("nav.signup")}
              </Button>
            </div>
          )}

          <button
            type="button"
            className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 text-white transition-colors hover:border-white/20 hover:bg-white/10"
            aria-label={menuOpen ? t("nav.closeMenu") : t("nav.menu")}
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((open) => !open)}
            aria-controls="module-navigation"
          >
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      <AnimatePresence initial={false}>
      {menuOpen && (
        <motion.nav
          id="module-navigation"
          aria-label={t("nav.modules")}
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          transition={{ duration: 0.22, ease: "easeOut" }}
          className="overflow-hidden border-t border-white/10 bg-navy/98 px-4 py-5 sm:px-6"
        >
          <div className="mx-auto max-w-7xl">
            <p className="mb-3 px-1 text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">
              {t("nav.modules")}
            </p>
            <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {MODULE_LINKS.map((link, index) => {
              const active =
                pathname === link.to ||
                (link.to !== "/dashboard" && pathname.startsWith(`${link.to}/`));
              return (
                <motion.div
                  key={link.to}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.18, delay: index * 0.025 }}
                >
                  <Link
                    to={link.to}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-current={active ? "page" : undefined}
                    onClick={() => setMenuOpen(false)}
                    className={`block rounded-xl border px-3.5 py-3 text-sm font-medium transition-colors ${
                      active
                        ? "border-royal/40 bg-royal/15 text-white"
                        : "border-white/5 text-slate-300 hover:border-white/10 hover:bg-white/5 hover:text-white"
                    }`}
                  >
                    {t(link.key)}
                  </Link>
                </motion.div>
              );
            })}
            </div>
            {isLoggedIn && (
              <button
                type="button"
                onClick={handleLogout}
                className="mt-3 rounded-lg px-3.5 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-white/5 hover:text-white"
              >
                {t("nav.logout")}
              </button>
            )}
          </div>
        </motion.nav>
      )}
      </AnimatePresence>
    </header>
  );
}

export default Navbar;
