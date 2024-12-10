CREATE TABLE notification (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid (),
    user_id uuid NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (
        type IN (
            'approved',
            'rejected',
            'submitted',
            'unapproved'
        )
    ),
    read BOOLEAN NOT NULL DEFAULT FALSE,
    start_date_of_the_week VARCHAR(20) NOT NULL,
    project_id uuid DEFAULT NULL,
    created_at TIMESTAMP
    WITH
        TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT notification_user_id_fk FOREIGN KEY (user_id) REFERENCES "user" (id) ON UPDATE NO ACTION ON DELETE CASCADE,
        CONSTRAINT notification_project_id_fk FOREIGN KEY (project_id) REFERENCES project (id) ON UPDATE NO ACTION ON DELETE CASCADE
);