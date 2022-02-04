import "./stackChart.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export default function StackedBarChart({ title, data, dataKey, grid }) {
  return (
    <div className="vuln-stackchart-container">
      <BarChart
        width={600}
        height={300}
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <XAxis dataKey="targetName" />
        <YAxis />
        <CartesianGrid strokeDasharray="3 3" />
        <Tooltip />
        <Legend layout="vertical" verticalAlign="top" align="right" />
        <Bar dataKey="highVulns" stackId="a" fill="#8884d8" />
        <Bar dataKey="criticalVulns" stackId="a" fill="#82ca9d" />
      </BarChart>
    </div>
  );
}
