import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
import os
import pickle

class CollaborativeFilteringRecommender:
    """Collaborative Filtering Recommender usando SVD"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.user_item_matrix = None
        self.user_to_idx = None
        self.artist_to_idx = None
        self.user_ids = None
        self.artist_ids = None
        self.user_factors = None
        self.artist_factors = None
        self.artists_df = None
        self.user_artists_df = None
        self.svd = None
        
    def load_data(self):
        """Cargar datos del dataset Last.fm"""
        print("Cargando datos...")
        
        # Cargar artistas
        artists_file = os.path.join(self.data_path, 'artists.dat')
        self.artists_df = pd.read_csv(artists_file, sep='\t', encoding='latin-1')
        self.artists_df = self.artists_df.rename(columns={'id': 'artistID'})
        
        # Cargar interacciones usuario-artista
        user_artists_file = os.path.join(self.data_path, 'user_artists.dat')
        self.user_artists_df = pd.read_csv(user_artists_file, sep='\t', encoding='latin-1')
        
        # Convertir a tipos numéricos
        self.user_artists_df['userID'] = pd.to_numeric(self.user_artists_df['userID'], errors='coerce')
        self.user_artists_df['artistID'] = pd.to_numeric(self.user_artists_df['artistID'], errors='coerce')
        self.user_artists_df['weight'] = pd.to_numeric(self.user_artists_df['weight'], errors='coerce')
        self.artists_df['artistID'] = pd.to_numeric(self.artists_df['artistID'], errors='coerce')
        
        # Eliminar nulos
        self.user_artists_df = self.user_artists_df.dropna()
        
        print(f"Datos cargados: {self.user_artists_df['userID'].nunique()} usuarios, "
              f"{self.user_artists_df['artistID'].nunique()} artistas")
        
    def create_user_item_matrix(self):
        """Crear matriz usuario-artista"""
        print("Creando matriz usuario-artista...")
        
        user_ids = sorted(self.user_artists_df['userID'].unique())
        artist_ids = sorted(self.user_artists_df['artistID'].unique())
        
        # Mapeo de IDs a índices
        self.user_to_idx = {uid: idx for idx, uid in enumerate(user_ids)}
        self.artist_to_idx = {aid: idx for idx, aid in enumerate(artist_ids)}
        self.user_ids = user_ids
        self.artist_ids = artist_ids
        
        # Crear matriz sparse
        rows, cols, data = [], [], []
        for _, row in self.user_artists_df.iterrows():
            user_idx = self.user_to_idx[row['userID']]
            artist_idx = self.artist_to_idx[row['artistID']]
            rows.append(user_idx)
            cols.append(artist_idx)
            data.append(row['weight'])
        
        self.user_item_matrix = csr_matrix(
            (data, (rows, cols)),
            shape=(len(user_ids), len(artist_ids))
        )
        
        print(f"Matriz creada: {self.user_item_matrix.shape}")
        
    def train_model(self, n_components=50):
        """Entrenar modelo SVD"""
        print(f"Entrenando modelo SVD con {n_components} componentes...")
        
        # Normalizar con log transform
        user_item_dense = self.user_item_matrix.toarray()
        user_item_log = np.log1p(user_item_dense)
        
        # SVD Truncado
        self.svd = TruncatedSVD(n_components=n_components, random_state=42)
        self.user_factors = self.svd.fit_transform(user_item_log)
        self.artist_factors = self.svd.components_.T
        
        variance_explained = self.svd.explained_variance_ratio_.sum()
        print(f"Modelo entrenado. Varianza explicada: {variance_explained:.3f}")
        
    def get_recommendations(self, user_id, top_k=10):
        """Generar recomendaciones para un usuario"""
        if user_id not in self.user_to_idx:
            return None, "Usuario no encontrado"
        
        user_idx = self.user_to_idx[user_id]
        user_vector = self.user_factors[user_idx]
        
        # Calcular scores para todos los artistas
        scores = np.dot(user_vector, self.artist_factors.T)
        
        # Obtener artistas ya escuchados
        listened_artists = set(self.user_item_matrix[user_idx].nonzero()[1])
        
        # Filtrar artistas ya escuchados y obtener top-k
        recommendations = []
        for artist_idx in np.argsort(scores)[::-1]:
            if artist_idx not in listened_artists:
                artist_id = self.artist_ids[artist_idx]
                artist_row = self.artists_df[self.artists_df['artistID'] == artist_id]
                
                if len(artist_row) > 0:
                    artist_name = artist_row['name'].iloc[0]
                    artist_url = artist_row['url'].iloc[0] if 'url' in artist_row.columns else ""
                    artist_pic = artist_row['pictureURL'].iloc[0] if 'pictureURL' in artist_row.columns else ""
                else:
                    artist_name = f"Artist_{artist_id}"
                    artist_url = ""
                    artist_pic = ""
                
                recommendations.append({
                    'artistID': int(artist_id),
                    'name': artist_name,
                    'score': float(scores[artist_idx]),
                    'url': artist_url,
                    'pictureURL': artist_pic
                })
                
                if len(recommendations) >= top_k:
                    break
        
        return recommendations, "OK"
    
    def get_user_history(self, user_id, top_k=10):
        """Obtener historial de reproducción de un usuario"""
        if user_id not in self.user_to_idx:
            return None, "Usuario no encontrado"
        
        user_data = self.user_artists_df[self.user_artists_df['userID'] == user_id]
        user_data = user_data.sort_values('weight', ascending=False).head(top_k)
        
        history = []
        for _, row in user_data.iterrows():
            artist_id = row['artistID']
            artist_row = self.artists_df[self.artists_df['artistID'] == artist_id]
            
            if len(artist_row) > 0:
                artist_name = artist_row['name'].iloc[0]
                artist_url = artist_row['url'].iloc[0] if 'url' in artist_row.columns else ""
                artist_pic = artist_row['pictureURL'].iloc[0] if 'pictureURL' in artist_row.columns else ""
            else:
                artist_name = f"Artist_{artist_id}"
                artist_url = ""
                artist_pic = ""
            
            history.append({
                'artistID': int(artist_id),
                'name': artist_name,
                'playcount': int(row['weight']),
                'url': artist_url,
                'pictureURL': artist_pic
            })
        
        return history, "OK"
    
    def get_all_users(self):
        """Obtener lista de todos los usuarios"""
        return sorted([int(uid) for uid in self.user_ids])
    
    def save_model(self, filepath):
        """Guardar modelo entrenado"""
        model_data = {
            'user_to_idx': self.user_to_idx,
            'artist_to_idx': self.artist_to_idx,
            'user_ids': self.user_ids,
            'artist_ids': self.artist_ids,
            'user_factors': self.user_factors,
            'artist_factors': self.artist_factors,
            'user_item_matrix': self.user_item_matrix,
            'svd': self.svd
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Modelo guardado en {filepath}")
    
    def load_model(self, filepath):
        """Cargar modelo entrenado"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.user_to_idx = model_data['user_to_idx']
        self.artist_to_idx = model_data['artist_to_idx']
        self.user_ids = model_data['user_ids']
        self.artist_ids = model_data['artist_ids']
        self.user_factors = model_data['user_factors']
        self.artist_factors = model_data['artist_factors']
        self.user_item_matrix = model_data['user_item_matrix']
        self.svd = model_data['svd']
        print(f"Modelo cargado desde {filepath}")
