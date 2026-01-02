CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_audit_entity ON audit_log(entity, entity_id);
CREATE INDEX idx_audit_created ON audit_log(created_at);
CREATE INDEX idx_contributions_member ON contributions(member_id);
CREATE INDEX idx_contributions_project ON contributions(project_id);
