"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*";

export function TextScramble({
  text,
  className,
  duration = 1.2,
}: {
  text: string;
  className?: string;
  duration?: number;
}) {
  const [display, setDisplay] = useState(text);

  useEffect(() => {
    let frame = 0;
    const totalFrames = Math.round(duration * 30);
    const interval = setInterval(() => {
      frame++;
      const progress = frame / totalFrames;
      const revealed = Math.floor(progress * text.length);
      let output = "";
      for (let i = 0; i < text.length; i++) {
        if (text[i] === " ") {
          output += " ";
        } else if (i < revealed) {
          output += text[i];
        } else {
          output += chars[Math.floor(Math.random() * chars.length)];
        }
      }
      setDisplay(output);
      if (frame >= totalFrames) {
        clearInterval(interval);
        setDisplay(text);
      }
    }, 1000 / 30);
    return () => clearInterval(interval);
  }, [text, duration]);

  return <span className={cn(className)}>{display}</span>;
}
