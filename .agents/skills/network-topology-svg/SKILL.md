---
name: network-topology-svg
description: Senior Network Visualization Engineer. Generates production-quality SVG illustrations for network topologies, protocol flows, CLI output, and interactive diagrams. CSS-variable-driven theming (dark/light), inline React components, and Containerlab-compatible topology rendering.
---

# Network Topology SVG Skill

## 1. CORE PRINCIPLES

### 1.1. Theming (CSS Custom Properties)

All SVGs MUST use CSS custom properties for dark/light theme compatibility:

```css
/* Light theme (default) */
:root {
  --svg-bg: #ffffff;
  --svg-bg-secondary: #f8fafc;
  --svg-text: #0f172a;
  --svg-text-secondary: #475569;
  --svg-line: #94a3b8;
  --svg-line-active: #22c55e;
  --svg-line-down: #ef4444;
  --svg-line-warning: #f59e0b;
  --svg-link-up: #16a34a;
  --svg-link-down: #dc2626;
  --svg-device-router: #1e293b;
  --svg-device-switch: #334155;
  --svg-device-firewall: #dc2626;
  --svg-device-host: #475569;
  --svg-device-server: #6366f1;
  --svg-cloud: #e2e8f0;
  --svg-highlight: #3b82f6;
  --svg-highlight-bg: rgba(59, 130, 246, 0.1);
  --svg-success-bg: rgba(34, 197, 94, 0.1);
  --svg-error-bg: rgba(239, 68, 68, 0.1);
  --svg-terminal-bg: #0f172a;
  --svg-terminal-text: #e2e8f0;
  --svg-terminal-green: #22c55e;
  --svg-terminal-yellow: #eab308;
  --svg-terminal-red: #ef4444;
}

/* Dark theme */
[data-theme="dark"] {
  --svg-bg: #0f172a;
  --svg-bg-secondary: #1e293b;
  --svg-text: #e2e8f0;
  --svg-text-secondary: #94a3b8;
  --svg-line: #475569;
  --svg-line-active: #4ade80;
  --svg-line-down: #f87171;
  --svg-line-warning: #fbbf24;
  --svg-link-up: #4ade80;
  --svg-link-down: #f87171;
  --svg-device-router: #e2e8f0;
  --svg-device-switch: #cbd5e1;
  --svg-device-firewall: #f87171;
  --svg-device-host: #94a3b8;
  --svg-device-server: #818cf8;
  --svg-cloud: #1e293b;
  --svg-highlight: #60a5fa;
  --svg-highlight-bg: rgba(96, 165, 250, 0.15);
  --svg-success-bg: rgba(74, 222, 128, 0.15);
  --svg-error-bg: rgba(248, 113, 113, 0.15);
  --svg-terminal-bg: #000000;
  --svg-terminal-text: #e2e8f0;
  --svg-terminal-green: #4ade80;
  --svg-terminal-yellow: #fbbf24;
  --svg-terminal-red: #f87171;
}
```

## 2. DEVICE ICONS

### 2.1. Router (cRPD / MX / XRv)

```svg
<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Router body -->
  <rect x="8" y="20" width="48" height="28" rx="4" fill="var(--svg-device-router)" opacity="0.9"/>
  <rect x="12" y="24" width="40" height="20" rx="2" fill="var(--svg-bg)" opacity="0.1"/>
  <!-- LED indicators -->
  <circle cx="20" cy="34" r="3" fill="var(--svg-line-active)"/>
  <circle cx="30" cy="34" r="3" fill="var(--svg-line-active)"/>
  <circle cx="40" cy="34" r="3" fill="var(--svg-line-warning)"/>
  <!-- Ports -->
  <rect x="12" y="40" width="6" height="4" rx="1" fill="var(--svg-text-secondary)" opacity="0.5"/>
  <rect x="22" y="40" width="6" height="4" rx="1" fill="var(--svg-text-secondary)" opacity="0.5"/>
  <rect x="32" y="40" width="6" height="4" rx="1" fill="var(--svg-text-secondary)" opacity="0.5"/>
  <!-- Label -->
  <text x="32" y="56" text-anchor="middle" fill="var(--svg-text)" font-size="6" font-family="Geist Mono, monospace">{label}</text>
  <!-- Antenna/rack ears -->
  <rect x="4" y="22" width="4" height="24" rx="1" fill="var(--svg-device-router)" opacity="0.6"/>
  <rect x="56" y="22" width="4" height="24" rx="1" fill="var(--svg-device-router)" opacity="0.6"/>
</svg>
```

### 2.2. Switch (vQFX / EX)

