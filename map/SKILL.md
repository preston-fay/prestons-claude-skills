---
name: map
description: "Create geographic visualizations from location data. Use for mapping points, regions, routes, choropleth maps, and spatial analysis. Supports coordinates, addresses, country/state data, and GeoJSON."
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash(python *)
  - Bash(pip install *)
  - WebFetch
hooks:
  PostToolUse:
    - matcher: "*"
      command: ["bash", "/Users/pfay01/.claude/hooks/log-tool-use.sh"]
---

# Geographic Visualization

Create beautiful, interactive maps from location data. Supports points, polygons, choropleths, heatmaps, and routes.

## Quick Start

```python
import folium

# Basic map centered on a location
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add a marker
folium.Marker(
    [40.7128, -74.0060],
    popup="New York City",
    icon=folium.Icon(color='purple')
).add_to(m)

# Save to HTML
m.save('map.html')
```

---

## Data Preparation

### From Coordinates

```python
import pandas as pd

# Data with lat/lon columns
df = pd.DataFrame({
    'name': ['NYC', 'LA', 'Chicago'],
    'lat': [40.7128, 34.0522, 41.8781],
    'lon': [-74.0060, -118.2437, -87.6298],
    'value': [8336817, 3979576, 2693976]
})
```

### From Addresses (Geocoding)

```python
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Initialize geocoder
geolocator = Nominatim(user_agent="my_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_coordinates(address):
    """Convert address to lat/lon."""
    try:
        location = geocode(address)
        if location:
            return location.latitude, location.longitude
    except:
        pass
    return None, None

# Apply to dataframe
df['lat'], df['lon'] = zip(*df['address'].apply(get_coordinates))
```

### From Country/State Names

```python
# Country centroids (common ones)
COUNTRY_COORDS = {
    'United States': (39.8283, -98.5795),
    'United Kingdom': (55.3781, -3.4360),
    'Germany': (51.1657, 10.4515),
    'France': (46.2276, 2.2137),
    'China': (35.8617, 104.1954),
    'Japan': (36.2048, 138.2529),
    'Australia': (-25.2744, 133.7751),
    'Brazil': (-14.2350, -51.9253),
    'India': (20.5937, 78.9629),
    'Canada': (56.1304, -106.3468),
}

# US State centroids
US_STATE_COORDS = {
    'California': (36.7783, -119.4179),
    'Texas': (31.9686, -99.9018),
    'New York': (40.7128, -74.0060),
    'Florida': (27.6648, -81.5158),
    # ... add more as needed
}
```

---

## Map Types

### Point Map (Markers)

```python
import folium

def create_point_map(df, lat_col, lon_col, label_col=None, value_col=None):
    """Create map with point markers."""
    # Center on data
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    for idx, row in df.iterrows():
        popup_text = f"{row[label_col]}" if label_col else ""
        if value_col:
            popup_text += f": {row[value_col]:,}"

        folium.Marker(
            location=[row[lat_col], row[lon_col]],
            popup=popup_text,
            icon=folium.Icon(color='purple', icon='info-sign')
        ).add_to(m)

    return m

# Usage
m = create_point_map(df, 'lat', 'lon', 'name', 'value')
m.save('point_map.html')
```

### Bubble Map (Sized Markers)

```python
def create_bubble_map(df, lat_col, lon_col, size_col, label_col=None,
                      min_radius=5, max_radius=30):
    """Create map with sized circle markers."""
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # Normalize sizes
    size_min = df[size_col].min()
    size_max = df[size_col].max()

    for idx, row in df.iterrows():
        # Scale radius
        normalized = (row[size_col] - size_min) / (size_max - size_min)
        radius = min_radius + normalized * (max_radius - min_radius)

        popup_text = f"{row[label_col]}: {row[size_col]:,}" if label_col else f"{row[size_col]:,}"

        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=radius,
            popup=popup_text,
            color='#7823DC',  # Kearney Purple border
            fill=True,
            fill_color='#9150E1',  # Lighter purple fill
            fill_opacity=0.6,
            weight=2
        ).add_to(m)

    return m

# Usage
m = create_bubble_map(df, 'lat', 'lon', 'population', 'city')
m.save('bubble_map.html')
```

### Heatmap

