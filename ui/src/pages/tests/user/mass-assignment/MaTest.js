import { DataGrid } from "@material-ui/data-grid";
import { useState } from "react";
import { useHistory } from "react-router";
import Message from "../../../../components/common/Message";
import { johnMessages } from "../../../../store/dummyData";
import TestBottombar from "../../../../layout/testbottombar/TestBottombar";
import "../../../proxyTraffic/msgList.css";
import "./maTest.css";

export default function MaTest() {
  const [data, setData] = useState(johnMessages);

  const [editMessage, setEditMessage] = useState(false);
  const [msgDetails, setMsgDetails] = useState({});
  const isBackBtnVisible = true;
  const isSaveBtnVisible = true;
  const isNextBtnVisible = true;
  const history = useHistory();

  const handleOnBack = () => {
    //Do nothing
    history.push("/tests/user");
  };

  const handleOnSave = () => {
    //TODO: Save to db and go back
    history.push("/tests/resource-limit");
  };

  function showMsgDetails(id) {
    console.log("Row with id clicked: " + id);
    console.log(data);
    const msgDetails = data.filter((item) => {
      return item.id === id;
    });
    if (msgDetails) {
      const msg = msgDetails[0];

      setEditMessage(true);
      const uri = msg.request.uri;
      const reqHeader = JSON.stringify(msg.request.headers);
      const reqBody = JSON.stringify(msg.request.body);
      const resHeader = JSON.stringify(msg.response.headers);
      const resBody = JSON.stringify(msg.response.body);
      setMsgDetails({
        uri: uri,
        reqHeader: reqHeader,
        reqBody: reqBody,
        resHeader: resHeader,
        resBody: resBody,
      });
    }
  }

  function hideMessage() {
    setEditMessage(false);
  }

  const columns = [
    { field: "id", headerName: "ID", width: 90 },
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
            <button
              className="msgListView"
              onClick={() => {
                showMsgDetails(params.row.id);
              }}
            >
              Edit
            </button>
          </>
        );
      },
    },
  ];

  if (editMessage) {
    return (
      <Message
        msgDetails={msgDetails}
        editable={editMessage}
        hideMessage={hideMessage}
        fuzzRequestPayload={true}
      />
    );
  } else {
    return (
      <div className="ma-test-container">
        <div className="ma-description">
          <p>
            <h2>Mass Assignment</h2>
          </p>
          <p>
            <h4>Description</h4>
          </p>
          <p>
            The API takes data that client provides and stores it without proper
            filtering for whitelisted properties. Attackers can try to guess
            object properties or provide additional object properties in their
            requests, read the documentation, or check out API endpoints for
            clues where to find the openings to modify properties they are not
            supposed to on the data objects stored in the backend.
          </p>
          <p>
            <h4>Process</h4>
          </p>
          <p>
            <ol>
              <li>Select POST URIs one by one</li>
              <li>Guess nearby properties and try fuzzing requests</li>
            </ol>
          </p>
        </div>
        <div className="ma-msgList">
          <DataGrid
            rows={data}
            disableSelectionOnClick
            columns={columns}
            pageSize={4}
            checkboxSelection
          />
        </div>
        <TestBottombar
          isBackBtnVisible={isBackBtnVisible}
          onBackHandle={handleOnBack}
          isSaveBtnVisible={isSaveBtnVisible}
          onSaveHandle={handleOnSave}
          isNextBtnVisible={isNextBtnVisible}
          onNextHandle={handleOnSave}
        />
      </div>
    );
  }
}