```svg
<svg viewBox="0 0 64 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="12" width="52" height="24" rx="3" fill="var(--svg-device-switch)" opacity="0.9"/>
  <!-- Port row -->
  <g opacity="0.7">
    <rect x="10" y="18" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="17" y="18" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="24" y="18" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="31" y="18" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="38" y="18" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="45" y="18" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="10" y="24" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="17" y="24" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="24" y="24" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="31" y="24" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="38" y="24" width="5" height="4" rx="1" fill="var(--svg-text)"/>
    <rect x="45" y="24" width="5" height="4" rx="1" fill="var(--svg-text)"/>
  </g>
  <!-- LED row -->
  <circle cx="12" cy="30" r="1.5" fill="var(--svg-link-up)"/>
  <circle cx="19" cy="30" r="1.5" fill="var(--svg-link-up)"/>
  <circle cx="26" cy="30" r="1.5" fill="var(--svg-link-up)"/>
  <circle cx="33" cy="30" r="1.5" fill="var(--svg-link-up)"/>
  <circle cx="40" cy="30" r="1.5" fill="var(--svg-link-down)"/>
  <circle cx="47" cy="30" r="1.5" fill="var(--svg-link-up)"/>
  <!-- Label -->
  <text x="32" y="42" text-anchor="middle" fill="var(--svg-text)" font-size="5" font-family="Geist Mono, monospace">{label}</text>
</svg>
```

### 2.3. Firewall (SRX / vSRX)

```svg
<svg viewBox="0 0 64 56" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="16" width="44" height="28" rx="4" fill="var(--svg-device-firewall)" opacity="0.85"/>
  <!-- Shield icon overlay -->
  <path d="M32 20l-8 4v6c0 6.67 3.33 10 8 12 4.67-2 8-5.33 8-12v-6l-8-4z" fill="var(--svg-bg)" opacity="0.9"/>
  <path d="M32 23l-5 2.5v4.5c0 4.67 2.33 7 5 8.5 2.67-1.5 5-3.83 5-8.5v-4.5L32 23z" fill="var(--svg-device-firewall)"/>
  <!-- Checkmark -->
  <path d="M28 30l3 3 5-5" stroke="var(--svg-bg)" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Label -->
  <text x="32" y="52" text-anchor="middle" fill="var(--svg-text)" font-size="5" font-family="Geist Mono, monospace">{label}</text>
</svg>
```

### 2.4. Host / Server / PC

```svg
<svg viewBox="0 0 48 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Monitor -->
  <rect x="4" y="4" width="40" height="28" rx="3" fill="var(--svg-device-host)" opacity="0.8"/>
  <rect x="8" y="8" width="32" height="20" rx="2" fill="var(--svg-terminal-bg)"/>
  <rect x="8" y="8" width="32" height="20" rx="2" fill="var(--svg-highlight-bg)" opacity="0.3"/>
  <!-- Screen content (CLI) -->
  <text x="12" y="16" fill="var(--svg-terminal-green)" font-size="3.5" font-family="Geist Mono, monospace">root@host:~$</text>
  <!-- Stand -->
  <rect x="18" y="32" width="12" height="3" rx="1" fill="var(--svg-device-host)" opacity="0.7"/>
  <rect x="14" y="35" width="20" height="2" rx="1" fill="var(--svg-device-host)" opacity="0.6"/>
  <!-- Keyboard -->
  <rect x="10" y="40" width="28" height="8" rx="2" fill="var(--svg-device-host)" opacity="0.5"/>
  <g opacity="0.4">
    <rect x="13" y="42" width="3" height="2" rx="0.5" fill="var(--svg-text)"/>
    <rect x="18" y="42" width="3" height="2" rx="0.5" fill="var(--svg-text)"/>
    <rect x="23" y="42" width="3" height="2" rx="0.5" fill="var(--svg-text)"/>
    <rect x="13" y="45" width="3" height="2" rx="0.5" fill="var(--svg-text)"/>
    <rect x="18" y="45" width="3" height="2" rx="0.5" fill="var(--svg-text)"/>
    <rect x="23" y="45" width="3" height="2" rx="0.5" fill="var(--svg-text)"/>
  </g>
  <!-- Label -->
  <text x="24" y="56" text-anchor="middle" fill="var(--svg-text)" font-size="5" font-family="Geist Mono, monospace">{label}</text>
</svg>
```

### 2.5. Cloud / Internet

```svg
<svg viewBox="0 0 80 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <g opacity="0.8">
    <ellipse cx="40" cy="28" rx="28" ry="12" fill="var(--svg-cloud)"/>
    <path d="M24 28 Q24 18 34 18 Q36 10 46 12 Q56 10 56 20 Q64 22 62 30 Q56 36 40 36 Q28 36 24 28Z" fill="var(--svg-cloud)" stroke="var(--svg-text-secondary)" stroke-width="1"/>
  </g>
  <text x="40" y="32" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="6" font-family="Geist Mono, monospace" opacity="0.6">INTERNET</text>
  <text x="40" y="46" text-anchor="middle" fill="var(--svg-text)" font-size="5" font-family="Geist Mono, monospace">{label}</text>
</svg>
```

## 3. LINK TYPES (Edges)

### 3.1. Link Solid (Up/Active)
```svg
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
  stroke="var(--svg-line-active)" stroke-width="2.5" 
  stroke-linecap="round"/>
```

### 3.2. Link Dashed (Down/Inactive)
```svg
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
  stroke="var(--svg-line-down)" stroke-width="2" 
  stroke-dasharray="6,4" stroke-linecap="round"/>
```

### 3.3. Link with Traffic Animation (Animated Dashed)
```svg
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
  stroke="var(--svg-highlight)" stroke-width="3" 
  stroke-dasharray="8,4" stroke-linecap="round">
  <animate attributeName="stroke-dashoffset" from="24" to="0" dur="1s" repeatCount="indefinite"/>
</line>
```

