"use client";

import { useEffect, useRef, useCallback } from "react";

interface LabTerminalProps {
  deviceName: string;
  wsUrl: string;
  className?: string;
}

export function LabTerminal({ deviceName, wsUrl, className = "" }: LabTerminalProps) {
  const terminalRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const termRef = useRef<any>(null);
  const cancelledRef = useRef(false);

  const connectWebSocket = useCallback((term: any) => {
    if (!wsUrl) {
      console.warn("[LabTerminal] wsUrl is empty, skipping connection");
      return;
    }

    if (wsRef.current) {
      wsRef.current.close();
    }

    console.log("[LabTerminal] Connecting to", wsUrl);
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("[LabTerminal] WebSocket open");
      if (cancelledRef.current) return;
      term.write(`\r\n\x1b[32m✓ Connected to ${deviceName}\x1b[0m\r\n`);
    };

    ws.onmessage = (event) => {
      if (cancelledRef.current) return;
      if (event.data instanceof Blob) {
        const reader = new FileReader();
        reader.onload = () => {
          if (!cancelledRef.current) {
            const text = reader.result as string;
            term.write(text);
          }
        };
        reader.readAsText(event.data);
      } else {
        term.write(event.data);
      }
    };

    ws.onerror = (err) => {
      console.error("[LabTerminal] WebSocket error", err);
      if (!cancelledRef.current) {
        term.write(`\r\n\x1b[31m⚠ WebSocket connection error\x1b[0m\r\n`);
      }
    };

    ws.onclose = (ev) => {
      console.log("[LabTerminal] WebSocket close", ev.code, ev.reason);
      if (cancelledRef.current) return;
      term.write(`\r\n\x1b[31m✗ Disconnected from ${deviceName}\x1b[0m\r\n`);
      term.write(`\x1b[33mReconnecting in 5 seconds...\x1b[0m\r\n`);
      const timer = setTimeout(() => {
        if (!cancelledRef.current && termRef.current === term) {
          connectWebSocket(term);
        }
      }, 5000);
      (ws as any)._reconnectTimer = timer;
    };
  }, [deviceName, wsUrl]);

  useEffect(() => {
    if (!terminalRef.current) return;

    cancelledRef.current = false;

    let termInstance: any = null;
    let resizeObserver: ResizeObserver | null = null;

    const init = async () => {
      if (cancelledRef.current) return;

      const { Terminal } = await import("@xterm/xterm");
      const { FitAddon } = await import("@xterm/addon-fit");

      if (cancelledRef.current) return;

      const term = new Terminal({
        cursorBlink: true,
        cursorStyle: "block",
        fontSize: 13,
        fontFamily: "'JetBrains Mono', 'Fira Code', 'Courier New', monospace",
        theme: {
          background: "#0d1117",
          foreground: "#c9d1d9",
          cursor: "#58a6ff",
          selectionBackground: "#264f78",
          black: "#484f58",
          red: "#ff7b72",
          green: "#3fb950",
          yellow: "#d29922",
          blue: "#58a6ff",
          magenta: "#bc8cff",
          cyan: "#39c5cf",
          white: "#b1bac4",
          brightBlack: "#6e7681",
          brightRed: "#ffa198",
          brightGreen: "#56d364",
          brightYellow: "#e3b341",
          brightBlue: "#79c0ff",
          brightMagenta: "#d2a8ff",
          brightCyan: "#56d4dd",
          brightWhite: "#f0f6fc",
        },
        allowProposedApi: true,
        cols: 80,
        rows: 24,
      });

      if (cancelledRef.current) {
        term.dispose();
        return;
      }

      termInstance = term;
      termRef.current = term;

      const fitAddon = new FitAddon();
      term.loadAddon(fitAddon);

      const container = terminalRef.current;
      if (!container || cancelledRef.current) {
        term.dispose();
        return;
      }

      term.open(container);
      fitAddon.fit();

      resizeObserver = new ResizeObserver(() => {
        try {
          fitAddon.fit();
        } catch {
          // ignore fit errors during unmount
        }
      });
      resizeObserver.observe(container);

      if (cancelledRef.current) {
        resizeObserver.disconnect();
        term.dispose();
        return;
      }

      term.onData((data: string) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(data);
        }
      });

      connectWebSocket(term);
    };

    init().catch((err) => {
      console.error("Terminal init failed:", err);
    });

    return () => {
      cancelledRef.current = true;
      if (resizeObserver) {
        resizeObserver.disconnect();
      }
      if (wsRef.current) {
        const timer = (wsRef.current as any)._reconnectTimer;
        if (timer) clearTimeout(timer);
        wsRef.current.close();
        wsRef.current = null;
      }
      if (termInstance) {
        termInstance.dispose();
        termInstance = null;
        termRef.current = null;
      }
    };
  }, [connectWebSocket]);

  return (
    <div
      ref={terminalRef}
      className={`w-full h-full overflow-hidden rounded-lg border border-[#30363d] bg-[#0d1117] ${className}`}
      style={{ minHeight: "300px" }}
    />
  );
}
