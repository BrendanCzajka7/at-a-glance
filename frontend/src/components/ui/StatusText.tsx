type Props = {
  error: string;
  isLoading: boolean;
};

export function StatusText({ error, isLoading }: Props) {
  if (error) {
    return <p className="status-text status-text--error">Error: {error}</p>;
  }

  if (isLoading) {
    return <p className="status-text">Loading dashboard...</p>;
  }

  return null;
}