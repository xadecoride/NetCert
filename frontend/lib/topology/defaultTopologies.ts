import type { LabTopologyData } from "./types";

// ─── Lab 1: JunOS CLI Basics (2 cRPD) ───
export const lab01Topology: LabTopologyData = {
  labId: "lab-01",
  labSlug: "junos-cli-basics",
  title: "JunOS CLI Basics",
  nodes: [
    {
      label: "R1",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.1/30", status: "up" },
        { name: "lo0", ip: "1.1.1.1/32", status: "up" },
      ],
    },
    {
      label: "R2",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.2/30", status: "up" },
        { name: "lo0", ip: "2.2.2.2/32", status: "up" },
      ],
    },
  ],
  edges: [
    {
      sourceNode: "R1",
      targetNode: "R2",
      label: "ge-0/0/0",
      status: "up",
      sourceInterface: "ge-0/0/0",
      targetInterface: "ge-0/0/0",
      bandwidth: "1G",
    },
  ],
  wsEndpoint: "wss://api.netcert.dev/labs/lab-01/ws",
};

// ─── Lab 2: OSPF Adjacency (3 cRPD triangle) ───
export const lab02Topology: LabTopologyData = {
  labId: "lab-02",
  labSlug: "ospf-adjacency",
  title: "OSPF Adjacency",
  nodes: [
    {
      label: "R1",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.1/30", status: "up" },
        { name: "ge-0/0/1", ip: "10.0.13.1/30", status: "up" },
        { name: "lo0", ip: "1.1.1.1/32", status: "up" },
      ],
    },
    {
      label: "R2",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.2/30", status: "up" },
        { name: "ge-0/0/1", ip: "10.0.23.2/30", status: "up" },
        { name: "lo0", ip: "2.2.2.2/32", status: "up" },
      ],
    },
    {
      label: "R3",
      type: "router",
      status: "warning",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.23.3/30", status: "up" },
        { name: "ge-0/0/1", ip: "10.0.13.2/30", status: "warning" },
        { name: "lo0", ip: "3.3.3.3/32", status: "up" },
      ],
    },
  ],
  edges: [
    {
      sourceNode: "R1",
      targetNode: "R2",
      label: "ge-0/0/0",
      status: "up",
      protocol: "OSPF",
      sourceInterface: "ge-0/0/0",
      targetInterface: "ge-0/0/0",
    },
    {
      sourceNode: "R1",
      targetNode: "R3",
      label: "ge-0/0/1",
      status: "up",
      protocol: "OSPF",
      sourceInterface: "ge-0/0/1",
      targetInterface: "ge-0/0/0",
    },
    {
      sourceNode: "R2",
      targetNode: "R3",
      label: "ge-0/0/1",
      status: "down",
      protocol: "OSPF",
      sourceInterface: "ge-0/0/1",
      targetInterface: "ge-0/0/1",
    },
  ],
};

// ─── Lab 3: EBGP Peering (3 cRPD line) ───
export const lab03Topology: LabTopologyData = {
  labId: "lab-03",
  labSlug: "ebgp-peering",
  title: "EBGP Peering",
  nodes: [
    {
      label: "R1",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.1/30", status: "up" },
        { name: "lo0", ip: "1.1.1.1/32", status: "up" },
      ],
    },
    {
      label: "R2",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.2/30", status: "up" },
        { name: "ge-0/0/1", ip: "10.0.23.2/30", status: "up" },
        { name: "lo0", ip: "2.2.2.2/32", status: "up" },
      ],
    },
    {
      label: "R3",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.23.3/30", status: "up" },
        { name: "lo0", ip: "3.3.3.3/32", status: "up" },
      ],
    },
  ],
  edges: [
    {
      sourceNode: "R1",
      targetNode: "R2",
      label: "eth1 | AS 65001↔65002",
      status: "traffic",
      protocol: "EBGP",
      sourceInterface: "ge-0/0/0",
      targetInterface: "ge-0/0/0",
    },
    {
      sourceNode: "R2",
      targetNode: "R3",
      label: "eth1 | AS 65002↔65003",
      status: "up",
      protocol: "EBGP",
      sourceInterface: "ge-0/0/1",
      targetInterface: "ge-0/0/0",
    },
  ],
};

