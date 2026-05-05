import { useEffect, useState } from "react";

import { fetchNatureThemes, ingestNaturePhoto } from "../api/nature";

type Props = {
  onChanged?: () => void;
};

export function NatureThemePicker({ onChanged }: Props) {
  const [themes, setThemes] = useState<string[]>([]);
  const [selectedTheme, setSelectedTheme] = useState("");
  const [isBusy, setIsBusy] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchNatureThemes()
      .then((items) => {
        setThemes(items);
        setSelectedTheme(items[0] ?? "");
      })
      .catch((err) =>
        setMessage(err instanceof Error ? err.message : "Failed to load themes")
      );
  }, []);

  async function handleUpdatePhoto() {
    if (!selectedTheme) return;

    try {
      setMessage("");
      setIsBusy(true);

      await ingestNaturePhoto(selectedTheme);

      setMessage(`Updated theme: ${selectedTheme}`);
      onChanged?.();
    } catch (err) {
      setMessage(
        err instanceof Error ? err.message : "Failed to update nature photo"
      );
    } finally {
      setIsBusy(false);
    }
  }

  return (
    <div>
      <h3>Theme</h3>

      <div className="tools-row">
        <select
          value={selectedTheme}
          onChange={(e) => setSelectedTheme(e.target.value)}
          disabled={isBusy || themes.length === 0}
        >
          {themes.map((theme) => (
            <option key={theme} value={theme}>
              {theme}
            </option>
          ))}
        </select>

        <button
          type="button"
          onClick={handleUpdatePhoto}
          disabled={isBusy || !selectedTheme}
        >
          {isBusy ? "Updating..." : "Update"}
        </button>
      </div>

      {message && <p className="tools-message">{message}</p>}
    </div>
  );
}