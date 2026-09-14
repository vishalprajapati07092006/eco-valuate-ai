import React from "react";
import { motion } from "framer-motion";
import {
  Cpu,
  Zap,
  Leaf,
  Shield,
  Activity,
  Compass,
  Recycle,
  Globe,
  BatteryCharging,
  Layers,
  Sparkles,
} from "lucide-react";

export default function FloatingBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden bg-[#040806]">
      {/* 1. Deep Background Lighting Glows */}
      <div className="absolute top-1/4 -left-20 w-96 h-96 bg-emerald-500/10 rounded-full blur-[140px]" />
      <div className="absolute top-1/2 right-10 w-80 h-80 bg-teal-500/10 rounded-full blur-[130px]" />
      <div className="absolute bottom-10 left-1/3 w-96 h-96 bg-emerald-600/5 rounded-full blur-[160px]" />

      {/* 2. Micro Floating Tech & Eco Nodes */}
      {/* Top Left - Layers Icon */}
      <motion.div
        animate={{ y: [0, -15, 0], rotate: [-5, 5, -5] }}
        transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-20 left-10 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-2xl backdrop-blur-md shadow-lg shadow-emerald-500/10 text-emerald-400"
      >
        <Layers className="w-5 h-5" />
      </motion.div>

      {/* Top Right - Energy Lightning Badge */}
      <motion.div
        animate={{ y: [0, -12, 0] }}
        transition={{ duration: 5.5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-24 right-20 p-3 bg-slate-900/60 border border-slate-800 rounded-2xl text-emerald-400 backdrop-blur-sm shadow-md"
      >
        <Zap className="w-5 h-5 fill-emerald-400/20" />
      </motion.div>

      {/* Middle Left - Micro CPU */}
      <motion.div
        animate={{ y: [0, 14, 0], rotate: [0, 15, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-1/3 left-16 p-2.5 bg-slate-900/60 border border-slate-800 rounded-xl text-emerald-400/90 shadow-md"
      >
        <Cpu className="w-4 h-4" />
      </motion.div>

      {/* Middle Right - Activity Graph */}
      <motion.div
        animate={{ y: [0, -16, 0] }}
        transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-1/2 right-12 p-3 bg-slate-900/60 border border-slate-800 rounded-2xl text-teal-400 backdrop-blur-sm shadow-md"
      >
        <Activity className="w-4 h-4" />
      </motion.div>

      {/* Center Top - Rotating Recycle Icon */}
      <motion.div
        animate={{
          y: [0, 10, 0],
          rotate: [0, 360],
        }}
        transition={{
          y: { duration: 6, repeat: Infinity, ease: "easeInOut" },
          rotate: { duration: 25, repeat: Infinity, ease: "linear" },
        }}
        className="absolute top-16 left-1/2 p-2.5 bg-emerald-950/30 border border-emerald-500/20 rounded-full text-emerald-400/80"
      >
        <Recycle className="w-4 h-4" />
      </motion.div>

      {/* Lower Left - Battery / Charging */}
      <motion.div
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 6.5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute bottom-1/3 left-12 p-2.5 bg-slate-900/60 border border-slate-800 rounded-xl text-cyan-400"
      >
        <BatteryCharging className="w-4 h-4" />
      </motion.div>

      {/* Lower Right - Security Shield */}
      <motion.div
        animate={{ y: [0, 12, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        className="absolute bottom-1/3 right-1/4 p-2.5 bg-slate-900/60 border border-slate-800 rounded-xl text-emerald-400"
      >
        <Shield className="w-4 h-4" />
      </motion.div>

      {/* Bottom Right - Compass Node */}
      <motion.div
        animate={{ y: [0, 18, 0], rotate: [5, -5, 5] }}
        transition={{ duration: 8.5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute bottom-28 right-16 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-2xl backdrop-blur-md shadow-lg shadow-emerald-500/10 text-emerald-400"
      >
        <Compass className="w-5 h-5" />
      </motion.div>

      {/* 3. Micro Floating Leaves */}
      <motion.div
        animate={{ y: [0, -10, 0], rotate: [20, 40, 20] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-1/3 left-1/3 text-emerald-400/40"
      >
        <Leaf className="w-5 h-5" />
      </motion.div>

      <motion.div
        animate={{ y: [0, 12, 0], rotate: [-15, -35, -15] }}
        transition={{ duration: 6.5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute bottom-1/4 right-1/3 text-emerald-500/30"
      >
        <Leaf className="w-4 h-4" />
      </motion.div>

      <motion.div
        animate={{ y: [0, -8, 0], rotate: [0, 20, 0] }}
        transition={{ duration: 5.8, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-2/3 left-1/4 text-teal-400/30"
      >
        <Leaf className="w-3.5 h-3.5" />
      </motion.div>

      {/* 4. Glowing Ambient Particles & Orbs */}
      <div className="absolute top-1/4 right-1/3 w-2 h-2 rounded-full bg-emerald-400/80 blur-[0.5px] animate-pulse" />
      <div className="absolute top-3/4 left-1/3 w-2.5 h-2.5 rounded-full bg-emerald-500/50 blur-[1px]" />
      <div className="absolute bottom-16 right-1/3 w-1.5 h-1.5 rounded-full bg-cyan-400/70 blur-[0.5px] animate-pulse" />
      <div className="absolute top-28 left-2/3 w-1.5 h-1.5 rounded-full bg-teal-300/60" />
      <div className="absolute bottom-1/2 right-20 w-2 h-2 rounded-full bg-emerald-400/60 blur-[1px]" />
    </div>
  );
}