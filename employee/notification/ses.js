import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses";

const sesClient = new SESClient();
const SENDER_EMAIL = "no-reply@serverless.mho879.com";

const htmlString = `
<!doctype html>
<html lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Simple Transactional Email</title>
    <style media="all" type="text/css">
    /* -------------------------------------
    GLOBAL RESETS
------------------------------------- */
    
    body {
      font-family: Helvetica, sans-serif;
      -webkit-font-smoothing: antialiased;
      font-size: 16px;
      line-height: 1.3;
      -ms-text-size-adjust: 100%;
      -webkit-text-size-adjust: 100%;
    }
    
    table {
      border-collapse: separate;
      mso-table-lspace: 0pt;
      mso-table-rspace: 0pt;
      width: 100%;
    }
    
    table td {
      font-family: Helvetica, sans-serif;
      font-size: 16px;
      vertical-align: top;
    }
    /* -------------------------------------
    BODY & CONTAINER
------------------------------------- */
    
    body {
      background-color: #f4f5f6;
      margin: 0;
      padding: 0;
    }
    
    .body {
      background-color: #f4f5f6;
      width: 100%;
    }
    
    .container {
      margin: 0 auto !important;
      max-width: 600px;
      padding: 0;
      padding-top: 24px;
      width: 600px;
    }
    
    .content {
      box-sizing: border-box;
      display: block;
      margin: 0 auto;
      max-width: 600px;
      padding: 0;
    }
    /* -------------------------------------
    HEADER, FOOTER, MAIN
------------------------------------- */
    
    .main {
      background: #ffffff;
      border: 1px solid #eaebed;
      border-radius: 16px;
      width: 100%;
    }
    
    .wrapper {
      box-sizing: border-box;
      padding: 24px;
    }
    
    .footer {
      clear: both;
      padding-top: 24px;
      text-align: center;
      width: 100%;
    }
    
    .footer td,
    .footer p,
    .footer span,
    .footer a {
      color: #9a9ea6;
      font-size: 16px;
      text-align: center;
    }
    /* -------------------------------------
    TYPOGRAPHY
------------------------------------- */
    
    p {
      font-family: Helvetica, sans-serif;
      font-size: 16px;
      font-weight: normal;
      margin: 0;
      margin-bottom: 16px;
    }
    
    a {
      color: #0867ec;
      text-decoration: underline;
    }
    /* -------------------------------------
    BUTTONS
------------------------------------- */
    
    .btn {
      box-sizing: border-box;
      min-width: 100% !important;
      width: 100%;
    }
    
    .btn > tbody > tr > td {
      padding-bottom: 16px;
    }
    
    .btn table {
      width: auto;
    }
    
    .btn table td {
      background-color: #ffffff;
      border-radius: 4px;
      text-align: center;
    }
    
    .btn a {
      background-color: #ffffff;
      border: solid 2px #0867ec;
      border-radius: 4px;
      box-sizing: border-box;
      color: #0867ec;
      cursor: pointer;
      display: inline-block;
      font-size: 16px;
      font-weight: bold;
      margin: 0;
      padding: 12px 24px;
      text-decoration: none;
      text-transform: capitalize;
    }
    
    .btn-primary table td {
      background-color: #0867ec;
    }
    
    .btn-primary a {
      background-color: #45B7AF;
      border-color: #45B7AF;
      color: #ffffff;
    }
    
    @media all {

    }
    
    /* -------------------------------------
    OTHER STYLES THAT MIGHT BE USEFUL
------------------------------------- */
    
    .last {
      margin-bottom: 0;
    }
    
    .first {
      margin-top: 0;
    }
    
    .align-center {
      text-align: center;
    }
    
    .align-right {
      text-align: right;
    }
    
    .align-left {
      text-align: left;
    }
    
    .text-link {
      color: #0867ec !important;
      text-decoration: underline !important;
    }
    
    .clear {
      clear: both;
    }
    
    .mt0 {
      margin-top: 0;
    }
    
    .mb0 {
      margin-bottom: 0;
    }
    
    .preheader {
      color: transparent;
      display: none;
      height: 0;
      max-height: 0;
      max-width: 0;
      opacity: 0;
      overflow: hidden;
      mso-hide: all;
      visibility: hidden;
      width: 0;
    }
    
    .powered-by a {
      text-decoration: none;
    }
    
    /* -------------------------------------
    RESPONSIVE AND MOBILE FRIENDLY STYLES
------------------------------------- */
    
    @media only screen and (max-width: 640px) {
      .main p,
      .main td,
      .main span {
        font-size: 16px !important;
      }
      .wrapper {
        padding: 8px !important;
      }
      .content {
        padding: 0 !important;
      }
      .container {
        padding: 0 !important;
        padding-top: 8px !important;
        width: 100% !important;
      }
      .main {
        border-left-width: 0 !important;
        border-radius: 0 !important;
        border-right-width: 0 !important;
      }
      .btn table {
        max-width: 100% !important;
        width: 100% !important;
      }
      .btn a {
        font-size: 16px !important;
        max-width: 100% !important;
        width: 100% !important;
      }
    }
    /* -------------------------------------
    PRESERVE THESE STYLES IN THE HEAD
------------------------------------- */
    
    @media all {
      .ExternalClass {
        width: 100%;
      }
      .ExternalClass,
      .ExternalClass p,
      .ExternalClass span,
      .ExternalClass font,
      .ExternalClass td,
      .ExternalClass div {
        line-height: 100%;
      }
      .apple-link a {
        color: inherit !important;
        font-family: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
        text-decoration: none !important;
      }
      #MessageViewBody a {
        color: inherit;
        text-decoration: none;
        font-size: inherit;
        font-family: inherit;
        font-weight: inherit;
        line-height: inherit;
      }
      .header {
        text-align: center;
        color: #333646;
      }
    }
    </style>
  </head>
  <body>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
      <tr>
        <td>&nbsp;</td>
        <td class="container">
          <div class="content">

            <!-- START CENTERED WHITE CONTAINER -->
            <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="main">

              <!-- START MAIN CONTENT AREA -->
              <tr>
                <td class="wrapper">
                  <h1 class="header">TimeTrack</h1>
                  <p>Hello, {name}</p>
                  <p>{body}</p>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
                    <tbody>
                      <tr>
                        <td align="left">
                          <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                            <tbody>
                              <tr>
                                <td> <a href="https://dev.d3ixi08j73y0x5.amplifyapp.com" target="_blank">Confirm now</a> </td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>

              <!-- END MAIN CONTENT AREA -->
              </table>

            <!-- START FOOTER -->
            <div class="footer">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                <tr>
                  <td class="content-block">
                    <span class="apple-link">TimeTrack, 555 Seymour Street, Vancouver V6B 3H6</span>
                    <br> Don't like these emails? <a href="https://dev.d3ixi08j73y0x5.amplifyapp.com">Unsubscribe</a>.
                  </td>
                </tr>
              </table>
            </div>

            <!-- END FOOTER -->
            
<!-- END CENTERED WHITE CONTAINER --></div>
        </td>
        <td>&nbsp;</td>
      </tr>
    </table>
  </body>
</html>
`;

