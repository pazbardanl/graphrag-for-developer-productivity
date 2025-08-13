DROP TABLE IF EXISTS repos;

CREATE TABLE repos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  reviewer_selector_strategy VARCHAR(255) CHECK (reviewer_selector_strategy IN ('undetermined', 'heuristic', 'openai'))
);