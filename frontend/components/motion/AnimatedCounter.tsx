"use client";

import { useEffect, useRef, useState } from "react";
import { useInView, useMotionValue, useSpring } from "framer-motion";
import { cn } from "@/lib/utils";

export function AnimatedCounter({
  value,
  suffix = "",
  prefix = "",
  className,
  duration = 1.5,
}: {
  value: number;
  suffix?: string;
  prefix?: string;
  className?: string;
  duration?: number;
}) {
  const ref = useRef<HTMLSpanElement>(null);
  const motionValue = useMotionValue(0);
  const springValue = useSpring(motionValue, {
    damping: 50,
    stiffness: 100,
    duration: duration * 1000,
  });
  const isInView = useInView(ref, { once: true, margin: "-50px" });
  const [display, setDisplay] = useState<string | null>(null);

  const safeValue = Number.isFinite(value) ? value : 0;

  // Kick off the spring animation once the element enters the viewport.
  useEffect(() => {
    if (isInView) {
      motionValue.set(safeValue);
    }
  }, [isInView, motionValue, safeValue]);

  useEffect(() => {
    const unsubscribe = springValue.on("change", (latest) => {
      const num = Number.isFinite(latest) ? latest : 0;
      setDisplay(Math.round(num).toLocaleString());
    });
    return unsubscribe;
  }, [springValue]);

  // SSR + before in-view: render the final value directly so the first paint
  // shows the real number (e.g. "9,150+") instead of a misleading "0+".
  // Once the spring starts firing changes, `display` takes over with the
  // animated count-up. See CLAUDE.md §7.8 / landing redesign.
  const shown = display ?? Math.round(safeValue).toLocaleString();

  return (
    <span ref={ref} className={cn(className)}>
      {prefix}
      {shown}
      {suffix}
    </span>
  );
}
