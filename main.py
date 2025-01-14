import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# Kreiranje SQLite baze i tabela
def create_database():
    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Dodavanje testnih podataka u bazu
def insert_test_data():
    data = [
        ("Bash Drive Šip", 43.881345, 18.401266),
        ("BASH Centar", 43.859994, 18.429427),
        ("Bash", 43.858419, 18.407821),
        ("BASH Drive Radon Plaza", 43.847039, 18.345673),
        ("BASH Ilidža", 43.832856, 18.321639)
    ]

    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO restaurants (name, latitude, longitude) VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()


# Dohvatanje podataka iz baze
def fetch_data():
    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude FROM restaurants")
    data = cursor.fetchall()
    conn.close()
    return np.array(data)


# Analiza i preporuka novih lokacija
def analyze_and_recommend(data, n_clusters=1):
    # K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, max_iter=600)
    kmeans.fit(data)

    # Centroidi (potencijalne nove lokacije)
    centroids = kmeans.cluster_centers_

    # Vizualizacija
    plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_, cmap='viridis', label="Postojeći restorani")
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='x', s=200, label="Preporučene lokacije")
    plt.title("Preporučene lokacije za nove restorane")
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    plt.legend()
    plt.show()

    return centroids


if __name__ == "__main__":
    # Kreiranje baze i unos podataka
    create_database()
    insert_test_data()

    # Učitavanje podataka
    data = fetch_data()

    # Analiza i preporuke
    recommended_locations = analyze_and_recommend(data)

    print("Preporučene lokacije za nove restorane:")
    for loc in recommended_locations:
        print(f"Latitude: {loc[0]:.6f}, Longitude: {loc[1]:.6f}")
