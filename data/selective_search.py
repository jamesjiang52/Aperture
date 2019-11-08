from selectivesearch import selective_search as ss


def selective_search(image):
    """A wrapper for the selective_search function in the selectivesearch
    library with fixed parameters.

    Returns a set of tuples (x, y, w, h) corresponding to candidate
    locations of objects in the input image.
    """
    regions = ss(image, scale=400, sigma=0.5, min_size=256)[1]
    candidates = set()
    for region in regions:
        if region["rect"] in candidates:
            continue

        # ignore elongated areas
        x, y, w, h = region["rect"]
        if w/h > 1.2 or h/w > 1.2:
            continue

        candidates.add(region["rect"])

    return candidates
