CREATE TABLE complaints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reference_code TEXT NOT NULL UNIQUE,
    ahu_id TEXT NOT NULL,
    description TEXT NOT NULL,
    submitted_at TIMESTAMP NOT NULL,
    matched_fault_id UUID REFERENCES fault_detections(id),
    match_type TEXT CHECK (match_type IN ('already_detected', 'escapee', 'false_complaint', 'watch')),
    complaint_count INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'received' CHECK (status IN ('received', 'investigating', 'resolved')),
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_complaints_ahu_time ON complaints (ahu_id, submitted_at);