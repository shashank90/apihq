import "./widgetLg.css";
import "../../pages/proxyTraffic/msgList.css";
import { DataGrid } from "@material-ui/data-grid";

export default function WidgetLg(props) {
  const data = props.summaryData;

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "Target Name",
      headerName: "Target Name",
      width: 200,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.targetName}</div>;
      },
    },
    {
      field: "Site",
      headerName: "Site",
      width: 200,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.targetSite}</div>;
      },
    },
    {
      field: "Total Vulns",
      headerName: "Total",
      width: 200,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.totalVulns}</div>;
      },
    },
    {
      field: "Open Vulns",
      headerName: "Open",
      width: 200,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.openVulns}</div>;
      },
    },
  ];
  return (
    <div className="vuln-summary">
      <DataGrid
        rows={data}
        disableSelectionOnClick
        columns={columns}
        pageSize={8}
        checkboxSelection
      />
    </div>
  );
}
