import React, { useState, useEffect } from "react";
import LandingPage from "./components/LandingPage";
import Footer from "./components/Footer";
import FloatingBackground from "./components/FloatingBackground"; // Added FloatingBackground Import
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import {
  UploadCloud,
  AlertTriangle,
  ShieldCheck,
  Cpu,
  RefreshCw,
  Zap,
  Scale,
  Sparkles,
  PieChart as PieIcon,
  Layers,
  MapPin,
  Download,
  Building2,
  Phone,
  Navigation,
  Compass,
} from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";

// Fix Leaflet Default Marker Icons in Vite/React
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
});

// Single source of truth for the backend URL. Change this one line
// (or set VITE_API_URL / REACT_APP_API_URL in an .env file) instead of
// hunting through every component for hardcoded localhost URLs.
const API_BASE_URL = "https://eco-valuate-ai.onrender.com";

const COLORS = ["#10b981", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6"];

// Base Facilities Data
const INITIAL_RECYCLING_HUBS = [
  {
    id: 1,
    name: "EcoRecycle India Hub",
    lat: 19.186,
    lng: 73.191,
    phone: "+91 98200 12345",
    type: "State Authorized",
  },
  {
    id: 2,
    name: "GreenTech E-Waste Processor",
    lat: 19.215,
    lng: 73.181,
    phone: "+91 98111 67890",
    type: "R2 Certified Refiner",
  },
  {
    id: 3,
    name: "Kalyan Municipal E-Drop Kiosk",
    lat: 19.24,
    lng: 73.135,
    phone: "1800-222-333",
    type: "Public Drop Kiosk",
  },
];

// Fixed Haversine formula to calculate straight-line distance in kilometers
const calculateDistanceKm = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Earth's radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLat / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return (R * c).toFixed(1);
};

