import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
  className?: string;
};

export function DashboardGrid({ children, className = "" }: Props) {
  return <div className={`dashboard-grid ${className}`.trim()}>{children}</div>;
}