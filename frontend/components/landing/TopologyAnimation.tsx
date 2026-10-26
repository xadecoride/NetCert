"use client";

import { useId } from "react";
import { motion, useReducedMotion } from "framer-motion";

/* ─────────────────────────────────────────────────────────────
 * TopologyAnimation — единая анимированная топология сети.
 *
 * Используется на главной странице (hero) и на экранах
 * регистрации/входа, чтобы брендинг выглядел консистентно.
 *
 * Модель сети — классическая трёхуровневая иерархия:
 *   Core (два резервируемых ядра) → PE (двойные аплинки)
 *   → CE (клиентские устройства).
 *
 * Поддерживает prefers-reduced-motion: при включённом режиме
 * цикличные анимации отключаются, остаётся статичная схема.
 * ───────────────────────────────────────────────────────────── */

type NodeKind = "core" | "pe" | "ce";
type LinkKind = "backbone" | "spine" | "access";

interface TopoNode {
  id: string;
  x: number;
  y: number;
  kind: NodeKind;
  label: string;
}

interface TopoLink {
  id: string;
  from: string;
  to: string;
  kind: LinkKind;
}

/* ─── Топологическая модель ─────────────────────────────────── */

const NODES: TopoNode[] = [
  // Core layer — дублированное ядро
  { id: "core-a", x: 38, y: 50, kind: "core", label: "CORE-1" },
  { id: "core-b", x: 62, y: 50, kind: "core", label: "CORE-2" },

  // Provider Edge — маршрутизаторы на границе сети оператора
  { id: "pe-1", x: 19, y: 27, kind: "pe", label: "PE-1" },
  { id: "pe-2", x: 81, y: 27, kind: "pe", label: "PE-2" },
  { id: "pe-3", x: 19, y: 73, kind: "pe", label: "PE-3" },
  { id: "pe-4", x: 81, y: 73, kind: "pe", label: "PE-4" },

  // Customer Edge — клиентские устройства
  { id: "ce-1", x: 9, y: 13, kind: "ce", label: "CE-1" },
  { id: "ce-2", x: 91, y: 13, kind: "ce", label: "CE-2" },
  { id: "ce-3", x: 9, y: 87, kind: "ce", label: "CE-3" },
  { id: "ce-4", x: 91, y: 87, kind: "ce", label: "CE-4" },
];

const LINKS: TopoLink[] = [
  // Backbone — связь между ядрами
  { id: "backbone", from: "core-a", to: "core-b", kind: "backbone" },

  // Spine — двойные аплинки каждого PE к обоим ядрам
  { id: "l1", from: "core-a", to: "pe-1", kind: "spine" },
  { id: "l2", from: "core-b", to: "pe-1", kind: "spine" },
  { id: "l3", from: "core-a", to: "pe-2", kind: "spine" },
  { id: "l4", from: "core-b", to: "pe-2", kind: "spine" },
  { id: "l5", from: "core-a", to: "pe-3", kind: "spine" },
  { id: "l6", from: "core-b", to: "pe-3", kind: "spine" },
  { id: "l7", from: "core-a", to: "pe-4", kind: "spine" },
  { id: "l8", from: "core-b", to: "pe-4", kind: "spine" },

  // Access — подключение клиентских устройств к своим PE
  { id: "a1", from: "pe-1", to: "ce-1", kind: "access" },
  { id: "a2", from: "pe-2", to: "ce-2", kind: "access" },
  { id: "a3", from: "pe-3", to: "ce-3", kind: "access" },
  { id: "a4", from: "pe-4", to: "ce-4", kind: "access" },
];

const nodeById = new Map(NODES.map((n) => [n.id, n]));

/* Пакеты трафика: id линка, направление, задержка */
const PACKETS: Array<{ link: string; reverse?: boolean; delay: number }> = [
  { link: "l1", delay: 0 },
  { link: "l8", reverse: true, delay: 0.6 },
  { link: "a2", delay: 1.2 },
  { link: "l5", delay: 1.8 },
  { link: "a3", reverse: true, delay: 2.4 },
];

