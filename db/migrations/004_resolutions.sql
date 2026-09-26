CREATE TABLE resolutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fault_id UUID NOT NULL UNIQUE REFERENCES fault_detections(id),
    ahu_id TEXT NOT NULL,
    cause TEXT NOT NULL,
    action_taken TEXT NOT NULL,
    resolution_method TEXT NOT NULL CHECK (resolution_method IN ('technician_form', 'auto_cleared', 'complaint_absence_confirmed')),
    confirmation_confidence NUMERIC,
    resolved_at TIMESTAMP NOT NULL,
    time_to_resolve_hours NUMERIC,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_resolutions_ahu ON resolutions (ahu_id);