MERGE INTO repos (name, reviewer_selector_strategy) KEY(name) VALUES ('core/utils', 'heuristic');
MERGE INTO repos (name, reviewer_selector_strategy) KEY(name) VALUES ('frontend/dashboard-ui', 'heuristic');
MERGE INTO repos (name, reviewer_selector_strategy) KEY(name) VALUES ('infra/auth-service', 'heuristic');
MERGE INTO repos (name, reviewer_selector_strategy) KEY(name) VALUES ('infra/metrics-service', 'heuristic');