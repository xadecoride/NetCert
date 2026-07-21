"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import InteractiveTopology from "./InteractiveTopology";
import {
  lab01Topology,
  lab02Topology,
  lab03Topology,
  lab04Topology,
  lab05Topology,
  jncieEntTopology,
} from "@/lib/topology/defaultTopologies";
import type { LabTopologyData } from "@/lib/topology/types";
import { Badge } from "@/components/ui/badge";
import {
  Play,
  Code,
} from "@phosphor-icons/react";

// ─── Lab Definitions ───
const labs = [
  { id: "lab-01", data: lab01Topology, level: "JNCIA", difficulty: 1 },
  { id: "lab-02", data: lab02Topology, level: "JNCIA", difficulty: 2 },
  { id: "lab-03", data: lab03Topology, level: "JNCIP", difficulty: 3 },
  { id: "lab-04", data: lab04Topology, level: "JNCIP", difficulty: 3 },
  { id: "lab-05", data: lab05Topology, level: "JNCIP", difficulty: 4 },
] as const;

const difficultyColor = (d: number) =>
  d <= 1
    ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
    : d <= 2
      ? "bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-400"
      : d <= 3
        ? "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400"
        : "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400";

export default function LabTopologyDemo() {
  const [activeLab, setActiveLab] = useState<string>("lab-02");
  const [showFullLab, setShowFullLab] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState<string | null>(null);

  const currentLab = labs.find((l) => l.id === activeLab)?.data ?? lab02Topology;
  const displayData: LabTopologyData = showFullLab ? jncieEntTopology : currentLab;

  return (
    <div className="min-h-[100dvh] bg-zinc-50 dark:bg-zinc-950 py-8">
      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
        {/* ─── Header ─── */}
        <div className="mb-8">
          <Badge variant="secondary" className="mb-3">
            <Code className="h-3 w-3 mr-1" weight="fill" />
            Lab Workspace Preview
          </Badge>
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tighter text-zinc-900 dark:text-zinc-100">
            Interactive Topology Demo
          </h1>
          <p className="mt-2 text-zinc-500 dark:text-zinc-400 max-w-2xl">
            React Flow-based interactive network topology with custom SVG nodes,
            status-aware connector edges, WebSocket live-updates, and animated traffic.
          </p>
        </div>

        {/* ─── Lab Selector ─── */}
        <div className="flex flex-wrap items-center gap-2 mb-6">
          {labs.map((lab) => (
            <button
              key={lab.id}
              onClick={() => {
                setActiveLab(lab.id);
                setShowFullLab(false);
                setSelectedDevice(null);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                activeLab === lab.id && !showFullLab
                  ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 shadow-sm"
                  : "bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 border border-zinc-200 dark:border-zinc-800"
              }`}
            >
              <span className="mr-1.5 opacity-50">ML0{lab.id.split("-")[1]}</span>
              {lab.data.title}
            </button>
          ))}
          <div className="w-px h-5 bg-zinc-200 dark:bg-zinc-800 mx-1" />
          <button
            onClick={() => {
              setShowFullLab(true);
              setSelectedDevice(null);
            }}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
              showFullLab
                ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 shadow-sm"
                : "bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 border border-zinc-200 dark:border-zinc-800"
            }`}
          >
            JNCIE-ENT
          </button>
        </div>

        {/* ─── Info Bar ─── */}
        <div className="flex flex-wrap items-center gap-3 mb-4 text-xs font-mono">
          <Badge
            variant="outline"
            className={`${difficultyColor(
              labs.find((l) => l.data === displayData)?.difficulty ?? 3,
            )}`}
          >
            {displayData.nodes.length} devices &middot;{" "}
            {displayData.edges.length} links
          </Badge>
          <Badge variant="secondary" className="text-xs">
            {displayData.title}
          </Badge>
          {selectedDevice && (
            <Badge variant="juniper" className="text-xs animate-in fade-in">
              <Play className="h-3 w-3 mr-1" weight="fill" />
              Selected: {selectedDevice}
            </Badge>
          )}
        </div>

        {/* ─── Topology ─── */}
        <div className="rounded-xl overflow-hidden border border-zinc-200 dark:border-zinc-800 shadow-lg bg-white dark:bg-zinc-900">
          <InteractiveTopology
            topologyData={displayData}
            onNodeClick={(nodeId) => setSelectedDevice(nodeId)}
            onEdgeClick={(edgeId) => console.log("Edge clicked:", edgeId)}
            className="h-[600px] lg:h-[700px]"
          />
        </div>

        {/* ─── Help Text ─── */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800">
            <h4 className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 mb-1">
              🖱 Interaction
            </h4>
            <p className="text-[11px] text-zinc-500 dark:text-zinc-400 leading-relaxed">
              Drag to pan · Scroll to zoom · Click a device to select · Drag nodes to rearrange
            </p>
          </div>
          <div className="p-4 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800">
            <h4 className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 mb-1">
              🎨 Custom Nodes
            </h4>
            <p className="text-[11px] text-zinc-500 dark:text-zinc-400 leading-relaxed">
              Router (cRPD), Switch (vQFX), Firewall (vSRX), Host, Cloud — each with status LEDs
            </p>
          </div>
          <div className="p-4 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800">
            <h4 className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 mb-1">
              🔌 Real-Time Updates
            </h4>
            <p className="text-[11px] text-zinc-500 dark:text-zinc-400 leading-relaxed">
              WebSocket pushes node_status / edge_status / node_metrics for live lab state
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
