CREATE TABLE fault_detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ahu_id TEXT NOT NULL,
    fault_type TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL,
    source TEXT NOT NULL CHECK (source IN ('predictive', 'complaint_escapee')),
    confidence NUMERIC,
    severity TEXT,
    energy_waste_estimate_kwh NUMERIC,
    outcome TEXT NOT NULL CHECK (outcome IN ('work_order', 'flagged_for_review', 'log_only')),
    shap_summary JSONB,
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'resolved')),
    jira_ticket_key TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_fault_detections_ahu_time ON fault_detections (ahu_id, detected_at);