import type { ReactNode } from "react";

type CardVariant = "default" | "hero" | "wide" | "compact";

type Props = {
  children: ReactNode;
  className?: string;
  variant?: CardVariant;
};

export function Card({ children, className = "", variant = "default" }: Props) {
  return (
    <section className={`dash-card dash-card--${variant} ${className}`.trim()}>
      {children}
    </section>
  );
}