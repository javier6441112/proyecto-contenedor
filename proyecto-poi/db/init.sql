CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE puntos_interes (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    descripcion TEXT,
    categoria TEXT,
    ubicacion GEOGRAPHY(Point, 4326)
);

INSERT INTO puntos_interes (nombre, descripcion, categoria, ubicacion)
VALUES 
('Parque Central', 'Centro', 'cultural', ST_MakePoint(-90.5,14.6)),
('Gasolinera', 'Servicio', 'servicio', ST_MakePoint(-90.52,14.63)),
('Museo', 'Historia', 'cultural', ST_MakePoint(-90.51,14.62)),
('Restaurante', 'Comida', 'gastronomico', ST_MakePoint(-90.50,14.61)),
('Hospital', 'Salud', 'salud', ST_MakePoint(-90.53,14.64));