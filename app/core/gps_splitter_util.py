def split_gps(gps_str: str):
    try:
        lat, lon, alt, acc = gps_str.split()
        return float(lat), float(lon), float(alt), float(acc)
    except Exception:
        return None, None, None, None
