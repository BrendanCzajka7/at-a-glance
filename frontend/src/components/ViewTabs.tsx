export type DashboardView = "today" | "week" | "month";

type Props = {
  value: DashboardView;
  onChange: (value: DashboardView) => void;
};

export function ViewTabs({ value, onChange }: Props) {
  return (
    <div>
      <button disabled={value === "today"} onClick={() => onChange("today")}>
        Today
      </button>
      <button disabled={value === "week"} onClick={() => onChange("week")}>
        Week
      </button>
      <button disabled={value === "month"} onClick={() => onChange("month")}>
        Month
      </button>
    </div>
  );
}