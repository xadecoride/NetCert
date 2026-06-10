"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { motion } from "framer-motion";
import { CaretDown, SpeakerHigh, SpeakerSlash } from "@phosphor-icons/react";

interface CommandItem {
  cmd: string;
  description: string;
}

interface AnimatedTerminalProps {
  commands: CommandItem[];
  onClose: () => void;
}

/**
 * AnimatedTerminal — интерактивный терминал, который печатает CLI-команды
 * посимвольно с мигающим курсором. После каждой команды выводит
 * ✓-подтверждение. При завершении показывает промпт `$ _`.
 */
// ─── Typing sound effects (Web Audio API) ────────────────────

function playTypingSound() {
  try {
    const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
    const gain = ctx.createGain();
    gain.connect(ctx.destination);

    // Mechanical click: shaped noise burst
    const bufferSize = ctx.sampleRate * 0.025; // 25ms
    const noise = ctx.createBufferSource();
    const buf = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      // Mix of noise + a slight tone for "clack" character
      data[i] = Math.random() * 2 - 1;
    }
    noise.buffer = buf;

    gain.gain.setValueAtTime(0.06, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.025);

    // Band-pass filter to shape the click
    const filter = ctx.createBiquadFilter();
    filter.type = "bandpass";
    filter.frequency.value = 1200 + Math.random() * 400;
    filter.Q.value = 1.5;
    noise.connect(filter);
    filter.connect(gain);

    noise.start();
    noise.stop(ctx.currentTime + 0.03);

    // Cleanup context after sound finishes
    setTimeout(() => ctx.close(), 100);
  } catch {
    // Audio not available — silently skip
  }
}

function playCommandSound() {
  try {
    const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.type = "sine";
    osc.frequency.setValueAtTime(800, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(1200, ctx.currentTime + 0.05);

    gain.gain.setValueAtTime(0.04, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);

    osc.start();
    osc.stop(ctx.currentTime + 0.08);

    setTimeout(() => ctx.close(), 200);
  } catch {
    // Audio not available — silently skip
  }
}

// ─── Component ───────────────────────────────────────────────

export default function AnimatedTerminal({ commands, onClose }: AnimatedTerminalProps) {
  const [buffer, setBuffer] = useState("");
  const [cmdIdx, setCmdIdx] = useState(0);
  const [charPos, setCharPos] = useState(0);
  const [finished, setFinished] = useState(false);
  const [muted, setMuted] = useState(false);
  const audioUnlocked = useRef(false);

  // Unlock AudioContext on first user interaction
  const ensureAudio = useCallback(() => {
    if (!audioUnlocked.current) {
      try {
        const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
        if (ctx.state === "suspended") ctx.resume();
        ctx.close();
      } catch {}
      audioUnlocked.current = true;
    }
  }, []);

  useEffect(() => {
    if (cmdIdx >= commands.length) {
      setFinished(true);
      return;
    }

    const cmd = commands[cmdIdx];
    const fullText = `$ ${cmd.cmd}  # ${cmd.description}\n`;

    if (charPos < fullText.length) {
      const timeout = setTimeout(() => {
        if (!muted) playTypingSound();
        setBuffer((prev) => prev + fullText[charPos]);
        setCharPos((p) => p + 1);
      }, 20 + Math.random() * 15);
      return () => clearTimeout(timeout);
    } else {
      // Command finished — append output and move to next
      if (!muted) playCommandSound();
      setBuffer((prev) => prev + `✓ ${cmd.description}\n\n`);
      const timeout = setTimeout(() => {
        setCmdIdx((i) => i + 1);
        setCharPos(0);
      }, 350);
      return () => clearTimeout(timeout);
    }
  }, [cmdIdx, charPos, commands, muted]);

  const lines = buffer.split("\n");

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      exit={{ opacity: 0, height: 0 }}
      className="overflow-hidden rounded-xl border border-zinc-700/50 mb-4"
    >
      {/* Terminal window chrome */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-zinc-900 border-b border-zinc-700/50">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500/80" />
          <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
          <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
          <span className="ml-2 text-xs text-zinc-500 font-mono">junos-terminal — bash</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              ensureAudio();
              setMuted((m) => !m);
            }}
            className={`p-1 rounded transition-all ${
              muted
                ? "bg-zinc-800 text-zinc-500"
                : "hover:bg-zinc-700 text-zinc-400 hover:text-zinc-200"
            }`}
            title={muted ? "Unmute" : "Mute"}
          >
            {muted ? (
              <SpeakerSlash className="h-3.5 w-3.5" weight="bold" />
            ) : (
              <SpeakerHigh className="h-3.5 w-3.5" weight="bold" />
            )}
          </button>
          <motion.span
            animate={{ opacity: [1, 0.5, 1] }}
            transition={{ repeat: Infinity, duration: 1.5 }}
            className="text-[10px] text-emerald-500/60 font-mono"
          >
            {finished ? "● done" : "● running"}
          </motion.span>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-zinc-700 text-zinc-400 hover:text-zinc-200 transition-all"
          >
            <CaretDown className="h-4 w-4" weight="bold" />
          </button>
        </div>
      </div>

      {/* Terminal content */}
      <div className="bg-black p-4 font-mono text-sm leading-relaxed min-h-[140px] max-h-[400px] overflow-y-auto">
        {lines.map((line, i) => (
          <div key={i} className="whitespace-pre-wrap">
            {line.startsWith("$") ? (
              <span className="text-emerald-400">{line}</span>
            ) : line.startsWith("✓") ? (
              <span className="text-zinc-500 italic">{line}</span>
            ) : line === "" && i === lines.length - 1 && !finished ? (
              <span className="text-zinc-500">&nbsp;</span>
            ) : (
              <span className="text-zinc-500">{line}</span>
            )}
            {/* Blinking cursor on the current line when typing or when idle */}
            {i === lines.length - 1 && !finished && (
              <motion.span
                animate={{ opacity: [1, 0] }}
                transition={{ repeat: Infinity, duration: 0.8 }}
                className="inline-block w-2 h-4 bg-emerald-400 ml-0.5 align-middle"
              />
            )}
          </div>
        ))}
        {finished && (
          <div className="mt-2 flex items-center gap-2">
            <span className="text-emerald-400">$</span>
            <motion.span
              animate={{ opacity: [1, 0] }}
              transition={{ repeat: Infinity, duration: 0.8 }}
              className="inline-block w-2 h-4 bg-emerald-400 align-middle"
            />
          </div>
        )}
      </div>
    </motion.div>
  );
}