### 3.4. Link Label
```svg
<text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 6}" 
  text-anchor="middle" fill="var(--svg-text-secondary)" 
  font-size="4" font-family="Geist Mono, monospace">
  {interface}  |  {protocol}
</text>
```

## 4. COMPLETE TOPOLOGY TEMPLATE

### 4.1. Simple 3-Router Topology (OSPF Example)

```svg
<svg viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <!-- Background -->
  <rect width="400" height="300" fill="var(--svg-bg)" rx="8"/>
  
  <style>
    @keyframes trafficFlow {
      from { stroke-dashoffset: 24; }
      to { stroke-dashoffset: 0; }
    }
    .traffic { animation: trafficFlow 1s linear infinite; }
  </style>

  <!-- Connections -->
  <!-- R1 to R2 (ge-0/0/0) -->
  <line x1="80" y1="150" x2="200" y2="100" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/>
  <text x="140" y="115" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">ge-0/0/0 | OSPF</text>

  <!-- R2 to R3 (ge-0/0/1) -->
  <line x1="200" y1="100" x2="320" y2="150" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round" class="traffic" stroke-dasharray="8,4"/>
  <text x="260" y="115" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">ge-0/0/1 | OSPF</text>

  <!-- R1 to R3 (Backup link - dashed) -->
  <line x1="80" y1="150" x2="320" y2="150" stroke="var(--svg-line-down)" stroke-width="1.5" stroke-dasharray="6,4" stroke-linecap="round"/>
  <text x="200" y="145" text-anchor="middle" fill="var(--svg-line-down)" font-size="4" font-family="Geist Mono, monospace">ge-0/0/2 | BACKUP (DOWN)</text>

  <!-- R1 Router -->
  <g transform="translate(40, 110)">
    <rect x="0" y="0" width="40" height="28" rx="4" fill="var(--svg-device-router)" opacity="0.9"/>
    <circle cx="10" cy="10" r="3" fill="var(--svg-line-active)"/>
    <circle cx="20" cy="10" r="3" fill="var(--svg-line-active)"/>
    <circle cx="30" cy="10" r="3" fill="var(--svg-line-active)"/>
    <text x="20" y="22" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">R1</text>
  </g>

  <!-- R2 Router -->
  <g transform="translate(180, 60)">
    <rect x="0" y="0" width="40" height="28" rx="4" fill="var(--svg-device-router)" opacity="0.9"/>
    <circle cx="10" cy="10" r="3" fill="var(--svg-line-active)"/>
    <circle cx="20" cy="10" r="3" fill="var(--svg-line-active)"/>
    <circle cx="30" cy="10" r="3" fill="var(--svg-line-warning)"/>
    <text x="20" y="22" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">R2</text>
  </g>

  <!-- R3 Router -->
  <g transform="translate(300, 110)">
    <rect x="0" y="0" width="40" height="28" rx="4" fill="var(--svg-device-router)" opacity="0.9"/>
    <circle cx="10" cy="10" r="3" fill="var(--svg-line-active)"/>
    <circle cx="20" cy="10" r="3" fill="var(--svg-line-active)"/>
    <circle cx="30" cy="10" r="3" fill="var(--svg-line-down)"/>
    <text x="20" y="22" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">R3</text>
  </g>

  <!-- Title -->
  <text x="200" y="280" text-anchor="middle" fill="var(--svg-text)" font-size="7" font-family="Geist, sans-serif" font-weight="600">OSPF Topology — Area 0</text>
  <text x="200" y="292" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">R1 (DR) — R2 (BDR) — R3 (DROTHER)</text>
</svg>
```

### 4.2. JNCIE-ENT Topology (Full Lab)

