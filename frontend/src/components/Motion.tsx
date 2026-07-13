"use client";

import { motion } from "framer-motion";

/**
 * Shared entrance animation primitives. Kept intentionally subtle - a
 * hackathon demo that leans on animation for its "wow" moment usually reads
 * as trying too hard. These exist to remove the "static hackathon prototype"
 * feel without becoming a distraction.
 */

export function FadeInStagger({
  children, className,
}: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      className={className}
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.06 } },
      }}
    >
      {children}
    </motion.div>
  );
}

export function FadeInItem({
  children, className,
}: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      className={className}
      variants={{
        hidden: { opacity: 0, y: 10 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.25, ease: "easeOut" } },
      }}
    >
      {children}
    </motion.div>
  );
}

export function PulseBadge({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.span
      className={className}
      animate={{ opacity: [1, 0.6, 1] }}
      transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
    >
      {children}
    </motion.span>
  );
}
