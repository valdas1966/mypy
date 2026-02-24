import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from "recharts";

const data = [
  { k: 20, Dijkstra: 9.8, Incremental: 2.6, Aggregative: 4.4 },
  { k: 40, Dijkstra: 9.8, Incremental: 3.0, Aggregative: 6.7 },
  { k: 60, Dijkstra: 9.8, Incremental: 3.2, Aggregative: 9.2 },
  { k: 80, Dijkstra: 9.8, Incremental: 3.4, Aggregative: 11.8 },
  { k: 100, Dijkstra: 9.8, Incremental: 3.6, Aggregative: 14.6 },
];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "#fff", border: "2px solid #333", borderRadius: 6, padding: "10px 14px", boxShadow: "0 2px 8px rgba(0,0,0,0.2)" }}>
      <div style={{ color: "#000", fontSize: 15, fontWeight: 900, marginBottom: 6 }}>k = {label}</div>
      {payload.map((p) => (
        <div key={p.name} style={{ color: p.color, fontSize: 15, margin: "3px 0", fontFamily: "monospace", fontWeight: 900 }}>
          {p.name}: {p.value}s
        </div>
      ))}
    </div>
  );
};

const Annotation = ({ viewBox }) => {
  const x = viewBox.width + viewBox.x - 8;
  const yTop = 14.6;
  const yBot = 3.6;
  const scale = viewBox.height / 16;
  const top = viewBox.y + viewBox.height - yTop * scale;
  const bot = viewBox.y + viewBox.height - yBot * scale;
  const mid = (top + bot) / 2;
  return (
    <g>
      <line x1={x} y1={top + 4} x2={x} y2={bot - 4} stroke="#c1121f" strokeWidth={2.5} strokeDasharray="4 3" />
      <polygon points={`${x - 4},${top + 9} ${x + 4},${top + 9} ${x},${top + 2}`} fill="#c1121f" />
      <polygon points={`${x - 4},${bot - 9} ${x + 4},${bot - 9} ${x},${bot - 2}`} fill="#c1121f" />
      <text x={x + 12} y={mid - 6} fill="#c1121f" fontSize={15} fontWeight={900} fontFamily="system-ui">
        ~75%
      </text>
      <text x={x + 12} y={mid + 10} fill="#c1121f" fontSize={13} fontWeight={800} fontFamily="system-ui">
        faster
      </text>
    </g>
  );
};

export default function Chart() {
  return (
    <div style={{ background: "#ffffff", height: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
      <div style={{ width: "100%", maxWidth: 760 }}>
        <h2 style={{ color: "#000", fontFamily: "system-ui", fontSize: 24, fontWeight: 900, textAlign: "center", margin: "0 0 4px" }}>
          Elapsed Time vs. Number of Goals (k)
        </h2>
        <p style={{ color: "#444", fontFamily: "system-ui", fontSize: 14, fontWeight: 700, textAlign: "center", margin: "0 0 24px" }}>
          Averaged over 5,000 benchmark instances across 5 domains
        </p>
        <ResponsiveContainer width="100%" height={420}>
          <LineChart data={data} margin={{ top: 10, right: 70, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#ccc" />
            <XAxis
              dataKey="k"
              stroke="#999"
              tick={{ fill: "#000", fontSize: 15, fontWeight: 800 }}
              label={{ value: "k (number of goals)", position: "insideBottom", offset: -10, fill: "#000", fontSize: 15, fontWeight: 800 }}
            />
            <YAxis
              stroke="#999"
              tick={{ fill: "#000", fontSize: 14, fontWeight: 800 }}
              tickFormatter={(v) => v + "s"}
              label={{ value: "Elapsed (seconds)", angle: -90, position: "insideLeft", offset: 0, fill: "#000", fontSize: 15, fontWeight: 800, style: { textAnchor: "middle" } }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: 12, fontSize: 15, fontWeight: 900, color: "#000" }} />
            <Line type="monotone" dataKey="Dijkstra" stroke="#d62728" strokeWidth={3} dot={{ r: 6, fill: "#d62728", stroke: "#fff", strokeWidth: 2 }} />
            <Line type="monotone" dataKey="Incremental" stroke="#2ca02c" strokeWidth={3} dot={{ r: 6, fill: "#2ca02c", stroke: "#fff", strokeWidth: 2 }} />
            <Line type="monotone" dataKey="Aggregative" stroke="#1f77b4" strokeWidth={3} dot={{ r: 6, fill: "#1f77b4", stroke: "#fff", strokeWidth: 2 }} />
            <ReferenceLine x={100} stroke="none" content={<Annotation />} />
          </LineChart>
        </ResponsiveContainer>
        <p style={{ color: "#000", fontFamily: "system-ui", fontSize: 13, fontWeight: 800, textAlign: "center", margin: "8px 0 0" }}>
          At k=100, Incremental runs ~75% faster than Aggregative
        </p>
      </div>
    </div>
  );
}
