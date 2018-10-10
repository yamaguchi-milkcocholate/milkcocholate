CREATE TABLE fitness_functions (
  id                integer    NOT NULL PRIMARY KEY,
  experiment_id     integer    NOT NULL,
  position          integer    NOT NULL,
  price             integer    NOT NULL,
  loged_at          timestamp  NOT NULL,
)