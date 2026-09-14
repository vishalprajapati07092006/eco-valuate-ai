import React from "react";
import { Zap, ShieldCheck, Github, Globe, CheckCircle2 } from "lucide-react";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-slate-800/80 bg-slate-950/90 mt-16 py-8 relative z-10">
      <div className="max-w-7xl mx-auto px-6 space-y-6">
        {/* Top Header Row */}
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 pb-6 border-b border-slate-800/60">
          {/* Brand Identity */}
          <div className="flex items-center gap-3">
            <div className="p-1.5 bg-emerald-500/10 rounded-lg border border-emerald-500/20 text-emerald-400">
              <Zap className="w-4 h-4 fill-emerald-400/20" />
            </div>
            <div>
              <span className="font-extrabold text-white text-sm tracking-wide block">
                ECO-VALUATE <span className="text-emerald-400">AI</span>
              </span>
              <p className="text-[11px] text-slate-500 font-mono">
                Enterprise E-Waste Valuation & Material Intelligence Platform
              </p>
            </div>
            <span className="ml-2 px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-[10px] text-emerald-400 font-mono font-semibold">
              v1.0.0
            </span>
          </div>

          {/* Infrastructure Metrics */}
          <div className="flex flex-wrap items-center justify-center gap-3 text-[11px]">
            <span className="flex items-center gap-2 bg-slate-900/80 px-3 py-1 rounded-full border border-slate-800 text-slate-400">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-60" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
              </span>
              99.9% API Uptime
            </span>

            <span className="flex items-center gap-1.5 bg-slate-900/80 px-3 py-1 rounded-full border border-slate-800 text-slate-400 font-mono">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              ISO 14001 Compliant
            </span>
          </div>
        </div>

        {/* Legal & Industry Copyright Row */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
          <p className="text-center sm:text-left">
            © {currentYear} Eco-Valuate AI Technologies Inc. All rights reserved.
          </p>

          <div className="flex items-center gap-4 text-[11px]">
            <a
              href="#privacy"
              className="hover:text-slate-300 transition-colors"
            >
              Privacy Policy
            </a>
            <span className="w-1 h-1 rounded-full bg-slate-800" />
            <a
              href="#terms"
              className="hover:text-slate-300 transition-colors"
            >
              Terms of Service
            </a>
            <span className="w-1 h-1 rounded-full bg-slate-800" />
            <a
              href="#security"
              className="flex items-center gap-1 hover:text-slate-300 transition-colors"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /> Security
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}