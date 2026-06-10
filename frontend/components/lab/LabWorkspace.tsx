"use client";

import { useState, useEffect, useCallback } from "react";
import { LabTerminal } from "./LabTerminal";
import { labsApi } from "@/lib/api";

interface LabDevice {
  name: string;
  kind: string;
  mgmt_ip: string;
  status: string;
}

interface LabSubmission {
  id: string;
  lab_id: string;
  status: string;
  pod_id: string;
  devices: LabDevice[];
  started_at: string;
  time_remaining_seconds: number;
  current_score: number;
  max_score: number;
  terminal_ws_url: string;
}

interface LabWorkspaceProps {
  submissionId: string;
  wsBaseUrl?: string;
}

export function LabWorkspace({
  submissionId,
  wsBaseUrl = "/ws",
}: LabWorkspaceProps) {
  const [submission, setSubmission] = useState<LabSubmission | null>(null);
  const [activeDevice, setActiveDevice] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [showTopology, setShowTopology] = useState(true);
  const [fullscreen, setFullscreen] = useState(false);

  // Fetch submission data
  useEffect(() => {
    const fetchSubmission = async () => {
      try {
        const data = await labsApi.getSubmission(submissionId);
        setSubmission(data);
        setTimeRemaining(data.time_remaining_seconds || 0);
        if (data.devices && data.devices.length > 0) {
          setActiveDevice(data.devices[0].name);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load lab");
      } finally {
        setLoading(false);
      }
    };
    fetchSubmission();
  }, [submissionId]);

  // Timer countdown
  useEffect(() => {
    if (timeRemaining <= 0) return;
    const interval = setInterval(() => {
      setTimeRemaining((prev) => Math.max(0, prev - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [timeRemaining]);

  // Format time
  const formatTime = useCallback((seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  }, []);

  // Get WebSocket URL for a device
  const getDeviceWsUrl = useCallback(
    (deviceName: string) => {
      return `${wsBaseUrl}/lab/${submissionId}/${deviceName}`;
    },
    [wsBaseUrl, submissionId]
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0d1117]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-2 border-[#58a6ff] border-t-transparent rounded-full animate-spin" />
          <p className="text-[#8b949e] text-sm">Starting lab environment...</p>
        </div>
      </div>
    );
  }

  if (error || !submission) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0d1117]">
        <div className="text-center">
          <p className="text-[#ff7b72] text-lg font-medium mb-2">
            Failed to load lab
          </p>
          <p className="text-[#8b949e] text-sm">{error || "Unknown error"}</p>
        </div>
      </div>
    );
  }

  const wsProtocol = typeof window !== "undefined" && window.location.protocol === "https:" ? "wss" : "ws";
  const wsHost = typeof window !== "undefined" ? window.location.host : "localhost:8080";
  const wsBase = `${wsProtocol}://${wsHost}${wsBaseUrl}`;

  return (
    <div
      className={`flex flex-col bg-[#0d1117] text-[#c9d1d9] ${
        fullscreen ? "fixed inset-0 z-50" : "h-full min-h-[600px]"
      }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-[#161b22] border-b border-[#30363d] shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-sm font-semibold text-[#e6edf3]">
            Lab Workspace
          </span>
          <span className="text-xs text-[#8b949e]">
            Pod: {submission.pod_id}
          </span>
          <span
            className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${
              submission.status === "running"
                ? "bg-[#3fb950]/10 text-[#3fb950]"
                : submission.status === "deploying"
                  ? "bg-[#d29922]/10 text-[#d29922]"
                  : "bg-[#8b949e]/10 text-[#8b949e]"
            }`}
          >
            <span
              className={`w-1.5 h-1.5 rounded-full ${
                submission.status === "running"
                  ? "bg-[#3fb950] animate-pulse"
                  : submission.status === "deploying"
                    ? "bg-[#d29922] animate-pulse"
                    : "bg-[#8b949e]"
              }`}
            />
            {submission.status}
          </span>
        </div>

        <div className="flex items-center gap-4">
          {/* Score */}
          <span className="text-xs text-[#8b949e]">
            Score:{" "}
            <span className="text-[#e6edf3] font-medium">
              {submission.current_score}/{submission.max_score}
            </span>
          </span>

          {/* Timer */}
          <span
            className={`text-sm font-mono font-bold ${
              timeRemaining < 300
                ? "text-[#ff7b72] animate-pulse"
                : timeRemaining < 900
                  ? "text-[#d29922]"
                  : "text-[#3fb950]"
            }`}
          >
            {formatTime(timeRemaining)}
          </span>

          {/* Controls */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowTopology((v) => !v)}
              className="px-2 py-1 text-xs rounded bg-[#21262d] hover:bg-[#30363d] border border-[#30363d] transition-colors"
              title="Toggle topology panel"
            >
              {showTopology ? "Hide Topology" : "Show Topology"}
            </button>
            <button
              onClick={() => setFullscreen((v) => !v)}
              className="px-2 py-1 text-xs rounded bg-[#21262d] hover:bg-[#30363d] border border-[#30363d] transition-colors"
              title="Toggle fullscreen"
            >
              {fullscreen ? "Exit Fullscreen" : "Fullscreen"}
            </button>
            <button
              onClick={async () => {
                if (
                  !confirm(
                    "Are you sure you want to end this lab session?"
                  )
                )
                  return;
                try {
                  await labsApi.stopSubmission(submissionId);
                  window.location.href = "/labs";
                } catch {
                  alert("Failed to stop lab");
                }
              }}
              className="px-3 py-1 text-xs rounded bg-[#ff7b72]/10 text-[#ff7b72] hover:bg-[#ff7b72]/20 border border-[#ff7b72]/30 transition-colors"
            >
              End Lab
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Topology Panel (left) */}
        {showTopology && (
          <div className="w-72 shrink-0 border-r border-[#30363d] bg-[#0d1117] overflow-y-auto">
            <div className="p-3">
              <h3 className="text-xs font-semibold text-[#8b949e] uppercase tracking-wider mb-3">
                Devices
              </h3>
              <div className="space-y-2">
                {(submission.devices || []).map((device) => (
                  <button
                    key={device.name}
                    onClick={() => setActiveDevice(device.name)}
                    className={`w-full flex items-center gap-3 p-2.5 rounded-lg text-left transition-all ${
                      activeDevice === device.name
                        ? "bg-[#1f2937] border border-[#58a6ff]/50 shadow-sm shadow-[#58a6ff]/5"
                        : "bg-[#161b22] border border-[#30363d] hover:border-[#58a6ff]/30"
                    }`}
                  >
                    {/* Device icon */}
                    <div className="flex-shrink-0 w-8 h-8 rounded-md bg-[#21262d] flex items-center justify-center">
                      {device.kind === "juniper_crpd" || device.kind === "router" ? (
                        <svg
                          viewBox="0 0 24 24"
                          className="w-5 h-5 text-[#58a6ff]"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                        >
                          <circle cx="12" cy="12" r="6" />
                          <path d="M12 6v12M6 12h12" />
                        </svg>
                      ) : device.kind === "firewall" || device.kind === "juniper_vsrx" ? (
                        <svg
                          viewBox="0 0 24 24"
                          className="w-5 h-5 text-[#d29922]"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                        >
                          <path d="M12 2l8 4v6c0 5-8 8-8 8s-8-3-8-8V6l8-4z" />
                        </svg>
                      ) : (
                        <svg
                          viewBox="0 0 24 24"
                          className="w-5 h-5 text-[#8b949e]"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                        >
                          <rect x="2" y="2" width="20" height="8" rx="2" />
                          <rect
                            x="2"
                            y="14"
                            width="20"
                            height="8"
                            rx="2"
                          />
                        </svg>
                      )}
                    </div>

                    {/* Device info */}
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-[#e6edf3] truncate">
                        {device.name}
                      </div>
                      <div className="flex items-center gap-1.5 mt-0.5">
                        <span
                          className={`w-1.5 h-1.5 rounded-full ${
                            device.status === "running"
                              ? "bg-[#3fb950]"
                              : device.status === "starting"
                                ? "bg-[#d29922]"
                                : "bg-[#ff7b72]"
                          }`}
                        />
                        <span className="text-xs text-[#8b949e]">
                          {device.status}
                        </span>
                      </div>
                    </div>

                    {/* Active indicator */}
                    {activeDevice === device.name && (
                      <div className="w-1.5 h-1.5 rounded-full bg-[#58a6ff]" />
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Task Info */}
            <div className="p-3 border-t border-[#30363d]">
              <h3 className="text-xs font-semibold text-[#8b949e] uppercase tracking-wider mb-2">
                Lab Info
              </h3>
              <div className="space-y-1 text-xs text-[#8b949e]">
                <p>
                  Status:{" "}
                  <span className="text-[#e6edf3] capitalize">
                    {submission.status}
                  </span>
                </p>
                <p>
                  Devices:{" "}
                  <span className="text-[#e6edf3]">
                    {(submission.devices || []).length}
                  </span>
                </p>
                <p>
                  Started:{" "}
                  <span className="text-[#e6edf3]">
                    {new Date(submission.started_at).toLocaleTimeString()}
                  </span>
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Terminal Panel (right) */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Device tabs */}
          <div className="flex items-center bg-[#161b22] border-b border-[#30363d] shrink-0 overflow-x-auto">
            {(submission.devices || []).map((device) => (
              <button
                key={device.name}
                onClick={() => setActiveDevice(device.name)}
                className={`flex items-center gap-1.5 px-3 py-2 text-xs border-b-2 transition-all whitespace-nowrap ${
                  activeDevice === device.name
                    ? "border-[#58a6ff] text-[#e6edf3] bg-[#1f2937]"
                    : "border-transparent text-[#8b949e] hover:text-[#c9d1d9] hover:bg-[#21262d]"
                }`}
              >
                <span
                  className={`w-1.5 h-1.5 rounded-full ${
                    device.status === "running"
                      ? "bg-[#3fb950]"
                      : "bg-[#d29922]"
                  }`}
                />
                {device.name}
                {device.kind && (
                  <span className="text-[10px] text-[#8b949e] ml-1">
                    ({device.kind.replace("juniper_", "")})
                  </span>
                )}
              </button>
            ))}
          </div>

          {/* Terminal */}
          <div className="flex-1 overflow-hidden">
            {activeDevice && (
              <LabTerminal
                key={activeDevice}
                deviceName={activeDevice}
                wsUrl={`${wsBase}/lab/${submissionId}/${activeDevice}`}
                className="h-full rounded-none border-0"
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