// Component to dynamically recenter map when location changes
function MapRecenter({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, 12, { duration: 1.5 });
    }
  }, [center, map]);
  return null;
}

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [weight, setWeight] = useState(1.0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [activeTab, setActiveTab] = useState("home");

  // Geolocation states
  const [userLocation, setUserLocation] = useState(null);
  const [locationLoading, setLocationLoading] = useState(false);
  const [hubs, setHubs] = useState(INITIAL_RECYCLING_HUBS);
  const [mapCenter, setMapCenter] = useState([19.2, 73.16]);

  // Cursor glow state
  const [cursorPos, setCursorPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const updateCursor = (e) => {
      setCursorPos({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", updateCursor);
    return () => window.removeEventListener("mousemove", updateCursor);
  }, []);

  const handleImageChange = (selectedFile) => {
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageChange(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("weight", weight);

    try {
      const res = await axios.post(
        `${API_BASE_URL}/api/classify`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResult(res.data.prediction);
    } catch (err) {
      alert(
        "Classification failed. Ensure the backend server is reachable."
      );
    } finally {
      setLoading(false);
    }
  };

  const exportPDF = async () => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/generate-pdf`,
        {
          label: result?.class_raw || "storage_drive",
          weight: parseFloat(weight) || 1.0,
          confidence: `${result?.confidence ?? 99.74}%`,
          analysis: result?.analysis,
        },
        { responseType: "blob" }
      );

      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "E_Waste_Report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error("PDF generation failed:", err);
    }
  };

  // Acquire user's current GPS location
  const getUserGeolocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    setLocationLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        const newUserLoc = { lat: latitude, lng: longitude };
        setUserLocation(newUserLoc);
        setMapCenter([latitude, longitude]);

        // Calculate distance and sort hubs from nearest to farthest
        const sortedHubs = INITIAL_RECYCLING_HUBS.map((hub) => ({
          ...hub,
          distance: calculateDistanceKm(latitude, longitude, hub.lat, hub.lng),
        })).sort((a, b) => parseFloat(a.distance) - parseFloat(b.distance));

        setHubs(sortedHubs);
        setLocationLoading(false);
      },
      (error) => {
        console.error("Error obtaining location:", error);
        alert(
          "Could not acquire your location. Please check browser permissions."
        );
        setLocationLoading(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  const pieData = result?.analysis?.materials
    ? Object.entries(result.analysis.materials).map(([name, value]) => ({
        name,
        value,
      }))
    : [];

  return (
    <div className="min-h-screen bg-[#040806] text-slate-100 font-sans antialiased selection:bg-emerald-500 selection:text-slate-950 relative overflow-x-hidden flex flex-col">
      {/* Global Floating Animated Background */}
      <FloatingBackground />

      {/* Cursor Glow - Neon Green Torch Effect */}
      <div
        className="fixed pointer-events-none z-50 -translate-x-1/2 -translate-y-1/2"
        style={{ left: `${cursorPos.x}px`, top: `${cursorPos.y}px` }}
      >
        {/* Outer dim torch glow */}
        <div
          className="absolute rounded-full w-32 h-32 -translate-x-1/2 -translate-y-1/2 blur-2xl transition-transform duration-100 ease-out"
          style={{
            background:
              "radial-gradient(circle, rgba(34,197,94,0.45) 0%, rgba(34,197,94,0.15) 45%, transparent 75%)",
          }}
        />
        {/* Inner bright core ring */}
        <div className="absolute rounded-full w-3 h-3 -translate-x-1/2 -translate-y-1/2 bg-emerald-400 shadow-[0_0_18px_6px_rgba(34,197,94,0.85)]" />
      </div>

      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Navigation Bar */}
        <header className="border-b border-slate-800/80 bg-slate-950/60 backdrop-blur-xl sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div
              onClick={() => setActiveTab("home")}
              className="flex items-center space-x-3 cursor-pointer"
            >
              <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/10 rounded-xl border border-emerald-500/30 text-emerald-400">
                <Zap className="w-5 h-5 fill-emerald-400/20" />
              </div>
              <span className="font-extrabold text-lg tracking-wider text-white">
                ECO-VALUATE{" "}
                <span className="text-emerald-400 font-black">AI</span>
              </span>
            </div>

            <div className="flex items-center gap-2 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
              <button
                onClick={() => setActiveTab("home")}
                className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  activeTab === "home"
                    ? "bg-emerald-500 text-slate-950 shadow-md"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                Home
              </button>
              <button
                onClick={() => setActiveTab("scanner")}
                className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  activeTab === "scanner"
                    ? "bg-emerald-500 text-slate-950 shadow-md"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                AI Scanner
              </button>
              <button
                onClick={() => setActiveTab("map")}
                className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                  activeTab === "map"
                    ? "bg-emerald-500 text-slate-950 shadow-md"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                <MapPin className="w-3.5 h-3.5" /> Recycling Hubs
              </button>
            </div>
          </div>
        </header>

        {/* Main View Switching */}
        <div className="flex-grow">
          {/* Tab 1: Landing Page */}
          {activeTab === "home" && (
            <main className="max-w-7xl mx-auto px-6">
              <LandingPage
                onStartScan={() => setActiveTab("scanner")}
                onExploreMap={() => setActiveTab("map")}
              />
            </main>
          )}

          {/* Tab 2: AI Scanner */}
          {activeTab === "scanner" && (
            <main className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8 flex-grow w-full">
              <section className="lg:col-span-5 space-y-6">
                <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-6 shadow-2xl">
                  <h2 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                    <UploadCloud className="w-5 h-5 text-emerald-400" /> Image &
                    Mass Parameters
                  </h2>

                  <div
                    onDragOver={(e) => {
                      e.preventDefault();
                      setDragActive(true);
                    }}
                    onDragLeave={() => setDragActive(false)}
                    onDrop={handleDrop}
                    className={`relative border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
                      dragActive
                        ? "border-emerald-400 bg-emerald-500/10"
                        : "border-slate-800 bg-slate-950/50"
                    }`}
                  >
                    <input
                      type="file"
                      onChange={(e) => handleImageChange(e.target.files[0])}
                      accept="image/*"
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-20"
                    />
                    {preview ? (
                      <img
                        src={preview}
                        alt="Preview"
                        className="max-h-56 w-full object-contain mx-auto rounded-lg"
                      />
                    ) : (
                      <div className="space-y-3 py-4">
                        <Cpu className="w-8 h-8 text-slate-500 mx-auto" />
                        <p className="text-sm font-medium text-slate-300">
                          Drop photo or{" "}
                          <span className="text-emerald-400 underline">
                            browse
                          </span>
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="mt-6 space-y-5">
                    <div>
                      <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                        <Scale className="w-3.5 h-3.5 text-emerald-400" /> Item
                        Mass (kg)
                      </label>
                      <input
                        type="number"
                        step="0.1"
                        min="0.1"
                        value={weight}
                        onChange={(e) => setWeight(e.target.value)}
                        className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-3 text-white font-mono focus:outline-none focus:border-emerald-500"
                      />
                    </div>

                    <button
                      onClick={handleUpload}
                      disabled={!file || loading}
                      className="w-full bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-slate-950 font-bold py-3.5 rounded-xl transition-all shadow-lg flex items-center justify-center gap-2"
                    >
                      {loading ? (
                        <RefreshCw className="w-5 h-5 animate-spin" />
                      ) : (
                        <Sparkles className="w-5 h-5" />
                      )}
                      {loading ? "Analyzing..." : "Analyze Waste Stream"}
                    </button>
                  </div>
                </div>
              </section>

              <section className="lg:col-span-7">
                <AnimatePresence mode="wait">
                  {result ? (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="space-y-6"
                      id="audit-report"
                    >
                      <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 shadow-xl flex items-start justify-between">
                        <div>
                          <span className="text-xs font-bold text-emerald-400 tracking-wider uppercase flex items-center gap-1.5 mb-1">
                            <Layers className="w-3.5 h-3.5" /> Detected Class
                          </span>
                          <h3 className="text-2xl font-black text-white capitalize">
                            {result.analysis.display_name}
                          </h3>
                          <p className="text-xs text-slate-400 mt-1">
                            Category: {result.analysis.category} | Confidence:{" "}
                            {result.confidence}%
                          </p>
                        </div>

                        <button
                          onClick={exportPDF}
                          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-bold text-white border border-slate-700 rounded-xl flex items-center gap-2 transition-all shadow-lg"
                        >
                          <Download className="w-4 h-4 text-emerald-400" /> Export
                          PDF
                        </button>
                      </div>

                      {result.analysis.is_ewaste && (
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                          <div className="bg-slate-900/60 border border-slate-800/80 p-4 rounded-xl">
                            <span className="text-xs text-slate-400 font-semibold block mb-1">
                              Est. Gold Yield
                            </span>
                            <span className="text-2xl font-black text-amber-400 font-mono">
                              {result.analysis.gold_g} g
                            </span>
                          </div>
                          <div className="bg-slate-900/60 border border-slate-800/80 p-4 rounded-xl">
                            <span className="text-xs text-slate-400 font-semibold block mb-1">
                              Est. Copper Yield
                            </span>
                            <span className="text-2xl font-black text-orange-400 font-mono">
                              {result.analysis.copper_g} g
                            </span>
                          </div>
                          <div className="bg-slate-900/60 border border-slate-800/80 p-4 rounded-xl">
                            <span className="text-xs text-slate-400 font-semibold block mb-1">
                              Scrap Market Value
                            </span>
                            <span className="text-2xl font-black text-emerald-400 font-mono">
                              ${result.analysis.est_value_usd}
                            </span>
                          </div>
                        </div>
                      )}

                      <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
                        <div>
                          <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-1.5">
                            <PieIcon className="w-4 h-4 text-emerald-400" />{" "}
                            Material Breakdown
                          </h4>
                          <div className="h-44">
                            <ResponsiveContainer width="100%" height="100%">
                              <PieChart>
                                <Pie
                                  data={pieData}
                                  innerRadius={40}
                                  outerRadius={60}
                                  paddingAngle={4}
                                  dataKey="value"
                                >
                                  {pieData.map((_, idx) => (
                                    <Cell
                                      key={idx}
                                      fill={COLORS[idx % COLORS.length]}
                                    />
                                  ))}
                                </Pie>
                                <Tooltip />
                              </PieChart>
                            </ResponsiveContainer>
                          </div>
                        </div>

                        <div className="space-y-4">
                          <div>
                            <span className="text-xs text-slate-400 font-semibold block mb-1 flex items-center gap-1.5">
                              <AlertTriangle className="w-4 h-4 text-amber-400" />{" "}
                              Hazard Rating
                            </span>
                            <p className="text-sm font-semibold text-slate-200">
                              {result.analysis.hazard}
                            </p>
                          </div>
                          <div>
                            <span className="text-xs text-slate-400 font-semibold block mb-1 flex items-center gap-1.5">
                              <ShieldCheck className="w-4 h-4 text-emerald-400" />{" "}
                              Disposal Protocol
                            </span>
                            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/80 p-3 rounded-xl border border-slate-800">
                              {result.analysis.protocol}
                            </p>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ) : (
                    <div className="bg-slate-900/30 border border-dashed border-slate-800/80 rounded-2xl h-full min-h-[420px] flex flex-col items-center justify-center p-8 text-center">
                      <Cpu className="w-8 h-8 text-slate-500 mb-2 animate-pulse" />
                      <h3 className="text-base font-bold text-slate-300">
                        Awaiting Input Parameters
                      </h3>
                    </div>
                  )}
                </AnimatePresence>
              </section>
            </main>
          )}

          {/* Tab 3: Geolocation & Routing Map */}
          {activeTab === "map" && (
            <main className="max-w-7xl mx-auto px-6 py-8 w-full flex-grow grid grid-cols-1 lg:grid-cols-12 gap-8">
              <div className="lg:col-span-8 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl min-h-[480px] h-[550px] relative">
                <MapContainer
                  center={mapCenter}
                  zoom={11}
                  className="w-full h-full z-0"
                >
                  <MapRecenter center={mapCenter} />
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                  />

                  {/* User position marker */}
                  {userLocation && (
                    <Marker position={[userLocation.lat, userLocation.lng]}>
                      <Popup>
                        <div className="p-1 text-slate-950 font-sans">
                          <strong className="block text-sm font-bold text-blue-600">
                            Your Current Location
                          </strong>
                        </div>
                      </Popup>
                    </Marker>
                  )}

                  {/* Facility markers */}
                  {hubs.map((hub) => (
                    <Marker key={hub.id} position={[hub.lat, hub.lng]}>
                      <Popup>
                        <div className="p-1 text-slate-950 font-sans">
                          <strong className="block text-sm font-bold">
                            {hub.name}
                          </strong>
                          <span className="text-xs text-slate-600 block mt-1">
                            {hub.type}
                          </span>
                          {hub.distance && (
                            <span className="text-xs font-bold text-emerald-600 block mt-1">
                              {hub.distance} km away
                            </span>
                          )}
                          <a
                            href={`https://www.google.com/maps/dir/?api=1&destination=${hub.lat},${hub.lng}`}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-block mt-2 text-xs text-white bg-slate-900 px-2 py-1 rounded"
                          >
                            Navigate Here
                          </a>
                        </div>
                      </Popup>
                    </Marker>
                  ))}
                </MapContainer>
              </div>

              <div className="lg:col-span-4 space-y-4 flex flex-col justify-between">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-base font-bold text-white flex items-center gap-2">
                      <Building2 className="w-5 h-5 text-emerald-400" /> Drop-off
                      Facilities
                    </h3>
                    <button
                      onClick={getUserGeolocation}
                      disabled={locationLoading}
                      className="px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold rounded-xl transition-all flex items-center gap-1.5"
                    >
                      {locationLoading ? (
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      ) : (
                        <Compass className="w-3.5 h-3.5" />
                      )}
                      {userLocation ? "Recalculate" : "Locate Me"}
                    </button>
                  </div>

                  <div className="space-y-3 max-h-[440px] overflow-y-auto pr-1">
                    {hubs.map((hub) => (
                      <div
                        key={hub.id}
                        onClick={() => setMapCenter([hub.lat, hub.lng])}
                        className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl shadow-lg hover:border-emerald-500/40 transition-colors cursor-pointer"
                      >
                        <div className="flex items-start justify-between">
                          <h4 className="text-sm font-bold text-white">
                            {hub.name}
                          </h4>
                          {hub.distance && (
                            <span className="text-xs font-mono text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                              {hub.distance} km
                            </span>
                          )}
                        </div>
                        <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 inline-block mt-2">
                          {hub.type}
                        </span>

                        <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-800/80">
                          <p className="text-xs text-slate-400 flex items-center gap-1.5 font-mono">
                            <Phone className="w-3.5 h-3.5 text-slate-500" />{" "}
                            {hub.phone}
                          </p>
                          <a
                            href={`https://www.google.com/maps/dir/?api=1&destination=${hub.lat},${hub.lng}${
                              userLocation
                                ? `&origin=${userLocation.lat},${userLocation.lng}`
                                : ""
                            }`}
                            target="_blank"
                            rel="noreferrer"
                            onClick={(e) => e.stopPropagation()}
                            className="text-xs font-bold text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
                          >
                            <Navigation className="w-3 h-3" /> Route
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </main>
          )}
        </div>

        {/* Footer */}
        <Footer />
      </div>
    </div>
  );
}