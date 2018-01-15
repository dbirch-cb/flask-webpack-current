def test_index_page(client):
    """ Expect to see the md5 tagged assets in the source code. """
    response = client.get('/')
    assert response.status_code == 200

    asset_path = 'https://yourdomainname_or_asset_cdn.com/assets/'
    css = 'app_css'
    js = 'app_js'
    image = 'images/dog/'

    response_data = response.data.decode('utf-8')
    assert asset_path in response_data
    assert css in response_data
    assert js in response_data
    # assert image in response_data