```svg
<svg viewBox="0 0 800 600" fill="none" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect width="800" height="600" fill="var(--svg-bg)" rx="8"/>
  
  <style>
    @keyframes trafficFlow { from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; } }
    .traffic { animation: trafficFlow 1s linear infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    .pulse { animation: pulse 2s ease-in-out infinite; }
  </style>

  <!-- === CORE LAYER === -->
  <rect x="300" y="20" width="200" height="40" rx="6" fill="var(--svg-highlight-bg)"/>
  <text x="400" y="45" text-anchor="middle" fill="var(--svg-highlight)" font-size="8" font-family="Geist, sans-serif" font-weight="600">Core Layer</text>

  <!-- CR1 -->
  <g transform="translate(260, 70)">
    <rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)"/>
    <text x="30" y="16" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">CR1</text>
    <text x="30" y="28" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">cRPD</text>
    <circle cx="8" cy="34" r="2.5" fill="var(--svg-link-up)"/>
    <circle cx="16" cy="34" r="2.5" fill="var(--svg-link-up)"/>
    <circle cx="24" cy="34" r="2.5" fill="var(--svg-link-up)"/>
  </g>
  
  <!-- CR1 ↔ CR2 (IS-IS) -->
  <line x1="320" y1="100" x2="480" y2="100" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/>
  <text x="400" y="95" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">IS-IS L2 | xe-0/0/0</text>

  <!-- CR2 -->
  <g transform="translate(480, 70)">
    <rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)"/>
    <text x="30" y="16" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">CR2</text>
    <text x="30" y="28" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">cRPD</text>
    <circle cx="8" cy="34" r="2.5" fill="var(--svg-link-up)"/>
    <circle cx="16" cy="34" r="2.5" fill="var(--svg-link-up)"/>
  </g>

  <!-- === AGGREGATION LAYER === -->
  <rect x="300" y="130" width="200" height="40" rx="6" fill="var(--svg-highlight-bg)"/>
  <text x="400" y="155" text-anchor="middle" fill="var(--svg-highlight)" font-size="8" font-family="Geist, sans-serif" font-weight="600">Aggregation Layer</text>

  <!-- CR1 → AG1 -->
  <line x1="300" y1="110" x2="260" y2="170" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/>
  <!-- CR2 → AG2 -->
  <line x1="510" y1="110" x2="540" y2="170" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/>

  <!-- AG1 -->
  <g transform="translate(220, 180)">
    <rect x="0" y="0" width="80" height="40" rx="4" fill="var(--svg-device-switch)"/>
    <text x="40" y="16" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">AG1</text>
    <text x="40" y="28" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">vQFX</text>
    <circle cx="10" cy="34" r="2" fill="var(--svg-link-up)"/>
    <circle cx="20" cy="34" r="2" fill="var(--svg-link-up)"/>
    <circle cx="30" cy="34" r="2" fill="var(--svg-link-up)"/>
    <circle cx="70" cy="34" r="2" fill="var(--svg-link-up)"/>
  </g>

  <!-- AG1 ↔ AG2 -->
  <line x1="300" y1="210" x2="500" y2="210" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round" class="traffic" stroke-dasharray="8,4"/>
  <text x="400" y="205" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">MC-LAG ICL | xe-0/0/3</text>

  <!-- AG2 -->
  <g transform="translate(500, 180)">
    <rect x="0" y="0" width="80" height="40" rx="4" fill="var(--svg-device-switch)"/>
    <text x="40" y="16" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">AG2</text>
    <text x="40" y="28" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">vQFX</text>
    <circle cx="10" cy="34" r="2" fill="var(--svg-link-up)"/>
    <circle cx="20" cy="34" r="2" fill="var(--svg-link-up)"/>
    <circle cx="30" cy="34" r="2" fill="var(--svg-link-up)"/>
    <circle cx="70" cy="34" r="2" fill="var(--svg-link-up)"/>
  </g>

  <!-- === ACCESS LAYER === -->
  <rect x="300" y="240" width="200" height="40" rx="6" fill="var(--svg-highlight-bg)"/>
  <text x="400" y="265" text-anchor="middle" fill="var(--svg-highlight)" font-size="8" font-family="Geist, sans-serif" font-weight="600">Access Layer</text>

  <!-- AG1 → AC1 -->
  <line x1="240" y1="220" x2="140" y2="290" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/>
  <!-- AG2 → AC2 -->
  <line x1="560" y1="220" x2="660" y2="290" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/>

  <!-- AC1 -->
  <g transform="translate(100, 300)">
    <rect x="0" y="0" width="80" height="35" rx="4" fill="var(--svg-device-switch)"/>
    <text x="40" y="14" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">AC1</text>
    <text x="40" y="25" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">vQFX</text>
  </g>

  <!-- AC2 -->
  <g transform="translate(620, 300)">
    <rect x="0" y="0" width="80" height="35" rx="4" fill="var(--svg-device-switch)"/>
    <text x="40" y="14" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">AC2</text>
    <text x="40" y="25" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">vQFX</text>
  </g>

  <!-- === SERVICES LAYER === -->
  <rect x="300" y="360" width="200" height="40" rx="6" fill="var(--svg-highlight-bg)"/>
  <text x="400" y="385" text-anchor="middle" fill="var(--svg-highlight)" font-size="8" font-family="Geist, sans-serif" font-weight="600">Services Layer</text>

  <!-- CR1 → SRX -->
  <line x1="290" y1="110" x2="140" y2="400" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/>
  <!-- CR2 → LB -->
  <line x1="540" y1="110" x2="660" y2="400" stroke="var(--svg-line-warning)" stroke-width="2" stroke-dasharray="8,4" stroke-linecap="round" class="pulse"/>

  <!-- SRX -->
  <g transform="translate(90, 410)">
    <rect x="0" y="0" width="100" height="45" rx="6" fill="var(--svg-device-firewall)"/>
    <path d="M50 10l-20 10v15c0 16.67 8.33 20 20 22.5 11.67-2.5 20-5.83 20-22.5V20L50 10z" fill="var(--svg-bg)" opacity="0.9"/>
    <path d="M50 14l-12 6v10c0 11.67 5.83 14 12 15.5 6.67-1.5 12-3.83 12-15.5V20l-12-6z" fill="var(--svg-device-firewall)"/>
    <text x="50" y="38" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">SRX | vSRX</text>
  </g>

  <!-- LB -->
  <g transform="translate(620, 410)">
    <rect x="0" y="0" width="100" height="45" rx="6" fill="var(--svg-device-router)"/>
    <text x="50" y="16" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">LB</text>
    <text x="50" y="28" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">cRPD (emulated)</text>
  </g>

  <!-- CUSTOMERS -->
  <!-- SRX → CUST1 -->
  <line x1="140" y1="455" x2="140" y2="500" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/>
  
  <g transform="translate(100, 510)">
    <rect x="0" y="0" width="80" height="35" rx="4" fill="var(--svg-device-router)"/>
    <text x="40" y="14" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">CUST1</text>
    <text x="40" y="25" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">cRPD</text>
  </g>

  <!-- LB → CUST2 -->
  <line x1="670" y1="455" x2="670" y2="500" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/>

  <g transform="translate(630, 510)">
    <rect x="0" y="0" width="80" height="35" rx="4" fill="var(--svg-device-router)"/>
    <text x="40" y="14" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">CUST2</text>
    <text x="40" y="25" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">cRPD</text>
  </g>

  <!-- ISP EXTERNAL -->
  <g transform="translate(370, 510)">
    <ellipse cx="30" cy="15" rx="30" ry="15" fill="var(--svg-cloud)"/>
    <text x="30" y="20" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="7" font-family="Geist, sans-serif" opacity="0.6">BGP</text>
  </g>
  
  <line x1="400" y1="525" x2="400" y2="560" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/>

  <g transform="translate(360, 560)">
    <rect x="0" y="0" width="80" height="35" rx="4" fill="var(--svg-device-router)"/>
    <text x="40" y="14" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">ISP-1</text>
    <text x="40" y="25" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="4" font-family="Geist Mono, monospace">cRPD</text>
  </g>

  <!-- Title -->
  <text x="400" y="590" text-anchor="middle" fill="var(--svg-text)" font-size="8" font-family="Geist, sans-serif" font-weight="600">JNCIE-ENT Lab Topology</text>
</svg>
```

