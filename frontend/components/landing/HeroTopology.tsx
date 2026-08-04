"use client";

import { useEffect } from "react";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";

const nodes = [
  { id: "core", x: 50, y: 50, type: "router", label: "CORE" },
  { id: "edge1", x: 20, y: 20, type: "switch", label: "EDGE-1" },
  { id: "edge2", x: 80, y: 20, type: "switch", label: "EDGE-2" },
  { id: "edge3", x: 20, y: 80, type: "switch", label: "EDGE-3" },
  { id: "edge4", x: 80, y: 80, type: "switch", label: "EDGE-4" },
];

const edges = [
  { from: "core", to: "edge1" },
  { from: "core", to: "edge2" },
  { from: "core", to: "edge3" },
  { from: "core", to: "edge4" },
];

export function HeroTopology({ className }: { className?: string }) {
  const time = useMotionValue(0);
  const pulse = useSpring(time, { stiffness: 100, damping: 15 });

  // Auto-animate time
  useEffect(() => {
    const start = Date.now();
    const frame = () => {
      time.set((Date.now() - start) / 1000);
      requestAnimationFrame(frame);
    };
    frame();
  }, [time]);

  return (
    <div className={`relative w-full h-full ${className ?? ""}`} aria-hidden="true">
      <motion.svg
        viewBox="0 0 100 100"
        className="w-full h-full"
        preserveAspectRatio="xMidYMid meet"
        style={{ filter: "drop-shadow(0 0 40px rgba(16,185,129,0.15))" }}
      >
        <defs>
          <linearGradient id="link-active" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="var(--svg-line-active)" stopOpacity="0.6" />
            <stop offset="50%" stopColor="var(--svg-line-accent)" stopOpacity="0.9" />
            <stop offset="100%" stopColor="var(--svg-line-active)" stopOpacity="0.6" />
          </linearGradient>
          <filter id="node-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="particle-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Animated connection lines */}
        {edges.map((edge, i) => {
          const from = nodes.find(n => n.id === edge.from)!;
          const to = nodes.find(n => n.id === edge.to)!;
          const midX = (from.x + to.x) / 2;
          const midY = (from.y + to.y) / 2;
          
          return (
            <motion.path
              key={edge.from + "-" + edge.to}
              d={`M${from.x} ${from.y} Q${midX} ${midY} ${to.x} ${to.y}`}
              stroke="url(#link-active)"
              strokeWidth={2}
              strokeLinecap="round"
              fill="none"
              style={{ 
                filter: "url(#node-glow)",
                strokeDasharray: "8 4",
              }}
              animate={{ 
                strokeDashoffset: [0, -20],
                pathLength: [0, 1]
              }}
              transition={{ 
                duration: 2, 
                repeat: Infinity, 
                ease: "linear", 
                delay: i * 0.2 
              }}
            />
          );
        })}

        {/* Nodes with pulse rings */}
        {nodes.map((node, i) => (
          <g key={node.id} filter="url(#node-glow)">
            {/* Outer pulse ring - multiple rings for depth */}
            <motion.circle
              cx={node.x} cy={node.y} r={12}
              stroke="var(--svg-line-active)"
              strokeWidth={1.5}
              fill="none"
              animate={{ 
                r: [10, 18], 
                opacity: [0.5, 0],
                strokeWidth: [1.5, 0.5]
              }}
              transition={{ duration: 3, repeat: Infinity, delay: i * 0.4, ease: "easeOut" }}
            />
            <motion.circle
              cx={node.x} cy={node.y} r={12}
              stroke="var(--svg-line-accent)"
              strokeWidth={1}
              fill="none"
              animate={{ 
                r: [12, 20], 
                opacity: [0.3, 0]
              }}
              transition={{ duration: 4, repeat: Infinity, delay: i * 0.4 + 0.5, ease: "easeOut" }}
            />
            {/* Core node */}
            <circle
              cx={node.x} cy={node.y} r={6}
              fill={node.type === "router" ? "var(--svg-device-router)" : "var(--svg-device-switch)"}
              stroke="var(--svg-bg)"
              strokeWidth={2}
            />
            {/* Inner glow */}
            <circle
              cx={node.x} cy={node.y} r={4}
              fill="var(--svg-line-active)"
              opacity={0.3}
              filter="url(#node-glow)"
            />
            {/* Label */}
            <text
              x={node.x} y={node.y + 16}
              textAnchor="middle"
              fontSize="3"
              fill="var(--svg-text-secondary)"
              fontFamily="var(--font-family-mono)"
              style={{ pointerEvents: "none" }}
            >
              {node.label}
            </text>
          </g>
        ))}

        {/* Floating particles with organic motion */}
        {[...Array(15)].map((_, i) => {
          const seedX = (i * 17) % 80 + 10;
          const seedY = (i * 23) % 70 + 15;
          return (
            <motion.circle
              key={`particle-${i}`}
              cx={seedX}
              cy={seedY}
              r={1.5}
              fill="var(--svg-line-accent)"
              opacity={0.5}
              filter="url(#particle-glow)"
              animate={{
                x: [-8, 8],
                y: [-12, 4],
                opacity: [0.2, 0.7, 0.2],
                scale: [0.7, 1.3, 0.7],
                r: [1, 2.5, 1]
              }}
              transition={{
                duration: 4 + i * 0.3,
                repeat: Infinity,
                delay: i * 0.3,
                ease: "easeInOut"
              }}
            />
          );
        })}

        {/* Subtle grid lines for depth */}
        <g stroke="var(--svg-line-active)" strokeWidth="0.3" opacity="0.05">
          {[0, 20, 40, 60, 80, 100].map(v => (
            <line key={`v-${v}`} x1={v} y1={0} x2={v} y2={100} />
          ))}
          {[0, 20, 40, 60, 80, 100].map(v => (
            <line key={`h-${v}`} x1={0} y1={v} x2={100} y2={v} />
          ))}
        </g>
      </motion.svg>
    </div>
  );
}