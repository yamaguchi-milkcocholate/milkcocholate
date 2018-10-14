CREATE TABLE experiments (
  id                      integer    NOT NULL PRIMARY KEY,
  genetic_algorithm_id    integer    NOT NULL,
  fitness_function_id     integer    NOT NULL,
  situation               char(200)   NOT NULL,
  mutation_rate           integer    NOT NULL,
  cross_rate              integer    NOT NULL,
  population              integer    NOT NULL,
  elite_num               integer    NOT NULL,
  start_at                timestamp  NOT NULL,
  end_at                  TIMESTAMP  NOT NULL,
  execute_time            integer    NOT NULL
)
