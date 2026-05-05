import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export function DashboardGrid({ children }: Props) {
  return <div className="dashboard-grid">{children}</div>;
}