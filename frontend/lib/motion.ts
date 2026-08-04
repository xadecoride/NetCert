"use client";

import { useEffect, useState } from "react";
import type { Transition, Variants } from "framer-motion";

export const springTransition: Transition = {
  type: "spring",
  stiffness: 100,
  damping: 20,
};

export const springSnappy: Transition = {
  type: "spring",
  stiffness: 300,
  damping: 25,
};

export const heroVariants: Variants = {
  hidden: { opacity: 0, y: 30, scale: 0.98 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.9, ease: [0.16, 1, 0.3, 1] },
  },
};

export const fadeInUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: springTransition,
  },
};

export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.4, ease: [0.16, 1, 0.3, 1] } },
};

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: 0.96 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: springTransition,
  },
};

export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.1,
    },
  },
};

export const staggerFast: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.04,
      delayChildren: 0.02,
    },
  },
};

export const cardHover = {
  rest: { y: 0, boxShadow: "0 20px 40px -15px rgba(0,0,0,0.05)" },
  hover: {
    y: -4,
    boxShadow: "0 30px 60px -20px rgba(0,0,0,0.12)",
    transition: springSnappy,
  },
};

export const accentCardHover = {
  rest: { y: 0, boxShadow: "0 20px 40px -15px rgba(0,0,0,0.05)" },
  hover: {
    y: -4,
    boxShadow: "0 30px 60px -20px rgba(6,182,212,0.18)",
    transition: springSnappy,
  },
};

export const pulseLoop = {
  scale: [1, 1.05, 1],
  opacity: [0.7, 1, 0.7],
  transition: {
    duration: 2,
    repeat: Infinity,
    ease: "easeInOut",
  },
};

export const floatLoop = {
  y: [0, -8, 0],
  transition: {
    duration: 4,
    repeat: Infinity,
    ease: "easeInOut",
  },
};

export const shimmer = {
  backgroundPosition: ["-200% 0", "200% 0"],
  transition: {
    duration: 1.5,
    repeat: Infinity,
    ease: "linear",
  },
};

/**
 * Respects user's prefers-reduced-motion setting.
 * Returns true if animations should be reduced/disabled.
 */
export function useReducedMotion(): boolean {
  const [reduce, setReduce] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduce(media.matches);
    const handler = () => setReduce(media.matches);
    media.addEventListener("change", handler);
    return () => media.removeEventListener("change", handler);
  }, []);

  return reduce;
}

/**
 * Helper to conditionally apply animation variants based on reduced motion preference.
 * Usage:
 *   const reduceMotion = useReducedMotion();
 *   <motion.div variants={fadeInUp} initial={reduceMotion ? false : "hidden"} animate={reduceMotion ? false : "visible"} />
 */
export function getAnimationProps(reduceMotion: boolean) {
  return reduceMotion
    ? { initial: false, animate: false, transition: false }
    : {};
}