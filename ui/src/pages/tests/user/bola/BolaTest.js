import { DataGrid } from "@material-ui/data-grid";
import { useState } from "react";
import { useHistory } from "react-router";
import Message from "../../../../components/common/Message";
import TestBottombar from "../../../../layout/testbottombar/TestBottombar";
import { johnMessages } from "../../../../store/dummyData";
import "../../../proxyTraffic/msgList.css";
import "./bolaTest.css";

export default function BolaTest() {
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
    history.push("/tests/bofa");
  };

  let data = johnMessages;

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
        fuzzRequestURI={true}
      />
    );
  } else {
    return (
      <div className="bola-test-container">
        <div className="bola-description">
          <p>
            <h2>Broken Object Level Authorization</h2>
          </p>
          <p>
            <h4>Description</h4>
          </p>
          <p>
            Attackers substitute the ID of their own resource in the API call
            with an ID of a resource belonging to another user. The lack of
            proper authorization checks allows attackers to access the specified
            resource
          </p>
          <p>Objective: Confidentiality</p>
          <p>
            <h4>Process</h4>
          </p>
          <p>
            <ol>
              <li>Select GET URIs one by one</li>
              <li>Modify either user or resource identifier</li>
            </ol>
          </p>
        </div>
        <div className="bola-msgList">
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
