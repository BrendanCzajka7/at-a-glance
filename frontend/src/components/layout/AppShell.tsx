import { useState, type ReactNode } from "react";

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
  const [isToolsOpen, setIsToolsOpen] = useState(false);

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

            <div className="app-shell__controls">
              {controls}

              {admin && (
                <button
                  type="button"
                  className="tools-open-button"
                  onClick={() => setIsToolsOpen(true)}
                >
                  Tools
                </button>
              )}
            </div>
          </header>
        </div>

        <main className="app-shell__content">{children}</main>
      </div>

      {admin && isToolsOpen && (
        <div
          className="tools-overlay"
          role="dialog"
          aria-modal="true"
          aria-label="Tools"
        >
          <button
            type="button"
            className="tools-backdrop"
            aria-label="Close tools"
            onClick={() => setIsToolsOpen(false)}
          />

          <aside className="tools-panel">
            <div className="tools-panel__header">
              <div>
                <p className="card-eyebrow">Dashboard controls</p>
                <h2>Tools</h2>
              </div>

              <button
                type="button"
                className="tools-close-button"
                onClick={() => setIsToolsOpen(false)}
              >
                Close
              </button>
            </div>

            <div className="tools-panel__body">{admin}</div>
          </aside>
        </div>
      )}
    </div>
  );
}