// ─── Lab 4: IS-IS Single-Level (3 cRPD triangle) ───
export const lab04Topology: LabTopologyData = {
  labId: "lab-04",
  labSlug: "isis-single-level",
  title: "IS-IS Level 2",
  nodes: [
    {
      label: "R1",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.1/30", status: "up" },
        { name: "ge-0/0/1", ip: "10.0.13.1/30", status: "up" },
        { name: "lo0", ip: "1.1.1.1/32", status: "up" },
      ],
    },
    {
      label: "R2",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.2/30", status: "up" },
        { name: "ge-0/0/1", ip: "10.0.23.2/30", status: "up" },
        { name: "lo0", ip: "2.2.2.2/32", status: "up" },
      ],
    },
    {
      label: "R3",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.23.3/30", status: "up" },
        { name: "ge-0/0/1", ip: "10.0.13.2/30", status: "up" },
        { name: "lo0", ip: "3.3.3.3/32", status: "up" },
      ],
    },
  ],
  edges: [
    {
      sourceNode: "R1",
      targetNode: "R2",
      label: "ge-0/0/0 | ISO",
      status: "traffic",
      protocol: "IS-IS",
      sourceInterface: "ge-0/0/0",
      targetInterface: "ge-0/0/0",
    },
    {
      sourceNode: "R1",
      targetNode: "R3",
      label: "ge-0/0/1 | ISO",
      status: "traffic",
      protocol: "IS-IS",
      sourceInterface: "ge-0/0/1",
      targetInterface: "ge-0/0/0",
    },
    {
      sourceNode: "R2",
      targetNode: "R3",
      label: "ge-0/0/1 | ISO",
      status: "up",
      protocol: "IS-IS",
      sourceInterface: "ge-0/0/1",
      targetInterface: "ge-0/0/1",
    },
  ],
};

// ─── Lab 5: MPLS LSP (3 cRPD line) ───
export const lab05Topology: LabTopologyData = {
  labId: "lab-05",
  labSlug: "mpls-lsp",
  title: "MPLS LSP with LDP",
  nodes: [
    {
      label: "PE1",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.1/30", status: "up" },
        { name: "lo0", ip: "1.1.1.1/32", status: "up" },
      ],
    },
    {
      label: "P",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.12.2/30", status: "up" },
        { name: "ge-0/0/1", ip: "10.0.23.2/30", status: "up" },
        { name: "lo0", ip: "2.2.2.2/32", status: "up" },
      ],
    },
    {
      label: "PE2",
      type: "router",
      status: "up",
      model: "cRPD",
      interfaces: [
        { name: "ge-0/0/0", ip: "10.0.23.3/30", status: "up" },
        { name: "lo0", ip: "3.3.3.3/32", status: "up" },
      ],
    },
  ],
  edges: [
    {
      sourceNode: "PE1",
      targetNode: "P",
      label: "ge-0/0/0 | MPLS",
      status: "traffic",
      protocol: "LDP",
      sourceInterface: "ge-0/0/0",
      targetInterface: "ge-0/0/0",
    },
    {
      sourceNode: "P",
      targetNode: "PE2",
      label: "ge-0/0/1 | MPLS",
      status: "traffic",
      protocol: "LDP",
      sourceInterface: "ge-0/0/1",
      targetInterface: "ge-0/0/0",
    },
  ],
};

