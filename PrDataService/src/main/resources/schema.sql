DROP TABLE IF EXISTS prs;

CREATE TABLE prs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  repo_name VARCHAR(255),
  pr_number VARCHAR(255),
  opened_at TIMESTAMP,
  closed_at TIMESTAMP,
  status VARCHAR(255) CHECK (status IS NULL OR status IN ('OPEN', 'IN_REVIEW', 'CLOSED')),
  last_recommended_reviewer VARCHAR(255),
  last_recommendation_at TIMESTAMP
);