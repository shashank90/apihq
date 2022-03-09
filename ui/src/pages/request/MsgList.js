import "./msgList.css";
import React, { useState, useEffect, useContext, useCallback } from "react";
import AuthContext from "../../store/auth-context";
import Message from "../../components/common/Message";
import DataTable from "../../components/dataTable/DataTable";
import { useParams } from "react-router-dom";
import buttons from "../../components/common/buttons.module.css";

const getRequestsBaseURL = "/apis/v1/requests";

export default function MsgList(props) {
  const [messages, setMessages] = useState([]);
  const [selectedMessage, setSelectedMessage] = useState({});
  const [showRequest, setShowRequest] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const authCtx = useContext(AuthContext);

  const params = useParams();
  const runId = params.runId;

  function showMessageDetails(requestId) {
    const msgs = messages.filter((message) => {
      return message.requestId === requestId;
    });
    let msg = null;
    if (msgs.length > 0) {
      msg = msgs[0];
    }
    // console.log(msg);
    if (msg !== null) {
      setShowRequest(true);
      setSelectedMessage(msg);
    }
  }

  const fetchRequestsHandler = useCallback(async () => {
    setLoading(true);
    setError(null);
    const getIssuesURL = getRequestsBaseURL + "/" + runId;
    try {
      const response = await fetch(getIssuesURL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": authCtx.token,
        },
      });
      const data = await response.json();
      console.log(data);
      // Set error and other success message(if any)
      if (!response.ok) {
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      }
      const transformedReqs = data.requests.map((item, index) => {
        return {
          id: index + 1,
          requestId: item.request_id,
          url: item.request.url,
          reqHeader: item.request.header,
          reqBody: item.request.body,
          statusCode: item.response.status,
          resHeader: item.response.header,
          resBody: item.response.body,
          message: item.response.message,
        };
      });
      setMessages(transformedReqs);
    } catch (error) {
      setError(error.message);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchRequestsHandler();
  }, [fetchRequestsHandler]);

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "URL",
      headerName: "URL",
      width: 400,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.url}</div>;
      },
    },
    {
      field: "Status Code",
      headerName: "Status Code",
      width: 200,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.statusCode}</div>;
      },
    },
    {
      field: "Message",
      headerName: "Message",
      width: 200,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.message}</div>;
      },
    },
    {
      field: "View",
      headerName: "View",
      width: 150,
      renderCell: (params) => {
        return (
          <>
            <button
              className={buttons.green_btn}
              onClick={() => {
                showMessageDetails(params.row.requestId);
              }}
            >
              View
            </button>
          </>
        );
      },
    },
  ];

  let content = <DataTable data={messages} columns={columns} />;

  if (error) {
    content = <p>{error}</p>;
  }

  if (loading) {
    content = <p>Loading...</p>;
  }

  if (showRequest) {
    return (
      <Message msgDetails={selectedMessage} showRequest={setShowRequest} />
    );
  } else {
    return (
      <div className="msgList">
        <h1>All Requests</h1>
        {content}
      </div>
    );
  }
}
