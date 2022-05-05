class Preprocess:
    def cryptorank_preprocess(self, data) -> dict:
        tmp = {
            'title': [],
            'description': [],
            'url': [],
            'icon': [],
            'tags': [],
            'source': [],
            'major_url': [],
            'minor_url': [],
            'date': []
        }

        for item in data:
            tmp['title'].append(
                item['title'] if 'title' in item.keys() else '')
            tmp['description'].append(
                item['description'] if 'description' in item.keys() else '')
            tmp['url'].append(item['url'] if 'url' in item.keys() else '')
            tmp['tags'].append(f"{item['relatedCoins']}"
                               if 'relatedCoins' in item.keys() else '')
            tmp['icon'].append(item['source']['icon']
                               if 'icon' in item['source'].keys() else '')
            tmp['source'].append(item['source']['name']
                                 if 'name' in item['source'].keys() else '')
            tmp['date'].append(item['date'] if 'date' in item.keys() else '')
            tmp['major_url'].append(str(item['url']).split(
                '/')[2] if 'url' in item.keys() else '')
            tmp['minor_url'].append(str(item['url']).split(
                '/')[3] if 'url' in item.keys() else '')

        return tmp
