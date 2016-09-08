BASE_URL = 'https://api.opendota.com/api'

API_PATH = {
        'Match': '/matches/{match_id}',
        'Player': '/players/{account_id}',
        'Metadata': '/metadata',
        'Distributions': '/distributions',
        'Search': '/search',
        'Rankings': '/rankings',
        'Benchmarks': '/benchmarks'
        }

PLAYER_PATH = {
        'wl': '/wl',
        'matches': '/matches',
        'heroes': '/heroes',
        'peers': '/peers',
        'activity': '/activity',
        'records': '/records',
        'counts': '/counts',
        'wardmap': '/wardmap',
        'items': '/items',
        'wordcloud': '/wordcloud',
        'ratings': '/ratings',
        'rankings': '/rankings',
        'histograms': '/histograms/{field}',
        'trends': '/trends/{field}'
}