```python
from folium.plugins import HeatMap

def create_heatmap(df, lat_col, lon_col, value_col=None):
    """Create density heatmap."""
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # Prepare data
    if value_col:
        heat_data = [[row[lat_col], row[lon_col], row[value_col]]
                     for idx, row in df.iterrows()]
    else:
        heat_data = [[row[lat_col], row[lon_col]]
                     for idx, row in df.iterrows()]

    HeatMap(
        heat_data,
        min_opacity=0.3,
        radius=15,
        blur=10,
        gradient={0.4: '#E0D2FA', 0.6: '#9150E1', 0.8: '#7823DC', 1: '#1E1E1E'}
    ).add_to(m)

    return m

# Usage
m = create_heatmap(df, 'lat', 'lon', 'intensity')
m.save('heatmap.html')
```

### Choropleth Map (Regions)

```python
import json

def create_choropleth(df, geo_json_path, region_col, value_col,
                      legend_name='Value'):
    """Create choropleth map colored by region values."""
    # Load GeoJSON
    with open(geo_json_path) as f:
        geo_data = json.load(f)

    # Find center
    coords = []
    for feature in geo_data['features']:
        if feature['geometry']['type'] == 'Polygon':
            coords.extend(feature['geometry']['coordinates'][0])
        elif feature['geometry']['type'] == 'MultiPolygon':
            for poly in feature['geometry']['coordinates']:
                coords.extend(poly[0])

    center_lon = sum(c[0] for c in coords) / len(coords)
    center_lat = sum(c[1] for c in coords) / len(coords)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # Kearney purple gradient
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth',
        data=df,
        columns=[region_col, value_col],
        key_on='feature.properties.name',  # Adjust based on GeoJSON structure
        fill_color='BuPu',  # Purple gradient
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend_name,
        highlight=True
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m

# Usage (requires GeoJSON file)
# m = create_choropleth(df, 'us_states.geojson', 'state', 'revenue', 'Revenue ($M)')
# m.save('choropleth.html')
```

### Clustered Markers

```python
from folium.plugins import MarkerCluster

def create_clustered_map(df, lat_col, lon_col, label_col=None):
    """Create map with clustered markers for dense data."""
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in df.iterrows():
        popup_text = str(row[label_col]) if label_col else ""
        folium.Marker(
            location=[row[lat_col], row[lon_col]],
            popup=popup_text
        ).add_to(marker_cluster)

    return m

# Usage
m = create_clustered_map(df, 'lat', 'lon', 'name')
m.save('clustered_map.html')
```

---

## Plotly Maps (Static/Interactive)

```python
import plotly.express as px
import plotly.graph_objects as go

# Kearney colors
KEARNEY_PURPLE = '#7823DC'
KEARNEY_COLORS = ['#D2D2D2', '#A5A6A5', '#787878', '#E0D2FA', '#C8A5F0',
                  '#AF7DEB', '#4B4B4B', '#1E1E1E', '#9150E1', '#7823DC']

def plotly_scatter_map(df, lat_col, lon_col, size_col=None, color_col=None,
                       hover_name=None, title='Map'):
    """Create Plotly scatter map."""
    fig = px.scatter_geo(
        df,
        lat=lat_col,
        lon=lon_col,
        size=size_col,
        color=color_col,
        hover_name=hover_name,
        color_continuous_scale=['#E0D2FA', '#7823DC'],  # Kearney gradient
        title=title
    )

    fig.update_layout(
        font_family='Arial',
        geo=dict(
            showland=True,
            landcolor='#F5F5F5',
            showocean=True,
            oceancolor='#FFFFFF',
            showlakes=True,
            lakecolor='#FFFFFF',
            showrivers=False,
            coastlinecolor='#A5A5A5',
            countrycolor='#A5A5A5'
        )
    )

    return fig

# Usage
fig = plotly_scatter_map(df, 'lat', 'lon', 'population', hover_name='city')
fig.write_html('plotly_map.html')
fig.show()
```

### US Choropleth with Plotly

```python
def plotly_us_choropleth(df, state_col, value_col, title='US Map'):
    """Create US state choropleth with Plotly."""
    fig = px.choropleth(
        df,
        locations=state_col,
        locationmode='USA-states',
        color=value_col,
        color_continuous_scale=['#E0D2FA', '#9150E1', '#7823DC'],
        scope='usa',
        title=title
    )

    fig.update_layout(
        font_family='Arial',
        geo=dict(
            showlakes=True,
            lakecolor='#FFFFFF'
        )
    )

    return fig

# Usage (state_col should have 2-letter state codes)
# fig = plotly_us_choropleth(df, 'state_code', 'revenue', 'Revenue by State')
```

