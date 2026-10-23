import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Upload,
  MessageSquare,
  ShieldCheck,
  TrendingUp,
  Scale as ScaleIcon,
  AlertTriangle,
  GitCompareArrows,
  ArrowUpRight,
} from "lucide-react";

import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import Button from "../../components/ui/Button";
import { useLanguage } from "../../i18n/LanguageContext";

const FEATURES = [
  {
    icon: ShieldCheck,
    titleKey: "home.feature.1.title",
    descKey: "home.feature.1.desc",
    to: "/analysis",
  },
  {
    icon: TrendingUp,
    titleKey: "home.feature.2.title",
    descKey: "home.feature.2.desc",
    to: "/analysis",
  },
  {
    icon: ScaleIcon,
    titleKey: "home.feature.3.title",
    descKey: "home.feature.3.desc",
    to: "/analysis",
  },
  {
    icon: AlertTriangle,
    titleKey: "home.feature.4.title",
    descKey: "home.feature.4.desc",
    to: "/analysis",
  },
  {
    icon: MessageSquare,
    titleKey: "home.feature.5.title",
    descKey: "home.feature.5.desc",
    to: "/qa",
  },
  {
    icon: GitCompareArrows,
    titleKey: "home.feature.6.title",
    descKey: "home.feature.6.desc",
    to: "/compare",
  },
];

function Landing() {
  const { t } = useLanguage();
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* HERO */}
      <section className="relative isolate overflow-hidden bg-navy">
        <div className="pointer-events-none absolute -right-32 -top-36 h-[34rem] w-[34rem] rounded-full bg-royal/20 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-56 left-1/3 h-[30rem] w-[30rem] rounded-full bg-teal/10 blur-3xl" />
        <div className="pointer-events-none absolute inset-0 opacity-[0.07] [background-image:radial-gradient(#fff_1px,transparent_1px)] [background-size:24px_24px]" />
        <div className="pointer-events-none absolute inset-x-0 bottom-0 h-28 bg-gradient-to-b from-transparent to-background" />

        <div className="relative mx-auto grid max-w-7xl grid-cols-1 items-center gap-12 px-4 py-16 sm:px-6 sm:py-20 lg:grid-cols-[1.1fr_0.9fr] lg:gap-16 lg:py-24">
          {/* LEFT */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            <span className="inline-flex items-center gap-2 rounded-full border border-teal/30 bg-teal/10 px-4 py-1.5 text-xs font-semibold tracking-wide text-teal shadow-sm shadow-teal/10 sm:text-sm">
              <span className="h-1.5 w-1.5 rounded-full bg-teal" />
              {t("home.eyebrow")}
            </span>

            <h1 className="mt-6 max-w-2xl text-balance text-4xl font-bold leading-[1.08] tracking-tight text-white sm:text-6xl">
              {t("home.title")}
            </h1>

            <p className="mt-6 max-w-xl text-base leading-7 text-slate-300 sm:text-lg sm:leading-8">
              {t("home.subtitle")}
            </p>

            <div className="mt-9 flex flex-wrap gap-3">
              <Button as={Link} to="/upload" variant="teal" className="!px-4 !py-3 text-sm sm:!px-6 sm:!py-3.5 sm:text-base">
                <Upload size={18} /> {t("home.upload")}
              </Button>
              <Button as={Link} to="/qa" variant="translucent" className="!px-4 !py-3 text-sm sm:!px-6 sm:!py-3.5 sm:text-base">
                <MessageSquare size={18} /> {t("home.ask")}
              </Button>
              <Button as={Link} to="/register" variant="outlineDark" className="!px-4 !py-3 text-sm sm:!px-6 sm:!py-3.5 sm:text-base">
                {t("home.learnMore")}
              </Button>
            </div>
          </motion.div>

          {/* RIGHT — citizen-centered legal document and AI illustration */}
          <motion.div
            className="flex min-w-0 justify-center lg:justify-end"
            initial={{ opacity: 0, y: 24, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.6, ease: "easeOut", delay: 0.15 }}
          >
            <img
              src="/legal-assistant-hero.svg"
              alt={t("home.illustrationAlt")}
              width="640"
              height="560"
              fetchPriority="high"
              className="h-auto w-full max-w-[34rem] drop-shadow-2xl"
            />
          </motion.div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-20">
        <div className="text-center">
          <span className="text-xs font-semibold uppercase tracking-[0.18em] text-royal">{t("home.eyebrow")}</span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-navy sm:text-4xl">
            {t("home.featuresTitle")}
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-base leading-7 text-slate-500 sm:text-lg">
            {t("home.featuresSubtitle")}
          </p>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map(({ icon: Icon, titleKey, descKey, to }, i) => (
            <motion.div
              key={titleKey}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.4, delay: i * 0.05, ease: "easeOut" }}
              whileHover={{ y: -4 }}
              className="h-full"
            >
              <Link
                to={to}
                className="group block h-full rounded-2xl border border-slate-200/80 bg-white p-7 shadow-sm shadow-slate-900/[0.02] transition-all hover:border-royal/25 hover:shadow-xl hover:shadow-royal/10 focus-visible:outline-royal"
              >
                <div className="flex items-start justify-between">
                  <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-royal/10 text-royal transition-all duration-200 group-hover:rotate-[-4deg] group-hover:bg-royal group-hover:text-white">
                    <Icon size={20} />
                  </span>
                  <ArrowUpRight size={18} aria-hidden="true" className="text-slate-300 transition-all group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-royal" />
                </div>
                <h3 className="mt-5 text-lg font-semibold tracking-tight text-navy">{t(titleKey)}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-500">{t(descKey)}</p>
              </Link>
            </motion.div>
          ))}
        </div>
      </section>

      <Footer />
    </div>
  );
}

export default Landing;