## 5. PROTOCOL FLOW DIAGRAMS

### 5.1. BGP Finite State Machine

```svg
<svg viewBox="0 0 500 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="500" height="400" fill="var(--svg-bg)" rx="8"/>
  
  <!-- FSM States as rounded rectangles -->
  <!-- IDLE -->
  <g transform="translate(20, 20)">
    <rect width="80" height="40" rx="6" fill="var(--svg-error-bg)" stroke="var(--svg-line-down)" stroke-width="2"/>
    <text x="40" y="26" text-anchor="middle" fill="var(--svg-line-down)" font-size="7" font-family="Geist Mono, monospace">IDLE</text>
  </g>
  
  <!-- CONNECT -->
  <g transform="translate(200, 20)">
    <rect width="100" height="40" rx="6" fill="var(--svg-highlight-bg)" stroke="var(--svg-highlight)" stroke-width="2"/>
    <text x="50" y="26" text-anchor="middle" fill="var(--svg-highlight)" font-size="7" font-family="Geist Mono, monospace">CONNECT</text>
  </g>

  <!-- ACTIVE -->
  <g transform="translate(380, 20)">
    <rect width="100" height="40" rx="6" fill="var(--svg-warning-bg)" stroke="var(--svg-line-warning)" stroke-width="2"/>
    <text x="50" y="26" text-anchor="middle" fill="var(--svg-line-warning)" font-size="7" font-family="Geist Mono, monospace">ACTIVE</text>
  </g>

  <!-- OPENSENT -->
  <g transform="translate(380, 140)">
    <rect width="100" height="40" rx="6" fill="var(--svg-highlight-bg)" stroke="var(--svg-highlight)" stroke-width="2"/>
    <text x="50" y="26" text-anchor="middle" fill="var(--svg-highlight)" font-size="7" font-family="Geist Mono, monospace">OPENSENT</text>
  </g>

  <!-- OPENCONFIRM -->
  <g transform="translate(200, 140)">
    <rect width="110" height="40" rx="6" fill="var(--svg-highlight-bg)" stroke="var(--svg-highlight)" stroke-width="2"/>
    <text x="55" y="26" text-anchor="middle" fill="var(--svg-highlight)" font-size="7" font-family="Geist Mono, monospace">OPENCONFIRM</text>
  </g>

  <!-- ESTABLISHED -->
  <g transform="translate(100, 260)">
    <rect width="140" height="50" rx="8" fill="var(--svg-success-bg)" stroke="var(--svg-line-active)" stroke-width="2.5"/>
    <text x="70" y="30" text-anchor="middle" fill="var(--svg-line-active)" font-size="8" font-family="Geist Mono, monospace" font-weight="bold">ESTABLISHED</text>
  </g>

  <!-- Transitions -->
  <!-- IDLE → CONNECT (Start) -->
  <line x1="100" y1="40" x2="200" y2="40" stroke="var(--svg-text-secondary)" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="150" y="35" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Start</text>

  <!-- CONNECT → ACTIVE (TCP fail) -->
  <line x1="300" y1="40" x2="380" y2="40" stroke="var(--svg-text-secondary)" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="340" y="35" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">TCP fail</text>

  <!-- ACTIVE → CONNECT (Retry) -->
  <path d="M430 60 L430 100 L300 100 L300 60" stroke="var(--svg-text-secondary)" stroke-width="1" stroke-dasharray="4,3" fill="none" marker-end="url(#arrow)"/>
  <text x="365" y="95" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Retry</text>

  <!-- CONNECT → OPENSENT (TCP ok) -->
  <path d="M250 60 L250 100 L430 100 L430 140" stroke="var(--svg-line-active)" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
  <text x="340" y="95" text-anchor="middle" fill="var(--svg-line-active)" font-size="5" font-family="Geist Mono, monospace">TCP estab → Open</text>

  <!-- OPENSENT → OPENCONFIRM -->
  <line x1="380" y1="160" x2="310" y2="160" stroke="var(--svg-line-active)" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="345" y="155" text-anchor="middle" fill="var(--svg-line-active)" font-size="5" font-family="Geist Mono, monospace">Open recv</text>

  <!-- OPENCONFIRM → ESTABLISHED -->
  <line x1="255" y1="180" x2="240" y2="260" stroke="var(--svg-line-active)" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="270" y="225" text-anchor="middle" fill="var(--svg-line-active)" font-size="5" font-family="Geist Mono, monospace">Keepalive recv</text>

  <!-- ESTABLISHED → IDLE (Error) -->
  <path d="M100 285 L50 285 L50 40 L100 40" stroke="var(--svg-line-down)" stroke-width="1.5" stroke-dasharray="6,3" fill="none" marker-end="url(#arrow)"/>
  <text x="30" y="160" text-anchor="middle" fill="var(--svg-line-down)" font-size="5" font-family="Geist Mono, monospace" transform="rotate(-90, 30, 160)">Error / Notification</text>

  <!-- Arrow marker -->
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0 L10 5 L0 10 Z" fill="var(--svg-text-secondary)"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="250" y="380" text-anchor="middle" fill="var(--svg-text)" font-size="9" font-family="Geist, sans-serif" font-weight="600">BGP Finite State Machine</text>
  <text x="250" y="395" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">RFC 4271 — 6 states, 2 timers (ConnectRetry, Hold)</text>
</svg>
```

