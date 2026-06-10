"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  BackgroundVariant,
  useNodesState,
  useEdgesState,
  ReactFlowProvider,
  Panel,
  type Node,
  type Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowsOut,
  Eye,
  EyeSlash,
  MapPin,
  WifiHigh,
  WifiSlash,
  CaretRight,
  CaretDown,
} from "@phosphor-icons/react";

import { nodeTypes } from "@/lib/topology/nodes";
import { edgeTypes } from "@/lib/topology/edges";
import type {
  LabTopologyData,
  DeviceNodeData,
  ConnectorEdgeData,
  TopologyEdgeData,
  TopologyUpdate,
  DeviceStatus,
  LinkStatus,
  TopologyConfig,
} from "@/lib/topology/types";
import { DEFAULT_TOPOLOGY_CONFIG } from "@/lib/topology/types";

// ─── Convert LabTopologyData → React Flow nodes/edges ───
function topologyToFlow(
  data: LabTopologyData,
): { nodes: Node[]; edges: Edge[] } {
  // Layout positions for common topologies
  const layouts: Record<string, { x: number; y: number }[]> = {
    // 2-node line (Lab 1)
    "junos-cli-basics": [
      { x: 0, y: 0 },
      { x: 0, y: 160 },
    ],
    // 3-node triangle (Labs 2, 4)
    "ospf-adjacency": [
      { x: 0, y: 0 },
      { x: -120, y: 160 },
      { x: 120, y: 160 },
    ],
    "isis-single-level": [
      { x: 0, y: 0 },
      { x: -120, y: 160 },
      { x: 120, y: 160 },
    ],
    // 3-node line (Labs 3, 5)
    "ebgp-peering": [
      { x: -160, y: 80 },
      { x: 0, y: 80 },
      { x: 160, y: 80 },
    ],
    "mpls-lsp": [
      { x: -160, y: 80 },
      { x: 0, y: 80 },
      { x: 160, y: 80 },
    ],
  };

  // Auto-layout for unrecognised topologies
  const positions =
    layouts[data.labSlug] ??
    data.nodes.map((_, i) => ({
      x: (i - (data.nodes.length - 1) / 2) * 180,
      y: Math.floor(i / 4) * 160,
    }));

  const nodes: Node[] = data.nodes.map((nd, i) => ({
    id: nd.label,
    type: nd.type,
    position: positions[i] ?? { x: i * 120, y: i * 120 },
    data: nd satisfies DeviceNodeData,
    draggable: true,
  }));

  const edges: Edge[] = data.edges.map((ed: TopologyEdgeData, i) => ({
    id: `e-${i}`,
    source: ed.sourceNode,
    target: ed.targetNode,
    type: "connector",
    data: {
      label: ed.label,
      status: ed.status,
      sourceInterface: ed.sourceInterface,
      targetInterface: ed.targetInterface,
      protocol: ed.protocol,
      metric: ed.metric,
      bandwidth: ed.bandwidth,
    } satisfies ConnectorEdgeData,
    animated: ed.status === "traffic",
  }));

  return { nodes, edges };
}

// ─── Status Legend ───
const statusLegendItems = [
  { label: "Up / Active", color: "#22c55e" },
  { label: "Traffic", color: "#3b82f6" },
  { label: "Warning", color: "#f59e0b" },
  { label: "Down", color: "#ef4444" },
  { label: "Unknown", color: "#94a3b8" },
] as const;

// ─── WebSocket status indicator ───
function WsIndicator({ connected }: { connected: boolean }) {
  return (
    <div className="flex items-center gap-1.5 text-[10px] font-mono">
      <div
        className={`w-1.5 h-1.5 rounded-full ${
          connected ? "bg-emerald-500" : "bg-red-500"
        }`}
      />
      <span style={{ color: "var(--svg-text-secondary, #94a3b8)" }}>
        {connected ? "WS Connected" : "WS Disconnected"}
      </span>
    </div>
  );
}

