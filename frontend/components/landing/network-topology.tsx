"use client";

import { useId } from "react";
import { motion } from "framer-motion";

const springTransition = { type: "spring", stiffness: 100, damping: 20 };

export function NetworkTopology({ className }: { className?: string }) {
  const id = useId();
  const linkGradientId = `link-gradient-${id}`;
  const glowId = `glow-${id}`;

  return (
    <div className={className}>
      <svg
        viewBox="0 0 400 400"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id={linkGradientId} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="var(--svg-line-active)" stopOpacity="0.3" />
            <stop offset="50%" stopColor="var(--svg-line-active)" stopOpacity="1" />
            <stop offset="100%" stopColor="var(--svg-line-active)" stopOpacity="0.3" />
          </linearGradient>
          <filter id={glowId} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2.5" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Background grid */}
        <g stroke="var(--svg-bg)" strokeWidth="0.5" opacity="0.5">
          {Array.from({ length: 9 }).map((_, i) => (
            <line key={`h-${i}`} x1="0" y1={i * 50} x2="400" y2={i * 50} />
          ))}
          {Array.from({ length: 9 }).map((_, i) => (
            <line key={`v-${i}`} x1={i * 50} y1="0" x2={i * 50} y2="400" />
          ))}
        </g>

        {/* Core ring */}
        <motion.g
          style={{ transformOrigin: "200px 200px" }}
          animate={{ rotate: 360 }}
          transition={{ duration: 60, repeat: Infinity, ease: "linear" }}
        >
          <circle
            cx="200"
            cy="200"
            r="120"
            stroke="var(--svg-line-active)"
            strokeWidth="1"
            strokeDasharray="8 8"
            strokeOpacity="0.25"
            fill="none"
          />
        </motion.g>

        {/* Spine links */}
        <motion.line
          x1="200" y1="80" x2="200" y2="320"
          stroke={`url(#${linkGradientId})`} strokeWidth="2" strokeLinecap="round"
          initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
          transition={{ duration: 1.5, ease: "easeInOut" }}
        />
        <motion.line
          x1="80" y1="200" x2="320" y2="200"
          stroke={`url(#${linkGradientId})`} strokeWidth="2" strokeLinecap="round"
          initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
          transition={{ duration: 1.5, ease: "easeInOut", delay: 0.2 }}
        />
        <motion.line
          x1="115" y1="115" x2="285" y2="285"
          stroke={`url(#${linkGradientId})`} strokeWidth="2" strokeLinecap="round"
          initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
          transition={{ duration: 1.5, ease: "easeInOut", delay: 0.4 }}
        />
        <motion.line
          x1="285" y1="115" x2="115" y2="285"
          stroke={`url(#${linkGradientId})`} strokeWidth="2" strokeLinecap="round"
          initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
          transition={{ duration: 1.5, ease: "easeInOut", delay: 0.6 }}
        />

        {/* Traffic pulses */}
        {[
          { x1: 200, y1: 80, x2: 200, y2: 320, delay: 0 },
          { x1: 80, y1: 200, x2: 320, y2: 200, delay: 1 },
          { x1: 115, y1: 115, x2: 285, y2: 285, delay: 0.5 },
          { x1: 285, y1: 115, x2: 115, y2: 285, delay: 1.5 },
        ].map((link, i) => (
          <motion.circle
            key={`pulse-${i}`}
            r="4"
            fill="var(--svg-line-active)"
            filter={`url(#${glowId})`}
            initial={{ x: link.x1, y: link.y1, opacity: 0 }}
            animate={{ x: [link.x1, link.x2, link.x1], y: [link.y1, link.y2, link.y1], opacity: [0, 1, 0] }}
            transition={{ duration: 3, repeat: Infinity, ease: "linear", delay: link.delay }}
          />
        ))}

        {/* Central router */}
        <motion.g
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ ...springTransition, delay: 0.3 }}
        >
          <rect x="168" y="168" width="64" height="64" rx="16" fill="var(--svg-device-router)" />
          <rect x="168" y="168" width="64" height="64" rx="16" stroke="var(--svg-line-active)" strokeWidth="2" />
          <circle cx="200" cy="200" r="12" fill="var(--svg-line-active)" />
          <text x="200" y="246" textAnchor="middle" fill="var(--svg-text-secondary)" fontSize="10" fontFamily="var(--font-family-mono)">
            CORE
          </text>
        </motion.g>

        {/* Edge routers / switches */}
        {[
          { x: 184, y: 56, label: "PE-1" },
          { x: 320, y: 184, label: "PE-2" },
          { x: 184, y: 320, label: "P-1" },
          { x: 48, y: 184, label: "P-2" },
          { x: 104, y: 104, label: "CE-A" },
          { x: 264, y: 104, label: "CE-B" },
          { x: 104, y: 264, label: "CE-C" },
          { x: 264, y: 264, label: "CE-D" },
        ].map((node, i) => (
          <motion.g
            key={node.label}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ ...springTransition, delay: 0.5 + i * 0.08 }}
          >
            <motion.rect
              x={node.x} y={node.y} width="32" height="32" rx="8"
              fill="var(--svg-device-switch)"
              stroke="var(--svg-line-active)"
              strokeWidth="1.5"
              animate={{ y: [node.y, node.y - 4, node.y] }}
              transition={{ duration: 3 + i * 0.3, repeat: Infinity, ease: "easeInOut" }}
            />
            <text
              x={node.x + 16}
              y={node.y + 46}
              textAnchor="middle"
              fill="var(--svg-text-secondary)"
              fontSize="9"
              fontFamily="var(--font-family-mono)"
            >
              {node.label}
            </text>
          </motion.g>
        ))}

        {/* Status dots */}
        {[
          { cx: 200, cy: 80, status: "up" },
          { cx: 320, cy: 200, status: "up" },
          { cx: 200, cy: 320, status: "up" },
          { cx: 80, cy: 200, status: "warning" },
        ].map((dot, i) => (
          <motion.circle
            key={`status-${i}`}
            cx={dot.cx}
            cy={dot.cy}
            r="4"
            fill={dot.status === "up" ? "var(--svg-line-active)" : "var(--svg-line-warning)"}
            animate={{ scale: [1, 1.3, 1], opacity: [0.7, 1, 0.7] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: i * 0.4 }}
          />
        ))}
      </svg>
    </div>
  );
}
