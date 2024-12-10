from sqlalchemy import create_engine, text, URL
from datetime import datetime, date
import boto3
import os
import json

url_object = URL.create(
    os.environ["DATABASE_TYPE"],
    username=os.environ["USER_NAME"],
    password=os.environ["PASSWORD"],
    host=os.environ["HOST"],
    port=os.environ["PORT"],
    database=os.environ["DATABASE_NAME"],
)
engine = create_engine(
    url_object,
    echo=True,
)
cors_headers = {
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST",
}

topic = os.environ["TOPIC_ARN"]
sns_client = boto3.client("sns")


def lambda_handler(event, context):
    try:
        json_body = json.loads(event["body"])
        print(json_body)
        stmt_update = text(
            """UPDATE timesheet
            SET status = :a, approved_date = :ad
            WHERE id = :id"""
        )
        stmt_select_email = text(
            """SELECT
                P.name, E.email, E.first_name, E.last_name, T.start_date_of_the_week, T.employee_id
                FROM timesheet T
                INNER JOIN project P
                ON T.project_id = P.id
                INNER JOIN "user" E
                ON T.employee_id = E.id
                WHERE T.id = :id
                """
        )
        stmt_notification = text(
            """INSERT INTO notification (user_id, type, start_date_of_the_week)
            VALUES (:uid, :type, :sd)"""
        )
        with engine.connect() as conn:
            result_update = conn.execute(
                stmt_update,
                {
                    "id": json_body["id"],
                    "a": json_body["approved"],
                    "ad": json_body["approved_date"],
                },
            )
            result_select_email = conn.execute(
                stmt_select_email,
                {
                    "id": json_body["id"],
                },
            )
            result_dicts_email = [
                dict(row) for row in result_select_email.mappings().all()
            ]
            result_insert = conn.execute(
                stmt_notification,
                {
                    "type": (
                        "approved"
                        if json_body["approved"] == "approved"
                        else "unapproved"
                    ),
                    "uid": result_dicts_email[0]["employee_id"],
                    "sd": result_dicts_email[0]["start_date_of_the_week"],
                },
            )
            print(result_dicts_email)
            conn.commit()

        subjectStr = (
            "Timesheet approved"
            if json_body["approved"] == "approved"
            else "Timesheet unapproved"
        )
        statusStr = (
            "approval" if json_body["approved"] == "approved" else "status change"
        )
        response = sns_client.publish(
            TopicArn=topic,
            Message=json.dumps(
                {
                    "emails": [result_dicts_email[0]["email"]],
                    "name": result_dicts_email[0].get("first_name", "")
                    + " "
                    + result_dicts_email[0].get("last_name", ""),
                    "body": f"""We would like to notify you of a timesheet {statusStr} for project: <b>{result_dicts_email[0]["name"]}</b>,
                    on the week of <b>{result_dicts_email[0]['start_date_of_the_week']}</b>.""",
                }
            ),
            Subject=subjectStr,
        )
    except Exception as error:
        print(error)
        return {
            "statusCode": "500",
            "headers": cors_headers,
            "body": json.dumps({"status": "error", "message": "Internal Server error"}),
        }
    else:
        return {
            "statusCode": "200",
            "headers": cors_headers,
            "body": json.dumps({"status": "success", "message": "Timesheet approved"}),
        }
