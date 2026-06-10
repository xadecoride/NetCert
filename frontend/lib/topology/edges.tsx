"use client";

import { memo } from "react";
import {
  BaseEdge,
  EdgeLabelRenderer,
  getBezierPath,
  type EdgeProps,
} from "@xyflow/react";
import type { ConnectorEdgeData, LinkStatus } from "./types";
import type { Edge } from "@xyflow/react";
import { statusColor } from "./types";

// ─── Connector Edge ───
export const ConnectorEdge = memo(function ConnectorEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
  selected,
}: EdgeProps<Edge<ConnectorEdgeData, "connector">>) {
  const status: LinkStatus = data?.status ?? "up";
  const color = statusColor(status);
  const isActive = status === "up" || status === "traffic";
  const isDown = status === "down";
  const isTraffic = status === "traffic";

  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  // Stroke style
  const strokeDasharray = isDown ? "6,4" : isTraffic ? "8,4" : undefined;
  const strokeWidth = isTraffic ? 3 : 2.5;
  const opacity = isDown ? 0.5 : 1;

  return (
    <>
      {/* Animated traffic layer (rendered behind) */}
      {isTraffic && (
        <BaseEdge
          id={`${id}-traffic`}
          path={edgePath}
          style={{
            stroke: "var(--svg-highlight, #3b82f6)",
            strokeWidth: 4,
            strokeDasharray: "8,4",
            opacity: 0.6,
          }}
          className="animate-traffic-flow"
        />
      )}

      {/* Main edge */}
      <BaseEdge
        id={id}
        path={edgePath}
        style={{
          stroke: color,
          strokeWidth,
          strokeDasharray,
          opacity,
          strokeLinecap: "round",
          transition: "stroke 0.3s ease, opacity 0.3s ease",
          filter: selected ? `drop-shadow(0 0 4px ${color})` : undefined,
        }}
      />

      {/* Down indicator — small X in the middle */}
      {isDown && (
        <EdgeLabelRenderer>
          <div
            className="absolute flex items-center justify-center rounded-full bg-red-500/20 border border-red-500/40"
            style={{
              transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
              width: 16,
              height: 16,
              pointerEvents: "none",
            }}
          >
            <svg width="8" height="8" viewBox="0 0 8 8" fill="none">
              <path d="M1 1l6 6M7 1l-6 6" stroke="#ef4444" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </div>
        </EdgeLabelRenderer>
      )}

      {/* Label */}
      {data?.label && (
        <EdgeLabelRenderer>
          <div
            className="absolute px-1.5 py-0.5 rounded text-[6px] font-mono leading-tight whitespace-nowrap pointer-events-none select-none"
            style={{
              transform: `translate(-50%, -50%) translate(${labelX}px,${labelY - 12}px)`,
              background: "var(--svg-bg-secondary, #1e293b)",
              color: "var(--svg-text-secondary, #94a3b8)",
              border: "1px solid var(--svg-line, #475569)",
              opacity,
            }}
          >
            {data.label}
          </div>
        </EdgeLabelRenderer>
      )}

      {/* Protocol badge */}
      {data?.protocol && (
        <EdgeLabelRenderer>
          <div
            className="absolute px-1 rounded-[2px] text-[5px] font-mono leading-tight pointer-events-none select-none"
            style={{
              transform: `translate(-50%, -50%) translate(${labelX}px,${labelY + 8}px)`,
              background:
                data.protocol === "BGP"
                  ? "rgba(59, 130, 246, 0.2)"
                  : data.protocol === "OSPF"
                    ? "rgba(34, 197, 94, 0.2)"
                    : data.protocol === "IS-IS"
                      ? "rgba(234, 179, 8, 0.2)"
                      : data.protocol === "LDP"
                        ? "rgba(168, 85, 247, 0.2)"
                        : "rgba(148, 163, 184, 0.2)",
              color: "var(--svg-text-secondary, #94a3b8)",
              opacity,
            }}
          >
            {data.protocol}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
});

// ─── Edge Type Map ───
export const edgeTypes = {
  connector: ConnectorEdge,
} as const;
