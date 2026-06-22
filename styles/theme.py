"""Central design tokens — import from here in all pages and components."""

COLORS = {
    "bg":           "#071129",
    "card":         "#0F172A",
    "card2":        "#111C35",
    "primary":      "#6366F1",
    "accent":       "#7C3AED",
    "blue":         "#2563EB",
    "green":        "#22C55E",
    "orange":       "#F59E0B",
    "red":          "#EF4444",
    "cyan":         "#06B6D4",
    "text":         "#F8FAFC",
    "muted":        "#94A3B8",
    "border":       "rgba(255,255,255,0.08)",
    "border_solid": "#1E2D4A",
}

CHART_COLORS = [
    "#6366F1","#7C3AED","#06B6D4","#22C55E",
    "#F59E0B","#EF4444","#EC4899","#8B5CF6",
]

PRIORITY_COLORS  = {"Low": "#22C55E", "Medium": "#F59E0B", "High": "#EF4444"}
STATUS_COLORS    = {"Pending": "#F59E0B", "In Progress": "#6366F1", "Resolved": "#22C55E"}
SENTIMENT_COLORS = {"Positive": "#22C55E", "Neutral": "#94A3B8", "Negative": "#EF4444"}