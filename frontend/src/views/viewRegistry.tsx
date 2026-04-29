// frontend/src/views/viewRegistry.tsx

import type { Dashboard } from "../types/dashboard";
import { TodayView } from "./TodayView";
import { WeekView } from "./WeekView";
import { MonthView } from "./MonthView";

export type DashboardView = "today" | "week" | "month";

type ViewConfig = {
  key: DashboardView;
  label: string;
  Component: (props: { dashboard: Dashboard }) => JSX.Element;
};

export const dashboardViews: ViewConfig[] = [
  { key: "today", label: "Today", Component: TodayView },
  { key: "week", label: "Week", Component: WeekView },
  { key: "month", label: "Month", Component: MonthView },
];

export function getDashboardView(key: DashboardView) {
  return dashboardViews.find((view) => view.key === key) ?? dashboardViews[0];
}