"use client";

import { memo } from "react";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import type { DeviceNodeData, DeviceNode } from "./types";
import { statusColor } from "./types";

// ─── Shared Node Shell ───
const NodeShell = memo(function NodeShell({
  children,
  data,
  selected,
  width = 64,
  height = 48,
}: {
  children: React.ReactNode;
  data: DeviceNodeData;
  selected: boolean;
  width?: number;
  height?: number;
}) {
  const borderColor = selected
    ? "var(--svg-highlight, #3b82f6)"
    : data.status === "down"
      ? statusColor("down")
      : "transparent";

  return (
    <div
      className="relative rounded-lg border-2 transition-all duration-200"
      style={{
        width,
        height,
        borderColor,
        background: "var(--svg-bg-secondary, #1e293b)",
        opacity: data.status === "down" ? 0.6 : 1,
        boxShadow: selected
          ? "0 0 0 1px var(--svg-highlight, #3b82f6), 0 4px 12px rgba(0,0,0,0.15)"
          : "0 1px 3px rgba(0,0,0,0.1)",
      }}
    >
      <Handle
        type="target"
        position={Position.Top}
        className="!w-2 !h-2 !border-2 !bg-zinc-800 !border-white/20"
        style={{ top: -5 }}
      />

      <div className="flex flex-col items-center justify-center h-full px-1">
        {children}
      </div>

      <Handle
        type="source"
        position={Position.Bottom}
        className="!w-2 !h-2 !border-2 !bg-zinc-800 !border-white/20"
        style={{ bottom: -5 }}
      />
    </div>
  );
});

// ─── Router Icon ───
function RouterSvg({ data }: { data: DeviceNodeData }) {
  return (
    <svg viewBox="0 0 64 64" width="36" height="36" fill="none">
      <rect x="8" y="16" width="48" height="28" rx="4" fill="var(--svg-device-router, #475569)" opacity={0.85} />
      <rect x="12" y="20" width="40" height="20" rx="2" fill="var(--svg-bg, #0f172a)" opacity={0.15} />
      {/* LEDs */}
      <circle cx="20" cy="30" r="3" fill={statusColor(data.status)} />
      <circle cx="30" cy="30" r="3" fill={statusColor(data.status === "down" ? "down" : "up")} />
      <circle cx="40" cy="30" r="3" fill={data.status === "warning" ? statusColor("warning") : statusColor("up")} />
      {/* Ports */}
      <rect x="14" y="35" width="4" height="3" rx="0.5" fill="var(--svg-text-secondary, #94a3b8)" opacity={0.5} />
      <rect x="21" y="35" width="4" height="3" rx="0.5" fill="var(--svg-text-secondary, #94a3b8)" opacity={0.5} />
      <rect x="38" y="35" width="4" height="3" rx="0.5" fill="var(--svg-text-secondary, #94a3b8)" opacity={0.5} />
      <rect x="45" y="35" width="4" height="3" rx="0.5" fill="var(--svg-text-secondary, #94a3b8)" opacity={0.5} />
      {/* Rack ears */}
      <rect x="4" y="18" width="4" height="24" rx="1" fill="var(--svg-device-router, #475569)" opacity={0.5} />
      <rect x="56" y="18" width="4" height="24" rx="1" fill="var(--svg-device-router, #475569)" opacity={0.5} />
    </svg>
  );
}

// ─── Switch Icon ───
function SwitchSvg({ data }: { data: DeviceNodeData }) {
  const color = statusColor(data.status);
  return (
    <svg viewBox="0 0 64 48" width="36" height="28" fill="none">
      <rect x="6" y="10" width="52" height="24" rx="3" fill="var(--svg-device-switch, #64748b)" opacity={0.85} />
      <g opacity={0.7}>
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <rect key={i} x={10 + i * 8} y={14} width="5" height="4" rx="0.5" fill="var(--svg-text, #e2e8f0)" />
        ))}
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <rect key={`b${i}`} x={10 + i * 8} y={20} width="5" height="4" rx="0.5" fill="var(--svg-text, #e2e8f0)" />
        ))}
      </g>
      {/* LEDs */}
      {[0, 1, 2, 3, 4].map((i) => (
        <circle
          key={i}
          cx={12 + i * 8}
          cy={28}
          r={1.5}
          fill={i === 3 ? statusColor("down") : statusColor("up")}
        />
      ))}
    </svg>
  );
}

