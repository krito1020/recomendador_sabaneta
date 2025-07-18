import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity

class RecomendadorEmpresas:
    def __init__(self, path_excel):
        if not os.path.exists(path_excel):
            raise FileNotFoundError(f"El archivo {path_excel} no fue encontrado.")

        self.df = pd.read_excel(path_excel, sheet_name='BBDD')

        # Validar que exista la columna ARTICULOS
        if 'ARTICULOS' not in self.df.columns:
            raise ValueError("La columna 'ARTICULOS' no existe en el archivo.")

        # Limpiar nulos por tipo
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                self.df[col] = self.df[col].fillna('')
            else:
                self.df[col] = self.df[col].fillna(0)

        # Preprocesamiento de texto
        self.df['ARTICULOS'] = self.df['ARTICULOS'].str.lower().str.strip()

        # Vectorización usando stopwords en español e inglés
        custom_stop_words = text.ENGLISH_STOP_WORDS.union([
            'producto', 'servicio', 'servicios', 'venta', 'sabaneta', 'local', 'comercio'
        ])
        self.vectorizador = TfidfVectorizer(stop_words=custom_stop_words)
        self.tfidf = self.vectorizador.fit_transform(self.df['ARTICULOS'])

    def recomendar(self, texto_usuario, top_n=5, min_similitud=0.2):
        if not texto_usuario:
            return pd.DataFrame(columns=self.df.columns)

        consulta = self.vectorizador.transform([texto_usuario.lower().strip()])
        similitudes = cosine_similarity(consulta, self.tfidf).flatten()
        indices = [i for i in similitudes.argsort()[::-1] if similitudes[i] >= min_similitud][:top_n]
        return self.df.iloc[indices].copy()