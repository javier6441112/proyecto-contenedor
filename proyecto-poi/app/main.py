from fastapi import FastAPI
import psycopg2
from fastapi.responses import FileResponse
from fastapi import Request

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="db",
        database="poi_db",
        user="user",
        password="password"
    )

@app.get("/api/puntos")
def listar(cat: str = None):
    conn = get_conn()
    cur = conn.cursor()

    if cat:
        cur.execute("""
            SELECT nombre, categoria,
                   ST_Y(ubicacion::geometry),
                   ST_X(ubicacion::geometry)
            FROM puntos_interes
            WHERE categoria = %s;
        """, (cat,))
    else:
        cur.execute("""
            SELECT nombre, categoria,
                   ST_Y(ubicacion::geometry),
                   ST_X(ubicacion::geometry)
            FROM puntos_interes;
        """)

    data = cur.fetchall()
    conn.close()
    return data

@app.get("/api/puntos/categoria")
def por_categoria(cat: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT nombre FROM puntos_interes WHERE categoria=%s;", (cat,))
    data = cur.fetchall()
    conn.close()
    return data

#@app.get("/api/puntos/cerca")
#def cerca(lat: float, lon: float, radio: float):
#    conn = get_conn()
#    cur = conn.cursor()
#    cur.execute("""
#        SELECT nombre
#        FROM puntos_interes
#        WHERE ST_DWithin(
#            ubicacion,
#            ST_MakePoint(%s, %s)::geography,
#            %s
#        );
#    """, (lon, lat, radio))
#    data = cur.fetchall()
#    conn.close()
#    return data

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/api/puntos/cerca")
def cerca(lat: float, lon: float, radio: float):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT nombre, categoria,
           ST_Distance(
               ubicacion,
               ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
           ) as distancia,
           ST_Y(ubicacion::geometry) as lat,
           ST_X(ubicacion::geometry) as lon
    FROM puntos_interes
    WHERE ST_DWithin(
        ubicacion,
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
        %s
    )
    ORDER BY distancia;
""", (lon, lat, lon, lat, radio))
    
    data = cur.fetchall()
    conn.close()
    return data


@app.post("/api/puntos")
async def crear_punto(request: Request):
    body = await request.json()

    nombre = body["nombre"]
    descripcion = body["descripcion"]
    categoria = body["categoria"]
    lat = body["lat"]
    lon = body["lon"]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO puntos_interes (nombre, descripcion, categoria, ubicacion)
        VALUES (%s, %s, %s,
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography)
    """, (nombre, descripcion, categoria, lon, lat))

    conn.commit()
    conn.close()

    return {"mensaje": "Punto guardado"}

@app.get("/api/categorias")
def obtener_categorias():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT categoria
        FROM puntos_interes
        ORDER BY categoria;
    """)

    data = [row[0] for row in cur.fetchall()]
    conn.close()

    return data