/* Статусы устройств (только для PE) */
const STATUS: Record<string, "up" | "warning"> = {
  "pe-1": "up",
  "pe-2": "up",
  "pe-3": "up",
  "pe-4": "warning",
};

/* ─── Утилиты ──────────────────────────────────────────────── */

const hexPoints = (cx: number, cy: number, r: number) =>
  Array.from({ length: 6 }, (_, i) => {
    const angle = (Math.PI / 3) * i - Math.PI / 2;
    return `${(cx + r * Math.cos(angle)).toFixed(2)},${(cy + r * Math.sin(angle)).toFixed(2)}`;
  }).join(" ");

const linkEndpoints = (link: TopoLink) => {
  const from = nodeById.get(link.from)!;
  const to = nodeById.get(link.to)!;
  return { from, to };
};

const pulseRadius = (kind: NodeKind) => (kind === "core" ? 9 : kind === "pe" ? 8 : 6);

/* ─── Вспомогательные компоненты ────────────────────────────── */

function DeviceShape({ node }: { node: TopoNode }) {
  const common = {
    stroke: "var(--svg-line-active)",
    strokeWidth: 0.8,
    fill: node.kind === "ce" ? "var(--svg-line-active)" : "var(--svg-device-switch)",
  };

  switch (node.kind) {
    case "core":
      return (
        <polygon
          points={hexPoints(node.x, node.y, 6.5)}
          fill="var(--svg-device-router)"
          stroke="var(--svg-line-accent)"
          strokeWidth={1}
        />
      );
    case "pe":
      return <rect x={node.x - 4.5} y={node.y - 4.5} width={9} height={9} rx={2.5} {...common} />;
    case "ce":
      return <circle cx={node.x} cy={node.y} r={3.8} {...common} />;
  }
}

function NodeLabel({ node }: { node: TopoNode }) {
  return (
    <text
      x={node.x}
      y={node.y + 12.5}
      textAnchor="middle"
      fontSize="2.8"
      fill="var(--svg-text-secondary)"
      fontFamily="var(--font-family-mono)"
      style={{ pointerEvents: "none" }}
    >
      {node.label}
    </text>
  );
}

/* ─── Основной компонент ────────────────────────────────────── */