### 5.2. MPLS LSP Path Display

```svg
<svg viewBox="0 0 600 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="120" fill="var(--svg-bg)" rx="6"/>
  
  <!-- PE1 -->
  <g transform="translate(10, 40)">
    <rect width="70" height="40" rx="4" fill="var(--svg-device-router)"/>
    <text x="35" y="18" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">PE1</text>
    <text x="35" y="30" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="5" font-family="Geist Mono, monospace">Ingress</text>
  </g>

  <!-- P1 -->
  <g transform="translate(140, 40)">
    <rect width="60" height="40" rx="4" fill="var(--svg-device-router)"/>
    <text x="30" y="18" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">P1</text>
    <text x="30" y="30" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="5" font-family="Geist Mono, monospace">LSP</text>
  </g>

  <!-- P2 -->
  <g transform="translate(270, 40)">
    <rect width="60" height="40" rx="4" fill="var(--svg-device-router)"/>
    <text x="30" y="18" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">P2</text>
    <text x="30" y="30" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="5" font-family="Geist Mono, monospace">LSP</text>
  </g>

  <!-- PE2 -->
  <g transform="translate(440, 40)">
    <rect width="70" height="40" rx="4" fill="var(--svg-device-router)"/>
    <text x="35" y="18" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">PE2</text>
    <text x="35" y="30" text-anchor="middle" fill="var(--svg-bg)" opacity="0.6" font-size="5" font-family="Geist Mono, monospace">Egress</text>
  </g>

  <!-- LSP Path (primary) -->
  <line x1="80" y1="60" x2="140" y2="60" stroke="var(--svg-line-active)" stroke-width="3" stroke-linecap="round" class="traffic" stroke-dasharray="10,5"/>
  <line x1="200" y1="60" x2="270" y2="60" stroke="var(--svg-line-active)" stroke-width="3" stroke-linecap="round" class="traffic" stroke-dasharray="10,5"/>
  <line x1="330" y1="60" x2="440" y2="60" stroke="var(--svg-line-active)" stroke-width="3" stroke-linecap="round" class="traffic" stroke-dasharray="10,5"/>

  <!-- LSP Labels -->
  <rect x="90" y="8" width="40" height="18" rx="3" fill="var(--svg-highlight-bg)"/>
  <text x="110" y="20" text-anchor="middle" fill="var(--svg-highlight)" font-size="6" font-family="Geist Mono, monospace">Label 100</text>

  <rect x="220" y="8" width="40" height="18" rx="3" fill="var(--svg-highlight-bg)"/>
  <text x="240" y="20" text-anchor="middle" fill="var(--svg-highlight)" font-size="6" font-family="Geist Mono, monospace">Label 200</text>

  <rect x="350" y="8" width="40" height="18" rx="3" fill="var(--svg-highlight-bg)"/>
  <text x="370" y="20" text-anchor="middle" fill="var(--svg-highlight)" font-size="6" font-family="Geist Mono, monospace">Label 300</text>

  <!-- Ingress Label Operation -->
  <text x="110" y="95" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Push 100</text>
  <!-- Transit Label Operations -->
  <text x="230" y="95" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Swap 100→200</text>
  <text x="360" y="95" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Swap 200→300</text>
  <!-- Egress Label Operation -->
  <text x="480" y="95" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Pop (PHP)</text>

  <!-- Title -->
  <text x="300" y="115" text-anchor="middle" fill="var(--svg-text)" font-size="7" font-family="Geist, sans-serif" font-weight="600">MPLS LSP — Label Swapping (RSVP-TE)</text>
</svg>
```

