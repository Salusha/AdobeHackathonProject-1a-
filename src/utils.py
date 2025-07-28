import pandas as pd
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from sklearn.cluster import KMeans
import re
from collections import Counter

def is_table_or_diagram(text_block):
    lines = text_block.strip().split('\n')
    if len(lines) > 5:
        return True
    if re.search(r'[|_+<>%#=•]', text_block):  # ASCII/table symbols
        return True
    return False

def extract_text_elements_with_page(pdf_path):
    records = []

    for page_num, layout in enumerate(extract_pages(pdf_path)):
        for element in layout:
            if not isinstance(element, LTTextContainer):
                continue

            for text_line in element:
                text = text_line.get_text().strip()
                if not text or is_table_or_diagram(text):
                    continue

                chars = [char for char in text_line if isinstance(char, LTChar)]
                if not chars:
                    continue

                font_sizes = [char.size for char in chars]
                fonts = [char.fontname for char in chars]

                avg_size = sum(font_sizes) / len(font_sizes)
                most_common_font = Counter(fonts).most_common(1)[0][0]
                is_bold = 'Bold' in most_common_font or text.isupper()

                records.append({
                    'text': text,
                    'font_size': round(avg_size, 1),
                    'font': most_common_font,
                    'x': text_line.x0,
                    'y': text_line.y0,
                    'page': page_num,
                    'is_bold': is_bold
                })

    return pd.DataFrame(records)

def classify_by_font_size(df, n_clusters=4):
    if df.empty:
        return df

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    df['cluster'] = kmeans.fit_predict(df[['font_size']])

    # Identify and drop smallest average font cluster (likely body text)
    cluster_means = df.groupby('cluster')['font_size'].mean()
    smallest_cluster = cluster_means.idxmin()
    df = df[df['cluster'] != smallest_cluster]

    # Sort remaining clusters and assign semantic labels
    sorted_clusters = cluster_means.drop(smallest_cluster).sort_values(ascending=False).index.tolist()
    labels = ['Title', 'Heading', 'Subheading', 'MinorHeading'][:len(sorted_clusters)]

    cluster_to_label = {cluster: labels[i] for i, cluster in enumerate(sorted_clusters)}
    df['label'] = df['cluster'].map(cluster_to_label)

    return df