export function TopologyAnimation({ className }: { className?: string }) {
  const uid = useId();
  const reduced = useReducedMotion();
  const animated = !reduced;

  const linkGradient = `topo-link-${uid}`;
  const linkGlow = `topo-glow-${uid}`;
  const coreGlow = `topo-core-glow-${uid}`;

  return (
    <div className={className} aria-hidden="true">
      <svg viewBox="0 0 100 100" className="w-full h-full" style={{ pointerEvents: "none" }}>
        <defs>
          <linearGradient id={linkGradient} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="var(--svg-line-active)" stopOpacity="0.25" />
            <stop offset="50%" stopColor="var(--svg-line-active)" stopOpacity="0.9" />
            <stop offset="100%" stopColor="var(--svg-line-active)" stopOpacity="0.25" />
          </linearGradient>

          <filter id={linkGlow} x="-60%" y="-60%" width="220%" height="220%">
            <feGaussianBlur stdDeviation="1.6" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          <filter id={coreGlow} x="-80%" y="-80%" width="260%" height="260%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* ── Фоновая сетка ── */}
        <g stroke="var(--svg-line-active)" strokeWidth="0.25" opacity="0.05">
          {Array.from({ length: 11 }, (_, i) => (
            <g key={i}>
              <line x1={i * 10} y1={0} x2={i * 10} y2={100} />
              <line x1={0} y1={i * 10} x2={100} y2={i * 10} />
            </g>
          ))}
        </g>

        {/* ── Вращающееся кольцо ядра (анимация штриха) ── */}
        <motion.circle
          cx={50}
          cy={50}
          r={31}
          fill="none"
          stroke="var(--svg-line-active)"
          strokeWidth="0.5"
          strokeDasharray="4 6"
          strokeOpacity="0.35"
          {...(animated
            ? { animate: { strokeDashoffset: [0, -40] }, transition: { duration: 60, repeat: Infinity, ease: "linear" } }
            : {})}
        />

        {/* ── Мягкое свечение за ядром ── */}
        <circle cx={50} cy={50} r={24} fill="var(--svg-line-active)" opacity={0.05} filter={`url(#${coreGlow})`} />

        {/* ── Связи ── */}
        {LINKS.map((link, i) => {
          const { from, to } = linkEndpoints(link);
          const strokeWidth = link.kind === "backbone" ? 1.6 : link.kind === "spine" ? 1.1 : 0.8;
          const stroke = link.kind === "backbone" ? "var(--svg-line-accent)" : `url(#${linkGradient})`;
          const dash = link.kind === "backbone" ? undefined : "5 3.5";

          return (
            <motion.line
              key={link.id}
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke={stroke}
              strokeWidth={strokeWidth}
              strokeLinecap="round"
              strokeDasharray={dash}
              {...(animated
                ? {
                    initial: { opacity: 0.45 },
                    animate: { opacity: [0.45, 1, 0.45], strokeDashoffset: [0, -17] },
                    transition: { duration: 3, repeat: Infinity, ease: "easeInOut", delay: 0.2 + i * 0.15 },
                  }
                : { initial: { opacity: 1 } })}
            />
          );
        })}

        {/* ── Пакеты трафика ── */}
        {PACKETS.map((packet, i) => {
          const link = LINKS.find((l) => l.id === packet.link)!;
          const { from, to } = linkEndpoints(link);
          const x1 = packet.reverse ? to.x : from.x;
          const y1 = packet.reverse ? to.y : from.y;
          const x2 = packet.reverse ? from.x : to.x;
          const y2 = packet.reverse ? from.y : to.y;

          return (
            <motion.circle
              key={`packet-${i}`}
              r={1.2}
              fill="var(--svg-line-accent)"
              filter={`url(#${linkGlow})`}
              initial={{ cx: x1, cy: y1, opacity: 0 }}
              {...(animated
                ? {
                    animate: { cx: [x1, x2, x1], cy: [y1, y2, y1], opacity: [0, 1, 0] },
                    transition: { duration: 4.5, repeat: Infinity, ease: "easeInOut", delay: packet.delay },
                  }
                : {})}
            />
          );
        })}

        {/* ── Узлы ── */}
        {NODES.map((node, i) => (
          <g key={node.id}>
            {/* Пульсирующие кольца */}
            {animated && (
              <>
                <motion.circle
                  cx={node.x}
                  cy={node.y}
                  r={pulseRadius(node.kind)}
                  stroke="var(--svg-line-active)"
                  strokeWidth={0.9}
                  fill="none"
                  animate={{ r: [pulseRadius(node.kind), pulseRadius(node.kind) + 6], opacity: [0.5, 0] }}
                  transition={{ duration: 3, repeat: Infinity, delay: i * 0.3, ease: "easeOut" }}
                />
                <motion.circle
                  cx={node.x}
                  cy={node.y}
                  r={pulseRadius(node.kind)}
                  stroke="var(--svg-line-accent)"
                  strokeWidth={0.6}
                  fill="none"
                  animate={{ r: [pulseRadius(node.kind) + 1, pulseRadius(node.kind) + 8], opacity: [0.3, 0] }}
                  transition={{ duration: 4, repeat: Infinity, delay: i * 0.3 + 0.6, ease: "easeOut" }}
                />
              </>
            )}

            {/* Сам узел */}
            <motion.g
              initial={{ opacity: 0, y: -3 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 + i * 0.05, ease: "easeOut" }}
            >
              <DeviceShape node={node} />
              {node.kind === "pe" && (
                <circle
                  cx={node.x + 3.2}
                  cy={node.y - 3.2}
                  r={1.4}
                  fill={STATUS[node.id] === "warning" ? "var(--svg-line-warning)" : "var(--svg-line-active)"}
                />
              )}
            </motion.g>

            <NodeLabel node={node} />
          </g>
        ))}
      </svg>
    </div>
  );
}
