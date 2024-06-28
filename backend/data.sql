
INSERT INTO app_person (id, name, email) VALUES
(1, 'John Doe', 'john.doe@example.com'),
(2, 'Jane Smith', 'jane.smith@example.com'),
(3, 'Alice Johnson', 'alice.johnson@example.com'),
(4, 'Bob Brown', 'bob.brown@example.com'),
(5, 'Charlie Davis', 'charlie.davis@example.com');

INSERT INTO app_vehicle (id, license_plate, brand, color, owner_id) VALUES
(1, 'ABC123', 'Toyota', 'Red', 1),
(2, 'XYZ789', 'Honda', 'Blue', 2),
(3, 'LMN456', 'Ford', 'Black', 3),
(4, 'DEF321', 'Chevrolet', 'White', 4),
(5, 'GHI654', 'Nissan', 'Green', 5);


INSERT INTO app_violation (id, vehicle_id, timestamp, comments, officer_id) VALUES
(1, 1, '2022-12-01T12:00:00Z', 'Infracción por exceso de velocidad', 1),
(2, 2, '2022-12-02T13:00:00Z', 'Infracción por estacionamiento ilegal', 1),
(3, 3, '2022-12-03T14:00:00Z', 'Infracción por pasar un semáforo en rojo', 1),
(4, 4, '2022-12-04T15:00:00Z', 'Infracción por conducir sin licencia', 1),
(5, 5, '2022-12-05T16:00:00Z', 'Infracción por exceso de velocidad', 1);

SELECT setval(pg_get_serial_sequence('app_vehicle', 'id'), COALESCE(MAX(id), 1) + 1, false) FROM app_vehicle;
SELECT setval(pg_get_serial_sequence('app_person', 'id'), COALESCE(MAX(id), 1) + 1, false) FROM app_person;
SELECT setval(pg_get_serial_sequence('app_violation', 'id'), COALESCE(MAX(id), 1) + 1, false) FROM app_violation;