const createHtmlBody = (message) =>
  htmlString.replace("{name}", message.name).replace("{body}", message.body);

const createSendEmailCommand = (toAddress, subject, messageObj) => {
  return new SendEmailCommand({
    Destination: {
      ToAddresses: [toAddress],
    },
    Message: {
      Body: {
        Html: {
          Charset: "UTF-8",
          Data: createHtmlBody(messageObj),
        },
        Text: {
          Charset: "UTF-8",
          Data: messageObj.body,
        },
      },
      Subject: {
        Charset: "UTF-8",
        Data: subject,
      },
    },
    Source: SENDER_EMAIL,
  });
};

const sendEmail = async (toEmail, subject, messageObj) => {
  const sendEmailCommand = createSendEmailCommand(toEmail, subject, messageObj);
  return await sesClient.send(sendEmailCommand);
};

export const handler = async (event) => {
  for (const record of event["Records"]) {
    const bodyObj = JSON.parse(record["body"]);
    const messageObj = JSON.parse(bodyObj.Message);
    const promisesArray = messageObj.emails.map((email) =>
      sendEmail(email, bodyObj.Subject, messageObj)
    );
    const response = await Promise.allSettled(promisesArray);
    console.log(response);
  }
};

// {
//     Records: [
//       {
//         messageId: '22ebcbdb-76de-4bba-9272-94b436cd0a14',
//         receiptHandle: 'AQEBdiEKlZjvG1BHwGTKgXOvcFU1fM+kfpgwNrafoluVqxslIzCTIH5NfQgJYkkjPISl0Rcz6yu/+1VvEZVlxs2aNjHar/fGrdNjHAT/h1p6Jo1IKVbqGjSWa0k02WFSismcUTMRtfcsAADo6URfz0Nrkev0H0f+9A3YLtvH7VJwM1zNN1su1eva0i3WBj9wN7GsM/r7kgdPscr1QY/JOl60Wql98j9uEWYGivVFua9TLSqQdWxwNOalSuPJWlfbGlF91mTQ/2eyBGZQ+iOUiJy/cHxgCxgMNij1yLe9gcptOQ1CDcBQ/9V+gjLHdoLdrBoOwKMYNA+fnv08YE8oNwH5CE8hsLWxmj8cO0WVE1UZNOhBD2wpAQk92RPBZ3CWcgAckA+gCxvpbs2Ra1FwA2wiXg==',
//         body: '{\n' +
//           '  "Type" : "Notification",\n' +
//           '  "MessageId" : "c87f51ca-5a0f-50da-a219-0e600efb501e",\n' +
//           '  "TopicArn" : "arn:aws:sns:us-west-2:127214187513:approval-topic",\n' +
//           '  "Subject" : "hi",\n' +
//           '  "Message" : "hi",\n' +
//           '  "Timestamp" : "2024-11-10T06:29:08.896Z",\n' +
//           '  "SignatureVersion" : "1",\n' +
//           '  "Signature" : "TOXCmgwZV2jqgtc1rjK8ikz6SFTjKaaUubLEV1qk1AFiv7g63s3xGoyDxUlwTILVXKwgYx0AzL3YOO0c1HQSbe4BLQtCI4C1vrEGj6oC9gO2Fzw9ougZIn6CjUFdZXwPdNpooPgyxK1lgUzpK9eK8iXqUsDd6jpF0WLkgJArCZ8/K43gxcKIAM2k5uqn5B9Yv30M0HASz3U0yJ/dYndhfpbzn2nNZMuefyTmMzZ48hvpxIkccuB2gzUjSL7EKuAW5AgmeA78qDWGqmLVyEZw+iRDRtCQigzC/GFvBO/w9Y/v1Az+TckAtsozYaGte0uvPTSggxE2ZF5wWGbxo2BopQ==",\n' +
//           '  "SigningCertURL" : "https://sns.us-west-2.amazonaws.com/SimpleNotificationService-60eadc530605d63b8e62a523676ef735.pem",\n' +
//           '  "UnsubscribeURL" : "https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:127214187513:approval-topic:99a6b8d0-a16b-45ce-8552-2156e27101a9",\n' +
//           '  "MessageAttributes" : {\n' +
//           '    "email" : {"Type":"String.Array","Value":"[\\"collinc812@gmail.com\\", \\"bill@gmail.com\\"]"}\n' +
//           '  }\n' +
//           '}',
//         attributes: [Object],
//         messageAttributes: {},
//         md5OfBody: '87eb15457fe0a59e04e7d8601a1bab78',
//         eventSource: 'aws:sqs',
//         eventSourceARN: 'arn:aws:sqs:us-west-2:127214187513:ses-queue',
//         awsRegion: 'us-west-2'
//       }
//     ]
//   }