// ─── Toolbar Button ───
function ToolBtn({
  icon: Icon,
  active,
  onClick,
  title,
}: {
  icon: React.ElementType;
  active?: boolean;
  onClick: () => void;
  title: string;
}) {
  return (
    <button
      onClick={onClick}
      title={title}
      className={`p-1.5 rounded-md transition-all duration-150 hover:scale-105 active:scale-95 ${
        active
          ? "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400"
          : "bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
      }`}
    >
      <Icon className="h-3.5 w-3.5" weight={active ? "fill" : "regular"} />
    </button>
  );
}

// ─── Device Node Summary ───
function DeviceSummary({ nodes }: { nodes: Node<DeviceNodeData>[] }) {
  const counts = useMemo(() => {
    const byStatus: Record<string, number> = {};
    const byType: Record<string, number> = {};
    nodes.forEach((n) => {
      byStatus[n.data.status] = (byStatus[n.data.status] ?? 0) + 1;
      byType[n.data.type] = (byType[n.data.type] ?? 0) + 1;
    });
    return { byStatus, byType };
  }, [nodes]);

  return (
    <div className="flex flex-wrap gap-3 text-[10px] font-mono">
      {Object.entries(counts.byStatus).map(([status, count]) => (
        <span key={status} className="flex items-center gap-1">
          <div
            className="w-1.5 h-1.5 rounded-full"
            style={{
              background:
                status === "up"
                  ? "#22c55e"
                  : status === "warning"
                    ? "#f59e0b"
                    : status === "down"
                      ? "#ef4444"
                      : "#94a3b8",
            }}
          />
          {count} {status}
        </span>
      ))}
    </div>
  );
}

// ─── InteractiveTopology Component ───
interface InteractiveTopologyProps {
  topologyData: LabTopologyData;
  onNodeClick?: (nodeId: string) => void;
  onEdgeClick?: (edgeId: string) => void;
  className?: string;
}

