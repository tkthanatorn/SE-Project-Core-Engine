class Preprocess:
    def cryptorank_preprocess(self, data) -> dict:
        tmp = []

        for item in data:
            tmp.append({
                'title': item['title'].replace("'", "''") if 'title' in item.keys() else '',
                'description': str(item['description']).replace("'", "''") if 'description' in item.keys() else '',
                'url': item['url'] if 'url' in item.keys() else '',
                'tags': item['relatedCoins']
                if 'relatedCoins' in item.keys() else [],
                'icon': item['source']['icon']
                if 'icon' in item['source'].keys() else '',
                'source': item['source']['name']
                if 'name' in item['source'].keys() else '',
                'date': item['date'] if 'date' in item.keys() else '',
                'major_url': str(item['url']).split(
                    '/')[2] if 'url' in item.keys() else '',
                'minor_url': str(item['url']).split(
                    '/')[3] if 'url' in item.keys() else ''
            })

        return tmp
