import React from "react";
import FloatingBackground from "./FloatingBackground";
import {
  Sparkles,
  ArrowRight,
  MapPin,
  Cpu,
  BarChart3,
  Recycle,
} from "lucide-react";

export default function LandingPage({ onStartScan, onExploreMap }) {
  return (
    <div className="relative min-h-screen text-white overflow-hidden">
      {/* 1. Animated Floating Background */}
      <FloatingBackground />

      {/* 2. Main Page Content Layer */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-8 space-y-16">
        {/* Hero Section */}
        <section className="text-center max-w-4xl mx-auto space-y-6 pt-4">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold uppercase tracking-widest">
            <Sparkles className="w-4 h-4" /> Circular Economy Engine
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-black text-white tracking-tight leading-tight">
            Turn Hazardous E-Waste into <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400">
              Valuable Recoverable Yields
            </span>
          </h1>

          <p className="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
            Instantly classify electronic waste, estimate gold and copper yield,
            compute market values, and locate certified local processing hubs
            using automated computer vision.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
            <button
              onClick={onStartScan}
              className="w-full sm:w-auto px-8 py-3.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold rounded-xl transition-all shadow-lg hover:shadow-emerald-500/20 flex items-center justify-center gap-2 text-sm cursor-pointer"
            >
              Launch AI Scanner <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={onExploreMap}
              className="w-full sm:w-auto px-8 py-3.5 bg-slate-900/80 hover:bg-slate-800 text-slate-200 border border-slate-800 font-bold rounded-xl transition-all flex items-center justify-center gap-2 text-sm cursor-pointer"
            >
              Find Drop-off Hubs <MapPin className="w-4 h-4 text-emerald-400" />
            </button>
          </div>
        </section>

        {/* Global Impact Counter */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-5xl mx-auto">
          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-5 rounded-2xl text-center transition-all duration-300 hover:border-emerald-400/60 hover:shadow-[0_0_25px_rgba(16,185,129,0.35)] hover:-translate-y-0.5">
            <span className="text-2xl sm:text-3xl font-black font-mono text-emerald-400 block">
              99.7%
            </span>
            <span className="text-[11px] text-slate-400 font-medium mt-1 block">
              AI Accuracy Rate
            </span>
          </div>

          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-5 rounded-2xl text-center transition-all duration-300 hover:border-emerald-400/60 hover:shadow-[0_0_25px_rgba(16,185,129,0.35)] hover:-translate-y-0.5">
            <span className="text-2xl sm:text-3xl font-black font-mono text-amber-400 block">
              50M+
            </span>
            <span className="text-[11px] text-slate-400 font-medium mt-1 block">
              Tons Global E-Waste
            </span>
          </div>

          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-5 rounded-2xl text-center transition-all duration-300 hover:border-emerald-400/60 hover:shadow-[0_0_25px_rgba(16,185,129,0.35)] hover:-translate-y-0.5">
            <span className="text-2xl sm:text-3xl font-black font-mono text-teal-400 block">
              $57B
            </span>
            <span className="text-[11px] text-slate-400 font-medium mt-1 block">
              Annual Material Waste
            </span>
          </div>

          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 p-5 rounded-2xl text-center transition-all duration-300 hover:border-emerald-400/60 hover:shadow-[0_0_25px_rgba(16,185,129,0.35)] hover:-translate-y-0.5">
            <span className="text-2xl sm:text-3xl font-black font-mono text-cyan-400 block">
              100%
            </span>
            <span className="text-[11px] text-slate-400 font-medium mt-1 block">
              Traceable Drop-offs
            </span>
          </div>
        </section>

        {/* 3-Step Process */}
        <section className="max-w-5xl mx-auto space-y-8">
          <div className="text-center space-y-1">
            <h2 className="text-xl sm:text-2xl font-bold text-white">
              How ECO-VALUATE Works
            </h2>
            <p className="text-xs text-slate-400">
              Automated end-to-end e-waste lifecycle processing
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 p-6 rounded-2xl space-y-3 transition-all duration-300 hover:border-emerald-400/60 hover:shadow-[0_0_30px_rgba(16,185,129,0.35)] hover:-translate-y-1">
              <div className="w-9 h-9 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-extrabold text-xs">
                01
              </div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Cpu className="w-4 h-4 text-emerald-400" /> Upload Image
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Drop a photo of discarded hardware or components along with
                estimated item mass.
              </p>
            </div>

            <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 p-6 rounded-2xl space-y-3 transition-all duration-300 hover:border-emerald-400/60 hover:shadow-[0_0_30px_rgba(16,185,129,0.35)] hover:-translate-y-1">
              <div className="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 font-extrabold text-xs">
                02
              </div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-amber-400" /> AI Valuation
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Computer vision models analyze material breakdown, precious
                metals (Gold/Copper), and hazards.
              </p>
            </div>

            <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 p-6 rounded-2xl space-y-3 transition-all duration-300 hover:border-emerald-400/60 hover:shadow-[0_0_30px_rgba(16,185,129,0.35)] hover:-translate-y-1">
              <div className="w-9 h-9 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-extrabold text-xs">
                03
              </div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Recycle className="w-4 h-4 text-cyan-400" /> Certified Route
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Locate verified local processing hubs with real-time distance
                matrix calculations and turn-by-turn routes.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}