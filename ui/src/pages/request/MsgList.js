import "./msgList.css";
import { DataGrid } from "@material-ui/data-grid";
import { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { johnMessages } from "../../store/dummyData";

export default function MsgList() {
  const [data, setData] = useState(johnMessages);
  //const proxyMessagesCtx = useContext(ProxyMessagesContext);
  //const contextData = proxyMessagesCtx.contextData;
  //const isLoading = proxyMessagesCtx.isLoading;

  //const data = contextData.getMessages();

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "URI",
      headerName: "URI",
      width: 400,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.request.uri}</div>;
      },
    },
    {
      field: "Status Code",
      headerName: "Status Code",
      width: 200,
      renderCell: (params) => {
        return (
          <div className="msgListItem">{params.row.response.statusCode}</div>
        );
      },
    },
    {
      field: "action",
      headerName: "Action",
      width: 150,
      renderCell: (params) => {
        return (
          <>
            <Link
              to={{
                pathname: "/proxy/messages/" + params.row.id,
                state: { action: "view", msgId: params.row.id },
              }}
            >
              <button className="msgListView">View</button>
            </Link>
          </>
        );
      },
    },
  ];

  return (
    <div className="msgList">
      <h1>Proxy Messages</h1>
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