// ─── JNCIE-ENT Full Lab ───
export const jncieEntTopology: LabTopologyData = {
  labId: "lab-jncie-ent",
  labSlug: "jncie-ent",
  title: "JNCIE Enterprise Routing & Switching",
  nodes: [
    { label: "CR1", type: "router", status: "up", model: "cRPD", interfaces: [{ name: "xe-0/0/0", ip: "10.0.1.1/30", status: "up" }, { name: "xe-0/0/1", ip: "10.0.2.1/30", status: "up" }, { name: "lo0", ip: "192.168.255.1/32", status: "up" }] },
    { label: "CR2", type: "router", status: "up", model: "cRPD", interfaces: [{ name: "xe-0/0/0", ip: "10.0.1.2/30", status: "up" }, { name: "xe-0/0/1", ip: "10.0.3.2/30", status: "up" }, { name: "lo0", ip: "192.168.255.2/32", status: "up" }] },
    { label: "AG1", type: "switch", status: "up", model: "vQFX", interfaces: [{ name: "xe-0/0/0", ip: "10.0.2.2/30", status: "up" }, { name: "xe-0/0/1", ip: "10.0.2.3/30", status: "up" }, { name: "xe-0/0/47", ip: "10.0.100.1/30", status: "up" }] },
    { label: "AG2", type: "switch", status: "warning", model: "vQFX", interfaces: [{ name: "xe-0/0/0", ip: "10.0.3.3/30", status: "up" }, { name: "xe-0/0/1", ip: "10.0.3.4/30", status: "warning" }, { name: "xe-0/0/47", ip: "10.0.100.2/30", status: "up" }] },
    { label: "SRX", type: "firewall", status: "up", model: "vSRX", interfaces: [{ name: "ge-0/0/0", ip: "172.16.1.1/30", status: "up" }, { name: "ge-0/0/1", ip: "10.0.99.1/30", status: "up" }] },
    { label: "CUST1", type: "host", status: "up", interfaces: [{ name: "eth0", ip: "172.16.1.2/30", status: "up" }] },
    { label: "ISP-1", type: "cloud", status: "up", interfaces: [{ name: "ge-0/0/0", ip: "203.0.113.1/30", status: "up" }] },
  ],
  edges: [
    { sourceNode: "CR1", targetNode: "CR2", label: "xe-0/0/0", status: "up", protocol: "IS-IS", sourceInterface: "xe-0/0/0", targetInterface: "xe-0/0/0" },
    { sourceNode: "CR1", targetNode: "AG1", label: "xe-0/0/1", status: "up", protocol: "IS-IS", sourceInterface: "xe-0/0/1", targetInterface: "xe-0/0/0" },
    { sourceNode: "CR1", targetNode: "CR2", label: "xe-0/0/0", status: "up", protocol: "LDP", sourceInterface: "xe-0/0/0", targetInterface: "xe-0/0/0" },
    { sourceNode: "CR2", targetNode: "AG2", label: "xe-0/0/1", status: "warning", protocol: "LDP", sourceInterface: "xe-0/0/1", targetInterface: "xe-0/0/1" },
    { sourceNode: "AG1", targetNode: "AG2", label: "ICL", status: "traffic", protocol: "MC-LAG", sourceInterface: "xe-0/0/47", targetInterface: "xe-0/0/47" },
    { sourceNode: "SRX", targetNode: "CUST1", label: "ge-0/0/0", status: "up", protocol: "BGP", sourceInterface: "ge-0/0/0", targetInterface: "eth0" },
    { sourceNode: "SRX", targetNode: "ISP-1", label: "ge-0/0/0", status: "up", protocol: "EBGP", sourceInterface: "ge-0/0/0", targetInterface: "ge-0/0/0" },
  ],
};

// ─── All micro-lab topologies by slug ───
export const topologiesBySlug: Record<string, LabTopologyData> = {
  "junos-cli-basics": lab01Topology,
  "ospf-adjacency": lab02Topology,
  "ebgp-peering": lab03Topology,
  "isis-single-level": lab04Topology,
  "mpls-lsp": lab05Topology,
  "jncie-ent": jncieEntTopology,
};