// ─── Firewall Icon ───
function FirewallSvg({ data }: { data: DeviceNodeData }) {
  return (
    <svg viewBox="0 0 64 56" width="32" height="30" fill="none">
      <rect x="10" y="14" width="44" height="28" rx="4" fill="var(--svg-device-firewall, #dc2626)" opacity={0.85} />
      {/* Shield */}
      <path
        d="M32 18l-8 4v6c0 6.67 3.33 10 8 12 4.67-2 8-5.33 8-12v-6l-8-4z"
        fill="var(--svg-bg, #0f172a)"
        opacity={0.9}
      />
      <path
        d="M32 21l-5 2.5v4.5c0 4.67 2.33 7 5 8.5 2.67-1.5 5-3.83 5-8.5v-4.5L32 21z"
        fill="var(--svg-device-firewall, #dc2626)"
      />
      {/* Checkmark */}
      <path
        d="M28 28l3 3 5-5"
        stroke="var(--svg-bg, #0f172a)"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

// ─── Host Icon ───
function HostSvg() {
  return (
    <svg viewBox="0 0 48 64" width="22" height="30" fill="none">
      <rect x="4" y="4" width="40" height="24" rx="3" fill="var(--svg-device-host, #64748b)" opacity={0.8} />
      <rect x="8" y="7" width="32" height="18" rx="2" fill="var(--svg-terminal-bg, #000)" />
      <text x="12" y="18" fill="var(--svg-terminal-green, #22c55e)" fontSize="4" fontFamily="monospace">
        root@host:~$
      </text>
      <rect x="18" y="28" width="12" height="3" rx="1" fill="var(--svg-device-host, #64748b)" opacity={0.7} />
      <rect x="14" y="31" width="20" height="2" rx="1" fill="var(--svg-device-host, #64748b)" opacity={0.6} />
    </svg>
  );
}

// ─── Cloud Icon ───
function CloudSvg() {
  return (
    <svg viewBox="0 0 80 48" width="40" height="26" fill="none">
      <ellipse cx="40" cy="24" rx="28" ry="12" fill="var(--svg-cloud, #e2e8f0)" opacity={0.8} />
      <path
        d="M24 24 Q24 14 34 14 Q36 6 46 8 Q56 6 56 16 Q64 18 62 26 Q56 32 40 32 Q28 32 24 24Z"
        fill="var(--svg-cloud, #e2e8f0)"
        stroke="var(--svg-text-secondary, #94a3b8)"
        strokeWidth="0.5"
      />
      <text
        x="40"
        y="28"
        textAnchor="middle"
        fill="var(--svg-text-secondary, #94a3b8)"
        fontSize="5"
        fontFamily="monospace"
        opacity={0.6}
      >
        NET
      </text>
    </svg>
  );
}

// ─── Interface Dots ───
function InterfaceDots({ interfaces }: { interfaces: DeviceNodeData["interfaces"] }) {
  if (!interfaces?.length) return null;
  return (
    <div className="flex gap-0.5 mt-0.5">
      {interfaces.slice(0, 4).map((iface, i) => (
        <div
          key={i}
          className="w-1.5 h-1.5 rounded-full"
          style={{
            background:
              iface.status === "up"
                ? "var(--svg-line-active, #22c55e)"
                : iface.status === "down"
                  ? "var(--svg-line-down, #ef4444)"
                  : "var(--svg-line-warning, #f59e0b)",
          }}
          title={`${iface.name} (${iface.ip}) — ${iface.status}`}
        />
      ))}
    </div>
  );
}

// ─── Custom Node Components ───

export const RouterNode = memo(function RouterNode({ data, selected }: NodeProps<DeviceNode>) {
  return (
    <NodeShell data={data} selected={selected} width={72} height={64}>
      <RouterSvg data={data} />
      <span
        className="text-[7px] font-mono font-semibold leading-tight truncate max-w-[60px] text-center"
        style={{ color: "var(--svg-text, #e2e8f0)" }}
      >
        {data.label}
      </span>
      {data.model && (
        <span
          className="text-[5px] font-mono opacity-60 leading-tight"
          style={{ color: "var(--svg-text-secondary, #94a3b8)" }}
        >
          {data.model}
        </span>
      )}
      <InterfaceDots interfaces={data.interfaces} />
    </NodeShell>
  );
});

export const SwitchNode = memo(function SwitchNode({ data, selected }: NodeProps<DeviceNode>) {
  return (
    <NodeShell data={data} selected={selected} width={72} height={56}>
      <SwitchSvg data={data} />
      <span
        className="text-[7px] font-mono font-semibold leading-tight truncate max-w-[60px] text-center"
        style={{ color: "var(--svg-text, #e2e8f0)" }}
      >
        {data.label}
      </span>
      <InterfaceDots interfaces={data.interfaces} />
    </NodeShell>
  );
});

export const FirewallNode = memo(function FirewallNode({ data, selected }: NodeProps<DeviceNode>) {
  return (
    <NodeShell data={data} selected={selected} width={72} height={64}>
      <FirewallSvg data={data} />
      <span
        className="text-[7px] font-mono font-semibold leading-tight truncate max-w-[60px] text-center"
        style={{ color: "var(--svg-text, #e2e8f0)" }}
      >
        {data.label}
      </span>
      <InterfaceDots interfaces={data.interfaces} />
    </NodeShell>
  );
});

export const HostNode = memo(function HostNode({ data, selected }: NodeProps<DeviceNode>) {
  return (
    <NodeShell data={data} selected={selected} width={64} height={64}>
      <HostSvg />
      <span
        className="text-[7px] font-mono font-semibold leading-tight truncate max-w-[52px] text-center"
        style={{ color: "var(--svg-text, #e2e8f0)" }}
      >
        {data.label}
      </span>
    </NodeShell>
  );
});

export const CloudNode = memo(function CloudNode({ data, selected }: NodeProps<DeviceNode>) {
  return (
    <NodeShell data={data} selected={selected} width={80} height={56}>
      <CloudSvg />
      <span
        className="text-[7px] font-mono font-semibold leading-tight"
        style={{ color: "var(--svg-text-secondary, #94a3b8)" }}
      >
        {data.label}
      </span>
    </NodeShell>
  );
});

// ─── Node Type Map ───
export const nodeTypes = {
  router: RouterNode,
  switch: SwitchNode,
  firewall: FirewallNode,
  host: HostNode,
  cloud: CloudNode,
} as const;

export type NodeTypeKey = keyof typeof nodeTypes;


