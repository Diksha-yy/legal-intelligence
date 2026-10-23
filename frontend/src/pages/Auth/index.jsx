import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FileText, ListChecks, LockKeyhole, Mail, Scale, UserRound } from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import LanguageToggle from "../../components/LanguageToggle";
import { login as apiLogin } from "../../api/authApi";
import { register as apiRegister } from "../../api/userApi";
import { extractErrorMessage } from "../../api/client";
import Button from "../../components/ui/Button";
import Input from "../../components/ui/Input";
import { useLanguage } from "../../i18n/LanguageContext";

function Auth() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const { t } = useLanguage();

  const isLogin = location.pathname !== "/register";

  function navigateAfterLogin() {
    const from = location.state?.from;
    const requestedPath = new URLSearchParams(location.search).get("returnTo");
    let safeRequestedPath = "";
    if (requestedPath) {
      try {
        const requestedUrl = new URL(requestedPath, window.location.origin);
        if (
          requestedUrl.origin === window.location.origin &&
          !["/login", "/register"].includes(requestedUrl.pathname)
        ) {
          safeRequestedPath = `${requestedUrl.pathname}${requestedUrl.search}${requestedUrl.hash}`;
        }
      } catch {
        safeRequestedPath = "";
      }
    }
    const destination = from?.pathname && !["/login", "/register"].includes(from.pathname)
      ? `${from.pathname}${from.search || ""}${from.hash || ""}`
      : safeRequestedPath || "/dashboard";
    navigate(destination, { replace: true });
  }

  function handleChange(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
    setError("");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (loading) return;
    setError("");
    setLoading(true);

    try {
      if (isLogin) {
        // POST /api/auth/login
        const data = await apiLogin({ email: form.email, password: form.password });
        // data = { message, token }
        if (!data?.token) {
          throw new Error(t("auth.missingToken"));
        }
        const userObj = { email: form.email };
        login(data.token, userObj);
        navigateAfterLogin();
      } else {
        // POST /api/users/register  — role CLIENT is the default for end users
        await apiRegister({
          name: form.name,
          email: form.email,
          password: form.password,
          role: "CLIENT",
        });
        // After registration, auto-login
        const data = await apiLogin({ email: form.email, password: form.password });
        if (!data?.token) {
          throw new Error(t("auth.missingToken"));
        }
        const userObj = { name: form.name, email: form.email };
        login(data.token, userObj);
        navigateAfterLogin();
      }
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 md:flex">
      <aside className="relative hidden min-h-screen overflow-hidden bg-navy px-10 py-12 text-white md:flex md:w-[44%] md:flex-col md:justify-center lg:px-16">
        <div className="pointer-events-none absolute -right-40 -top-32 h-[34rem] w-[34rem] rounded-full border border-white/10" />
        <div className="pointer-events-none absolute -right-20 -top-12 h-[26rem] w-[26rem] rounded-full border border-white/10" />
        <div className="pointer-events-none absolute -bottom-32 -left-32 h-96 w-96 rounded-full bg-royal/20 blur-3xl" />

        <Link to="/" className="absolute left-10 top-12 z-10 inline-flex w-fit items-center gap-3 lg:left-16">
          <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-royal text-sm font-bold shadow-lg shadow-royal/30">
            AI
          </span>
          <span className="text-lg font-bold tracking-tight">{t("common.appName")}</span>
        </Link>

        <div className="relative mx-auto w-full max-w-lg py-12">
          <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border border-teal/30 bg-teal/10 text-teal">
            <Scale size={22} aria-hidden="true" />
          </div>
          <h1 className="max-w-lg text-4xl font-bold leading-tight tracking-tight lg:text-5xl">
            {t("auth.heroTitle")}
          </h1>
          <p className="mt-5 max-w-md text-base leading-7 text-slate-300">
            {t("auth.heroDescription")}
          </p>

          <div className="mt-10 rounded-2xl border border-white/10 bg-white/[0.07] p-5 shadow-2xl shadow-black/20 backdrop-blur-sm">
            <div className="flex items-center gap-3 border-b border-white/10 pb-4">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-royal/20 text-blue-200">
                <FileText size={19} aria-hidden="true" />
              </span>
              <div className="h-2.5 w-32 rounded-full bg-white/70" />
              <div className="ml-auto h-2.5 w-12 rounded-full bg-white/20" />
            </div>
            <div className="mt-5 grid grid-cols-[1fr_auto] gap-4">
              <div className="space-y-3 pt-1">
                <div className="h-2 w-full rounded-full bg-white/20" />
                <div className="h-2 w-11/12 rounded-full bg-white/20" />
                <div className="h-2 w-4/5 rounded-full bg-white/20" />
                <div className="mt-5 h-2 w-full rounded-full bg-white/10" />
                <div className="h-2 w-3/4 rounded-full bg-white/10" />
              </div>
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-xs text-slate-200">
                  <ListChecks size={15} className="text-teal" aria-hidden="true" />
                  {t("analysis.clauses.title")}
                </div>
                <div className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-xs text-slate-200">
                  <Scale size={15} className="text-blue-300" aria-hidden="true" />
                  {t("analysis.fairness.title")}
                </div>
              </div>
            </div>
          </div>
        </div>

      </aside>

      <main className="relative flex min-h-screen w-full flex-col justify-center px-5 py-20 sm:px-10 md:w-[56%] md:px-8 lg:px-14">
        <div className="absolute right-5 top-5 sm:right-8 sm:top-8">
          <LanguageToggle className="bg-white" />
        </div>

        <Link to="/" className="mx-auto mb-7 inline-flex items-center gap-2.5 md:hidden">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-royal text-xs font-bold text-white shadow-md shadow-royal/20">
            AI
          </span>
          <span className="text-base font-bold tracking-tight text-navy">{t("common.appName")}</span>
        </Link>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: "easeOut" }}
          className="mx-auto w-full max-w-md rounded-3xl border border-slate-200/80 bg-white p-6 shadow-xl shadow-slate-900/[0.06] sm:p-9"
        >
          <div className="mb-7">
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-royal">
              {t("common.appName")}
            </p>
            <h2 className="text-2xl font-bold tracking-tight text-navy sm:text-3xl">
            {isLogin ? t("auth.loginTitle") : t("auth.registerTitle")}
            </h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">
            {isLogin
              ? t("auth.loginDescription")
              : t("auth.registerDescription")}
            </p>
          </div>

          {error && (
            <div role="alert" className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {t(error)}
            </div>
          )}

          <form className="space-y-5" onSubmit={handleSubmit}>
            {!isLogin && (
              <div>
                <label htmlFor="auth-name" className="mb-2 block text-sm font-semibold text-slate-700">
                  {t("auth.fullName")}
                </label>
                <div className="relative">
                  <UserRound size={17} aria-hidden="true" className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                  <Input
                    id="auth-name"
                    name="name"
                    type="text"
                    autoComplete="name"
                    placeholder={t("auth.namePlaceholder")}
                    value={form.name}
                    onChange={handleChange}
                    required
                    className="rounded-xl border-slate-200 py-3.5 pl-11 shadow-sm shadow-slate-900/[0.02] transition focus:border-royal focus:ring-4 focus:ring-royal/10"
                  />
                </div>
              </div>
            )}

            <div>
              <label htmlFor="auth-email" className="mb-2 block text-sm font-semibold text-slate-700">
                {t("auth.email")}
              </label>
              <div className="relative">
                <Mail size={17} aria-hidden="true" className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                <Input
                  id="auth-email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder={t("auth.emailPlaceholder")}
                  value={form.email}
                  onChange={handleChange}
                  required
                  className="rounded-xl border-slate-200 py-3.5 pl-11 shadow-sm shadow-slate-900/[0.02] transition focus:border-royal focus:ring-4 focus:ring-royal/10"
                />
              </div>
            </div>

            <div>
              <div className="mb-1.5 flex items-center justify-between">
                <label htmlFor="auth-password" className="block text-sm font-semibold text-slate-700">
                  {t("auth.password")}
                </label>
              </div>
              <div className="relative">
                <LockKeyhole size={17} aria-hidden="true" className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                <Input
                  id="auth-password"
                  name="password"
                  type="password"
                  autoComplete={isLogin ? "current-password" : "new-password"}
                  placeholder="••••••••••"
                  value={form.password}
                  onChange={handleChange}
                  required
                  minLength={8}
                  className="rounded-xl border-slate-200 py-3.5 pl-11 shadow-sm shadow-slate-900/[0.02] transition focus:border-royal focus:ring-4 focus:ring-royal/10"
                />
              </div>
            </div>

            <Button
              type="submit"
              variant="royal"
              className="mt-2 w-full !rounded-xl !py-3.5 !text-sm !shadow-md !shadow-royal/20"
              disabled={loading}
            >
              {loading
                ? isLogin ? t("auth.loginLoading") : t("auth.registerLoading")
                : isLogin ? t("auth.loginSubmit") : t("auth.registerSubmit")}
            </Button>
          </form>

          <p className="mt-7 border-t border-slate-100 pt-6 text-center text-sm text-slate-500">
            {isLogin ? t("auth.newHere") : t("auth.existingAccount")}{" "}
            <button
              type="button"
              onClick={() => {
                navigate(isLogin ? "/register" : "/login", {
                  state: location.state,
                  replace: true,
                });
                setError("");
              }}
              className="font-semibold text-royal hover:underline"
            >
              {isLogin ? t("auth.createAccount") : t("auth.signIn")}
            </button>
          </p>
        </motion.div>
      </main>
    </div>
  );
}

export default Auth;