function InteractiveTopologyInner({
  topologyData,
  onNodeClick,
  onEdgeClick,
  className = "",
}: InteractiveTopologyProps) {
  const [config, setConfig] = useState<TopologyConfig>(DEFAULT_TOPOLOGY_CONFIG);
  const [wsConnected, setWsConnected] = useState(false);
  const [showLegend, setShowLegend] = useState(true);
  const [showSummary, setShowSummary] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reactFlowRef = useRef<HTMLDivElement>(null);

  // Convert topology data to React Flow nodes/edges
  const initialFlow = useMemo(
    () => topologyToFlow(topologyData),
    [topologyData],
  );
  const [nodes, setNodes, onNodesChange] = useNodesState(initialFlow.nodes as Node[]);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialFlow.edges as Edge[]);

  // WebSocket connection
  useEffect(() => {
    if (!topologyData.wsEndpoint) return;

    const ws = new WebSocket(topologyData.wsEndpoint);
    wsRef.current = ws;

    ws.onopen = () => setWsConnected(true);
    ws.onclose = () => setWsConnected(false);
    ws.onerror = () => setWsConnected(false);

    ws.onmessage = (event) => {
      try {
        const update: TopologyUpdate = JSON.parse(event.data);
        handleTopologyUpdate(update);
      } catch {
        // ignore malformed messages
      }
    };

    return () => {
      ws.close();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topologyData.wsEndpoint]);

  const handleTopologyUpdate = useCallback(
    (update: TopologyUpdate) => {
      switch (update.type) {
        case "node_status":
          setNodes((nds: Node[]) =>
            nds.map((n: Node) =>
              n.id === update.data.nodeId
                ? {
                    ...n,
                    data: {
                      ...n.data,
                      status: (update.data
                        .status as DeviceStatus) ?? n.data.status,
                      interfaces:
                        update.data.interfaces ?? n.data.interfaces,
                    },
                  }
                : n,
            ),
          );
          break;
        case "node_metrics":
          setNodes((nds: Node[]) =>
            nds.map((n: Node) =>
              n.id === update.data.nodeId
                ? {
                    ...n,
                    data: {
                      ...n.data,
                      cpu: update.data.cpu ?? n.data.cpu,
                      memory: update.data.memory ?? n.data.memory,
                    },
                  }
                : n,
            ),
          );
          break;
        case "edge_status":
          setEdges((eds: Edge[]) =>
            eds.map((e: Edge) =>
              e.id === update.data.edgeId
                ? {
                    ...e,
                    data: {
                      ...e.data,
                      status: (update.data
                        .status as LinkStatus) ?? e.data?.status,
                    },
                    animated: update.data.status === "traffic",
                  }
                : e,
            ),
          );
          break;
        case "full_sync":
          // Full topology reload from server
          if (update.data) {
            // Full sync replaces everything
          }
          break;
      }
    },
    [setNodes, setEdges],
  );

  const onNodeClickHandler = useCallback(
    (_: React.MouseEvent, node: Node) => {
      onNodeClick?.(node.id);
    },
    [onNodeClick],
  );

  const onEdgeClickHandler = useCallback(
    (_: React.MouseEvent, edge: Edge) => {
      onEdgeClick?.(edge.id);
    },
    [onEdgeClick],
  );

  const fitView = useCallback(() => {
    const rf = document.querySelector(".react-flow");
    if (rf) {
      const event = new CustomEvent("reactflow-fitview");
      rf.dispatchEvent(event);
    }
  }, []);

  const toggleTraffic = useCallback(() => {
    setConfig((c) => {
      const newTraffic = !c.showTraffic;
      setEdges((eds: Edge[]) =>
        eds.map((e: Edge) => ({
          ...e,
          animated: newTraffic ? e.data?.status === "traffic" : false,
        })),
      );
      return { ...c, showTraffic: newTraffic };
    });
  }, [setEdges]);

  const toggleLabels = useCallback(() => {
    setConfig((c) => ({ ...c, showLabels: !c.showLabels }));
  }, []);

  const toggleMinimap = useCallback(() => {
    setConfig((c) => ({ ...c, showMinimap: !c.showMinimap }));
  }, []);

  return (
    <div
      ref={reactFlowRef}
      className={`relative w-full h-full min-h-[400px] rounded-xl overflow-hidden border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950 ${className}`}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClickHandler}
        onEdgeClick={onEdgeClickHandler}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.3}
        maxZoom={2.5}
        defaultEdgeOptions={{
          type: "connector",
          style: { transition: "all 0.3s ease" },
        }}
        panOnDrag
        selectNodesOnDrag={false}
        selectionOnDrag
        nodesDraggable
        nodesFocusable
        edgesFocusable
        deleteKeyCode={null}
        className="bg-zinc-50 dark:bg-zinc-950"
      >
        <Background
          variant={BackgroundVariant.Dots}
          gap={20}
          size={1}
          color="var(--svg-line, #475569)"
          style={{ opacity: 0.15 }}
        />

        {/* Minimap */}
        {config.showMinimap && (
          <MiniMap
            nodeStrokeColor={(n) =>
              n.data?.status === "down"
                ? "#ef4444"
                : n.data?.status === "warning"
                  ? "#f59e0b"
                  : "#22c55e"
            }
            nodeColor={(n) =>
              n.data?.status === "down"
                ? "rgba(239, 68, 68, 0.3)"
                : n.data?.status === "warning"
                  ? "rgba(245, 158, 11, 0.3)"
                  : "rgba(34, 197, 94, 0.3)"
            }
            maskColor="rgba(0, 0, 0, 0.08)"
            style={{ background: "var(--svg-bg-secondary, #1e293b)" }}
            className="!rounded-lg !border !border-zinc-200 dark:!border-zinc-800"
          />
        )}

        <Controls
          className="!rounded-lg !border !border-zinc-200 dark:!border-zinc-800 !bg-white dark:!bg-zinc-900 !shadow-sm"
          showInteractive={false}
        />

        {/* Top Toolbar */}
        <Panel position="top-left" className="flex flex-col gap-2">
          <div className="flex items-center gap-1.5 p-1.5 rounded-lg bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 shadow-sm">
            <ToolBtn
              icon={config.showTraffic ? WifiHigh : WifiSlash}
              active={config.showTraffic}
              onClick={toggleTraffic}
              title={config.showTraffic ? "Hide traffic" : "Show traffic"}
            />
            <div className="w-px h-4 bg-zinc-200 dark:bg-zinc-700" />
            <ToolBtn
              icon={config.showLabels ? Eye : EyeSlash}
              active={config.showLabels}
              onClick={toggleLabels}
              title={config.showLabels ? "Hide labels" : "Show labels"}
            />
            <div className="w-px h-4 bg-zinc-200 dark:bg-zinc-700" />
            <ToolBtn
              icon={MapPin}
              onClick={fitView}
              title="Fit view"
            />
            <ToolBtn
              icon={config.showMinimap ? MapPin : ArrowsOut}
              active={config.showMinimap}
              onClick={toggleMinimap}
              title={
                config.showMinimap ? "Hide minimap" : "Show minimap"
              }
            />
          </div>

          {/* WebSocket + Summary */}
          {topologyData.wsEndpoint && (
            <div className="flex items-center gap-2 p-1.5 rounded-lg bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 shadow-sm">
              <WsIndicator connected={wsConnected} />
              <div className="w-px h-3 bg-zinc-200 dark:bg-zinc-700" />
              <button
                onClick={() => setShowSummary(!showSummary)}
                className="flex items-center gap-1 text-[10px] font-mono text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
              >
                {nodes.filter((n) => n.data?.status === "down").length > 0 ? (
                  <div className="flex items-center gap-1">
                    <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                    <span>
                      {nodes.filter((n) => n.data?.status === "down").length}{" "}
                      down
                    </span>
                  </div>
                ) : (
                  <span>All online</span>
                )}
              </button>
            </div>
          )}

          {/* Summary Panel (collapsible) */}
          <AnimatePresence>
            {showSummary && (
              <motion.div
                initial={{ opacity: 0, y: -8, height: 0 }}
                animate={{ opacity: 1, y: 0, height: "auto" }}
                exit={{ opacity: 0, y: -8, height: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="p-2 rounded-lg bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 shadow-sm">
                  <DeviceSummary nodes={nodes as Node<DeviceNodeData>[]} />
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </Panel>

        {/* Bottom Legend */}
        <Panel position="bottom-left">
          <button
            onClick={() => setShowLegend(!showLegend)}
            className="flex items-center gap-1 text-[10px] text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 mb-1"
          >
            {showLegend ? (
              <CaretDown className="h-3 w-3" />
            ) : (
              <CaretRight className="h-3 w-3" />
            )}
            Legend
          </button>
          <AnimatePresence>
            {showLegend && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 8 }}
                transition={{ duration: 0.15 }}
                className="flex flex-wrap gap-2 p-2 rounded-lg bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 shadow-sm"
              >
                {statusLegendItems.map((item) => (
                  <div
                    key={item.label}
                    className="flex items-center gap-1.5 text-[10px] font-mono"
                    style={{ color: "var(--svg-text-secondary, #94a3b8)" }}
                  >
                    <div
                      className="w-2 h-2 rounded-full"
                      style={{ background: item.color }}
                    />
                    {item.label}
                  </div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </Panel>

        {/* Lab Title */}
        <Panel position="top-right">
          <div className="px-3 py-1.5 rounded-lg bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 shadow-sm">
            <h3 className="text-xs font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
              {topologyData.title}
            </h3>
          </div>
        </Panel>
      </ReactFlow>
    </div>
  );
}

// ─── Wrapper with ReactFlowProvider ───
export default function InteractiveTopology(
  props: InteractiveTopologyProps,
) {
  return (
    <ReactFlowProvider>
      <InteractiveTopologyInner {...props} />
    </ReactFlowProvider>
  );
}
