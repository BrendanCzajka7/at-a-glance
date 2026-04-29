import { dashboardViews, type DashboardView } from "../views/viewRegistry";

type Props = {
  value: DashboardView;
  onChange: (value: DashboardView) => void;
};

export function ViewTabs({ value, onChange }: Props) {
  return (
    <div>
      {dashboardViews.map((view) => (
        <button
          key={view.key}
          disabled={value === view.key}
          onClick={() => onChange(view.key)}
        >
          {view.label}
        </button>
      ))}
    </div>
  );
}