---

## Kepler.gl (Advanced Visualization)

For large datasets and advanced spatial analysis:

```python
from keplergl import KeplerGl

def create_kepler_map(df, config=None):
    """Create Kepler.gl map for advanced visualization."""
    map_1 = KeplerGl(height=600)
    map_1.add_data(data=df, name='data')

    if config:
        map_1.config = config

    return map_1

# Usage
# map_1 = create_kepler_map(df)
# map_1.save_to_html(file_name='kepler_map.html')
```

---

## GeoJSON Resources

### Common GeoJSON Sources

```python
# World countries
# https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson

# US States
# https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json

# US Counties
# https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json
```

### Loading GeoJSON

```python
import requests

def load_geojson(url):
    """Load GeoJSON from URL."""
    response = requests.get(url)
    return response.json()

# US States example
us_states_geojson = load_geojson(
    'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'
)
```

---

## Styling with Kearney Colors

### Folium Custom Styling

```python
# Custom icon with Kearney colors
kearney_icon = folium.Icon(
    color='purple',
    icon_color='white',
    icon='info-sign',
    prefix='glyphicon'
)

# Custom circle style
folium.CircleMarker(
    location=[lat, lon],
    radius=10,
    color='#7823DC',      # Kearney Purple border
    fill=True,
    fill_color='#9150E1', # Lighter fill
    fill_opacity=0.7,
    weight=2
)

# Custom polygon style
folium.GeoJson(
    geojson_data,
    style_function=lambda x: {
        'fillColor': '#E0D2FA',
        'color': '#7823DC',
        'weight': 2,
        'fillOpacity': 0.5
    }
)
```

---

## Complete Example

```python
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster

def create_comprehensive_map(df, lat_col, lon_col, value_col, label_col,
                              output_file='comprehensive_map.html'):
    """Create map with multiple layers."""
    # Center
    center = [df[lat_col].mean(), df[lon_col].mean()]

    # Base map
    m = folium.Map(location=center, zoom_start=4,
                   tiles='cartodbpositron')  # Clean base map

    # Layer 1: Heatmap
    heat_group = folium.FeatureGroup(name='Heatmap')
    heat_data = [[row[lat_col], row[lon_col], row[value_col]]
                 for _, row in df.iterrows()]
    HeatMap(heat_data, radius=15,
            gradient={0.4: '#E0D2FA', 0.65: '#9150E1', 1: '#7823DC'}
           ).add_to(heat_group)
    heat_group.add_to(m)

    # Layer 2: Clustered markers
    cluster_group = folium.FeatureGroup(name='Clustered Points')
    marker_cluster = MarkerCluster().add_to(cluster_group)
    for _, row in df.iterrows():
        folium.Marker(
            [row[lat_col], row[lon_col]],
            popup=f"{row[label_col]}: {row[value_col]:,}"
        ).add_to(marker_cluster)
    cluster_group.add_to(m)

    # Layer 3: Sized bubbles
    bubble_group = folium.FeatureGroup(name='Bubbles', show=False)
    size_range = df[value_col].max() - df[value_col].min()
    for _, row in df.iterrows():
        radius = 5 + (row[value_col] - df[value_col].min()) / size_range * 25
        folium.CircleMarker(
            [row[lat_col], row[lon_col]],
            radius=radius,
            color='#7823DC',
            fill=True,
            fill_color='#9150E1',
            fill_opacity=0.6,
            popup=f"{row[label_col]}: {row[value_col]:,}"
        ).add_to(bubble_group)
    bubble_group.add_to(m)

    # Layer control
    folium.LayerControl().add_to(m)

    # Save
    m.save(output_file)
    print(f"Map saved to {output_file}")

    return m

# Usage
# m = create_comprehensive_map(df, 'lat', 'lon', 'revenue', 'city')
```

---

## Tips

1. **Clean your coordinates**: Remove nulls, check for swapped lat/lon
2. **Choose appropriate zoom**: Start broad, let users zoom in
3. **Use clustering for large datasets**: > 1000 points should cluster
4. **Layer strategically**: Let users toggle between views
5. **Mobile-friendly**: Test on mobile devices if sharing
6. **File size**: Large GeoJSON files slow down maps - simplify geometries
7. **Apply Kearney colors**: Use the brand palette for professional output
