import LabTopologyDemo from "@/components/lab/LabTopologyDemo";

export const metadata = {
  title: "Lab Topology Demo — NetCert",
  description: "Interactive React Flow network topology with custom SVG nodes and WebSocket live-updates.",
};

export default function LabDemoPage() {
  return <LabTopologyDemo />;
}
