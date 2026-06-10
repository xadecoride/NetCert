import type { Node, Edge } from "@xyflow/react";

// ─── Device Types ───
export type DeviceType = "router" | "switch" | "firewall" | "host" | "cloud";

export type DeviceStatus = "up" | "down" | "warning" | "unknown";

export type InterfaceStatus = "up" | "down" | "admin-down" | "warning";

export interface TopologyInterface {
  name: string;
  ip: string;
  status: InterfaceStatus;
}

// ─── Device Node Data ───
export interface DeviceNodeData {
  label: string;
  type: DeviceType;
  status: DeviceStatus;
  interfaces: TopologyInterface[];
  model?: string;
  mgmtIp?: string;
  cpu?: number;       // optional load %
  memory?: number;    // optional load %
  isOnline?: boolean;
  [key: string]: unknown;  // index signature for React Flow compatibility
}

export type DeviceNode = Node<DeviceNodeData, "device">;

// ─── Edge Data ───
export type LinkStatus = "up" | "down" | "warning" | "traffic";

export interface ConnectorEdgeData {
  label?: string;
  status: LinkStatus;
  sourceInterface?: string;
  targetInterface?: string;
  protocol?: string;    // "OSPF" | "IS-IS" | "BGP" | "LDP" | "MPLS"
  metric?: number;
  bandwidth?: string;   // "10G" | "1G" | "100M"
  [key: string]: unknown;  // index signature for React Flow compatibility
}

export type ConnectorEdge = Edge<ConnectorEdgeData, "connector">;

// ─── WebSocket Topology Update ───
export interface TopologyUpdate {
  type: "node_status" | "edge_status" | "node_metrics" | "full_sync";
  data: {
    nodeId?: string;
    edgeId?: string;
    status?: DeviceStatus | LinkStatus;
    interfaces?: TopologyInterface[];
    cpu?: number;
    memory?: number;
  };
}

// ─── Layout Presets ───
export type LayoutDirection = "TB" | "LR" | "RL" | "BT";

export interface TopologyConfig {
  direction: LayoutDirection;
  showTraffic: boolean;
  showLabels: boolean;
  showMinimap: boolean;
  showControls: boolean;
  animated: boolean;
  fitView: boolean;
}

export const DEFAULT_TOPOLOGY_CONFIG: TopologyConfig = {
  direction: "TB",
  showTraffic: true,
  showLabels: true,
  showMinimap: true,
  showControls: true,
  animated: true,
  fitView: true,
};

// ─── Edge with source/target node references (serialised from backend) ───
export interface TopologyEdgeData extends ConnectorEdgeData {
  sourceNode: string;
  targetNode: string;
}

// ─── Lab Topology (serialised from backend) ───
export interface LabTopologyData {
  labId: string;
  labSlug: string;
  title: string;
  nodes: DeviceNodeData[];
  edges: TopologyEdgeData[];
  wsEndpoint?: string;
}

// ─── Node Styling Helpers ───
export function statusColor(status: DeviceStatus | InterfaceStatus | LinkStatus): string {
  switch (status) {
    case "up":
    case "traffic":
      return "#22c55e";
    case "down":
    case "admin-down":
      return "#ef4444";
    case "warning":
      return "#f59e0b";
    case "unknown":
    default:
      return "#94a3b8";
  }
}

export function statusLabel(status: DeviceStatus | InterfaceStatus | LinkStatus): string {
  switch (status) {
    case "up":
      return "Up";
    case "down":
      return "Down";
    case "warning":
      return "Warning";
    case "traffic":
      return "Active";
    case "admin-down":
      return "Admin Down";
    case "unknown":
    default:
      return "Unknown";
  }
}
