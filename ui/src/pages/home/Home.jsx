import StackedBarChart from "../../components/chart/StackChart";
import React, { useContext, useEffect, useState } from "react";
import { targetSummary } from "../../store/dummyData";
import "./home.css";
import WidgetLg from "../../components/widgetLg/WidgetLg";

export default function Home() {
  const [targetSummaryData, setTargetSummaryData] = useState();
  const [barChartData, setBarChartData] = useState();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    console.log("Fetching target summary data");
    setIsLoading(true);
    setTargetSummaryData(targetSummary);
    setIsLoading(false);

    // Preparing TargetSummary chart data
    console.log("Preparing Stacked Bar Chart Data...");
    const barChartDat = [];
    for (let x in targetSummary) {
      const targetData = targetSummary[x];
      console.log(targetData);
      const item = {
        targetName: targetData.targetName,
        highVulns: targetData.highVulns,
        criticalVulns: targetData.criticalVulns,
        totalVulns: targetData.totalVulns,
      };
      barChartDat.push(item);
    }
    document.title = "AppSecHQ";
    setBarChartData(barChartDat);
  }, []);

  if (isLoading) {
    return (
      <section>
        <p>Loading...</p>
      </section>
    );
  }

  return (
    <div className="home">
      <h1>Scan Summary</h1>
      <StackedBarChart data={barChartData} />
      <WidgetLg summaryData={targetSummaryData} />
    </div>
  );
}