## 6. CLI TERMINAL OUTPUT

### 6.1. Junos CLI Output

```svg
<svg viewBox="0 0 600 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="200" fill="var(--svg-terminal-bg)" rx="6"/>
  
  <!-- Terminal title bar -->
  <rect x="0" y="0" width="600" height="24" rx="6" fill="var(--svg-terminal-bg)" opacity="0.8"/>
  <rect x="0" y="12" width="600" height="12" fill="var(--svg-terminal-bg)"/>
  
  <!-- Terminal dots -->
  <circle cx="16" cy="12" r="4" fill="#ef4444"/>
  <circle cx="30" cy="12" r="4" fill="#eab308"/>
  <circle cx="44" cy="12" r="4" fill="#22c55e"/>
  
  <text x="300" y="16" text-anchor="middle" fill="var(--svg-terminal-text)" font-size="7" font-family="Geist, sans-serif" opacity="0.6">user@router — Junos CLI</text>

  <!-- CLI content -->
  <text x="16" y="40" fill="var(--svg-terminal-green)" font-size="6" font-family="Geist Mono, monospace">user@R1> show bgp summary</text>
  <text x="16" y="52" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">Groups: 2 Peers: 4 Down peers: 1</text>
  <text x="16" y="62" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.5">Table: inet.0</text>
  <text x="16" y="72" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">---------------------------------------------------------------------</text>
  <text x="16" y="82" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">Peer                 AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State</text>
  <text x="16" y="92" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">10.0.0.1             65001   12450     12500     0      0     2w5d   <tspan fill="var(--svg-terminal-green)" font-weight="bold">Establ</tspan></text>
  <text x="16" y="102" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">10.0.0.2             65001   9800      10020     0      0     1w3d   <tspan fill="var(--svg-terminal-green)" font-weight="bold">Establ</tspan></text>
  <text x="16" y="112" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">10.0.0.3             65002   5200      5400      0      1     2d     <tspan fill="var(--svg-terminal-green)" font-weight="bold">Establ</tspan></text>
  <text x="16" y="122" fill="var(--svg-terminal-yellow)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">10.0.0.4             65002   0         0         0      5     00:12   <tspan fill="var(--svg-terminal-red)" font-weight="bold">Active</tspan></text>
  <text x="16" y="132" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">---------------------------------------------------------------------</text>
  <text x="16" y="142" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">Total peers: 4  Established: 3  Down: 1 <tspan fill="var(--svg-terminal-yellow)">⚠ Last flap: 12 min ago</tspan></text>
  
  <!-- Cursor blinking -->
  <text x="16" y="165" fill="var(--svg-terminal-green)" font-size="6" font-family="Geist Mono, monospace">user@R1></text>
  <rect x="74" y="152" width="2" height="12" fill="var(--svg-terminal-green)" opacity="0.8">
    <animate attributeName="opacity" values="0.8;0;0.8" dur="1s" repeatCount="indefinite"/>
  </rect>

  <!-- Title -->
  <text x="300" y="190" text-anchor="middle" fill="var(--svg-terminal-text)" font-size="6" font-family="Geist, sans-serif" opacity="0.5">show bgp summary — Junos CLI Output</text>
</svg>
```

### 6.2. Cisco IOS CLI Output

```svg
<svg viewBox="0 0 600 220" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="220" fill="var(--svg-terminal-bg)" rx="6"/>
  
  <rect x="0" y="0" width="600" height="24" rx="6" fill="var(--svg-terminal-bg)" opacity="0.8"/>
  <rect x="0" y="12" width="600" height="12" fill="var(--svg-terminal-bg)"/>
  
  <circle cx="16" cy="12" r="4" fill="#ef4444"/>
  <circle cx="30" cy="12" r="4" fill="#eab308"/>
  <circle cx="44" cy="12" r="4" fill="#22c55e"/>
  
  <text x="300" y="16" text-anchor="middle" fill="var(--svg-terminal-text)" font-size="7" font-family="Geist, sans-serif" opacity="0.6">Router# — Cisco IOS CLI</text>

  <!-- CLI content -->
  <text x="16" y="42" fill="var(--svg-terminal-yellow)" font-size="6" font-family="Geist Mono, monospace">Router# show ip ospf neighbor</text>
  <text x="16" y="56" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">Neighbor ID     Pri   State           Dead Time   Address         Interface</text>
  <text x="16" y="68" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">10.0.0.2         1     <tspan fill="var(--svg-terminal-green)" font-weight="bold">FULL/DR</tspan>        00:00:35    192.168.1.2     GigabitEthernet0/0</text>
  <text x="16" y="80" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">10.0.0.3         1     <tspan fill="var(--svg-terminal-green)" font-weight="bold">FULL/BDR</tspan>       00:00:38    192.168.1.3     GigabitEthernet0/0</text>
  <text x="16" y="92" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">10.0.0.4         1     <tspan fill="var(--svg-terminal-yellow)" font-weight="bold">2WAY/DROTHER</tspan>    00:00:40    192.168.1.4     GigabitEthernet0/0</text>
  <text x="16" y="104" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">10.0.0.5         1     <tspan fill="var(--svg-terminal-red)" font-weight="bold">EXSTART/DR</tspan>     00:00:28    192.168.1.5     GigabitEthernet1/0</text>
  <text x="16" y="116" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">---------------------------------------------------------------------</text>
  <text x="16" y="128" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.7">Total neighbors: 4  FULL: 2  Problem: 1 <tspan fill="var(--svg-terminal-red)">⚠ EXSTART</tspan></text>
  
  <!-- Config snippet -->
  <text x="16" y="150" fill="var(--svg-terminal-yellow)" font-size="6" font-family="Geist Mono, monospace">Router# show running-config interface GigabitEthernet0/0</text>
  <text x="16" y="164" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">!</text>
  <text x="16" y="174" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">interface GigabitEthernet0/0</text>
  <text x="16" y="184" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9"> ip address 192.168.1.1 255.255.255.0</text>
  <text x="16" y="194" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9"> ip ospf network broadcast</text>
  <text x="16" y="204" fill="var(--svg-terminal-text)" font-size="5" font-family="Geist Mono, monospace" opacity="0.9">!</text>
</svg>
```

