import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useLanguage } from "../i18n/LanguageContext";

import Landing from "../pages/Landing";
import Auth from "../pages/Auth";
import Dashboard from "../pages/Dashboard";
import Upload from "../pages/Upload";
import Processing from "../pages/Processing";
import Analysis from "../pages/Analysis";
import AnalysisSection from "../pages/Analysis/Section";
import Compare from "../pages/Compare";
import Chat from "../pages/Chat";
import Reports from "../pages/Reports";
import Settings from "../pages/Settings";
import ProtectedRoute from "./ProtectedRoute";
import { LanguageProvider } from "../i18n/LanguageContext";

function PageNotFound() {
  const { t } = useLanguage();
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto flex max-w-3xl flex-col items-center px-6 py-24 text-center">
        <h1 className="text-3xl font-bold text-navy">{t("common.pageNotFound")}</h1>
        <p className="mt-3 text-slate-500">{t("common.pageNotFoundDescription")}</p>
        <Link to="/" className="mt-6 rounded-xl bg-royal px-5 py-3 text-sm font-semibold text-white hover:bg-royal/90">
          {t("common.goHome")}
        </Link>
      </main>
    </div>
  );
}

function AppRoutes() {
  return (
    <LanguageProvider>
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Auth />} />
        <Route path="/register" element={<Auth />} />

        {/* Protected routes — require JWT authentication */}
        <Route
          path="/dashboard"
          element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
        />
        <Route
          path="/upload"
          element={<ProtectedRoute><Upload /></ProtectedRoute>}
        />
        <Route
          path="/documents"
          element={<ProtectedRoute><Upload /></ProtectedRoute>}
        />
        <Route
          path="/processing"
          element={<ProtectedRoute><Processing /></ProtectedRoute>}
        />
        <Route
          path="/analysis"
          element={<ProtectedRoute><Analysis /></ProtectedRoute>}
        />
        <Route
          path="/analysis/:documentId"
          element={<ProtectedRoute><Analysis /></ProtectedRoute>}
        />
        <Route
          path="/analysis/:documentId/:section"
          element={<ProtectedRoute><AnalysisSection /></ProtectedRoute>}
        />
        <Route
          path="/compare"
          element={<ProtectedRoute><Compare /></ProtectedRoute>}
        />
        <Route
          path="/qa"
          element={<ProtectedRoute><Chat /></ProtectedRoute>}
        />
        <Route
          path="/reports"
          element={<ProtectedRoute><Reports /></ProtectedRoute>}
        />
        <Route
          path="/settings"
          element={<ProtectedRoute><Settings /></ProtectedRoute>}
        />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </BrowserRouter>
    </LanguageProvider>
  );
}

export default AppRoutes;
