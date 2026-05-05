import type { ReactNode } from "react";

type Props = {
  title: string;
  updatedAt?: string | null;
  controls?: ReactNode;
  admin?: ReactNode;
  children: ReactNode;
};

function formatUpdatedAt(value?: string | null) {
  if (!value) return "Waiting for data";

  return new Date(value).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });
}

export function AppShell({ title, updatedAt, controls, admin, children }: Props) {
  return (
    <div className="app-page">
      <div className="app-shell">
        <div className="app-shell__top">
          <header className="app-shell__header">
            <div className="app-shell__title-block">
              <p className="app-shell__eyebrow">Personal dashboard</p>
              <h1 className="app-shell__title">{title}</h1>
              <p className="app-shell__updated">
                Updated: {formatUpdatedAt(updatedAt)}
              </p>
            </div>

            {controls && <div className="app-shell__controls">{controls}</div>}
          </header>

          {admin && (
            <details className="app-shell__admin">
              <summary>Tools</summary>
              <div className="app-shell__admin-body">{admin}</div>
            </details>
          )}
        </div>

        <main className="app-shell__content">{children}</main>
      </div>
    </div>
  );
}