## 7. REACT FLOW COMPATIBLE SVG NODES

When generating SVG for React Flow, use the following pattern:

```tsx
import { Handle, Position, type NodeProps } from '@xyflow/react';

export function NetworkNode({ data, selected }: NodeProps) {
  const { label, type = 'router', interfaces = [], status = 'up' } = data;
  
  const bgColor = status === 'down' ? 'var(--svg-line-down)' 
    : status === 'warning' ? 'var(--svg-line-warning)'
    : 'var(--svg-device-router)';
  
  return (
    <div className={`
      relative px-4 py-3 rounded-lg border-2 min-w-[100px]
      ${selected ? 'border-blue-500 shadow-lg' : 'border-transparent'}
      ${status === 'down' ? 'opacity-60' : ''}
      transition-all duration-200
    `}
      style={{ 
        background: 'var(--svg-bg-secondary)',
        borderColor: selected ? 'var(--svg-highlight)' : 'transparent'
      }}
    >
      <Handle type="target" position={Position.Top} className="!bg-blue-500" />
      
      <div className="flex items-center gap-2">
        {/* Device icon SVG (inline) */}
        <svg width="24" height="24" viewBox="0 0 64 64" className="flex-shrink-0">
          {type === 'router' && <RouterIcon />}
          {type === 'switch' && <SwitchIcon />}
          {type === 'firewall' && <FirewallIcon />}
        </svg>
        <span className="font-mono text-sm font-medium" style={{ color: 'var(--svg-text)' }}>
          {label}
        </span>
      </div>
      
      {/* Status indicator */}
      <div className="flex gap-1 mt-2">
        {interfaces.map((iface: any, i: number) => (
          <div 
            key={i}
            className="w-2 h-2 rounded-full"
            style={{ 
              background: iface.status === 'up' ? 'var(--svg-line-active)' 
                : iface.status === 'down' ? 'var(--svg-line-down)' 
                : 'var(--svg-line-warning)' 
            }}
          />
        ))}
      </div>
      
      <Handle type="source" position={Position.Bottom} className="!bg-blue-500" />
    </div>
  );
}
```

## 8. USAGE GUIDELINES

### 8.1. When to use which SVG template

| Use Case | Template | Notes |
|----------|----------|-------|
| **Question exhibit (topology)** | Section 4 (Complete Topology) | Embed directly in question body. Simple 2-4 device topologies. |
| **Lab workspace overview** | Section 4.2 (JNCIE Topology) | Full 10+ device topology with layers and labels. |
| **Protocol explanation** | Section 5 (Flow Diagrams) | BGP FSM, MPLS LSP, OSPF adjacencies, EVPN routes. |
| **CLI output display** | Section 6 (Terminal SVG) | Show Junos/Cisco show-command output in explanations. |
| **Interactive lab workspace** | Section 7 (React Flow) | Dynamic topology with state-aware nodes. |

### 8.2. Animation Guidelines

| Animation | CSS Class | Use Case |
|-----------|-----------|----------|
| `trafficFlow` | `.traffic` | Active data paths, routing protocol adjacencies |
| `pulse` | `.pulse` | Warning states, flapping interfaces, troubleshooting hints |
| `cursorBlink` | `.cursor` | CLI terminal cursor indication |
| `fadeIn` | `@keyframes fadeIn` | Device appearance on topology load |

### 8.3. Accessibility

- All SVGs must have `xmlns`, `viewBox`, `width`, and `height` attributes
- Add `<title>` and `<desc>` elements for screen readers
- Use `font-family="Geist Mono, monospace"` for technical text
- Use `font-family="Geist, sans-serif"` for headings
- Minimum font size: 4px for technical labels, 6px for readable text
- Maintain minimum 1.5px stroke width for visibility
